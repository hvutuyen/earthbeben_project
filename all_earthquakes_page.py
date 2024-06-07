import streamlit as st
from fetch_data import fetch_earthquake_data
import pydeck as pdk
import pandas as pd
import plotly.express as px

def show_earthquake_visualization_page():
    
    # Retrieve all data
    earthquakes = fetch_earthquake_data()
    df = pd.DataFrame(earthquakes)

    st.title("Visualisierung von Erdbebendaten der letzten 7 Tage")

    # ------------ Filter Data Section --------

    # Filter widgets
    min_magnitude = st.slider("Magnitude", 0.0, 10.0, 2.5, 0.1)

    # Daten filtern
    filtered_df = df[df['magnitude'] >= min_magnitude]

    # ------------ Map Section ---------------

    # Create basemap for all earthquakes
    st.subheader("Karte aller Erdbeben der letzten 7 Tage")
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
                'ScatterplotLayer', # Visualise location of earthquakes as points 
                data=filtered_df,
                get_position='[longitude, latitude]',
                get_color='[200, 30, 0, 160]',
                get_radius='magnitude * 30000',
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

    st.markdown("---")

    # ----------- Diagram Section -----------

    # Histogram magnitude
    st.subheader("Verteilung der Erdbebenmagnituden")
    fig_histogram = px.histogram(filtered_df, x='magnitude', nbins=30, title='Histogramm der Erdbebenmagnituden')
    fig_histogram.update_layout(
        xaxis_title='Magnitude',
        yaxis_title='Häufigkeit',
        bargap=0.1
    )
    st.plotly_chart(fig_histogram)


    st.markdown("""
        | Richter-Magnituden | Stärke     | Spürbarkeit und Auswirkungen                                         |
        |--------------------|------------|---------------------------------------------------------------------|
        | < 2,0              | Mikro      | Nicht spürbar                                                       |
        | 2,0 - < 3,0        | Gering     | Normalerweise nicht spürbar, aber messbar                           |
        | 3,0 - < 4,0        | Gering     | Oft spürbar, verursacht aber nur selten Schäden                     |
        | 4,0 - < 5,0        | Leicht     | Zimmergegenstände bewegen sich, Erschütterungsgeräusche sind zu hören, Schäden sind unwahrscheinlich |
        | 5,0 - < 6,0        | Moderat    | Anfällige Gebäude tragen Schäden davon, robuste Gebäude nur leichte oder keine Schäden |
        | 6,0 - < 7,0        | Stark      | Kann zu Zerstörungen in besiedelten Gebieten führen                 |
        | 7,0 - < 8,0        | Groß       | Kann schwere Schäden über weite Gebiete verursachen                 |
        | 8,0 - < 9,0        | Sehr groß  | Kann starke Zerstörung in Bereichen von einigen hundert Kilometern verursachen |
        | 9,0 - < 10,0       | Sehr groß  | Verheerende Zerstörung in Bereichen von tausend Kilometern          |
        | ≥ 10,0             | Massiv     | Wurde noch nie gemessen                                             |

        [Quelle](https://www.aktion-deutschland-hilft.de/de/fachthemen/natur-humanitaere-katastrophen/erdbeben/richterskala-ab-staerke-5-wird-es-gefaehrlich/)
                        
    """)

    st.markdown("---")


    st.subheader("Zeitreihe der Erdbeben")
    filtered_df['timestamp'] = pd.to_datetime(filtered_df['time'])
    filtered_df.set_index('timestamp', inplace=True)
    time_series = filtered_df.resample('D').size()
    fig_time_series = px.line(time_series, title='Anzahl der Erdbeben der letzten 7 Tage')
    fig_time_series.update_layout(
        xaxis_title='Datum',
        yaxis_title='Anzahl der Erdbeben'
    )
    st.plotly_chart(fig_time_series)

    st.markdown("---")


    # Count earthquakes by region
    st.subheader("Anzahl der Erdbeben nach Region")
    region_counts = filtered_df['region'].value_counts()
    fig_region_counts = px.bar(region_counts, x=region_counts.index, y=region_counts.values, title='Anzahl der Erdbeben nach Region')
    fig_region_counts.update_layout(
        xaxis_title='Region',
        yaxis_title='Anzahl der Erdbeben',
    )
    st.plotly_chart(fig_region_counts)
