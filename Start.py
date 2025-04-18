import streamlit as st
import pandas as pd
import os
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# Seitenkonfiguration
st.set_page_config(page_title="SanaView", layout="centered")

# Initialisiere Login-Manager & Data
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="SanaView2")
login_manager = LoginManager(data_manager)
login_manager.login_register()

# ❌ Stop wenn nicht eingeloggt
if not st.session_state.get("authentication_status", False):
    st.stop()

# ✅ Eingeloggt → Seite anzeigen
username = st.session_state.get("username", "Unbekannt")

# === GROSSES LOGO OBEN LINKS PER CSS ===
st.markdown("""
    <style>
        .logo-container {
            position: absolute;
            top: 20px;
            left: 20px;
        }
        .logo-container img {
            height: 120px; /* 👈 Hier kannst du die Größe ändern */
        }
    </style>
    <div class="logo-container">
        <img src="img/sanaview_logo.png" alt="SanaView Logo">
    </div>
""", unsafe_allow_html=True)

# === Titel & Untertitel ZENTRIERT ===
st.markdown("""
<div style='text-align: center; margin-top: 50px;'>
    <h1 style='font-size: 36px;'>🧬 Willkommen bei SanaView</h1>
    <p style='font-size: 18px; color: gray; margin-top: -10px;'>
        Ihre Werte sicher gespeichert – ohne Diagnose, aber mit Überblick.
    </p>
</div>
""", unsafe_allow_html=True)

# === Eingeloggt-Box ===
st.markdown(f"""
<div style="background-color: #e6f2ff; padding: 12px; border-radius: 10px;
            margin-top: 25px; margin-bottom: 30px;">
    👋 <strong>Eingeloggt als:</strong> {username}
</div>
""", unsafe_allow_html=True)

# === Autorenbereich ===
st.markdown("### Autoren")
st.write("""
Diese App wurde im Rahmen des Moduls *Informatik 2* an der **ZHAW** entwickelt von:

- Ana Maria ([andraana@students.zhaw.com](mailto:andraana@students.zhaw.com))  
- Lou-Salomé Frehner ([frehnlou@students.zhaw.ch](mailto:frehnlou@students.zhaw.ch))  
- Cristiana Bastos ([pereicri@students.zhaw.ch](mailto:pereicri@students.zhaw.ch))
""")
