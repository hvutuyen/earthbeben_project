import streamlit as st
from fetch_data import fetch_earthquake_data
import pydeck as pdk
from ml_model import prepare_data, train_model, predict
import time
import pandas as pd

# retrieve data
earthquakes = fetch_earthquake_data()
df = pd.DataFrame(earthquakes)

### Streamlit App
st.title("Eartquake Visualisation and Prediction")
st.write("Map.")

# create map
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=20,
        longitude=0,
        zoom=1.5,
        pitch=0,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=df,
            get_position='[longitude, latitude]',
            get_color='[200, 30, 0, 160]',
            get_radius='magnitude * 10000',
            pickable=True,
            auto_highlight=True
        ),
        pdk.Layer(
            'TextLayer',
            data=df,
            get_position='[longitude, latitude]',
            get_text='place',
            get_color='[0, 0, 0, 200]',
            get_size=15,
            get_alignment_baseline='"bottom"',
            pickable=True
        ),
    ],
))

# ML
df_prepared = prepare_data(earthquakes)
model = train_model(df_prepared)

st.subheader("Erdbeben Vorhersage")
latitude = st.number_input("Breitengrad", value=0.0)
longitude = st.number_input("Längengrad", value=0.0)
timestamp = st.number_input("Unix-Zeitstempel", value=time.time())

if st.button("Vorhersage"):
    magnitude = predict(model, latitude, longitude, timestamp)
    st.write(f"Vorhergesagte Magnitude: {magnitude[0]:.2f}")
