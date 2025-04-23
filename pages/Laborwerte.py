import streamlit as st
import datetime
import pandas as pd
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# === Login-Schutz ===
LoginManager().go_to_login('Start.py')

# === Nutzername prüfen ===
username = st.session_state.get("username")
if not username:
    st.error("⚠️ Kein Benutzer eingeloggt! Anmeldung erforderlich.")
    st.stop()

# === DataManager initialisieren ===
data_manager = DataManager()

# === Benutzerdaten laden → Dateiname basierend auf Benutzername ===
session_key = f"user_data_{username}"
file_name = f"{username}_daten.csv"  # Dynamischer Dateiname basierend auf Benutzername

data_manager.load_user_data(
    session_state_key=session_key,
    file_name=file_name,  # Übergabe des dynamischen Dateinamens
    initial_value=pd.DataFrame(columns=["Datum", "Laborwert", "Wert", "Einheit", "Referenz", "Ampel"])
)

# === Titel & Laborwert-Auswahl ===
st.title(" Laborwerte – Eingabe")

laboroptionen = {
    "CRP": {"einheit": "mg/L", "ref_min": 0, "ref_max": 10},
    "TSH": {"einheit": "mIU/L", "ref_min": 0.4, "ref_max": 4.0},
    "Glucose": {"einheit": "mg/dL", "ref_min": 70, "ref_max": 99}
}

ausgewählt = st.selectbox("Laborwert", list(laboroptionen.keys()))
einheit = laboroptionen[ausgewählt]["einheit"]
ref_min = laboroptionen[ausgewählt]["ref_min"]
ref_max = laboroptionen[ausgewählt]["ref_max"]

# === Eingabeformular ===
col1, col2 = st.columns(2)
with col1:
    wert = st.number_input("Wert", min_value=0.0, step=0.1)
    datum = st.date_input("Datum", value=datetime.date.today())
with col2:
    st.text_input("Einheit", value=einheit, disabled=True)
    st.text_input("Referenz", value=f"{ref_min}–{ref_max} {einheit}", disabled=True)

# === Speichern ===
if st.button(" Speichern"):
    if wert < ref_min:
        ampel = "🟡 (zu niedrig)"
    elif wert > ref_max:
        ampel = "🔴 (zu hoch)"
    else:
        ampel = "🟢 (normal)"

    neuer_eintrag = {
        "Datum": datum.strftime("%d.%m.%Y"),
        "Laborwert": ausgewählt,
        "Wert": wert,
        "Einheit": einheit,
        "Referenz": f"{ref_min}–{ref_max}",
        "Ampel": ampel
    }

    data_manager.append_record(
        session_state_key=session_key,
        record_dict=neuer_eintrag
    )

    st.success(" Laborwert erfolgreich gespeichert!")

# === Tabelle anzeigen ===
if not st.session_state[session_key].empty:
    st.markdown("---")
    st.subheader(" Ihre gespeicherten Laborwerte")
    st.dataframe(st.session_state[session_key], use_container_width=True)