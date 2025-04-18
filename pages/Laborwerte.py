import streamlit as st
import pandas as pd
import datetime
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# Login & DataManager initialisieren
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="SanaView2")
login_manager = LoginManager(data_manager)
login_manager.login_register()

# Authentifizierung prüfen
if not st.session_state.get("authentication_status", False):
    st.stop()

username = st.session_state.get("username", "Unbekannt")
filename = f"{username}_laborwerte.csv"

# Standardstruktur
initial_df = pd.DataFrame(columns=["Datum", "Laborwert", "Wert", "Einheit", "Referenz", "Ampel"])

# Daten laden
try:
    df = data_manager.load_user_file(filename, as_df=True, parse_dates=["Datum"])
except FileNotFoundError:
    df = initial_df.copy()

# UI: Eingabe
st.title("🧪 Laborwerte – Eingabe")

laboroptionen = {
    "CRP": {"einheit": "mg/L", "ref_min": 0, "ref_max": 5},
    "TSH": {"einheit": "mIU/L", "ref_min": 0.4, "ref_max": 4.0},
    "Glucose": {"einheit": "mg/dL", "ref_min": 70, "ref_max": 99}
}

ausgewählt = st.selectbox("Laborwert auswählen", list(laboroptionen.keys()))
einheit = laboroptionen[ausgewählt]["einheit"]
ref_min = laboroptionen[ausgewählt]["ref_min"]
ref_max = laboroptionen[ausgewählt]["ref_max"]

col1, col2 = st.columns(2)
with col1:
    wert = st.number_input("Wert", min_value=0.0, step=0.1)
    datum = st.date_input("Datum", value=datetime.date.today())
with col2:
    st.text_input("Einheit", value=einheit, disabled=True)
    st.text_input("Referenzbereich", value=f"{ref_min} – {ref_max} {einheit}", disabled=True)

# Speichern
if st.button("💾 Speichern"):
    if wert < ref_min:
        ampel = "🟡 (zu niedrig)"
    elif wert > ref_max:
        ampel = "🔴 (zu hoch)"
    else:
        ampel = "🟢 (normal)"

    neuer_eintrag = pd.DataFrame([{
        "Datum": datum,
        "Laborwert": ausgewählt,
        "Wert": wert,
        "Einheit": einheit,
        "Referenz": f"{ref_min}–{ref_max}",
        "Ampel": ampel
    }])

    df = pd.concat([df, neuer_eintrag], ignore_index=True)
    data_manager.save_user_file(filename, df)
    st.success("✅ Laborwert erfolgreich gespeichert!")

# Anzeige
st.markdown("---")
st.subheader("🧾 Ihre bisherigen Einträge")
st.dataframe(df.sort_values("Datum", ascending=False), use_container_width=True)
