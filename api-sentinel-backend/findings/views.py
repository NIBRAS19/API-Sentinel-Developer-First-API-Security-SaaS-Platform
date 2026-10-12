from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils import timezone
from organizations.permissions import membership_for
from organizations.models import Membership
from .models import Finding,FindingComment,FindingStatusHistory
from .serializers import FindingSerializer,CommentSerializer
from audit.services import audit
class FindingListView(generics.ListAPIView):
    serializer_class=FindingSerializer
    filterset_fields=['severity','status','category','project']
    search_fields=['title','check_id','category','description']
    ordering_fields=['severity','status','first_seen_at','last_seen_at']
    def get_queryset(self): return Finding.objects.filter(project__organization__memberships__user=self.request.user).select_related('endpoint','assignee').prefetch_related('evidence').distinct()
class FindingDetailView(generics.RetrieveUpdateAPIView):
    serializer_class=FindingSerializer
    def get_queryset(self): return Finding.objects.filter(project__organization__memberships__user=self.request.user).select_related('endpoint','assignee').prefetch_related('evidence').distinct()
    def perform_update(self,serializer):
        obj=self.get_object(); old=obj.status; new=serializer.validated_data.get('status',old); obj=serializer.save()
        if new!=old:
            FindingStatusHistory.objects.create(finding=obj,from_status=old,to_status=new,changed_by=self.request.user)
        audit('FINDING_UPDATED',self.request,project=obj.project,metadata={'finding_id':str(obj.id),'old_status':old,'new_status':new})
class FindingCommentListCreateView(generics.ListCreateAPIView):
    serializer_class=CommentSerializer
    def get_queryset(self): return FindingComment.objects.filter(finding_id=self.kwargs['finding_id'],finding__project__organization__memberships__user=self.request.user).select_related('author')
    def perform_create(self,s):
        finding=get_object_or_404(Finding,pk=self.kwargs['finding_id']); m=membership_for(self.request.user,finding.project.organization)
        if not m: raise PermissionDenied()
        s.save(finding=finding,author=self.request.user)
class FindingAssignView(APIView):
    def post(self,request,finding_id):
        finding=get_object_or_404(Finding.objects.select_related('project__organization'),pk=finding_id); m=membership_for(request.user,finding.project.organization)
        if not m or m.role in {Membership.Role.VIEWER}: raise PermissionDenied()
        user_id=request.data.get('user_id'); from django.contrib.auth import get_user_model; User=get_user_model(); user=get_object_or_404(User,pk=user_id)
        if not membership_for(user,finding.project.organization): raise PermissionDenied('Assignee must belong to the organization.')
        finding.assignee=user; finding.save(update_fields=['assignee','last_seen_at']); audit('FINDING_ASSIGNED',request,project=finding.project,metadata={'finding_id':str(finding.id),'assignee_id':str(user.id)}); return Response(FindingSerializer(finding).data)
