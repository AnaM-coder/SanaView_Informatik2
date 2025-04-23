import streamlit as st
import pandas as pd
import datetime
import re
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# === Login-Schutz ===
LoginManager().go_to_login("Start.py")

# === Initialisierung
username = st.session_state.get("username")
session_key = "laborwerte"
file_name = f"{username}_daten.csv"
data_manager = DataManager()
data_manager.load_user_data(session_state_key=session_key, file_name=file_name)

# === Daten laden & prüfen
if session_key not in st.session_state or st.session_state[session_key].empty:
    st.info("Noch keine Laborwerte vorhanden.")
    st.stop()

df = st.session_state[session_key].copy()
df["Datum"] = pd.to_datetime(df["Datum"], format="%d.%m.%Y")

# === Auswahl
st.title("Verlauf")
laborwert = st.selectbox("Laborwert auswählen", df["Laborwert"].unique())
daten = df[df["Laborwert"] == laborwert].sort_values("Datum")

# === Referenzbereich ermitteln
ref_string = daten["Referenz"].iloc[0]
ref_clean = re.sub(r"[–—−]", "-", ref_string).replace(" ", "")
try:
    ref_min, ref_max = map(float, ref_clean.split("-"))
except:
    ref_min, ref_max = None, None

# === Daten filtern nach Ampel
alle = daten.copy()
grün = daten[daten["Ampel"].str.contains("🟢")]
gelb = daten[daten["Ampel"].str.contains("🟡")]
rot = daten[daten["Ampel"].str.contains("🔴")]

# === Layout mit 2x2 Spalten
st.markdown("###Diagramme")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Alle Werte**")
    st.line_chart(alle.set_index("Datum")["Wert"])

with col2:
    if not grün.empty:
        st.markdown("**🟢 Normalbereich**")
        st.line_chart(grün.set_index("Datum")["Wert"])
    else:
        st.info("Keine Werte im Normalbereich.")

col3, col4 = st.columns(2)
with col3:
    if not gelb.empty:
        st.markdown("**🟡 Leicht ausserhalb**")
        st.line_chart(gelb.set_index("Datum")["Wert"])
    else:
        st.info("Keine leicht abweichenden Werte.")

with col4:
    if not rot.empty:
        st.markdown("**🔴 Stark abweichend**")
        st.line_chart(rot.set_index("Datum")["Wert"])
    else:
        st.info("Keine stark abweichenden Werte.")

# === Legende
st.markdown("---")
st.markdown("### 🟢🟡🔴 Ampelfarben-Legende")
st.markdown("""
- 🟢 Wert im Referenzbereich  
- 🟡 Wert unter dem Referenzbereich  
- 🔴 Wert über dem Referenzbereich  
""")
