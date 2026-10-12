from django.urls import path
from .views import AuditLogListView
urlpatterns=[path('organizations/<uuid:organization_id>/audit-logs/',AuditLogListView.as_view())]
