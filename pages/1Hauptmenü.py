import streamlit as st
import datetime
import pandas as pd
from utils.data_manager import DataManager
from utils.login_manager import LoginManager
import os

# === Seitenlayout ===
st.set_page_config(page_title="SanaView – Hauptmenü", layout="wide")

# === Login & Logout ===
login_manager = LoginManager(data_manager=DataManager())
login_manager.authenticator.logout("Logout", "sidebar")
login_manager.go_to_login("Start.py")

# === Logo links oben (korrekt eingebunden) ===
if os.path.exists("img/sanaview_logo.png"):
    st.image("img/sanaview_logo.png", width=200)
else:
    st.warning("⚠️ Logo nicht gefunden.")

# === Haupttitel & Begrüssung (NICHT zentriert) ===
st.markdown("## Willkommen auf der Hauptmenü")
st.markdown("#### Liebe Nutzerinnen und Nutzer 🧬")

# === Beschreibung der Funktionen ===
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

# === Abschluss — linke Ausrichtung beibehalten ===
st.markdown("<p style='margin-top: 25px; font-size:18px;'><strong>Behalten Sie Ihre Gesundheit im Blick – einfach, sicher und übersichtlich.</strong></p>", unsafe_allow_html=True)
