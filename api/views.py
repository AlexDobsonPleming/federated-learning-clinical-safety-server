from rest_framework import viewsets
from .models import FlModel, LocalModel
from .serializers import FlModelSerializer, LocalModelSerializer

class FlModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset         = FlModel.objects.all()
    serializer_class = FlModelSerializer

class LocalModelViewSet(viewsets.ModelViewSet):
    serializer_class = LocalModelSerializer

    def get_queryset(self):
        # `model_pk` comes from the nested router lookup
        return LocalModel.objects.filter(fl_model_id=self.kwargs['model_pk'])
