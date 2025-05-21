from django.db import models

class FlModel(models.Model):
    name = models.CharField(max_length=100)
    accuracy = models.FloatField()
    generalisability = models.FloatField()
    security = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

class LocalModel(models.Model):
    fl_model = models.ForeignKey(
        FlModel,
        related_name='local_models',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    relatability = models.FloatField()
    source = models.CharField(max_length=100)     # <-- new field

    def __str__(self):
        return f"{self.name} ({self.fl_model.name})"
