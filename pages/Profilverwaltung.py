import streamlit as st
import pandas as pd
import os
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# === Login-Check (optional) ===
if not st.session_state.get("authentication_status", False):
    st.stop()

# === Profil-Verwaltung Seite ===
st.title("🧾 Profilverwaltung")
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
