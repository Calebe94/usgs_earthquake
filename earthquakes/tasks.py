#!/usr/bin/env python3
from celery import shared_task
from .utils import get_earthquakes, find_closest_earthquake
from .models import City
import asyncio


@shared_task
def fetch_earthquakes_task(city_id, start_date, end_date):
    try:
        city = City.objects.get(id=city_id)
    except City.DoesNotExist:
        return {"message": "City not found"}

    earthquakes = asyncio.run(get_earthquakes(start_date, end_date))
    if earthquakes is None:
        return {"message": "Failed to retrieve earthquakes"}

    closest_earthquake, distance = find_closest_earthquake(city, earthquakes)
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

    # TODO: save results in cache with TTL of 1 day
    return result
