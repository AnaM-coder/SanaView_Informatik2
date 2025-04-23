import streamlit as st
import datetime
import pandas as pd
from utils.data_manager import DataManager
from utils.login_manager import LoginManager
import os

# === Login-Schutz ===
LoginManager().go_to_login("Start.py")

# === Seitenlayout ===
st.set_page_config(page_title="SanaView – Hauptmenü", layout="wide")

# === Logo oben links ===
col_logo, _ = st.columns([1, 8])
with col_logo:
    if os.path.exists("img/sanaview_logo.png"):
        st.image("img/sanaview_logo.png", width=300)
    else:
        st.warning("⚠️ Logo nicht gefunden.")

# === Haupttitel & Begrüßung ===
st.markdown("<h1 style='margin-top: 20px;'>Willkommen auf der Hauptmenü</h1>", unsafe_allow_html=True)
st.markdown("<h4>Liebe Nutzerinnen und Nutzer 🧬 </h4>", unsafe_allow_html=True)

# === Funktionsbeschreibung ===
st.markdown("<p style='margin-top: 15px; font-size:18px;'>Mit der <strong>SanaView App</strong> können Sie:</p>", unsafe_allow_html=True)

st.markdown("""
<ul style='font-size:18px; line-height: 1.8;'>
    <li>Laborwerte erfassen</li>
    <li>Verlauf grafisch anzeigen</li>
    <li>Ampelfarben zur Bewertung nutzen</li>
    <li>Referenzwerte individuell einsehen</li>
    <li>Ihr Gesundheitsprofil verwalten</li>
</ul>
""", unsafe_allow_html=True)

# === Abschluss ===
st.markdown("<p style='margin-top: 25px; font-size:18px;'><strong>Behalten Sie Ihre Gesundheit im Blick – einfach, sicher und übersichtlich.</strong></p>", unsafe_allow_html=True)
