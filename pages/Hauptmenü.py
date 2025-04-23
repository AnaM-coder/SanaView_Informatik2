import streamlit as st
import datetime
import pandas as pd
from utils.data_manager import DataManager
from utils.login_manager import LoginManager
import os

# === Login-Schutz ===
LoginManager().go_to_login("Start.py")

# === Seitenlayout ===
st.set_page_config(page_title="SanaView – Übersicht", layout="wide")

# === Logo oben links ===
col_logo, _ = st.columns([1, 8])
with col_logo:
    if os.path.exists("img/sanaview_logo.png"):
        st.image("img/sanaview_logo.png", width=350)
    else:
        st.warning("⚠️ Logo nicht gefunden.")

# === Einleitung + Liste ===
st.markdown("## Willkommen bei SanaView 🧬")
st.markdown("Mit der SanaView App können Sie:")

st.markdown("""
<ul style='line-height: 1.8; font-size: 18px;'>
  <li>Laborwerte erfassen</li>
  <li>Verlauf grafisch anzeigen</li>
  <li>Ampelfarben zur Bewertung nutzen</li>
  <li>Referenzwerte individuell einsehen</li>
  <li>Ihr Gesundheitsprofil verwalten</li>
</ul>
""", unsafe_allow_html=True)

st.markdown("Behalten Sie Ihre Gesundheit im Blick – einfach, sicher und übersichtlich.")
