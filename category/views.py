from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
import pandas as pd

from category import models, serializers


class StateViewSet(viewsets.ModelViewSet):
    queryset = models.State.objects.all()
    serializer_class = serializers.StateSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('name', )
    pagination_class = None


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = models.District.objects.all()
    serializer_class = serializers.DistrictSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('name', )
    pagination_class = None

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.DistrictSerializerGet
        else:
            return serializers.DistrictSerializer


class IndicatorCategoryViewSet(viewsets.ModelViewSet):
    queryset = models.IndicatorCategory.objects.all().order_by('id')
    serializer_class = serializers.IndicatorCategorySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('name', )
    pagination_class = None


class IndicatorSubCategoryViewSet(viewsets.ModelViewSet):
    queryset = models.IndicatorSubCategory.objects.all().order_by('id')
    serializer_class = serializers.IndicatorSubCategorySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('name', )
    pagination_class = None

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.IndicatorSubCategorySerializerGet
        else:
            return serializers.IndicatorSubCategorySerializer


class NewsCategoryViewSet(viewsets.ModelViewSet):
    queryset = models.NewsCategory.objects.all()
    serializer_class = serializers.NewsCategorySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('name', )
    pagination_class = None


class ImageViewSet(viewsets.ModelViewSet):
    queryset = models.Image.objects.all()
    serializer_class = serializers.ImageSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('title', )
    pagination_class = None


class GraphCategoryViewSet(viewsets.ModelViewSet):
    queryset = models.GraphCategory.objects.all()
    serializer_class = serializers.GraphCategorySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('name', )
    pagination_class = None

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.GraphCategorySerializerGet
        else:
            return serializers.GraphCategorySerializer


class ImportCategoryView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        excel_file = request.FILES['file']
        try:
            xlsx = pd.ExcelFile(excel_file, engine='openpyxl')
            sheets_data = {sheet_name: xlsx.parse(sheet_name) for sheet_name in xlsx.sheet_names}
            json_data = {'data': data.to_dict(orient='records') for sheet_name, data in sheets_data.items()}

            try:
                for item in json_data['data']:
                    category = models.IndicatorCategory.objects.create(
                        name=item['name'], description=item['description'],
                        icon=item['icon'], iconSecond=item['iconSecond']
                    )
                return Response({'status': 'ok'}, status=status.HTTP_200_OK)
            except:
                return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            pass


class ImportSubCategoryView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        excel_file = request.FILES['file']
        try:
            xlsx = pd.ExcelFile(excel_file, engine='openpyxl')
            sheets_data = {sheet_name: xlsx.parse(sheet_name) for sheet_name in xlsx.sheet_names}
            json_data = {'data': data.to_dict(orient='records') for sheet_name, data in sheets_data.items()}

            try:
                for item in json_data['data']:
                    subcategory = models.IndicatorSubCategory.objects.create(
                        name=item['name'], category_id=item['category'], description=item['description'],
                        icon=item['icon'], iconSecond=item['iconSecond'],
                        additionalDataTitle=item['additionalDataTitle'], addDataDesc=item['addDataDesc']
                    )
                return Response({'status': 'ok'}, status=status.HTTP_200_OK)
            except:
                return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            pass
