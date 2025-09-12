from django.urls import path, include
from rest_framework import routers
from categoria import api


router = routers.DefaultRouter()
router.register(r'categoria', api.categoriaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]