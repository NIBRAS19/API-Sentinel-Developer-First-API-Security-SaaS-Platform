import uuid
from django.conf import settings
from django.db import models
from projects.models import Project
from apis.models import Endpoint
class Finding(models.Model):
    class Severity(models.TextChoices): CRITICAL='critical','Critical'; HIGH='high','High'; MEDIUM='medium','Medium'; LOW='low','Low'; INFO='info','Informational'
    class Status(models.TextChoices): OPEN='open','Open'; TRIAGED='triaged','Triaged'; IN_PROGRESS='in_progress','In Progress'; FIXED='fixed','Fixed'; VERIFIED='verified','Verified'; CLOSED='closed','Closed'; FALSE_POSITIVE='false_positive','False Positive'
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='findings'); endpoint=models.ForeignKey(Endpoint,on_delete=models.SET_NULL,null=True,blank=True,related_name='findings')
    check_id=models.CharField(max_length=100); category=models.CharField(max_length=120); title=models.CharField(max_length=240); severity=models.CharField(max_length=20,choices=Severity.choices); status=models.CharField(max_length=20,choices=Status.choices,default=Status.OPEN)
    description=models.TextField(); impact=models.TextField(blank=True); remediation=models.TextField(blank=True); verification=models.TextField(blank=True); fingerprint=models.CharField(max_length=128,unique=True); first_seen_at=models.DateTimeField(auto_now_add=True); last_seen_at=models.DateTimeField(auto_now=True)
    assignee=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name='assigned_findings')
class Evidence(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); finding=models.ForeignKey(Finding,on_delete=models.CASCADE,related_name='evidence'); kind=models.CharField(max_length=50); request_data=models.JSONField(default=dict,blank=True); response_data=models.JSONField(default=dict,blank=True); notes=models.TextField(blank=True); created_at=models.DateTimeField(auto_now_add=True)
class FindingComment(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); finding=models.ForeignKey(Finding,on_delete=models.CASCADE,related_name='comments'); author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT); body=models.TextField(); created_at=models.DateTimeField(auto_now_add=True)
class FindingStatusHistory(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); finding=models.ForeignKey(Finding,on_delete=models.CASCADE,related_name='status_history'); from_status=models.CharField(max_length=20,blank=True); to_status=models.CharField(max_length=20); changed_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT); created_at=models.DateTimeField(auto_now_add=True)
