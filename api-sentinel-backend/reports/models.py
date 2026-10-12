import uuid
from django.db import models
from projects.models import Project
class Report(models.Model):
    class Format(models.TextChoices): JSON='json','JSON'; HTML='html','HTML'
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='reports'); name=models.CharField(max_length=240); report_format=models.CharField(max_length=10,choices=Format.choices,default=Format.HTML)
    scope=models.JSONField(default=dict,blank=True); content=models.JSONField(default=dict,blank=True); created_by=models.ForeignKey('auth.User',on_delete=models.PROTECT); created_at=models.DateTimeField(auto_now_add=True)
