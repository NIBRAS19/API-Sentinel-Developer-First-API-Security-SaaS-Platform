from django.db import migrations,models
from django.conf import settings
import django.db.models.deletion, uuid
class Migration(migrations.Migration):
    initial=True; dependencies=[migrations.swappable_dependency(settings.AUTH_USER_MODEL),('projects','0001_initial')]
    operations=[migrations.CreateModel(name='Report',fields=[('id',models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True,serialize=False)),('name',models.CharField(max_length=240)),('report_format',models.CharField(choices=[('json','JSON'),('html','HTML')],default='html',max_length=10)),('scope',models.JSONField(blank=True,default=dict)),('content',models.JSONField(blank=True,default=dict)),('created_at',models.DateTimeField(auto_now_add=True)),('created_by',models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,to=settings.AUTH_USER_MODEL)),('project',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='reports',to='projects.project'))])]
