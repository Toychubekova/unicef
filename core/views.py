from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
import pandas as pd
from core import models, serializers, filters


class IndicatorViewSet(viewsets.ModelViewSet):
    queryset = models.Indicator.objects.all()
    serializer_class = serializers.IndicatorSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = filters.IndicatorFilter
    search_fields = ('name', )

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.IndicatorSerializerGet
        else:
            return serializers.IndicatorSerializer


class MetaDataViewSet(viewsets.ModelViewSet):
    queryset = models.MetaData.objects.all()
    serializer_class = serializers.MetaDataSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = filters.MetaDataFilter
    search_fields = ('name', )

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.MetaDataSerializerGet
        else:
            return serializers.MetaDataSerializer


class MediaViewSet(viewsets.ModelViewSet):
    queryset = models.Media.objects.all().order_by('-ordering')
    serializer_class = serializers.MediaSerializer


class NewsViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = models.News.objects.all()
    serializer_class = serializers.NewsSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('title', )

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.NewsSerializerGet
        else:
            return serializers.NewsSerializer


class PublicationViewSet(viewsets.ModelViewSet):
    queryset = models.Publication.objects.all()
    serializer_class = serializers.PublicationSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('title', )


class UseFullLinkViewSet(viewsets.ModelViewSet):
    queryset = models.UsefulLinks.objects.all()
    serializer_class = serializers.UsefulLinksSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('title', )


class HistoryViewSet(viewsets.ModelViewSet):
    queryset = models.History.objects.all()
    serializer_class = serializers.HistorySerializer

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.HistorySerializerGet
        else:
            return serializers.HistorySerializer


class DeleteIndicatorView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(request_body=serializers.DeleteIndicatorsSerializer())
    def post(self, request):
        indicators_ids = request.data['indicators']
        for indicator_id in indicators_ids:
            try:
                indicator = models.Indicator.objects.get(pk=indicator_id)
                indicator.delete()
            except:
                pass
        return Response('Indicator deleted', status=status.HTTP_200_OK)


class ImportIndicatorsView(APIView):
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
                    indicator = models.Indicator.objects.create(
                        name=item['name'], unit=item['unit'], category_id=item['category'],
                        subCategory_id=item['subCategory'], dateStart=item['dateStart'], dateEnd=item['dateEnd'],
                        accepted=item['accepted'], graphCategory_id=item['graphCategory'], value=item['value'],
                        color=item['color'], year=item['year'],
                        district_id=item['district'], state_id=item['state'], isVerified=item['isVerified']
                    )

                # for item in json_data['data']:
                #     indicator = models.Indicator.objects.create(**item)

                return Response({'status': 'ok'}, status=status.HTTP_200_OK)
            except:
                return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'File cannot be imported'}, status=status.HTTP_400_BAD_REQUEST)


class ImportMetaDataView(APIView):
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
                    indicator = models.MetaData.objects.create(
                        name=item['name'], type=item['type'], description=item['description'], icon=item['icon'],
                        indicator_id=item['indicator'], subCategory_id=item['subCategory'], value=item['value'],
                    )
                return Response({'status': 'ok'}, status=status.HTTP_200_OK)
            except:
                return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            pass
