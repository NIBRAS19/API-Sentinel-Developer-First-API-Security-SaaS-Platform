from rest_framework import serializers
from .models import Environment,APIService,Endpoint,AuthProfile
class EnvironmentSerializer(serializers.ModelSerializer):
    class Meta: model=Environment; fields=['id','project','name','kind','base_url','created_at','updated_at']; read_only_fields=['id','created_at','updated_at','project']
class APISerializer(serializers.ModelSerializer):
    class Meta: model=APIService; fields=['id','project','environment','name','version','base_url','imported_at','created_at','updated_at']; read_only_fields=['id','project','imported_at','created_at','updated_at']
class EndpointSerializer(serializers.ModelSerializer):
    class Meta: model=Endpoint; fields=['id','api','method','path','operation_id','summary','security_required','parameters','tags','created_at','updated_at']; read_only_fields=['id','api','created_at','updated_at']
class AuthProfileSerializer(serializers.ModelSerializer):
    class Meta: model=AuthProfile; fields=['id','api','name','auth_type','config','is_default','created_at']; read_only_fields=['id','api','created_at']
class OpenAPIImportSerializer(serializers.Serializer):
    spec=serializers.JSONField()
class APICheckConnectSerializer(serializers.Serializer):
    timeout_seconds=serializers.IntegerField(min_value=1,max_value=10,default=5)
