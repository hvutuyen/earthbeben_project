import json
import requests
import time

def fetch_earthquake_data():
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.geojson"
    resp = requests.get(url=url)
    data = resp.json()  

    # extract data
    earthquakes = []
    for j in data["features"]:
        earthquake = {
            "longitude": j["geometry"]["coordinates"][0],
            "latitude": j["geometry"]["coordinates"][1],
            "magnitude": j["properties"]["mag"],
            "place": j["properties"]["place"],
            "time": time.ctime(j["properties"]["time"] / 1000)
        }
        earthquakes.append(earthquake)
    return earthquakes
