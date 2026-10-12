import uuid
from django.conf import settings
from django.db import models
from projects.models import Project
from apis.models import APIService
class Scan(models.Model):
    class Profile(models.TextChoices): QUICK='quick','Quick'; STANDARD='standard','Standard'; DEEP='deep','Deep'
    class Status(models.TextChoices): QUEUED='queued','Queued'; RUNNING='running','Running'; COMPLETED='completed','Completed'; FAILED='failed','Failed'; CANCELED='canceled','Canceled'
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='scans'); api=models.ForeignKey(APIService,on_delete=models.CASCADE,related_name='scans')
    profile=models.CharField(max_length=20,choices=Profile.choices,default=Profile.STANDARD); status=models.CharField(max_length=20,choices=Status.choices,default=Status.QUEUED); safe_mode=models.BooleanField(default=True); authorization_confirmed=models.BooleanField(default=False)
    requested_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='requested_scans'); progress=models.PositiveSmallIntegerField(default=0); summary=models.JSONField(default=dict,blank=True); started_at=models.DateTimeField(null=True,blank=True); completed_at=models.DateTimeField(null=True,blank=True); created_at=models.DateTimeField(auto_now_add=True)
class ScanLog(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); scan=models.ForeignKey(Scan,on_delete=models.CASCADE,related_name='logs'); level=models.CharField(max_length=20,default='info'); message=models.TextField(); created_at=models.DateTimeField(auto_now_add=True)
