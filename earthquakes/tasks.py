#!/usr/bin/env python3
from celery import shared_task
from django.core.cache import cache
from .utils import get_earthquakes, find_closest_earthquake
from .models import City, CachedEarthquakeData
import asyncio
from datetime import datetime, timedelta


@shared_task
def fetch_earthquakes_task(city_id, start_date, end_date):
    try:
        city = City.objects.get(id=city_id)
    except City.DoesNotExist:
        return {"message": "City not found"}

    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    cached_entries = CachedEarthquakeData.find_cached_data(
        city, start_date, end_date)

    missing_ranges = []
    current_start = start_date

    cached_data = []

    if cached_entries.exists():
        for entry in cached_entries:
            cached_data.append(entry.data)
            if current_start < entry.start_date:
                missing_ranges.append(
                    (current_start, entry.start_date - timedelta(days=1)))
            current_start = max(
                current_start, entry.end_date + timedelta(days=1))

    if current_start <= end_date:
        missing_ranges.append((current_start, end_date))

    new_data = []
    for missing_start, missing_end in missing_ranges:
        earthquakes = asyncio.run(get_earthquakes(missing_start, missing_end))
        if earthquakes is None:
            return {"message": "Failed to retrieve earthquakes"}

        closest_earthquake, distance = find_closest_earthquake(
            city, earthquakes)
        if closest_earthquake:
            new_data.append({
                "city": city.name,
                "magnitude": closest_earthquake['properties']['mag'],
                "place": closest_earthquake['properties']['place'],
                "date": closest_earthquake['properties']['time'],
                "distance_km": distance
            })

        CachedEarthquakeData.objects.create(
            city=city,
            start_date=missing_start,
            end_date=missing_end,
            data=new_data[-1]
        )

    combined_data = cached_data + new_data

    return combined_data
