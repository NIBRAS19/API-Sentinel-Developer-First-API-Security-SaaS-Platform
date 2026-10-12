from django.urls import path
from .views import ScanListView,ScanCreateView,ScanDetailView,ScanLogsView
urlpatterns=[path('scans/',ScanListView.as_view()),path('scans/run/',ScanCreateView.as_view()),path('scans/<uuid:pk>/',ScanDetailView.as_view()),path('scans/<uuid:scan_id>/logs/',ScanLogsView.as_view())]
