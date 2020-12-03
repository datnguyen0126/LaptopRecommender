from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action

from .services import DataServices, ListDataServices, ScoreServices
from .serializers import LaptopSerializers
from .models import Laptop, CpuScore


class DataViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = LaptopSerializers

    @action(methods=['GET'], detail=False)
    def get_data(self, request):
        # query_max = self.request.query_params.get('max', None)
        ListDataServices.start_get_list()
        DataServices.start_get_items()
        data = { 'detail': 'get data successful' }
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def clean(self, request):
        DataServices.restore_data()
        data = { 'detail': 'Clean data done' }
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def cpu_scores(self, request):
        ScoreServices.save_cpu_scores()
        data = { 'detail': 'get cpu data done' }
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def gpu_scores(self, request):
        ScoreServices.save_gpu_scores()
        data = { 'detail': 'get gpu data done' }
        return Response(data, status=status.HTTP_200_OK)

    def list(self, request):
        query_text = request.query_params.get('name', None)
        query_option = request.query_params.get('option', None)
        queryset = Laptop.objects.all().values('id', 'name', 'price')
        if query_option == 'name':
            queryset = Laptop.objects.filter(name__icontains=query_text).values('id', 'name', 'price')
        elif query_option == 'cpu':
            queryset = Laptop.objects.filter(cpu__icontains=query_text).values('id', 'name', 'price')
        return Response(queryset)

    def retrieve(self, request, pk=None):
        laptop = get_object_or_404(Laptop, pk=pk)
        serializer = self.get_serializer(laptop)
        return Response(serializer.data)

    def update(self, request, pk=None):
        laptop = Laptop.objects.filter(id=pk).first()
        if not laptop:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(laptop, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def gpu_scores(self, request):
        ScoreServices.save_gpu_scores()
        data = { 'detail': 'get gpu data done' }
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def get_thumnails(self, request):
        ListDataServices.get_thumnails()
        data = { 'detail': 'get thumnails data done' }
        return Response(data, status=status.HTTP_200_OK)

