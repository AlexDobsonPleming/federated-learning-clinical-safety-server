from django.db import models

class FlModel(models.Model):
    name = models.CharField(max_length=100)
    accuracy = models.FloatField()
    generalisability = models.FloatField()
    security = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name