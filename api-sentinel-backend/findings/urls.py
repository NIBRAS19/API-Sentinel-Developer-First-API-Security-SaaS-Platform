from django.urls import path
from .views import FindingListView,FindingDetailView,FindingCommentListCreateView,FindingAssignView
urlpatterns=[path('findings/',FindingListView.as_view()),path('findings/<uuid:pk>/',FindingDetailView.as_view()),path('findings/<uuid:finding_id>/comments/',FindingCommentListCreateView.as_view()),path('findings/<uuid:finding_id>/assign/',FindingAssignView.as_view())]
