import uuid
from django.conf import settings
from django.db import models
from organizations.models import Organization
class AuditLog(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); organization=models.ForeignKey(Organization,on_delete=models.CASCADE,related_name='audit_logs')
    actor=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name='audit_actions')
    action=models.CharField(max_length=120); resource_type=models.CharField(max_length=80,blank=True); resource_id=models.CharField(max_length=80,blank=True)
    metadata=models.JSONField(default=dict,blank=True); ip_address=models.GenericIPAddressField(null=True,blank=True); created_at=models.DateTimeField(auto_now_add=True)
