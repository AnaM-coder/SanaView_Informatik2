import streamlit as st
import pandas as pd
import datetime
import re
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# === Login-Schutz ===
LoginManager().go_to_login("Start.py")

# === Session & Data ===
username = st.session_state.get("username")
session_key = "laborwerte"
file_name = f"{username}_daten.csv"
data_manager = DataManager()
data_manager.load_user_data(session_state_key=session_key, file_name=file_name)

# === Daten prüfen ===
if session_key not in st.session_state or st.session_state[session_key].empty:
    st.info("Noch keine Laborwerte vorhanden.")
    st.stop()

df = st.session_state[session_key].copy()
df["Datum"] = pd.to_datetime(df["Datum"], format="%d.%m.%Y")

# === Layout ===
st.title("📈 Verlauf Ihrer Laborwerte")

# === Laborwert-Auswahl ===
laborwert = st.selectbox("Laborwert auswählen", df["Laborwert"].unique())
daten = df[df["Laborwert"] == laborwert].copy()
daten = daten.sort_values("Datum")

# === Referenzbereich auslesen & bereinigen (z.B. "0–5") ===
raw_ref = daten["Referenz"].iloc[0]
ref_clean = re.sub(r"[–—−]", "-", raw_ref).replace(" ", "")
try:
    ref_min, ref_max = map(float, ref_clean.split("-"))
except:
    st.warning("Referenzwerte konnten nicht korrekt gelesen werden.")
    ref_min, ref_max = None, None

# === Daten nach Ampelfarbe filtern ===
grün = daten[daten["Ampel"].str.contains("🟢")]
gelb = daten[daten["Ampel"].str.contains("🟡")]
rot = daten[daten["Ampel"].str.contains("🔴")]

# === Diagramm 1 – Alle Werte ===
st.subheader(f"📊 Verlauf aller {laborwert}-Werte")
st.line_chart(daten.set_index("Datum")["Wert"])

# === Diagramm 2 – Nur 🟢 Normalwerte ===
if not grün.empty:
    st.subheader("🟢 Nur Werte im Normalbereich")
    st.line_chart(grün.set_index("Datum")["Wert"])

# === Diagramm 3 – Nur 🟡 Zu niedrig ===
if not gelb.empty:
    st.subheader("🟡 Zu niedrige Werte")
    st.line_chart(gelb.set_index("Datum")["Wert"])

# === Diagramm 4 – Nur 🔴 Zu hoch ===
if not rot.empty:
    st.subheader("🔴 Zu hohe Werte")
    st.line_chart(rot.set_index("Datum")["Wert"])

# === Legende ===
st.markdown("---")
st.markdown("### 🟢🟡🔴 Ampelfarben-Legende")
st.markdown("""
- 🟢 Wert im Referenzbereich  
- 🟡 Wert unterhalb des Referenzbereichs  
- 🔴 Wert oberhalb des Referenzbereichs
""")
