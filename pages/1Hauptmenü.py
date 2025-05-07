import streamlit as st
import datetime
import pandas as pd
from utils.data_manager import DataManager
from utils.login_manager import LoginManager
from utils.logo_loader import zeige_logo
import os

# === Seitenlayout ganz oben ===
st.set_page_config(page_title="SanaView – Hauptmenü", layout="wide")

# === Login & Logout ===
login_manager = LoginManager(data_manager=DataManager())
login_manager.authenticator.logout("Logout", "sidebar")
login_manager.go_to_login("Start.py")

# === Logo oben links (grösser) ===
col_logo, _ = st.columns([1, 8])
with col_logo:
    zeige_logo(breite=250)

# === Begrüßung & Inhalte ===
st.markdown("<h1 style='margin-top: 20px;'>Willkommen auf der Hauptmenü</h1>", unsafe_allow_html=True)
st.markdown("<h4>Liebe Nutzerinnen und Nutzer 🧬 </h4>", unsafe_allow_html=True)

st.markdown("<p style='margin-top: 15px; font-size:18px;'>Mit der <strong>SanaView App</strong> können Sie:</p>", unsafe_allow_html=True)

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

st.markdown("<p style='margin-top: 25px; font-size:18px;'><strong>Behalten Sie Ihre Gesundheit im Blick – einfach, sicher und übersichtlich.</strong></p>", unsafe_allow_html=True)
