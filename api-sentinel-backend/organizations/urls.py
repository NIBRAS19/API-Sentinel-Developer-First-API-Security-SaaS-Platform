from django.urls import path
from .views import OrganizationListCreateView, OrganizationDetailView, OrganizationMembersView
urlpatterns=[path('organizations/',OrganizationListCreateView.as_view()),path('organizations/<uuid:pk>/',OrganizationDetailView.as_view()),path('organizations/<uuid:organization_id>/members/',OrganizationMembersView.as_view())]
