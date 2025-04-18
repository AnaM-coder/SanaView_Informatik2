import streamlit as st
import pandas as pd
import os
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# Seitenkonfiguration
st.set_page_config(page_title="SanaView", layout="centered")

# Initialisiere Login-Manager
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="SanaView2")
login_manager = LoginManager(data_manager)
login_manager.login_register()

# Abbruch wenn nicht eingeloggt
if not st.session_state.get("authentication_status", False):
    st.stop()

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Seite auswählen", [
    "Start",
    "Profilverwaltung",
    "Laborwerte"
])

# --- SEITEN ---
if page == "Start":
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Logout oben
    if st.button("Logout"):
        login_manager.logout()
    
    # Logo
    col1, col2 = st.columns([1, 8])
    with col1:
        if os.path.exists("img/sanaview_logo.png"):
            st.image("img/sanaview_logo.png", width=120)
        else:
            st.warning("⚠️ Logo nicht gefunden.")
    
    with col2:
        st.markdown("## 🧬 Willkommen bei SanaView")
        st.write("Ihre Werte sicher gespeichert – ohne Diagnose, aber mit Überblick.")

    username = st.session_state.get("username", "Unbekannt")
    st.markdown(f"""
    <div style="background-color: #e6f2ff; padding: 12px; border-radius: 10px; margin-top: 25px; margin-bottom: 30px;">
        👋 <strong>Eingeloggt als:</strong> {username}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Autoren")
    st.write("""
    Diese App wurde im Rahmen des Moduls *Informatik 2* an der **ZHAW** entwickelt von:

    - Ana Maria (andraana@students.zhaw.com)  
    - Lou-Salomé Frehner (frehnlou@students.zhaw.ch)  
    - Cristiana Bastos (pereicri@students.zhaw.ch)
    """)

elif page == "Profilverwaltung":
    from pages.Profilverwaltung import show_profil_verwaltung
    show_profil_verwaltung()

elif page == "Laborwerte":
    from pages.Laborwerte import show_labor
    show_labor()

