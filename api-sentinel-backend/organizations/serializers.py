from rest_framework import serializers
from .models import Organization, Membership
class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Organization; fields=['id','name','slug','owner','created_at','updated_at']; read_only_fields=['id','owner','created_at','updated_at','slug']
class MembershipSerializer(serializers.ModelSerializer):
    user_email=serializers.EmailField(source='user.email',read_only=True)
    class Meta:
        model=Membership; fields=['id','user','user_email','role','created_at']; read_only_fields=['id','created_at','user_email']
