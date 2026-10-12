from rest_framework import generics
from .models import AuditLog
from .serializers import AuditLogSerializer
class AuditLogListView(generics.ListAPIView):
    serializer_class=AuditLogSerializer
    def get_queryset(self): return AuditLog.objects.filter(organization_id=self.kwargs['organization_id'],organization__memberships__user=self.request.user).select_related('actor').order_by('-created_at')
