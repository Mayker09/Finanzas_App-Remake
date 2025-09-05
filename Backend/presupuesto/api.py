from rest_framework import viewsets
from .models import presupuesto
from .serializers import PresupuestoSerializer
from rest_framework import permissions

class PresupuestoViewSet(viewsets.ModelViewSet):
    queryset = presupuesto.objects.all()
    serializer_class = PresupuestoSerializer
    permission_classes = [permissions.AllowAny]