from django.conf import settings
from django.db import migrations,models
import django.db.models.deletion, uuid
class Migration(migrations.Migration):
    initial=True; dependencies=[migrations.swappable_dependency(settings.AUTH_USER_MODEL),('organizations','0001_initial')]
    operations=[migrations.CreateModel(name='AuditLog',fields=[('id',models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True,serialize=False)),('action',models.CharField(max_length=120)),('resource_type',models.CharField(blank=True,max_length=80)),('resource_id',models.CharField(blank=True,max_length=80)),('metadata',models.JSONField(blank=True,default=dict)),('ip_address',models.GenericIPAddressField(blank=True,null=True)),('created_at',models.DateTimeField(auto_now_add=True)),('actor',models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.SET_NULL,related_name='audit_actions',to=settings.AUTH_USER_MODEL)),('organization',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='audit_logs',to='organizations.organization'))])]
