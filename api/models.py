from django.db import models

class FlModel(models.Model):
    name              = models.CharField(max_length=100)
    accuracy          = models.FloatField()
    precision         = models.FloatField()
    cross_validation  = models.FloatField()
    security          = models.FloatField()

    def __str__(self):
        return self.name
