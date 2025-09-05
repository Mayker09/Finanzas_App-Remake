from rest_framework import serializers
from .models import presupuesto

class PresupuestoSerializer(serializers.ModelSerializer):
    class Meta:        
        model = presupuesto
        fields = '__all__'
