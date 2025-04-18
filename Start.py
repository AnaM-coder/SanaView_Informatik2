import streamlit as st
import pandas as pd
import os
import base64
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# Seitenkonfiguration
st.set_page_config(page_title="SanaView", layout="centered")

# Initialisiere DataManager & Login
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="BMLD_CPBLSF_App")
login_manager = LoginManager(data_manager)
login_manager.login_register()

# Falls der Benutzer nicht eingeloggt ist, stoppe den weiteren Code
if "authentication_status" not in st.session_state or not st.session_state["authentication_status"]:
    st.warning("🔒 Sie sind nicht eingeloggt. Bitte melden Sie sich an.")
    st.stop()

# Benutzername auslesen
username = st.session_state.get("username", "Unbekannt")

# Logout-Button oben rechts
logout_col = st.columns([10, 1])[1]
with logout_col:
    if st.button("Logout"):
        login_manager.logout()

# === GROSSER LOGO-HEADER ===
logo_path = "img/sanaview_logo.png"
if os.path.exists(logo_path):
    with open(logo_path, "rb") as image_file:
        encoded_logo = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f"""
        <div style='text-align: center; margin-top: -40px; margin-bottom: 30px;'>
            <img src="data:image/png;base64,{encoded_logo}" alt="SanaView Logo" style="max-width: 100%; width: 280px; height: auto;" />
            <h1 style='margin-top: 10px;'>🧬 Willkommen bei SanaView</h1>
            <p style='font-size: 18px;'>Diese App hilft Ihnen dabei, Ihre Werte sicher zu speichern – ohne Diagnose, aber mit Überblick.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("⚠️ Logo konnte nicht geladen werden.")

# === Angemeldet als... ===
st.markdown(f"""
<div style="border: 2px solid #00cc99; border-radius: 8px; padding: 12px; margin: 25px 0; background-color: #eafff5;">
<b>✅ Angemeldet als:</b> <span style='color: green; font-weight: bold;'>{username}</span>
</div>
""", unsafe_allow_html=True)

# === Autorenbereich ===
st.markdown("### 👩‍💻 Autoren")
st.write("""
Diese App wurde im Rahmen des Moduls Informatik 2 an der *ZHAW* entwickelt von:

- Ana Maria ([andraana@students.zhaw.com](mailto:andraana@students.zhaw.com))  
- Lou-Salomé Frehner ([frehnlou@students.zhaw.ch](mailto:frehnlou@students.zhaw.ch))  
- Cristiana Bastos ([pereicri@students.zhaw.ch](mailto:pereicri@students.zhaw.ch))
""")