from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from organizations.models import Organization, Membership
from organizations.permissions import membership_for
from .models import Project, ProjectAPIKey
from .serializers import ProjectSerializer, APIKeyCreateSerializer
from audit.services import audit
class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class=ProjectSerializer
    def get_queryset(self): return Project.objects.filter(organization__memberships__user=self.request.user,archived=False).distinct()
    def perform_create(self,serializer):
        org=Organization.objects.get(pk=self.request.data['organization'])
        m=membership_for(self.request.user,org)
        if not m or m.role not in {Membership.Role.OWNER,Membership.Role.ADMIN,Membership.Role.DEVELOPER}: raise PermissionDenied()
        p=serializer.save(organization=org); audit('PROJECT_CREATED',self.request,organization=org,project=p,metadata={})
class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=ProjectSerializer
    def get_queryset(self): return Project.objects.filter(organization__memberships__user=self.request.user).distinct()
class APIKeyListCreateView(generics.ListCreateAPIView):
    serializer_class=APIKeyCreateSerializer
    def get_queryset(self):
        p=Project.objects.get(pk=self.kwargs['project_id']); return ProjectAPIKey.objects.filter(project=p,revoked_at__isnull=True)
    def post(self,request,*args,**kwargs):
        p=Project.objects.get(pk=kwargs['project_id']); m=membership_for(request.user,p.organization)
        if not m or m.role not in {Membership.Role.OWNER,Membership.Role.ADMIN,Membership.Role.DEVELOPER}: raise PermissionDenied()
        s=APIKeyCreateSerializer(data=request.data); s.is_valid(raise_exception=True); obj,raw=ProjectAPIKey.generate(p,request.user,s.validated_data['name']); audit('PROJECT_API_KEY_CREATED',request,organization=p.organization,project=p,metadata={'key_id':str(obj.id)}); return Response({'id':str(obj.id),'name':obj.name,'prefix':obj.prefix,'key':raw},status=201)
class APIKeyRevokeView(generics.GenericAPIView):
    def post(self,request,pk):
        obj=ProjectAPIKey.objects.select_related('project__organization').get(pk=pk); m=membership_for(request.user,obj.project.organization)
        if not m or m.role not in {Membership.Role.OWNER,Membership.Role.ADMIN}: raise PermissionDenied()
        obj.revoked_at=timezone.now(); obj.save(update_fields=['revoked_at']); return Response({'status':'revoked'})
