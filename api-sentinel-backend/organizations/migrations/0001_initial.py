from django.conf import settings
from django.db import migrations,models
import django.db.models.deletion, uuid
class Migration(migrations.Migration):
    initial=True
    dependencies=[migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations=[
        migrations.CreateModel(name='Organization',fields=[('id',models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True,serialize=False)),('name',models.CharField(max_length=200)),('slug',models.SlugField(max_length=220,unique=True)),('created_at',models.DateTimeField(auto_now_add=True)),('updated_at',models.DateTimeField(auto_now=True)),('owner',models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name='owned_organizations',to=settings.AUTH_USER_MODEL))]),
        migrations.CreateModel(name='Membership',fields=[('id',models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True,serialize=False)),('role',models.CharField(choices=[('owner','Owner'),('admin','Admin'),('analyst','Security Analyst'),('developer','Developer'),('viewer','Viewer')],default='viewer',max_length=20)),('created_at',models.DateTimeField(auto_now_add=True)),('organization',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='memberships',to='organizations.organization')),('user',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='memberships',to=settings.AUTH_USER_MODEL))]),
        migrations.AddConstraint(model_name='membership',constraint=models.UniqueConstraint(fields=('organization','user'),name='uniq_org_member')),
    ]
