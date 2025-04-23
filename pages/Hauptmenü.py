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
col1, _ = st.columns([1, 10])
with col1:
    if os.path.exists("img/sanaview_logo.png"):
        st.image("img/sanaview_logo.png", width=300)
    else:
        st.warning("⚠️ Logo nicht gefunden.")

# === Willkommens-Titel zentriert ===
st.markdown("<h1 style='text-align: center;'>👋 Willkommen bei SanaView</h1>", unsafe_allow_html=True)

# === Kurze Einleitung ===
st.markdown("**Mit SanaView können Sie:**")

# === Funktionen als Liste ===
funktionen = [
    "Laborwerte erfassen und verwalten",
    "Verlauf Ihrer Werte grafisch anzeigen",
    "Ampelfarben zur schnellen Einordnung nutzen",
    "Individuelle Referenzbereiche anzeigen",
    "Gesundheitsprofil verwalten"
]

for punkt in funktionen:
    st.markdown(f"- {punkt}")
