from django.urls import path
from .views import ReportListView,ReportCreateView,ReportDetailView,ReportDownloadView
urlpatterns=[path('reports/',ReportListView.as_view()),path('reports/generate/',ReportCreateView.as_view()),path('reports/<uuid:pk>/',ReportDetailView.as_view()),path('reports/<uuid:pk>/download/',ReportDownloadView.as_view())]
