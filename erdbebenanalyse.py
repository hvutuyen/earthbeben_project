import json
import folium
import requests
import time

def mapping():

    #### Daten request ueber API

    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.geojson"
    param = dict()
    resp = requests.get(url=url, params = param)
    data = resp.json()  

    #### benoetigte Daten extrahieren  

    ln = []
    lt = []
    mag = []
    place = []
    utc_time = []

    for j in data["features"]:
        longi = j["geometry"]["coordinates"][0]
        lati = j["geometry"]["coordinates"][1]
        magni = j["properties"]["mag"]
        ort = j["properties"]["place"]
        utc = time.ctime(j["properties"]["time"]/1000) # Unixzeit in [ms] nach UTC umwandeln
        lt.append(longi)
        ln.append(lati)
        mag.append(magni)
        place.append(ort)
        utc_time.append(utc)

    #### Karte erstellen 

    map = folium.Map(location=[29.892464, 11.576124], zoom_start=1.5)
    fg = folium.FeatureGroup(name="Erdbeben")

    #### Funktion definieren, die die Magnitude in unterschiedlichen Farbskalen visualisiert 
    def colour(magnitude):
        if magnitude is not None:
            if magnitude < 4:
                return "green"
            elif 4 <= magnitude < 6:
                return "yellow"
            else:
                return "#FF0000"
        else:
            pass
    
    #### Funktion, die die groesse der Marker entsprechend der Magnitude darstellt
    def radien(magnitude):
        if magnitude is not None:
            return magnitude**3/15
        else:
            pass

    #### Marker durch iteration auf die Karte setzen  
    for lon, lat, plc, mg, utctime in zip(ln,lt, place, mag, utc_time):
        fg.add_child(folium.CircleMarker(location=[lon,lat],tooltip= str(plc),
                                        popup=folium.Popup("Magnitude: " + str(mg)+"\n"+"Zeitpunkt: " + utctime), 
                                        fill_color = colour(mg),color="grey",fill_opacity=0.6, radius = radien(mg)))

    map.add_child(fg)
    return map.save("templates/karte.html") # speichern der Karte in den Ordner "static", damit sie in das iFrame eingebunden werden kann


