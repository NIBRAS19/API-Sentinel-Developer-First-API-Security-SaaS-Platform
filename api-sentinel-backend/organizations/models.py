import uuid, re
from django.conf import settings
from django.db import models
class Organization(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name=models.CharField(max_length=200)
    slug=models.SlugField(max_length=220,unique=True)
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='owned_organizations')
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    @staticmethod
    def slugify(value):
        return re.sub(r'[^a-z0-9]+','-',value.lower()).strip('-') or 'workspace'
    def __str__(self): return self.name
class Membership(models.Model):
    class Role(models.TextChoices):
        OWNER='owner','Owner'; ADMIN='admin','Admin'; ANALYST='analyst','Security Analyst'; DEVELOPER='developer','Developer'; VIEWER='viewer','Viewer'
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,related_name='memberships')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='memberships')
    role=models.CharField(max_length=20,choices=Role.choices,default=Role.VIEWER)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints=[models.UniqueConstraint(fields=['organization','user'],name='uniq_org_member')]
