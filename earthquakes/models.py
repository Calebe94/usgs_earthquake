from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        # Garantir unicidade
        unique_together = ('name', 'latitude', 'longitude')

    def __str__(self):
        return self.name
