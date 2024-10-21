#!/usr/bin/env python3
import httpx
from geopy.distance import geodesic
from typing import Any, Dict, Tuple, Optional


async def get_earthquakes(start_date: str, end_date: str, min_magnitude: float = 5.0) -> Optional[Dict[str, Any]]:
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query.geojson"
    params = {
        "starttime": start_date,
        "endtime": end_date,
        "minmagnitude": min_magnitude,
        "orderby": "time"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()
    except httpx.RequestError as e:
        print(f"Request error: {e}")
    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e.response.status_code} - {e.response.text}")
    return None


def find_closest_earthquake(city, earthquakes: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], float]:
    city_coords = (city.latitude, city.longitude)
    closest_event = None
    closest_distance = float('inf')

    for quake in earthquakes['features']:
        # Lon/Lat to Lat/Lon
        quake_coords = quake['geometry']['coordinates'][:2][::-1]
        distance = geodesic(city_coords, quake_coords).kilometers
        if distance < closest_distance:
            closest_distance = distance
            closest_event = quake

    return closest_event, closest_distance
