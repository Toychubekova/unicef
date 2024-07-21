from django.urls import path, include
from . import views
from .views import *
from rest_framework.routers import SimpleRouter

app_name = 'category'

router = SimpleRouter()

router.register(r'state', views.StateViewSet)
router.register(r'district', views.DistrictViewSet)
router.register(r'indicatorCategory', views.IndicatorCategoryViewSet)
router.register(r'indicatorSubCategory', views.IndicatorSubCategoryViewSet)
router.register(r'newsCategory', views.NewsCategoryViewSet)
router.register(r'image', views.ImageViewSet)
router.register(r'graph_category', views.GraphCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('import_category/', views.ImportCategoryView.as_view()),
    path('import_sub_category/', views.ImportSubCategoryView.as_view()),
]
