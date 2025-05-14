import streamlit as st
import pandas as pd
import datetime
import re
import matplotlib.pyplot as plt
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# === Hintergrundfarbe korrekt setzen ===
st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] > .main {
            background-color: #f0f8ff;
        }
        .element-container:has(figure) {
            padding-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# === Login initialisieren ===
login_manager = LoginManager(data_manager=DataManager())

# === Wenn nicht eingeloggt → stoppen ===
if not st.session_state.get("authentication_status", False):
    st.error("⚠️ Kein Benutzer eingeloggt! Anmeldung erforderlich.")
    st.stop()

# === Logout-Button nur in der Sidebar ===
with st.sidebar:
    login_manager.authenticator.logout("Logout", key="logout_sidebar")

# === Benutzername und Daten laden ===
username = st.session_state.get("username")
session_key = f"user_data_{username}"
file_name = f"{username}_daten.csv"
data_manager = DataManager()
data_manager.load_user_data(session_state_key=session_key, file_name=file_name)

# === Daten prüfen ===
if session_key not in st.session_state or st.session_state[session_key].empty:
    st.info("Noch keine Laborwerte vorhanden.")
    st.stop()

# === Daten vorbereiten ===
df = st.session_state[session_key].copy()
df["Datum"] = pd.to_datetime(df["Datum"], format="%d.%m.%Y")

# === Auswahl des Laborwerts ===
st.title("Verlauf")
laborwert = st.selectbox("Laborwert auswählen", df["Laborwert"].unique())
daten = df[df["Laborwert"] == laborwert].sort_values("Datum")

# === Referenzbereich auslesen ===
ref_string = daten["Referenz"].iloc[0]
ref_clean = re.sub(r"[–—−]", "-", ref_string).replace(" ", "")
try:
    ref_min, ref_max = map(float, ref_clean.split("-"))
except:
    ref_min, ref_max = None, None

# === Ampelfilter anwenden ===
alle = daten.copy()
grün = daten[daten["Ampel"].str.contains("🟢")]
gelb = daten[daten["Ampel"].str.contains("🟡")]
rot = daten[daten["Ampel"].str.contains("🔴")]

# === Liniendiagramm anzeigen ===
st.markdown("### Verlauf aller Werte")
st.line_chart(alle.set_index("Datum")["Wert"])

# === Histogramm-Einstellungen berechnen ===
def max_anzahl(df):
    return df["Wert"].value_counts().max() if not df.empty else 0

y_max = max(1, max(max_anzahl(grün), max_anzahl(gelb), max_anzahl(rot)))

x_min = min(
    grün["Wert"].min() if not grün.empty else float("inf"),
    gelb["Wert"].min() if not gelb.empty else float("inf"),
    rot["Wert"].min() if not rot.empty else float("inf")
)
x_max = max(
    grün["Wert"].max() if not grün.empty else float("-inf"),
    gelb["Wert"].max() if not gelb.empty else float("-inf"),
    rot["Wert"].max() if not rot.empty else float("-inf")
)

# === Histogramm anzeigen ===
def zeige_histogramm(df, farbe, titel, y_max, x_min, x_max):
    fig, ax = plt.subplots(figsize=(4, 3))
    if not df.empty:
        ax.hist(df["Wert"], bins=10, color=farbe, edgecolor='black')
    ax.set_title(titel)
    ax.set_xlabel("Wert")
    ax.set_ylabel("Anzahl")
    ax.set_ylim(0, y_max)
    ax.set_xlim(x_min, x_max)
    ax.set_facecolor("#ffffff")
    ax.grid(False)
    st.pyplot(fig)

# === Drei Spalten ===
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🟢 Normalbereich")
    zeige_histogramm(grün, "green", "Normalbereich", y_max, x_min, x_max)

with col2:
    st.markdown("### 🟡 Leicht ausserhalb")
    zeige_histogramm(gelb, "yellow", "Leicht ausserhalb", y_max, x_min, x_max)

with col3:
    st.markdown("### 🔴 Stark abweichend")
    zeige_histogramm(rot, "red", "Stark abweichend", y_max, x_min, x_max)

# === Legende ===
st.markdown("---")
st.markdown("### Ampelfarben-Legende")
st.markdown("""
- 🟢 Wert im Normalbereich  
- 🟡 Wert leicht ausserhalb  
- 🔴 Wert stark abweichend  
""")
