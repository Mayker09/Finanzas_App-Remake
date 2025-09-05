from rest_framework import serializers
from .models import transaccion

class transaccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = transaccion
        fields = '__all__'
