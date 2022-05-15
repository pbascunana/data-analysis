from django.urls import path

from .views import AnalysisViewSet

urlpatterns = [
    path('analysis', AnalysisViewSet.as_view())
]
