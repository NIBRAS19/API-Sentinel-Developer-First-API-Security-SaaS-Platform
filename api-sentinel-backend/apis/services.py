from urllib.parse import urljoin
from django.utils import timezone
from .models import Endpoint, AuthProfile
METHODS={'get','post','put','patch','delete','head','options'}
def normalize_path(p): return p if p.startswith('/') else '/'+p

def import_openapi(api, spec):
    api.openapi_spec=spec
    info=spec.get('info') or {}; api.version=str(info.get('version',''))
    servers=spec.get('servers') or []
    if servers:
        api.base_url=servers[0].get('url') or api.base_url
    api.imported_at=timezone.now(); api.save(update_fields=['openapi_spec','version','base_url','imported_at','updated_at'])
    api.endpoints.all().delete()
    created=[]
    paths=spec.get('paths') or {}
    for path, item in paths.items():
        if not isinstance(item,dict): continue
        path_item_security=item.get('security',None)
        for method,data in item.items():
            if method.lower() not in METHODS or not isinstance(data,dict): continue
            security=data.get('security',path_item_security)
            endpoint=Endpoint.objects.create(api=api,method=method.upper(),path=normalize_path(path),operation_id=data.get('operationId',''),summary=data.get('summary') or data.get('description','')[:500],security_required=bool(security),parameters=data.get('parameters') or [],tags=data.get('tags') or [])
            created.append(endpoint)
    return created
