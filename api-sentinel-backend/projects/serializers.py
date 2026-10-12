from rest_framework import serializers
from .models import Project, ProjectAPIKey
class ProjectSerializer(serializers.ModelSerializer):
    class Meta: model=Project; fields=['id','organization','name','slug','description','archived','created_at','updated_at']; read_only_fields=['id','organization','created_at','updated_at']
class APIKeyCreateSerializer(serializers.Serializer): name=serializers.CharField(max_length=120)
