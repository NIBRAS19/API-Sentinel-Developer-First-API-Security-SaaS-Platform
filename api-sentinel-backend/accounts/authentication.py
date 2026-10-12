import jwt
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from .tokens import decode_token
from projects.models import ProjectAPIKey
from django.utils import timezone

User=get_user_model()

class JWTAuthentication(BaseAuthentication):
    keyword='Bearer'
    def authenticate(self, request):
        raw=get_authorization_header(request).split()
        if not raw or raw[0].lower() != self.keyword.lower().encode():
            return None
        if len(raw)!=2:
            raise AuthenticationFailed('Invalid authorization header')
        try:
            payload=decode_token(raw[1].decode(), expected_type='access')
            user=User.objects.get(pk=payload['sub'], is_active=True)
        except (jwt.PyJWTError, User.DoesNotExist, KeyError):
            raise AuthenticationFailed('Invalid or expired access token')
        return (user, payload)

class ProjectAPIKeyAuthentication(BaseAuthentication):
    keyword='Api-Key'
    def authenticate(self, request):
        raw=get_authorization_header(request).split()
        if not raw or raw[0].lower() != self.keyword.lower().encode():
            return None
        if len(raw)!=2:
            raise AuthenticationFailed('Invalid API key header')
        key=raw[1].decode()
        obj=ProjectAPIKey.find_valid(key)
        if not obj:
            raise AuthenticationFailed('Invalid or revoked API key')
        ProjectAPIKey.objects.filter(pk=obj.pk).update(last_used_at=timezone.now())
        return (obj.user, {'auth_type':'api_key','project_id':str(obj.project_id),'key_id':str(obj.id)})
