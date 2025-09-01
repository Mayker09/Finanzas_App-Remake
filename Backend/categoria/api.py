from rest_framework import viewsets
from .models import categoria
from .serializers import categoriaSerializer

class categoriaViewSet(viewsets.ModelViewSet):
    queryset = categoria.objects.all()
    serializer_class = categoriaSerializer
    permission_classes = [permissions.AllowAny]
