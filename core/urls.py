from django.urls import path, include
from . import views
from .views import *
from rest_framework.routers import SimpleRouter

app_name = 'core'

router = SimpleRouter()

router.register(r'indicator', views.IndicatorViewSet)
router.register(r'metaData', views.MetaDataViewSet)
router.register(r'media', views.MediaViewSet)
router.register(r'news', views.NewsViewSet)
router.register(r'publication', views.PublicationViewSet)
router.register(r'usefulLinks', views.UseFullLinkViewSet)
router.register(r'history', views.HistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('delete_indicator/', views.DeleteIndicatorView.as_view()),
    path('import_indicators/', views.ImportIndicatorsView.as_view()),
    path('import_metaData/', views.ImportMetaDataView.as_view()),
]
