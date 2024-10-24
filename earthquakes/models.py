from django.db import models
from django.core.exceptions import ValidationError


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def clean(self):
        if not (-90 <= self.latitude <= 90):
            raise ValidationError(
                "Latitude must be between -90 and 90 degrees")
        if not (-90 <= self.longitude <= 90):
            raise ValidationError(
                "Longitude must be between -90 and 90 degrees")

    class Meta:
        unique_together = ('name', 'latitude', 'longitude')

    def __str__(self):
        return self.name


class CachedEarthquakeData(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    data = models.JSONField()

    class Meta:
        unique_together = ('city', 'start_date', 'end_date')

    def __str__(self):
        return f"Cached data for {self.city.name} from {self.start_date} to {self.end_date}"

    @staticmethod
    def find_cached_data(city, start_date, end_date):
        return CachedEarthquakeData.objects.filter(
            city=city,
            start_date__lte=end_date,
            end_date__gte=start_date
        )

    def clean(self):
        if self.end_date > timezone.now().date():
            self.end_date = timezone.now().date()
