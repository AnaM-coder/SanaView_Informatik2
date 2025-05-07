import streamlit as st
import pandas as pd
from datetime import date
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# === Login absichern ===
LoginManager().go_to_login("Start.py")
username = st.session_state.get("username")
if not username:
    st.stop()

# === DataManager & SessionState
session_key = "profil_daten"
data_manager = DataManager()

data_manager.load_user_data(
    session_state_key=session_key,
    file_name="profil.csv",
    initial_value=pd.DataFrame(columns=[
        "Name", "Vorname", "Geburtsdatum", "Geschlecht", "Schwanger",
        "Herkunft", "Vorerkrankung", "Medikamente", "Allergien"
    ])
)

# === UI: Formular
st.title("Profilverwaltung")
st.subheader("Persönliche Angaben")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Name*", help="Pflichtfeld")
    geburtsdatum = st.date_input("Geburtsdatum*", value=date(2000, 1, 1), help="Pflichtfeld")
with col2:
    vorname = st.text_input("Vorname*", help="Pflichtfeld")
    geschlecht = st.radio("Geschlecht*", ["Weiblich", "Männlich"], horizontal=True, help="Pflichtfeld")

schwanger = st.radio("Schwanger*", ["Ja", "Nein", "Weiss nicht"], horizontal=True, help="Pflichtfeld")

herkunft = st.text_input(
    "Herkunft / ethnischer Hintergrund",
    help="Für eine medizinisch fundierte Einordnung Ihrer Werte können Faktoren wie ethnischer Hintergrund, genetische Veranlagung oder regionale Besonderheiten eine Rolle spielen. Diese Daten dienen ausschliesslich der individuellen Bewertung und werden vertraulich behandelt."
)

st.subheader("Gesundheit")
vorerkrankung = st.text_area("Vorerkrankung")
medikamente = st.text_area("Medikamente")
allergien = st.text_area("Allergien / Besonderheiten")

# === Validierung & Speichern
if st.button("Profil speichern"):
    if not name or not vorname or not geschlecht or not schwanger:
        st.error("❌ Bitte füllen Sie alle mit * markierten Pflichtfelder aus.")
    else:
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
        st.success("✅ Profil erfolgreich gespeichert!")

# === Navigation
if st.button("Zurück zur Startseite"):
    st.switch_page("Start.py")
