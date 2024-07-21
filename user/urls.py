from django.urls import path, include
from . import views
from .views import *
from rest_framework.routers import SimpleRouter

app_name = 'user'

router = SimpleRouter()

router.register(r'user', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
