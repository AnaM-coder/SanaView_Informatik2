import streamlit as st
import pandas as pd
from utils.data_manager import DataManager
from utils.login_manager import LoginManager
from datetime import date

# === Login prüfen ===
LoginManager().go_to_login("Start.py")
username = st.session_state.get("username")
if not username:
    st.stop()

# === Session Key & Datei ===
session_key = "profil_daten"
data_manager = DataManager()

# === Benutzerspezifisch laden ===
data_manager.load_user_data(
    session_state_key=session_key,
    file_name="profil.csv",
    initial_value=pd.DataFrame(columns=[
        "Name", "Vorname", "Geburtsdatum", "Geschlecht", "Schwanger",
        "Herkunft", "Vorerkrankung", "Medikamente", "Allergien"
    ])
)

# === Layout ===
st.title("Profilverwaltung")
st.subheader("Persönliche Angaben")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Name")
    geburtsdatum = st.date_input("Geburtsdatum", value=date(2000, 1, 1))

with col2:
    vorname = st.text_input("Vorname")
    geschlecht = st.radio("Geschlecht", ["Weiblich", "Männlich"])

schwanger = st.radio("Schwanger", ["Ja", "Nein", "Weiss nicht"])

herkunft = st.text_input("Herkunft / ethnischer Hintergrund")

st.subheader("Gesundheit")
vorerkrankung = st.text_area("Vorerkrankung")
medikamente = st.text_area("Medikamente")
allergien = st.text_area("Allergien / Besonderheiten")

# === Speichern ===
if st.button("Profil speichern"):
    eintrag = {
        "Name": name,
        "Vorname": vorname,
        "Geburtsdatum": geburtsdatum.strftime("%d.%m.%Y"),
        "Geschlecht": geschlecht,
        "Schwanger": schwanger,
        "Herkunft": herkunft,
        "Vorerkrankung": vorerkrankung,
        "Medikamente": medikamente,
        "Allergien": allergien
    }

    data_manager.append_record(session_state_key=session_key, record_dict=eintrag)
    st.success(" Profil gespeichert!")

# === Zurück zur Startseite ===
if st.button("Zurück zur Startseite"):
    st.switch_page("Start.py")
