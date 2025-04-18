import streamlit as st

def show_profil_verwaltung():
    st.title("Profilverwaltung")
    st.subheader("Persönliche Angaben")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name")
        geschlecht = st.radio("Geschlecht", ["Weiblich", "Männlich"])
        schwanger = st.radio("Schwanger", ["Ja", "Nein", "Weiss nicht"])
    with col2:
        vorname = st.text_input("Vorname")
        geburtsdatum = st.date_input("Geburtsdatum")

    herkunft = st.text_input("Herkunft / ethnischer Hintergrund")

    st.subheader("Gesundheit")
    vorerkrankung = st.text_area("Vorerkrankungen")
    medikamente = st.text_area("Medikamente")
    allergien = st.text_area("Allergien / Besonderheiten")

    col1, col2 = st.columns(2)
    with col1:
        if st.button(" Profil speichern"):
            st.success(" Profil erfolgreich gespeichert!")
    with col2:
        if st.button("Zurück zur Startseite"):
            st.switch_page("Start.py")  # funktioniert nur bei multipage Setupv