from django.urls import path
from .views import ProjectListCreateView,ProjectDetailView,APIKeyListCreateView,APIKeyRevokeView
urlpatterns=[path('projects/',ProjectListCreateView.as_view()),path('projects/<uuid:pk>/',ProjectDetailView.as_view()),path('projects/<uuid:project_id>/api-keys/',APIKeyListCreateView.as_view()),path('api-keys/<uuid:pk>/revoke/',APIKeyRevokeView.as_view())]
