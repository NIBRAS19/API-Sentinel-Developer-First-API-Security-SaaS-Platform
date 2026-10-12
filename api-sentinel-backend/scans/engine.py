import hashlib, re
from urllib.parse import urljoin
import requests
from django.utils import timezone
from apis.models import Endpoint
from findings.models import Finding,Evidence
from .models import Scan,ScanLog
from .network_policy import validate_target_url

SENSITIVE_NAMES={'password','passwd','secret','token','access_token','refresh_token','api_key','authorization','ssn','credit_card','card_number'}

def _log(scan,msg,level='info'):
    ScanLog.objects.create(scan=scan,message=msg,level=level)

def _fingerprint(project_id,check_id,endpoint_id,title):
    return hashlib.sha256(f'{project_id}:{check_id}:{endpoint_id}:{title}'.encode()).hexdigest()

def _finding(scan,endpoint,check_id,category,title,severity,description,impact,remediation,verification,evidence=None):
    fp=_fingerprint(scan.project_id,check_id,endpoint.id if endpoint else 'none',title)
    obj,created=Finding.objects.update_or_create(fingerprint=fp,defaults={'project':scan.project,'endpoint':endpoint,'check_id':check_id,'category':category,'title':title,'severity':severity,'description':description,'impact':impact,'remediation':remediation,'verification':verification})
    if evidence: Evidence.objects.create(finding=obj,**evidence)
    return obj,created

def run_scan(scan_id):
    scan=Scan.objects.select_related('api','project','requested_by').get(pk=scan_id); scan.status=Scan.Status.RUNNING; scan.started_at=timezone.now(); scan.progress=5; scan.save(update_fields=['status','started_at','progress'])
    try:
        if not scan.authorization_confirmed: raise ValueError('Authorization confirmation is required.')
        api=scan.api; endpoints=list(api.endpoints.all()); total=max(1,len(endpoints)); _log(scan,f'Starting {scan.profile} safe scan for {api.name}.'); findings=[]
        # Inventory and static OpenAPI checks
        for idx,ep in enumerate(endpoints,1):
            scan.progress=min(95,int(5+80*(idx/total))); scan.save(update_fields=['progress'])
            if ep.security_required is False and ep.path not in {'/health','/status'}:
                f,_=_finding(scan,ep,'API2-AUTHENTICATION','authentication','Endpoint has no documented security requirement','medium','The OpenAPI operation does not declare a security requirement.','An endpoint may be unintentionally exposed without authentication.','Review whether the endpoint is intentionally public. If protected, declare and enforce authentication server-side.','Verify an unauthenticated request is denied when authentication is required.')
                findings.append(f)
            param_text=' '.join(str(p).lower() for p in ep.parameters)
            if any(x in param_text for x in ('url','uri','callback','redirect','webhook')):
                f,_=_finding(scan,ep,'API7-SSRF','ssrf','Endpoint contains URL-like input that may require SSRF review','low','URL or callback-style parameters are present and may cause server-side outbound requests.','If unvalidated, attackers may influence outbound requests from the server.','Allowlist destinations, validate schemes/hosts, block internal ranges, and avoid server-side fetches when unnecessary.','Verify destination validation with controlled, non-routable test cases.')
                findings.append(f)
            if any(s in param_text for s in SENSITIVE_NAMES):
                f,_=_finding(scan,ep,'API3-PROPERTY_AUTHORIZATION','property_authorization','Sensitive property names require authorization review','medium','The endpoint contains parameter names associated with sensitive properties.','Improper field-level authorization can expose or modify data beyond a user role.','Enforce server-side property allowlists per role and validate writable fields.','Verify restricted fields cannot be read or modified by lower-privilege identities.')
                findings.append(f)
        # API9 inventory: spec present but has no endpoints or missing version
        if not api.openapi_spec:
            f,_=_finding(scan,None,'API9-INVENTORY','inventory','API has no imported OpenAPI inventory','medium','No OpenAPI specification is stored for this API.','Undocumented endpoints and versions are harder to secure and review.','Import and maintain an OpenAPI inventory for each deployed API version.','Re-run import and confirm expected endpoints are listed.')
            findings.append(f)
        # Safe connectivity check: GET only, no custom payloads, no auth replay.
        try:
            validate_target_url(api.base_url)
            r=requests.get(api.base_url,timeout=5,allow_redirects=False,headers={'User-Agent':'API-Sentinel/0.1 safe-check'})
            headers={k.lower():v for k,v in r.headers.items()}
            missing=[h for h in ('x-content-type-options','content-security-policy','referrer-policy') if h not in headers]
            if missing:
                f,_=_finding(scan,None,'API8-MISCONFIGURATION','configuration','Recommended security response headers are missing','low',f'The API base response is missing: {", ".join(missing)}.','Missing browser-facing headers can weaken defense-in-depth for API consumers and documentation surfaces.','Add appropriate security headers where applicable to the service and gateway.','Recheck the response headers after configuration changes.')
                findings.append(f)
            if 'server' in headers:
                f,_=_finding(scan,None,'API8-MISCONFIGURATION','configuration','Server header exposes implementation information','low','The base response exposes a Server header.','Technology/version disclosure can provide unnecessary reconnaissance information.','Minimize server banner details at the gateway or application layer.','Recheck the response and confirm the banner is minimized.')
                findings.append(f)
        except requests.RequestException as exc:
            _log(scan,f'Connectivity check failed: {exc}','warning')
        counts={s:sum(1 for f in findings if f.severity==s) for s in Finding.Severity.values}
        critical=counts.get('critical',0); high=counts.get('high',0); medium=counts.get('medium',0); low=counts.get('low',0)
        score=max(0,100-(critical*30+high*15+medium*6+low*2))
        scan.summary={'security_score':score,'findings':counts,'endpoints_checked':len(endpoints)}; scan.progress=100; scan.status=Scan.Status.COMPLETED; scan.completed_at=timezone.now(); scan.save(update_fields=['summary','progress','status','completed_at']); _log(scan,'Scan completed.')
    except Exception as exc:
        scan.status=Scan.Status.FAILED; scan.summary={'error':str(exc)}; scan.completed_at=timezone.now(); scan.save(update_fields=['status','summary','completed_at']); _log(scan,f'Scan failed: {exc}','error'); raise
