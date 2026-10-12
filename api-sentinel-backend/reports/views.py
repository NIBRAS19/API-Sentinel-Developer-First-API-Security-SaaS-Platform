from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from organizations.permissions import membership_for
from projects.models import Project
from .models import Report
from .serializers import ReportCreateSerializer,ReportSerializer
from .services import build_content,render_html
from audit.services import audit
class ReportListView(generics.ListAPIView):
    serializer_class=ReportSerializer
    def get_queryset(self): return Report.objects.filter(project__organization__memberships__user=self.request.user).order_by('-created_at')
class ReportCreateView(APIView):
    def post(self,request):
        s=ReportCreateSerializer(data=request.data); s.is_valid(raise_exception=True); project=get_object_or_404(Project,pk=s.validated_data['project_id']); m=membership_for(request.user,project.organization)
        if not m: raise PermissionDenied()
        content=build_content(project,s.validated_data.get('scope') or {}); r=Report.objects.create(project=project,name=s.validated_data['name'],report_format=s.validated_data['report_format'],scope=s.validated_data.get('scope') or {},content=content,created_by=request.user); audit('REPORT_CREATED',request,project=project,metadata={'report_id':str(r.id)}); return Response(ReportSerializer(r).data,status=201)
class ReportDetailView(generics.RetrieveAPIView):
    serializer_class=ReportSerializer
    def get_queryset(self): return Report.objects.filter(project__organization__memberships__user=self.request.user)
class ReportDownloadView(APIView):
    def get(self,request,pk):
        r=get_object_or_404(Report,pk=pk,project__organization__memberships__user=request.user)
        if r.report_format==Report.Format.JSON: return Response(r.content)
        return HttpResponse(render_html(r.content),content_type='text/html; charset=utf-8')
