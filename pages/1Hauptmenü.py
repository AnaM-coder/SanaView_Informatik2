import streamlit as st
import os
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# === Seitenlayout ===
st.set_page_config(page_title="SanaView – Hauptmenü", layout="wide")

# === Login prüfen ===
login_manager = LoginManager(data_manager=DataManager())

if not st.session_state.get("authentication_status", False):
    st.error("⚠️ Kein Benutzer eingeloggt! Anmeldung erforderlich.")
    st.stop()

# === Logout nur in der Sidebar ===
with st.sidebar:
    login_manager.authenticator.logout("Logout", key="logout_sidebar")

# === Logo links oben ===
if os.path.exists("img/sanaview_logo.png"):
    st.image("img/sanaview_logo.png", width=180)
else:
    st.warning("⚠️ Logo nicht gefunden.")

# === Haupttitel & Begrüssung ===
st.markdown("## Willkommen auf dem Hauptmenü")
st.markdown("#### Liebe Nutzerinnen und Nutzer 🧬")

# === Beschreibung ===
st.markdown("Mit der **SanaView App** können Sie:")

st.markdown("""
<ul style='font-size:18px; line-height: 1.8;'>
    <li>Laborwerte erfassen</li>
    <li>Verlauf grafisch anzeigen</li>
    <li>Ampelfarben zur Bewertung nutzen</li>
    <li>Referenzwerte individuell einsehen</li>
    <li>Ihr Gesundheitsprofil verwalten</li>
    <li>Laborberichte als PDF hochladen</li>
</ul>
""", unsafe_allow_html=True)

# === Abschluss ===
st.markdown("<p style='margin-top: 25px; font-size:18px;'><strong>Behalten Sie Ihre Gesundheit im Blick – einfach, sicher und übersichtlich.</strong></p>", unsafe_allow_html=True)
