from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer, RefreshSerializer, UserSerializer, token_pair
from organizations.models import Organization, Membership
from audit.services import audit
from rest_framework import serializers

class RegisterView(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        s=RegisterSerializer(data=request.data); s.is_valid(raise_exception=True)
        user=s.save(); org_name=s.validated_data.get('organization_name') or f"{user.first_name or user.email.split('@')[0]}'s Workspace"
        org=Organization.objects.create(name=org_name,slug=Organization.slugify(org_name),owner=user)
        Membership.objects.create(organization=org,user=user,role=Membership.Role.OWNER)
        audit('ACCOUNT_REGISTERED',request,user=user,organization=org,metadata={})
        return Response({'user':UserSerializer(user).data,'organization':{'id':str(org.id),'name':org.name,'slug':org.slug},'tokens':token_pair(user)},status=201)

class LoginView(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        s=LoginSerializer(data=request.data); s.is_valid(raise_exception=True)
        return Response({'user':UserSerializer(s.validated_data['user']).data,'tokens':token_pair(s.validated_data['user'])})

class RefreshView(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        s=RefreshSerializer(data=request.data); s.is_valid(raise_exception=True)
        user_id=s.validated_data['payload']['sub']
        from django.contrib.auth import get_user_model
        User=get_user_model(); user=User.objects.filter(pk=user_id,is_active=True).first()
        if not user: raise serializers.ValidationError('User is inactive or missing.')
        return Response({'tokens':token_pair(user)})

class MeView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request): return Response(UserSerializer(request.user).data)
