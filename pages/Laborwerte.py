import streamlit as st
import datetime
import pandas as pd
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# === Login-Check ===
data_manager = DataManager()
login_manager = LoginManager(data_manager)
login_manager.go_to_login("Start.py")

# === Nutzername prüfen ===
username = st.session_state.get("username")
if not username:
    st.stop()

# === Benutzer-Dateiname automatisch festlegen
session_key = "laborwerte_df"
dateiname = "laborwerte.csv"

# === Benutzerspezifische Daten laden
data_manager.load_user_data(
    session_state_key=session_key,
    file_name=dateiname,
    initial_value=pd.DataFrame(columns=["Datum", "Laborwert", "Wert", "Einheit", "Referenz", "Ampel"])
)

# === Titel
st.title("🧪 Laborwerte – Eingabe")

# === Laboroptionen
laboroptionen = {
    "CRP": {"einheit": "mg/L", "ref_min": 0, "ref_max": 5},
    "TSH": {"einheit": "mIU/L", "ref_min": 0.4, "ref_max": 4.0},
    "Glucose": {"einheit": "mg/dL", "ref_min": 70, "ref_max": 99}
}

# === Auswahl & Formular
auswahl = st.selectbox("Laborwert", list(laboroptionen.keys()))
meta = laboroptionen[auswahl]
einheit, ref_min, ref_max = meta["einheit"], meta["ref_min"], meta["ref_max"]

col1, col2 = st.columns(2)
with col1:
    wert = st.number_input("Wert", min_value=0.0, step=0.1)
    datum = st.date_input("Datum", value=datetime.date.today())
with col2:
    st.text_input("Einheit", value=einheit, disabled=True)
    st.text_input("Referenz", value=f"{ref_min}–{ref_max} {einheit}", disabled=True)

# === Speichern
if st.button("💾 Speichern"):
    ampel = "🟡 (zu niedrig)" if wert < ref_min else "🔴 (zu hoch)" if wert > ref_max else "🟢 (normal)"

    neuer_eintrag = {
        "Datum": datum.strftime("%d.%m.%Y"),
        "Laborwert": auswahl,
        "Wert": wert,
        "Einheit": einheit,
        "Referenz": f"{ref_min}–{ref_max}",
        "Ampel": ampel
    }

    data_manager.append_record(session_state_key=session_key, record_dict=neuer_eintrag)
    st.success("✅ Laborwert gespeichert.")

# === Tabelle anzeigen
df = st.session_state[session_key]
if not df.empty:
    st.markdown("---")
    st.subheader("📋 Gespeicherte Laborwerte")
    st.dataframe(df, use_container_width=True)

    # DEBUG: Pfad zeigen
    pfad = data_manager.data_reg.get(session_key, "⚠️ Kein Pfad gefunden")
    st.caption(f"Aktive Datei: `{pfad}`")
