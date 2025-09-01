from django.urls import path, include
from rest_framework import routers
from . import api

router = routers.DefaultRouter()
router.register(r'transaccion', api.transaccionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]