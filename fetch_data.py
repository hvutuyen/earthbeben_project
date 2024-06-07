import json
import requests
import pandas as pd
import time
import re
from geopy.geocoders import Nominatim
import streamlit as st

# US-Bundesstaaten und deren abkuerzungen
US_STATES = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
    'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH',
    'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC',
    'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA',
    'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN',
    'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
    'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}

def geocode_place(geolocator, place):
    """Führt Geokodierung durch, um die Region basierend auf dem place-String zu bestimmen."""
    location = geolocator.geocode(place, language='en')
    if location:
        return location.address.split(',')[-1].strip()
    return 'Unknown'

def determine_region(place, geolocator):
    """Bestimmt die Region basierend auf dem place-String oder durch Geokodierung."""
    country_match = re.search(r'[^,]+$', place)
    region = country_match.group(0).strip() if country_match else 'Unknown'

    if region in US_STATES.values() or region in US_STATES.keys():
        return 'United States'
    
    if region == 'Unknown' or len(region) < 3:
        return geocode_place(geolocator, place)
    
    return region

@st.cache_data(ttl=3600)
def fetch_earthquake_data():
    """Abfrage der Erdbebendaten der letzten 30 Tage von der USGS API."""
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",
        "starttime": (pd.to_datetime('today') - pd.Timedelta(days=7)).strftime('%Y-%m-%d'),
        "endtime": pd.to_datetime('today').strftime('%Y-%m-%d'),
        "minmagnitude": 0.0
    }

    resp = requests.get(url=url, params=params)
    data = resp.json()
    geolocator = Nominatim(user_agent="earthquake-streamlit-app", timeout=10)
    earthquakes = []

    for feature in data["features"]:
        longitude = feature["geometry"]["coordinates"][0]
        latitude = feature["geometry"]["coordinates"][1]
        magnitude = feature["properties"]["mag"]
        place = feature["properties"]["place"]
        time_utc = time.ctime(feature["properties"]["time"] / 1000)
        region = determine_region(place, geolocator)

        earthquake = {
            "longitude": longitude,
            "latitude": latitude,
            "magnitude": magnitude,
            "place": place,
            "region": region,
            "time": time_utc
        }
        earthquakes.append(earthquake)
    
    return earthquakes

@st.cache_data(ttl=3600)
def fetch_strongest_earthquakes():
    """Abfrage der 10 stärksten Erdbeben seit 1900 von der USGS API."""
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",
        "starttime": "1900-01-01",
        "endtime": pd.to_datetime('today').strftime('%Y-%m-%d'),
        "minmagnitude": 8.0,
        "orderby": "magnitude",
        "limit": 10
    }

    resp = requests.get(url=url, params=params)
    data = resp.json()
    geolocator = Nominatim(user_agent="earthquake-streamlit-app", timeout=10)
    earthquakes = []

    for feature in data["features"]:
        longitude = feature["geometry"]["coordinates"][0]
        latitude = feature["geometry"]["coordinates"][1]
        magnitude = feature["properties"]["mag"]
        place = feature["properties"]["place"]
        time_utc = time.ctime(feature["properties"]["time"] / 1000)
        region = determine_region(place, geolocator)

        earthquake = {
            "longitude": longitude,
            "latitude": latitude,
            "magnitude": magnitude,
            "place": place,
            "region": region,
            "time": time_utc
        }
        earthquakes.append(earthquake)
    
    return earthquakes
