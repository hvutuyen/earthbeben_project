import streamlit as st
from fetch_data import fetch_earthquake_data
import pydeck as pdk
from ml_model import prepare_data, train_model, predict
import time
import pandas as pd

# ------- get data -----------------

# retrieve data
earthquakes = fetch_earthquake_data()
df = pd.DataFrame(earthquakes)

# -------- Streamlit Section -------------

### Streamlit App
st.title("Eartquake Visualisation and Prediction")

# ------------ filter data section --------

# filter widgets
min_magnitude = st.slider("Magnitude", 0.0, 10.0, 2.5, 0.1)
start_date = st.date_input("Startdatum", pd.to_datetime("today") - pd.Timedelta(days=7))
end_date = st.date_input("Enddatum", pd.to_datetime("today"))

# Daten filtern
filtered_df = df[(df['magnitude'] >= min_magnitude) & 
                 (pd.to_datetime(df['time']).dt.date >= start_date) & 
                 (pd.to_datetime(df['time']).dt.date <= end_date)]


# ------------ Map Section ---------------

# create basemap
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/dark-v9',
    initial_view_state=pdk.ViewState(
        latitude=20,
        longitude=0,
        zoom=0.5,
        pitch=0,
    ),

    # Layers 
    layers=[ 
        pdk.Layer(
            'ScatterplotLayer', # visualise location of eartquakes as points 
            data=filtered_df,
            get_position='[longitude, latitude]',
            get_color='[200, 30, 0, 160]',
            get_radius='magnitude * 30000',
            pickable=True,
            auto_highlight=True,
            tooltip=True,
        ),

        # pdk.Layer(
        #     'TextLayer', # text
        #     data=df,
        #     get_position='[longitude, latitude]',
        #     get_text='place',
        #     get_color='[0, 0, 0, 200]',
        #     get_size=15,
        #     get_alignment_baseline='"bottom"',
        #     pickable=True
        # ),
    ],

    tooltip={
        "html": "<b>Ort:</b> {place}<br/><b>Magnitude:</b> {magnitude}<br/><b>Zeit:</b> {time}",
        "style": {"color": "white"}
    },

    height=1000,
    width="100%"

))

# ----------- ML section ----------------

df_prepared = prepare_data(earthquakes)
model = train_model(df_prepared)

st.subheader("Erdbeben Vorhersage")
latitude = st.number_input("Breitengrad", value=0.0)
longitude = st.number_input("Längengrad", value=0.0)
timestamp = st.number_input("Unix-Zeitstempel", value=time.time())

if st.button("Vorhersage"):
    magnitude = predict(model, latitude, longitude, timestamp)
    st.write(f"Vorhergesagte Magnitude: {magnitude[0]:.2f}")