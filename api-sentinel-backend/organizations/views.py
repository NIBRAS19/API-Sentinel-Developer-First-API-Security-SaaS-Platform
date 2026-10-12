from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Organization, Membership
from .serializers import OrganizationSerializer, MembershipSerializer
from .permissions import membership_for
from audit.services import audit
class OrganizationListCreateView(generics.ListCreateAPIView):
    serializer_class=OrganizationSerializer
    def get_queryset(self):
        return Organization.objects.filter(memberships__user=self.request.user).distinct()
    def perform_create(self,serializer):
        org=serializer.save(owner=self.request.user); Membership.objects.create(organization=org,user=self.request.user,role=Membership.Role.OWNER); audit('ORGANIZATION_CREATED',self.request,organization=org,metadata={})
class OrganizationDetailView(generics.RetrieveUpdateAPIView):
    serializer_class=OrganizationSerializer
    queryset=Organization.objects.all()
    def get_queryset(self): return super().get_queryset().filter(memberships__user=self.request.user).distinct()
class OrganizationMembersView(generics.ListCreateAPIView):
    serializer_class=MembershipSerializer
    def get_queryset(self):
        org=Organization.objects.get(pk=self.kwargs['organization_id']); return Membership.objects.filter(organization=org)
    def perform_create(self,serializer):
        org=Organization.objects.get(pk=self.kwargs['organization_id']); m=membership_for(self.request.user,org)
        if not m or m.role not in {Membership.Role.OWNER,Membership.Role.ADMIN}: from rest_framework.exceptions import PermissionDenied; raise PermissionDenied()
        serializer.save(organization=org)
