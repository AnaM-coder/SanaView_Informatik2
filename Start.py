import streamlit as st
import os
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# Seitenkonfiguration
st.set_page_config(page_title="SanaView", layout="wide")

# Login
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="SanaView2")
login_manager = LoginManager(data_manager)
login_manager.login_register()

# Stop wenn nicht eingeloggt
if not st.session_state.get("authentication_status", False):
    st.stop()

# ==== Kopfbereich: Logo und Logout in einer Zeile ====
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0;">
    <div>
        <img src="img/sanaview_logo.png" alt="SanaView Logo" style="width: 160px;">
    </div>
    <div>
        <button style="background-color: #e0e0e0; color: black; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;" onclick="logout()">Logout</button>
    </div>
</div>
""", unsafe_allow_html=True)

# ==== Begrüßung in der Mitte ====
st.markdown("""
<div style="text-align: center; margin-top: 50px;">
    <h1>🧬 Willkommen bei SanaView</h1>
    <p>Ihre Werte sicher gespeichert – ohne Diagnose, dennoch mit Überblick.</p>
</div>
""", unsafe_allow_html=True)

# ==== Eingeloggt-Info ====
username = st.session_state.get("username", "Unbekannt")
st.markdown(f"""
<div style="background-color: #e6f2ff; padding: 12px; border-radius: 10px; margin-top: 25px; margin-bottom: 30px; text-align: center;">
    👋 <strong>Eingeloggt als:</strong> {username}
</div>
""", unsafe_allow_html=True)

# ==== Autoren ====
st.markdown("### Autoren")
st.write("""
Diese App wurde im Rahmen des Moduls *Informatik 2* an der **ZHAW** entwickelt von:

- Ana Maria (andraana@students.zhaw.com)  
- Lou-Salomé Frehner (frehnlou@students.zhaw.ch)  
- Cristiana Bastos (pereicri@students.zhaw.ch)
""")