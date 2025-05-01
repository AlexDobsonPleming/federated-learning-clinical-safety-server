from rest_framework import serializers
from .models import FlModel

class ModelMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model  = FlModel
        fields = ['id', 'name', 'accuracy', 'generalisability', 'security']