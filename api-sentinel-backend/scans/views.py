from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from organizations.permissions import membership_for
from .models import Scan
from .serializers import ScanCreateSerializer,ScanSerializer,ScanLogSerializer
from .tasks import execute_scan
from audit.services import audit
class ScanListView(generics.ListAPIView):
    serializer_class=ScanSerializer
    filterset_fields=['status','profile','api']
    ordering_fields=['created_at','completed_at','status']
    def get_queryset(self): return Scan.objects.filter(project__organization__memberships__user=self.request.user).order_by('-created_at').distinct()
class ScanCreateView(APIView):
    def post(self,request):
        s=ScanCreateSerializer(data=request.data); s.is_valid(raise_exception=True)
        from apis.models import APIService
        api=get_object_or_404(APIService,pk=s.validated_data['api_id']); m=membership_for(request.user,api.project.organization)
        if not m: raise PermissionDenied()
        scan=Scan.objects.create(project=api.project,api=api,requested_by=request.user,profile=s.validated_data['profile'],safe_mode=s.validated_data['safe_mode'],authorization_confirmed=s.validated_data['authorization_confirmed'])
        audit('SCAN_CREATED',request,project=api.project,metadata={'scan_id':str(scan.id),'api_id':str(api.id)})
        execute_scan.delay(str(scan.id))
        return Response(ScanSerializer(scan).data,status=202)
class ScanDetailView(generics.RetrieveAPIView):
    serializer_class=ScanSerializer
    def get_queryset(self): return Scan.objects.filter(project__organization__memberships__user=self.request.user)
class ScanLogsView(generics.ListAPIView):
    serializer_class=ScanLogSerializer
    def get_queryset(self): return Scan.objects.filter(project__organization__memberships__user=self.request.user).get(pk=self.kwargs['scan_id']).logs.order_by('created_at')
