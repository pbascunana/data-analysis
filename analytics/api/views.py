from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class AnalysisViewSet(APIView):
    def get(self, request):
        return Response({'msg': 'Hello world'}, status=status.HTTP_200_OK)
