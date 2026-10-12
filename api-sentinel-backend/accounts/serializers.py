from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .tokens import access_token, refresh_token, decode_token

User=get_user_model()

class RegisterSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True,min_length=10)
    first_name=serializers.CharField(required=False,allow_blank=True)
    last_name=serializers.CharField(required=False,allow_blank=True)
    organization_name=serializers.CharField(required=False,allow_blank=True)
    authorized_testing_acknowledgement=serializers.BooleanField()
    def validate(self, attrs):
        if not attrs['authorized_testing_acknowledgement']:
            raise serializers.ValidationError({'authorized_testing_acknowledgement':'Required to use API Sentinel.'})
        if User.objects.filter(username=attrs['email'].lower()).exists():
            raise serializers.ValidationError({'email':'An account already exists.'})
        validate_password(attrs['password'])
        return attrs
    def create(self, validated):
        return User.objects.create_user(username=validated['email'].lower(),email=validated['email'].lower(),password=validated['password'],first_name=validated.get('first_name',''),last_name=validated.get('last_name',''))

class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)
    def validate(self, attrs):
        from django.contrib.auth import authenticate
        user=authenticate(username=attrs['email'].lower(),password=attrs['password'])
        if not user or not user.is_active:
            raise serializers.ValidationError('Invalid email or password.')
        attrs['user']=user
        return attrs

class RefreshSerializer(serializers.Serializer):
    refresh=serializers.CharField()
    def validate(self, attrs):
        try: attrs['payload']=decode_token(attrs['refresh'],expected_type='refresh')
        except Exception: raise serializers.ValidationError({'refresh':'Invalid or expired refresh token.'})
        return attrs

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','first_name','last_name','is_active','date_joined']
        read_only_fields=['id','email','is_active','date_joined']

def token_pair(user):
    return {'access':access_token(user.id),'refresh':refresh_token(user.id)}
