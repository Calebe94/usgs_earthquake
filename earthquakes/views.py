from django.shortcuts import get_object_or_404
from .utils import get_earthquakes, find_closest_earthquake
# from rest_framework.views import APIView
from adrf.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import generics, viewsets, status
from .models import City
from .serializers import CitySerializer
from asgiref.sync import sync_to_async


class CityCreateView(generics.CreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class EarthquakeSearchView(APIView):
    async def get(self, request, city_id):
        try:
            city = await sync_to_async(get_object_or_404)(City, id=city_id)
        except City.DoesNotExist:
            return Response({"message": "City not found"},
                            status=status.HTTP_404_NOT_FOUND)

        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:
            return Response({"message": "Start date and end date are required"},
                            status=status.HTTP_400_BAD_REQUEST)

        earthquakes = await get_earthquakes(start_date, end_date)
        if earthquakes is None:
            return Response({"message": "Failed to retrieve earthquakes"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        closest_earthquake, distance = await sync_to_async(
            find_closest_earthquake)(city, earthquakes)
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

        return Response(result, status=status.HTTP_200_OK)
