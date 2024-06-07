import streamlit as st

def show_explanation_page():

    st.title("Erläuterung zu den APIs und deren Nutzung")

    st.markdown("""
    ## USGS Earthquake API

    Die USGS Earthquake API stellt Daten über Erdbeben weltweit bereit. Diese API wird vom United States Geological Survey (USGS) betrieben und liefert detaillierte Informationen über Erdbeben, einschließlich Zeitpunkt, Ort, Magnitude, Tiefe etc.

    **Hauptmerkmale:**
    - **Zeitraum:** Daten ab 1900, für einige Regionen sogar früher.
    - **Datenformat:** GeoJSON, das sich gut für die Integration in geografische Informationssysteme (GIS) eignet.
    - **Frei verfügbar:** kostenlos, jedoch Rate Limits.

    Weitere Informationen: [USGS Earthquake API Dokumentation](https://earthquake.usgs.gov/fdsnws/event/1/).
    
    ---
    ## Geopy

    Geopy ist eine Python-Bibliothek für das Geocoding. Sie unterstützt mehrere Geokodierungsdienste, darunter Nominatim (OpenStreetMap), Google Geocoding API, Bing Maps API und viele andere.

    **Hauptmerkmale:**
    - **Unterstützte Dienste:** Nominatim (OpenStreetMap), Google Geocoding API, Bing Maps API, OpenCage und andere.
    - **Einheitliche API:** Einfache Integration und Wechsel zwischen verschiedenen Geocoding-Diensten.
    - **Kosten:** kostenlos (Nominatin), aber andere Geocoding-Dienste können Kosten verursachen.

    Weitere Informationen: [Geopy Dokumentation](https://geopy.readthedocs.io/).

    ## Nutzung

    Die Daten für diese Applikation werden von der USGS Earthquake API bezogen. Zusätzlich wird Geopy verwendet, um geografische Koordinaten in Ortsnamen umzuwandeln.

    **Variablen:**
    - **Zeit:** Zeitpunkt des Erdbebens im UTC-Format.
    - **Ort:** Beschreibung des Ortes, an dem das Erdbeben stattgefunden hat.
    - **Magnitude:** Stärke des Erdbebens auf der Richterskala.

    """)
