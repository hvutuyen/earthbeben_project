import streamlit as st
from fetch_data import fetch_strongest_earthquakes
import pydeck as pdk
import pandas as pd
import plotly.express as px

def show_strongest_earthquakes_page():
    # Retrieve strongest earthquakes
    strongest_earthquakes = fetch_strongest_earthquakes()
    strongest_df = pd.DataFrame(strongest_earthquakes)

    st.title("Die 10 stärksten Erdbeben seit 1990")

    # ------------ Strongest Earthquakes Map Section ---------------

    # Create basemap for strongest earthquakes
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v9',
        initial_view_state=pdk.ViewState(
            latitude=20,
            longitude=0,
            zoom=0.5,
            pitch=0,
        ),
        layers=[ 
            pdk.Layer(
                'ScatterplotLayer', # Visualise location of earthquakes as points 
                data=strongest_df,
                get_position='[longitude, latitude]',
                get_color='[200, 30, 0, 160]',
                get_radius='magnitude * 40000',
                pickable=True,
                auto_highlight=True,
            ),
        ],
        tooltip={
            "html": "<b>Ort:</b> {place}<br/><b>Magnitude:</b> {magnitude}<br/><b>Zeit:</b> {time}",
            "style": {"color": "white"}
        },
        height=800,
        width="100%"
    ))

    # strongest earthquake barchart
    strongest_df = strongest_df.sort_values(by='magnitude', ascending=False)
    fig_strongest = px.bar(strongest_df, y='place', x='magnitude',
                           hover_data=['time', 'region'], orientation='h')
    fig_strongest.update_layout(
        xaxis_title='Magnitude',
        yaxis_title='Ort',
        yaxis={'categoryorder':'total ascending'}
    )
    st.plotly_chart(fig_strongest)
