from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .services import DataServices, ListDataServices


class DataViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]

    def list(self, request):
        query_max = self.request.query_params.get('max', None)
        #ListDataServices.start_get_list()
        DataServices.start_get_items()
        data = { 'detail': 'get data successful' }
        return Response(data, status=status.HTTP_200_OK)

