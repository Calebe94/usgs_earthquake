#!/usr/bin/env python3
from celery import shared_task
from django.core.cache import cache
from .utils import get_earthquakes, find_closest_earthquake
from .models import City
import asyncio


@shared_task
def fetch_earthquakes_task(city_id, start_date, end_date):
    cache_key = f"earthquake_{city_id}_{start_date}_{end_date}"

    cached_result = cache.get(cache_key)
    if cached_result:
        return cached_result

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

    cache.set(cache_key, result, timeout=60*60*24)

    return result
