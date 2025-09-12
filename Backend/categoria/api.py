from rest_framework import viewsets
from .models import categoria
from .serializers import categoriaSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes

class categoriaViewSet(viewsets.ModelViewSet):
    queryset = categoria.objects.all()
    serializer_class = categoriaSerializer
    permission_classes = [AllowAny] 
