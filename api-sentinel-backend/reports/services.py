from .models import Report
from findings.models import Finding

def build_content(project,scope=None):
    qs=Finding.objects.filter(project=project).select_related('endpoint').order_by('severity','first_seen_at')
    if scope and scope.get('finding_status'): qs=qs.filter(status__in=scope['finding_status'])
    findings=[]
    for f in qs:
        findings.append({'id':str(f.id),'check_id':f.check_id,'title':f.title,'severity':f.severity,'status':f.status,'category':f.category,'endpoint':f'{f.endpoint.method} {f.endpoint.path}' if f.endpoint else None,'description':f.description,'impact':f.impact,'remediation':f.remediation,'verification':f.verification})
    counts={x:sum(1 for f in findings if f['severity']==x) for x in ['critical','high','medium','low','info']}
    score=max(0,100-(counts['critical']*30+counts['high']*15+counts['medium']*6+counts['low']*2))
    return {'project':{'id':str(project.id),'name':project.name},'security_score':score,'counts':counts,'findings':findings}

def render_html(content):
    rows=''.join(f"<tr><td>{f['severity'].upper()}</td><td>{f['title']}</td><td>{f['endpoint'] or '—'}</td><td>{f['status']}</td></tr>" for f in content['findings'])
    return f"""<!doctype html><html><head><meta charset='utf-8'><title>API Sentinel Report</title><style>body{{font-family:Inter,Arial,sans-serif;background:#0b0d14;color:#e7edf7;padding:32px}}h1{{font-size:32px}}table{{width:100%;border-collapse:collapse;margin-top:24px}}th,td{{padding:10px;border-bottom:1px solid #263041;text-align:left}}.score{{font-size:48px;font-weight:800}}.muted{{color:#94a3b8}}</style></head><body><h1>API Sentinel Security Report</h1><div class='muted'>{content['project']['name']}</div><div class='score'>{content['security_score']} / 100</div><div>Critical {content['counts']['critical']} · High {content['counts']['high']} · Medium {content['counts']['medium']} · Low {content['counts']['low']}</div><table><thead><tr><th>Severity</th><th>Finding</th><th>Endpoint</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table></body></html>"""
