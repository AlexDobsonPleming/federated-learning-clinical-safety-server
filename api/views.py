from rest_framework import viewsets
from .models import FlModel
from .serializers import ModelMetricSerializer

class FlModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset         = FlModel.objects.all()
    serializer_class = ModelMetricSerializer
