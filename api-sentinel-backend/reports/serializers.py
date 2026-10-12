from rest_framework import serializers
from .models import Report
class ReportCreateSerializer(serializers.Serializer):
    project_id=serializers.UUIDField(); name=serializers.CharField(max_length=240); report_format=serializers.ChoiceField(choices=Report.Format.choices); scope=serializers.JSONField(required=False)
class ReportSerializer(serializers.ModelSerializer):
    class Meta: model=Report; fields=['id','project','name','report_format','scope','content','created_by','created_at']; read_only_fields=['id','project','content','created_by','created_at']
