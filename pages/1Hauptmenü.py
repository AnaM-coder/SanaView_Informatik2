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

# === Logo links anzeigen ===
col1, col2, col3 = st.columns([2, 3, 2])
with col2:
    if os.path.exists("img/sanaview_logo.png"):
        st.image("img/sanaview_logo.png", width=250)
    else:
        st.warning("⚠️ Logo nicht gefunden.")

# === Haupttitel & Begrüßung ===
st.markdown("<h1 style='text-align: center;'>Willkommen auf der Hauptmenü</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Liebe Nutzerinnen und Nutzer 🧬</h4>", unsafe_allow_html=True)

# === Funktionsbeschreibung ===
st.markdown("""
<div style='font-size:18px; line-height: 1.8; margin-top: 20px;'>
    <p style='text-align: center;'>Mit der <strong>SanaView App</strong> können Sie:</p>
    <ul>
        <li>Laborwerte erfassen</li>
        <li>Verlauf grafisch anzeigen</li>
        <li>Ampelfarben zur Bewertung nutzen</li>
        <li>Referenzwerte individuell einsehen</li>
        <li>Ihr Gesundheitsprofil verwalten</li>
        <li>Laborberichte als PDF hochladen</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# === Abschluss ===
st.markdown("<p style='margin-top: 25px; font-size:18px; text-align:center;'><strong>Behalten Sie Ihre Gesundheit im Blick – einfach, sicher und übersichtlich.</strong></p>", unsafe_allow_html=True)
