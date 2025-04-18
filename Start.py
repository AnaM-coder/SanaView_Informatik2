import streamlit as st
import pandas as pd 
import os
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# Seitenkonfiguration
st.set_page_config(page_title="SanaView", layout="centered")

# Login-Manager
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="SanaView2")
login_manager = LoginManager(data_manager)
login_manager.login_register()

# Schutz – nicht eingeloggt
if not st.session_state.get("authentication_status", False):
    st.stop()

# Username
username = st.session_state.get("username", "Unbekannt")

# Logout Button
if st.button("Logout"):
    login_manager.logout()

# Logo zentriert
st.markdown("<div style='text-align: center; margin-top: 30px;'>", unsafe_allow_html=True)
if os.path.exists("img/sanaview_logo.png"):
    st.image("img/sanaview_logo.png", width=150)
else:
    st.warning("⚠️ Logo nicht gefunden.")
st.markdown("</div>", unsafe_allow_html=True)

# Titel & Beschreibung
st.markdown("## 🧬 Willkommen bei SanaView")
st.markdown("""
<p style='text-align: center; font-size: 18px; color: grey;'>
Ihre Werte sicher gespeichert – ohne Diagnose, dennoch mit Überblick.
</p>
""", unsafe_allow_html=True)

# Eingeloggt-Box
st.markdown(f"""
<div style="background-color: #e6f2ff; padding: 12px; border-radius: 10px; 
            margin-top: 25px; margin-bottom: 30px; width: 100%;">
    👋 <strong>Eingeloggt als:</strong> {username}
</div>
""", unsafe_allow_html=True)

# Autoren
st.markdown("### Autoren")
st.write("""
Diese App wurde im Rahmen des Moduls *Informatik 2* an der **ZHAW** entwickelt von:

- Ana Maria ([andraana@students.zhaw.com](mailto:andraana@students.zhaw.com))  
- Lou-Salomé Frehner ([frehnlou@students.zhaw.ch](mailto:frehnlou@students.zhaw.ch))  
- Cristiana Bastos ([pereicri@students.zhaw.ch](mailto:pereicri@students.zhaw.ch))
""")

