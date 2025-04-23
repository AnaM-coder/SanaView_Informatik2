import streamlit as st
import datetime
import pandas as pd
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# === Login-Schutz ===
LoginManager().go_to_login("Start.py")

# === Layout konfigurieren
st.set_page_config(page_title="SanaView – Übersicht", layout="centered")

# === Willkommenstitel
st.markdown("<h1 style='text-align: center;'>Willkommen bei SanaView</h1>", unsafe_allow_html=True)

# === Einleitung (nur ein Satz)
st.markdown("**Mit SanaView können Sie:**")

# === Funktionen
funktionen = [
    "Laborwerte erfassen und verwalten",
    "Verlauf Ihrer Werte grafisch anzeigen",
    "Ampelfarben zur schnellen Einordnung nutzen",
    "Individuelle Referenzbereiche anzeigen",
    "Gesundheitsprofil verwalten"
]

for punkt in funktionen:
    st.markdown(f"- {punkt}")
