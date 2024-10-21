#!/usr/bin/env python3
import requests
from geopy.distance import geodesic


def get_earthquakes(start_date, end_date, min_magnitude=5.0):
    url = f"https://earthquake.usgs.gov/fdsnws/event/1/query.geojson"
    params = {
        "starttime": start_date,
        "endtime": end_date,
        "minmagnitude": min_magnitude,
        "orderby": "time"
    }
    response = requests.get(url, params=params)
    return response.json()


def find_closest_earthquake(city, earthquakes):
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
