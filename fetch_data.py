import json
import requests
import time
from geopy.geocoders import Nominatim

def fetch_earthquake_data():
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.geojson"
    resp = requests.get(url=url)
    data = resp.json()  

    earthquakes = []
    geolocator = Nominatim(user_agent="geoapiExercises")

    for j in data["features"]:
        longitude = j["geometry"]["coordinates"][0]
        latitude = j["geometry"]["coordinates"][1]
        magnitude = j["properties"]["mag"]
        place = j["properties"]["place"]
        time_utc = time.ctime(j["properties"]["time"] / 1000)

        # determine country from location
        location = geolocator.reverse(f"{latitude}, {longitude}", language='en', exactly_one=True)
        country = location.raw['address'].get('country', 'Unknown') if location else 'Unknown'

        earthquake = {
            "longitude": longitude,
            "latitude": latitude,
            "depth": depth,
            "magnitude": magnitude,
            "place": place,
            "country": country,
            "time": time_utc
        }
        earthquakes.append(earthquake)
    
    return earthquakes
