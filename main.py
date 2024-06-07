import streamlit as st
from all_earthquakes_page import show_earthquake_visualization_page
from strongest_earthquakes_page import show_strongest_earthquakes_page
from expl_page import show_explanation_page

def main():

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Wähle eine Seite aus", ["Einleitung", "Erdbebenvisualisierung", "Historische Erdbeben", "API und Nutzung"])

    if page == "Einleitung":
        show_home_page()
    elif page == "Erdbebenvisualisierung":
        show_earthquake_visualization_page()
    elif page == "Historische Erdbeben":
        show_strongest_earthquakes_page()
    elif page == "API und Nutzung":
        show_explanation_page()

def show_home_page():
    st.title("Visualisierung von Erdbebendaten")
    st.markdown("""
    Diese Applikation zeigt Erdbebendaten, basierend auf Daten, die von der USGS Earthquake API bereitgestellt werden. 

    - **Erdbebenvisualisierung:** Zeigt die Erdbeben der letzten 7 Tage.
    - **Historische Erdbeben:** Zeigt die 10. stärksten Erdbeben seit 1990.
    - **API und Nutzung:** Erläuterung der APIs und wie sie verwendet werden.
    """)

if __name__ == "__main__":
    main()
