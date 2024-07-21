from rest_framework import serializers
from category import models
from django.contrib.auth import get_user_model, authenticate, password_validation
from django_filters import rest_framework as filters
User = get_user_model()
from rest_framework.authtoken.models import Token


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.State
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.District
        fields = ('id', 'name', 'state')


class DistrictSerializerGet(serializers.ModelSerializer):
    state = StateSerializer()

    class Meta:
        model = models.District
        fields = ('id', 'name', 'state')


class IndicatorCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IndicatorCategory
        fields = '__all__'


class IndicatorSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IndicatorSubCategory
        fields = ('id', 'name', 'category', 'icon', 'iconSecond', 'description', 'additionalDataTitle', 'addDataDesc')


class IndicatorSubCategorySerializerGet(serializers.ModelSerializer):
    category = IndicatorCategorySerializer()

    class Meta:
        model = models.IndicatorSubCategory
        fields = ('id', 'name', 'category', 'icon', 'iconSecond', 'description', 'additionalDataTitle', 'addDataDesc')


class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NewsCategory
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = ('id', 'title', 'image', 'forSvg')


class GraphCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GraphCategory
        fields = ('id', 'name', 'value', 'subCategory')


class GraphCategorySerializerGet(serializers.ModelSerializer):
    subCategory = IndicatorSubCategorySerializerGet()

    class Meta:
        model = models.GraphCategory
        fields = ('id', 'name', 'value', 'subCategory')
