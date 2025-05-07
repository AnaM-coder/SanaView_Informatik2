import streamlit as st
import pandas as pd
import datetime
import re
import matplotlib.pyplot as plt
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# === Login-Schutz ===
LoginManager().go_to_login("Start.py")

# === Initialisierung
username = st.session_state.get("username")
session_key = f"user_data_{username}"
file_name = f"{username}_daten.csv"
data_manager = DataManager()
data_manager.load_user_data(session_state_key=session_key, file_name=file_name)

# === Daten prüfen
if session_key not in st.session_state or st.session_state[session_key].empty:
    st.info("Noch keine Laborwerte vorhanden.")
    st.stop()

df = st.session_state[session_key].copy()
df["Datum"] = pd.to_datetime(df["Datum"], format="%d.%m.%Y")

# === Auswahl
st.title("Verlauf")
laborwert = st.selectbox("Laborwert auswählen", df["Laborwert"].unique())
daten = df[df["Laborwert"] == laborwert].sort_values("Datum")

# === Referenzbereich auslesen
ref_string = daten["Referenz"].iloc[0]
ref_clean = re.sub(r"[–—−]", "-", ref_string).replace(" ", "")
try:
    ref_min, ref_max = map(float, ref_clean.split("-"))
except:
    ref_min, ref_max = None, None

# === Ampelfilter
alle = daten.copy()
grün = daten[daten["Ampel"].str.contains("🟢")]
gelb = daten[daten["Ampel"].str.contains("🟡")]
rot = daten[daten["Ampel"].str.contains("🔴")]

# === Liniendiagramm: Alle Werte
st.markdown("### Alle Werte")
st.line_chart(alle.set_index("Datum")["Wert"])

# === Matplotlib Histogramm Funktion
def zeige_histogramm(df, farbe, titel):
    fig, ax = plt.subplots()
    ax.hist(df["Wert"], bins=10, color=farbe, edgecolor='black')
    ax.set_title(titel)
    ax.set_xlabel("Wert")
    ax.set_ylabel("Anzahl")
    st.pyplot(fig)

# === Drei Histogramme nebeneinander
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🟢 Normalbereich")
    if not grün.empty:
        zeige_histogramm(grün, "green", "Normalbereich")
    else:
        st.info("Keine grünen Werte.")

with col2:
    st.markdown("### 🟡 Leicht ausserhalb")
    if not gelb.empty:
        zeige_histogramm(gelb, "yellow", "Leicht ausserhalb")
    else:
        st.info("Keine gelben Werte.")

with col3:
    st.markdown("### 🔴 Stark abweichend")
    if not rot.empty:
        zeige_histogramm(rot, "red", "Stark abweichend")
    else:
        st.info("Keine roten Werte.")

# === Legende
st.markdown("---")
st.markdown("### Ampelfarben-Legende")
st.markdown("""
- 🟢 Wert im Referenzbereich  
- 🟡 Wert unter dem Referenzbereich  
- 🔴 Wert über dem Referenzbereich  
""")
