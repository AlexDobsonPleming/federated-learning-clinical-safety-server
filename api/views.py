from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import FlModel, LocalModel
from .serializers import FlModelSerializer, LocalModelSerializer


class FlModelViewSet(viewsets.ModelViewSet):
    queryset         = FlModel.objects.all()
    serializer_class = FlModelSerializer
    permission_classes = [IsAuthenticated]

class LocalModelViewSet(viewsets.ModelViewSet):
    serializer_class = LocalModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # `model_pk` comes from the nested router lookup
        return LocalModel.objects.filter(fl_model_id=self.kwargs['model_pk'])

    def perform_create(self, serializer):
        # serializer.save() will set fl_model based on the URL
        serializer.save(fl_model_id=self.kwargs['model_pk'])
