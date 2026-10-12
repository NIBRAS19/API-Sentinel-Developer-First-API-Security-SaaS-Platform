from rest_framework import serializers
from .models import AuditLog
class AuditLogSerializer(serializers.ModelSerializer):
    actor_email=serializers.EmailField(source='actor.email',read_only=True)
    class Meta: model=AuditLog; fields=['id','action','resource_type','resource_id','metadata','ip_address','actor_email','created_at']
