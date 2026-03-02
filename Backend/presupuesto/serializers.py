from rest_framework import serializers
from .models import presupuesto



class PresupuestoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(
        source='categoria.nombre',
        read_only=True
    )
    class Meta:        
        model = presupuesto
        fields = '__all__'
