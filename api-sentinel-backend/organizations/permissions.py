from rest_framework.permissions import BasePermission
from .models import Membership

def membership_for(user, organization):
    return Membership.objects.filter(user=user,organization=organization).first()

class IsOrgMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        org=getattr(obj,'organization',obj if obj.__class__.__name__=='Organization' else None)
        return bool(org and membership_for(request.user,org))

class HasOrgWritePermission(IsOrgMember):
    roles={Membership.Role.OWNER,Membership.Role.ADMIN,Membership.Role.ANALYST,Membership.Role.DEVELOPER}
    def has_object_permission(self,request,view,obj):
        m=membership_for(request.user,getattr(obj,'organization',obj)); return bool(m and m.role in self.roles)

class HasOrgAdminPermission(IsOrgMember):
    roles={Membership.Role.OWNER,Membership.Role.ADMIN}
    def has_object_permission(self,request,view,obj):
        m=membership_for(request.user,getattr(obj,'organization',obj)); return bool(m and m.role in self.roles)
