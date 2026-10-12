from django.conf import settings
from django.db import migrations,models
import django.db.models.deletion, uuid
class Migration(migrations.Migration):
    initial=True
    dependencies=[migrations.swappable_dependency(settings.AUTH_USER_MODEL),('organizations','0001_initial')]
    operations=[
        migrations.CreateModel(name='Project',fields=[('id',models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True,serialize=False)),('name',models.CharField(max_length=200)),('slug',models.SlugField(max_length=220)),('description',models.TextField(blank=True)),('archived',models.BooleanField(default=False)),('created_at',models.DateTimeField(auto_now_add=True)),('updated_at',models.DateTimeField(auto_now=True)),('organization',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='projects',to='organizations.organization'))]),
        migrations.CreateModel(name='ProjectAPIKey',fields=[('id',models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True,serialize=False)),('name',models.CharField(max_length=120)),('prefix',models.CharField(db_index=True,max_length=12)),('hashed_key',models.CharField(max_length=128,unique=True)),('created_at',models.DateTimeField(auto_now_add=True)),('last_used_at',models.DateTimeField(blank=True,null=True)),('revoked_at',models.DateTimeField(blank=True,null=True)),('project',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='api_keys',to='projects.project')),('user',models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name='project_api_keys',to=settings.AUTH_USER_MODEL))]),
        migrations.AddConstraint(model_name='project',constraint=models.UniqueConstraint(fields=('organization','slug'),name='uniq_project_slug')),
    ]
