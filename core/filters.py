from django_filters import rest_framework as filters
from core import models
from django_filters import FilterSet


class IndicatorFilter(FilterSet):
    subCategory = filters.CharFilter('subCategory')
    graphCategory = filters.CharFilter('graphCategory')
    year = filters.CharFilter('year')
    district = filters.CharFilter('district')
    state = filters.CharFilter('state')
    isVerified = filters.BooleanFilter('isVerified')
    category = filters.CharFilter('category')

    class Meta:
        models = models.Indicator
        fields = ('subCategory', 'graphCategory', 'year', 'district', 'state', 'isVerified', 'category')


class MetaDataFilter(FilterSet):
    subCategory = filters.CharFilter('subCategory')

    class Meta:
        model = models.MetaData
        fields = ('subCategory', )
