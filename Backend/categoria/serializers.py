from rest_framework import serializers
from .models import categoria

class categoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = categoria
        fields = '__all__'
