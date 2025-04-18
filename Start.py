import streamlit as st
import os
import base64
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# Seitenkonfiguration
st.set_page_config(page_title="SanaView", layout="centered")

# Initialisiere Login & Data
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="SanaView2")
login_manager = LoginManager(data_manager)
login_manager.login_register()

# Stop wenn nicht eingeloggt
if not st.session_state.get("authentication_status", False):
    st.stop()

username = st.session_state.get("username", "Unbekannt")

# === LOGO & TITEL in einer Linie ===
logo_path = "img/sanaview_logo.png"
if os.path.exists(logo_path):
    with open(logo_path, "rb") as image_file:
        encoded_logo = base64.b64encode(image_file.read()).decode()

    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 25px; margin-top: 30px; margin-bottom: 30px;">
        <img src="data:image/png;base64,{encoded_logo}" alt="SanaView Logo" style="height: 80px;" />
        <div>
            <h1 style="margin: 0;">🧬 Willkommen bei SanaView</h1>
            <p style="margin: 0; font-size: 16px; color: gray;">
                Ihre Werte sicher gespeichert – ohne Diagnose, aber mit Überblick.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.warning("⚠️ Logo nicht gefunden.")

# === Eingeloggt-Box ===
st.markdown(f"""
<div style="background-color: #e6f2ff; padding: 12px; border-radius: 10px; margin-top: 10px; margin-bottom: 30px;">
    👋 <strong>Eingeloggt als:</strong> {username}
</div>
""", unsafe_allow_html=True)

# === Autorenbereich ===
st.markdown("### Autoren")
st.write("""
Diese App wurde im Rahmen des Moduls *Informatik 2* an der **ZHAW** entwickelt von:

- Ana Maria (andraana@students.zhaw.com)
- Lou-Salomé Frehner (frehnlou@students.zhaw.ch)
- Cristiana Bastos (pereicri@students.zhaw.ch)
""")

