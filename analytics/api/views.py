from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from services.analytics import Analytics


class AnalysisViewSet(APIView):
    def get(self, request):
        analytics = Analytics()
        return Response(analytics.response, status=status.HTTP_200_OK)
