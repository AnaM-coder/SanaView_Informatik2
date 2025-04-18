import streamlit as st
import os
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# === Streamlit Seite vorbereiten ===
st.set_page_config(page_title="SanaView", layout="centered")

# === Login Handling ===
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="SanaView2")
login_manager = LoginManager(data_manager)
login_manager.login_register()

if not st.session_state.get("authentication_status", False):
    st.stop()

username = st.session_state.get("username", "Unbekannt")

# === LOGO UND HEADER ===
col1, col2 = st.columns([1, 6])
with col1:
    if os.path.exists("img/Sanaview_logo.png"):
        st.image("img/Sanaview_logo.png", width=100)
    else:
        st.write("🔬")
with col2:
    st.markdown("""
    <h1 style='margin-bottom: 0;'>Willkommen bei SanaView</h1>
    <p style='margin-top: 0; color: gray;'>Diese App hilft Ihnen dabei, Ihre Werte sicher zu speichern – ohne Diagnose, aber mit Überblick.</p>
    """, unsafe_allow_html=True)

# === ANGEMELDET ALS ===
st.markdown(f"""
<div style="background-color: #ccf5d5; padding: 10px; border-radius: 10px; margin: 20px 0; text-align: center;">
<b>Angemeldet als:</b> <span style='color: darkgreen; font-weight: bold;'>{username}</span>
</div>
""", unsafe_allow_html=True)

# ================================
# 👉 SEITE: PROFILVERWALTUNG
# ================================
st.markdown("---")
st.header("👤 Profilverwaltung")

import pages.Profilerwaltung as Profil
Profil.show_profil_page()  # du brauchst def show_profil_page(): in 1. Profilverwaltung.py

# ================================
# 👉 SEITE: LABORWERTE
# ================================
st.markdown("---")
st.header("🧪 Laborwerte")

import pages.Laborwerte as Labor
Labor.show_labor_page()  # du brauchst def show_labor_page(): in 2. Laborwerte.py

# ================================
# 👉 SEITE: AUTOREN
# ================================
st.markdown("---")
st.header("👩‍💻 Autoren")

st.markdown("""
Diese App wurde im Rahmen des Moduls Informatik 2 an der *ZHAW* entwickelt von:

- Ana Maria (andraana@students.zhaw.com)  
- Lou-Salomé Frehner (frehnlou@students.zhaw.ch)  
- Cristiana Bastos (pereicri@students.zhaw.ch)
""")