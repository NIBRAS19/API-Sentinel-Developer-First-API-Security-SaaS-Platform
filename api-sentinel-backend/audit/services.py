from .models import AuditLog

def audit(action,request,organization=None,project=None,user=None,metadata=None,resource=None):
    if organization is None and project is not None: organization=project.organization
    actor=user or getattr(request,'user',None)
    if not organization: return
    if resource is not None:
        rtype=resource.__class__.__name__; rid=str(resource.pk)
    else: rtype=rid=''
    forwarded=request.META.get('HTTP_X_FORWARDED_FOR','') if request else ''
    ip=forwarded.split(',')[0].strip() if forwarded else (request.META.get('REMOTE_ADDR') if request else None)
    AuditLog.objects.create(organization=organization,actor=actor if getattr(actor,'is_authenticated',False) else None,action=action,resource_type=rtype,resource_id=rid,metadata=metadata or {},ip_address=ip)
