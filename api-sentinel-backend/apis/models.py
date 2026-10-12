import uuid
from django.db import models
from projects.models import Project
class Environment(models.Model):
    class Kind(models.TextChoices): DEV='development','Development'; STAGING='staging','Staging'; PROD='production','Production'; OTHER='other','Other'
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='environments')
    name=models.CharField(max_length=120); kind=models.CharField(max_length=20,choices=Kind.choices,default=Kind.STAGING); base_url=models.URLField(max_length=500)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
class APIService(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='apis')
    environment=models.ForeignKey(Environment,on_delete=models.CASCADE,related_name='apis'); name=models.CharField(max_length=200); version=models.CharField(max_length=80,blank=True)
    base_url=models.URLField(max_length=500); openapi_spec=models.JSONField(default=dict,blank=True); imported_at=models.DateTimeField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
class Endpoint(models.Model):
    class Method(models.TextChoices): GET='GET','GET'; POST='POST','POST'; PUT='PUT','PUT'; PATCH='PATCH','PATCH'; DELETE='DELETE','DELETE'; HEAD='HEAD','HEAD'; OPTIONS='OPTIONS','OPTIONS'
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); api=models.ForeignKey(APIService,on_delete=models.CASCADE,related_name='endpoints')
    method=models.CharField(max_length=10,choices=Method.choices); path=models.CharField(max_length=500); operation_id=models.CharField(max_length=200,blank=True); summary=models.CharField(max_length=500,blank=True)
    security_required=models.BooleanField(default=False); documented=True
    parameters=models.JSONField(default=list,blank=True); tags=models.JSONField(default=list,blank=True); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: constraints=[models.UniqueConstraint(fields=['api','method','path'],name='uniq_api_endpoint')]; indexes=[models.Index(fields=['api','method']),models.Index(fields=['path'])]
class AuthProfile(models.Model):
    class Type(models.TextChoices): NONE='none','No Auth'; BEARER='bearer','Bearer'; API_KEY='api_key','API Key'; BASIC='basic','Basic'; OAUTH2='oauth2','OAuth2'
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); api=models.ForeignKey(APIService,on_delete=models.CASCADE,related_name='auth_profiles')
    name=models.CharField(max_length=120); auth_type=models.CharField(max_length=20,choices=Type.choices); config=models.JSONField(default=dict,blank=True); is_default=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
