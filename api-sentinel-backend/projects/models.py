import uuid, hashlib, secrets
from django.conf import settings
from django.db import models
from organizations.models import Organization
class Project(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,related_name='projects')
    name=models.CharField(max_length=200); slug=models.SlugField(max_length=220)
    description=models.TextField(blank=True); archived=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: constraints=[models.UniqueConstraint(fields=['organization','slug'],name='uniq_project_slug')]
class ProjectAPIKey(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='api_keys')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='project_api_keys')
    name=models.CharField(max_length=120)
    prefix=models.CharField(max_length=12,db_index=True)
    hashed_key=models.CharField(max_length=128,unique=True)
    created_at=models.DateTimeField(auto_now_add=True); last_used_at=models.DateTimeField(null=True,blank=True); revoked_at=models.DateTimeField(null=True,blank=True)
    @staticmethod
    def generate(project,user,name):
        raw='aps_'+secrets.token_urlsafe(32); prefix=raw[:10]; hashed=hashlib.sha256(raw.encode()).hexdigest(); obj=ProjectAPIKey.objects.create(project=project,user=user,name=name,prefix=prefix,hashed_key=hashed); return obj,raw
    @staticmethod
    def find_valid(raw):
        h=hashlib.sha256(raw.encode()).hexdigest(); return ProjectAPIKey.objects.select_related('project','user').filter(hashed_key=h,revoked_at__isnull=True).first()
