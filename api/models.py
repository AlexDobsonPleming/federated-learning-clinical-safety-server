from typing import Optional
from django.db import models

class FlModel(models.Model):
    name: str = models.CharField(max_length=100)
    accuracy: Optional[float] = models.FloatField(null=True, blank=True)
    generalisability: Optional[float] = models.FloatField(null=True, blank=True)
    privacy: Optional[float] = models.FloatField(null=True, blank=True)
    leakage_chance: Optional[float] = models.FloatField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class LocalModel(models.Model):
    fl_model: FlModel = models.ForeignKey(
        FlModel,
        related_name='local_models',
        on_delete=models.CASCADE
    )
    name: str = models.CharField(max_length=100)
    privacy: Optional[float] = models.FloatField(null=True, blank=True)
    leakage_chance: Optional[float] = models.FloatField(null=True, blank=True)
    noise: Optional[float] = models.FloatField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.fl_model.name})"
