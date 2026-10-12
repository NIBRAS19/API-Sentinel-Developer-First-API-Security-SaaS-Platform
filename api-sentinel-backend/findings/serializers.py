from rest_framework import serializers
from .models import Finding,Evidence,FindingComment,FindingStatusHistory
class EvidenceSerializer(serializers.ModelSerializer):
    class Meta: model=Evidence; fields=['id','kind','request_data','response_data','notes','created_at']
class CommentSerializer(serializers.ModelSerializer):
    author_email=serializers.EmailField(source='author.email',read_only=True)
    class Meta: model=FindingComment; fields=['id','author_email','body','created_at']; read_only_fields=['id','author_email','created_at']
class FindingSerializer(serializers.ModelSerializer):
    evidence=EvidenceSerializer(many=True,read_only=True); assignee_email=serializers.EmailField(source='assignee.email',read_only=True)
    class Meta: model=Finding; fields=['id','project','endpoint','check_id','category','title','severity','status','description','impact','remediation','verification','assignee','assignee_email','evidence','first_seen_at','last_seen_at']; read_only_fields=['id','first_seen_at','last_seen_at']
