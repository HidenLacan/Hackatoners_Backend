from rest_framework import serializers
from .models import DataRecord

class DataRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataRecord
        fields = '__all__'  # Incluir todos los campos en la salida serializada
