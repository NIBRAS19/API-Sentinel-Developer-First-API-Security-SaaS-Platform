from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied,NotFound
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from organizations.permissions import membership_for
from organizations.models import Membership
from projects.models import Project
from .models import Environment,APIService,Endpoint,AuthProfile
from .serializers import EnvironmentSerializer,APISerializer,EndpointSerializer,AuthProfileSerializer,OpenAPIImportSerializer,APICheckConnectSerializer
from .services import import_openapi
from scans.network_policy import validate_target_url
from audit.services import audit
import requests

class ProjectScopedMixin:
    def check_project(self,p):
        m=membership_for(self.request.user,p.organization)
        if not m: raise PermissionDenied()
        return m

class EnvironmentListCreateView(generics.ListCreateAPIView,ProjectScopedMixin):
    serializer_class=EnvironmentSerializer
    def get_project(self): return get_object_or_404(Project,pk=self.kwargs['project_id'])
    def get_queryset(self): self.check_project(self.get_project()); return Environment.objects.filter(project=self.get_project())
    def perform_create(self,s): self.check_project(self.get_project()); s.save(project=self.get_project())

class EnvironmentDetailView(generics.RetrieveUpdateDestroyAPIView,ProjectScopedMixin):
    serializer_class=EnvironmentSerializer
    def get_queryset(self): return Environment.objects.filter(project__organization__memberships__user=self.request.user).distinct()

class APIListCreateView(generics.ListCreateAPIView,ProjectScopedMixin):
    serializer_class=APISerializer
    def get_project(self): return get_object_or_404(Project,pk=self.kwargs['project_id'])
    def get_queryset(self): self.check_project(self.get_project()); return APIService.objects.filter(project=self.get_project())
    def perform_create(self,s): self.check_project(self.get_project()); s.save(project=self.get_project())

class APIDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=APISerializer
    def get_queryset(self): return APIService.objects.filter(project__organization__memberships__user=self.request.user).distinct()

class EndpointListView(generics.ListAPIView):
    serializer_class=EndpointSerializer
    def get_queryset(self): return Endpoint.objects.filter(api_id=self.kwargs['api_id'],api__project__organization__memberships__user=self.request.user).distinct().order_by('path','method')

class EndpointDetailView(generics.RetrieveAPIView):
    serializer_class=EndpointSerializer
    def get_queryset(self): return Endpoint.objects.filter(api__project__organization__memberships__user=self.request.user).distinct()

class AuthProfileListCreateView(generics.ListCreateAPIView):
    serializer_class=AuthProfileSerializer
    def get_queryset(self): return AuthProfile.objects.filter(api_id=self.kwargs['api_id'],api__project__organization__memberships__user=self.request.user)
    def perform_create(self,s):
        api=get_object_or_404(APIService,pk=self.kwargs['api_id']); membership_for(self.request.user,api.project.organization) or (_ for _ in ()).throw(PermissionDenied()); s.save(api=api)

class OpenAPIImportView(APIView):
    def post(self,request,api_id):
        api=get_object_or_404(APIService,pk=api_id)
        if not membership_for(request.user,api.project.organization): raise PermissionDenied()
        s=OpenAPIImportSerializer(data=request.data); s.is_valid(raise_exception=True)
        created=import_openapi(api,s.validated_data['spec']); audit('OPENAPI_IMPORTED',request,organization=api.project.organization,project=api.project,metadata={'api_id':str(api.id),'endpoint_count':len(created)})
        return Response({'api_id':str(api.id),'endpoints_imported':len(created)})

class APIConnectivityCheckView(APIView):
    def post(self,request,api_id):
        api=get_object_or_404(APIService,pk=api_id)
        if not membership_for(request.user,api.project.organization): raise PermissionDenied()
        s=APICheckConnectSerializer(data=request.data); s.is_valid(raise_exception=True)
        try:
            validate_target_url(api.base_url)
            r=requests.get(api.base_url,timeout=s.validated_data['timeout_seconds'],allow_redirects=False,headers={'User-Agent':'API-Sentinel/0.1 safety-check'})
            return Response({'reachable':True,'status_code':r.status_code,'headers':{k:v for k,v in r.headers.items() if k.lower() in {'content-type','server','strict-transport-security','content-security-policy','x-content-type-options','x-frame-options','referrer-policy','x-ratelimit-limit','x-ratelimit-remaining'}}})
        except requests.RequestException as e:
            return Response({'reachable':False,'error':str(e)},status=502)
