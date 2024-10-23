from django.shortcuts import get_object_or_404
from .utils import get_earthquakes, find_closest_earthquake
from adrf.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import generics, viewsets, status
from .models import City
from .serializers import CitySerializer
from asgiref.sync import sync_to_async
from .tasks import fetch_earthquakes_task
from celery.result import AsyncResult


class CityCreateView(generics.CreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class EarthquakeSearchView(APIView):
    def get(self, request, city_id):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:
            return Response(
                {"message": "Start date and end date are required"},
                status=status.HTTP_400_BAD_REQUEST)

        task = fetch_earthquakes_task.delay(city_id, start_date, end_date)
        return JsonResponse(
            {"id": task.id},
            status=status.HTTP_202_ACCEPTED)


class EarthquakeResultView(APIView):
    def get(self, request, task_id):
        task_result = AsyncResult(task_id)

        if task_result.state == 'PENDING':
            return JsonResponse({"status": "Pending..."},
                                status=status.HTTP_202_ACCEPTED)
        elif task_result.state != 'FAILURE':
            return JsonResponse({"result": task_result.result},
                                status=status.HTTP_200_OK)
        else:
            return JsonResponse({"message": "Task failed"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
