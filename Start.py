import streamlit as st
import pandas as pd
import os
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# Seitenkonfiguration
st.set_page_config(page_title="SanaView", layout="centered")

# Initialisiere Login
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="SanaView2")
login_manager = LoginManager(data_manager)
login_manager.login_register()

# ❌ Stop wenn nicht eingeloggt
if not st.session_state.get("authentication_status", False):
    st.stop()

# Username holen
username = st.session_state.get("username", "Unbekannt")

# === Navigation (Session-State)
if "seite" not in st.session_state:
    st.session_state["seite"] = "home"

# Navigation Buttons
st.markdown("---")
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)
with nav_col1:
    if st.button("🏠 Startseite"):
        st.session_state["seite"] = "home"
with nav_col2:
    if st.button("👤 Profilverwaltung"):
        st.session_state["seite"] = "profil"
with nav_col3:
    if st.button("🧪 Laborwerte"):
        st.session_state["seite"] = "labor"
with nav_col4:
    if st.button("📊 Verlauf"):
        st.session_state["seite"] = "verlauf"
st.markdown("---")

# === Startseite ===
if st.session_state["seite"] == "home":
    # Logo
    col_logo, col_space = st.columns([1, 5])
    with col_logo:
        if os.path.exists("img/sanaview_logo.png"):
            st.image("img/sanaview_logo.png", width=500)
        else:
            st.warning("⚠️ Logo nicht gefunden.")

    # Titel & Untertitel
    st.markdown("""
    <div style='text-align: center; margin-top: -20px;'>
        <h1 style='font-size: 36px;'>🧬 Willkommen bei SanaView</h1>
        <p style='font-size: 18px; color: gray; margin-top: -10px;'>
            Ihre Werte sicher gespeichert – ohne Diagnose, dennoch mit Überblick.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Eingeloggt
    st.markdown(f"""
    <div style="background-color: #e6f2ff; padding: 12px; border-radius: 10px;
                margin-top: 25px; margin-bottom: 30px;">
        👋 <strong>Eingeloggt als:</strong> {username}
    </div>
    """, unsafe_allow_html=True)

    # Autoren
    st.markdown("### Autoren")
    st.write("""
    Diese App wurde im Rahmen des Moduls Informatik 2 an der *ZHAW* entwickelt von:

    - Ana Maria (andraana@students.zhaw.com)  
    - Lou-Salomé Frehner (frehnlou@students.zhaw.ch)  
    - Cristiana Bastos (pereicri@students.zhaw.ch)
    """)

# === Profilverwaltung anzeigen (aus anderer Datei) ===
elif st.session_state["seite"] == "profil":
    from pages import Profil  # Datei: pages/Profil.py
    Profil.show_profil_page()  # Funktion in Profil.py (siehe unten)

# === Weitere Seiten folgen (Platzhalter) ===
elif st.session_state["seite"] == "labor":
    st.info("🧪 Laborwerte-Seite kommt bald...")
elif st.session_state["seite"] == "verlauf":
    st.info("📊 Verlaufsseite kommt bald...")