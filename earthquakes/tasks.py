#!/usr/bin/env python3
import logging
from celery import shared_task
from django.core.cache import cache
from .utils import get_earthquakes, find_closest_earthquake
from .models import City, CachedEarthquakeData
import asyncio
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


@shared_task
def fetch_earthquakes_task(city_id, start_date, end_date):
    logger.info(
        f"Fetching earthquake data for city ID {city_id}, start: {start_date}, end: {end_date}")  # noqa

    city = get_city(city_id)
    if not city:
        logger.error(f"City with ID {city_id} not found.")
        return {"message": "City not found"}

    start_date, end_date = parse_dates(start_date, end_date)

    cached_data, missing_ranges = get_cached_and_missing_ranges(
        city, start_date, end_date)

    new_data = fetch_and_store_new_data(city, missing_ranges)

    combined_data = cached_data + new_data

    logger.info(
        f"Data fetching complete for city {city.name}. Combined data length: {len(combined_data)}")  # noqa
    return combined_data


def get_city(city_id):
    try:
        return City.objects.get(id=city_id)
    except City.DoesNotExist:
        return None


def parse_dates(start_date, end_date):
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    return start_date, end_date


def get_cached_and_missing_ranges(city, start_date, end_date):
    cached_entries = CachedEarthquakeData.find_cached_data(
        city, start_date, end_date)
    missing_ranges = []
    cached_data = []
    current_start = start_date

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

    logger.info(
        f"Found {len(cached_entries)} cached entries and {len(missing_ranges)} missing ranges for city {city.name}.")  # noqa
    return cached_data, missing_ranges


def fetch_and_store_new_data(city, missing_ranges):
    new_data = []
    for missing_start, missing_end in missing_ranges:
        logger.info(
            f"Fetching new data for missing range: {missing_start} to {missing_end}")  # noqa
        earthquakes = asyncio.run(get_earthquakes(missing_start, missing_end))
        if earthquakes is None:
            logger.error(
                f"Failed to retrieve earthquakes for range: {missing_start} to {missing_end}")  # noqa
            return {"message": "Failed to retrieve earthquakes"}

        closest_earthquake, distance = find_closest_earthquake(
            city, earthquakes)
        if closest_earthquake:
            earthquake_data = {
                "city": city.name,
                "magnitude": closest_earthquake['properties']['mag'],
                "place": closest_earthquake['properties']['place'],
                "date": closest_earthquake['properties']['time'],
                "distance_km": distance
            }
            new_data.append(earthquake_data)

            CachedEarthquakeData.objects.create(
                city=city,
                start_date=missing_start,
                end_date=missing_end,
                data=earthquake_data
            )
            logger.info(
                f"Stored new data for city {city.name} for range: {missing_start} to {missing_end}")  # noqa

    return new_data
