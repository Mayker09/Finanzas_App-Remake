from rest_framework import viewsets
from .models import transaccion
from .serializers import transaccionSerializer

class transaccionViewSet(viewsets.ModelViewSet):
    queryset = transaccion.objects.all()
    serializer_class = transaccionSerializer
    permission_classes = [permissions.AllowAny]