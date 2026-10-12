from rest_framework import serializers
from .models import Scan,ScanLog
class ScanCreateSerializer(serializers.Serializer):
    api_id=serializers.UUIDField(); profile=serializers.ChoiceField(choices=Scan.Profile.choices,default=Scan.Profile.STANDARD); safe_mode=serializers.BooleanField(default=True); authorization_confirmed=serializers.BooleanField()
    def validate_authorization_confirmed(self,v):
        if not v: raise serializers.ValidationError('You must confirm that you own or are explicitly authorized to test this API.')
        return v
class ScanSerializer(serializers.ModelSerializer):
    class Meta: model=Scan; fields=['id','project','api','profile','status','safe_mode','authorization_confirmed','requested_by','progress','summary','started_at','completed_at','created_at']; read_only_fields=['id','project','status','requested_by','progress','summary','started_at','completed_at','created_at']
class ScanLogSerializer(serializers.ModelSerializer):
    class Meta: model=ScanLog; fields=['id','level','message','created_at']
