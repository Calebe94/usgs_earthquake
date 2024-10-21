from .utils import get_earthquakes, find_closest_earthquake
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render

from rest_framework import generics, viewsets
from .models import City
from .serializers import CitySerializer


class CityCreateView(generics.CreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class EarthquakeSearchView(APIView):
    def get(self, request, city_id):
        city = City.objects.get(id=city_id)
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        earthquakes = get_earthquakes(start_date, end_date)
        closest_earthquake, distance = find_closest_earthquake(
            city, earthquakes)

        if closest_earthquake:
            result = {
                "city": city.name,
                "magnitude": closest_earthquake['properties']['mag'],
                "place": closest_earthquake['properties']['place'],
                "date": closest_earthquake['properties']['time'],
                "distance_km": distance
            }
        else:
            result = {"message": "No results found"}

        return Response(result)
