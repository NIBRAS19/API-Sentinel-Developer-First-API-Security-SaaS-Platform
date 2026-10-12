from django.urls import path
from .views import EnvironmentListCreateView,EnvironmentDetailView,APIListCreateView,APIDetailView,EndpointListView,EndpointDetailView,AuthProfileListCreateView,OpenAPIImportView,APIConnectivityCheckView
urlpatterns=[
path('projects/<uuid:project_id>/environments/',EnvironmentListCreateView.as_view()),path('environments/<uuid:pk>/',EnvironmentDetailView.as_view()),
path('projects/<uuid:project_id>/apis/',APIListCreateView.as_view()),path('apis/<uuid:pk>/',APIDetailView.as_view()),
path('apis/<uuid:api_id>/endpoints/',EndpointListView.as_view()),path('endpoints/<uuid:pk>/',EndpointDetailView.as_view()),
path('apis/<uuid:api_id>/auth-profiles/',AuthProfileListCreateView.as_view()),path('apis/<uuid:api_id>/openapi/import/',OpenAPIImportView.as_view()),path('apis/<uuid:api_id>/connectivity-check/',APIConnectivityCheckView.as_view()),
]
