import json
import requests
import time
import re
from geopy.geocoders import Nominatim

# states in the us
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

def fetch_earthquake_data():
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.geojson"
    resp = requests.get(url=url)
    data = resp.json()  

    earthquakes = []
    geolocator = Nominatim(user_agent="earthquake-streamlit-app")

    for j in data["features"]:
        longitude = j["geometry"]["coordinates"][0]
        latitude = j["geometry"]["coordinates"][1]
        magnitude = j["properties"]["mag"]
        place = j["properties"]["place"]
        time_utc = time.ctime(j["properties"]["time"] / 1000)

        # extract country name from string with regex
        country_match = re.search(r'[^,]+$', place)
        region = country_match.group(0).strip() if country_match else 'Unknown'

        # if state in the us then set country to USA
        if region in US_STATES.values() or region in US_STATES.keys():
            region = 'United States'

        # if state name
        if region == 'Unknown' or len(region) < 3:
            location = geolocator.geocode(place, language='en')
            region = location.address.split(',')[-1].strip() if location else 'Unknown'

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
