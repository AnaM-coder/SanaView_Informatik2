import streamlit as st
import pandas as pd
import datetime
import os
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# === Seitenlayout ganz oben ===
st.set_page_config(page_title="SanaView – Hauptmenü", layout="wide")

# === Login & Logout ===
login_manager = LoginManager(data_manager=DataManager())
login_manager.authenticator.logout("Logout", "sidebar")
login_manager.go_to_login("Start.py")

# === Zentriertes Logo ===
st.markdown("""
<div style='text-align: center; margin-top: 30px; margin-bottom: 30px;'>
    <img src='img/sanaview_logo.png' style='width: 250px;' alt='SanaView Logo'>
</div>
""", unsafe_allow_html=True)

# === Begrüßung ===
st.markdown("<h1 style='text-align: center;'>Willkommen auf der Hauptmenü</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Liebe Nutzerinnen und Nutzer 🧬</h4>", unsafe_allow_html=True)

# === Funktionen auflisten ===
st.markdown("<p style='margin-top: 20px; font-size:18px;'>Mit der <strong>SanaView App</strong> können Sie:</p>", unsafe_allow_html=True)
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

# === Abschluss-Hinweis ===
st.markdown("<p style='margin-top: 25px; font-size:18px;'><strong>Behalten Sie Ihre Gesundheit im Blick – einfach, sicher und übersichtlich.</strong></p>", unsafe_allow_html=True)
