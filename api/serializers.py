from rest_framework import serializers
from .models import FlModel, LocalModel

class FlModelSerializer(serializers.ModelSerializer):
    class Meta:
        model  = FlModel
        fields = ['id', 'name', 'accuracy', 'generalisability', 'security']

class LocalModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalModel
        fields = ('id', 'name', 'relatability', 'source')