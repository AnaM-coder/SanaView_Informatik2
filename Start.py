import streamlit as st
import pandas as pd
import os
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

username = st.session_state.get("username", "Unbekannt")

# Logout rechts oben
st.markdown(
    """
    <div style="text-align: right;">
        <form action="?">
            <button style="background-color: #f0f0f5; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer;" type="submit">Logout</button>
        </form>
    </div>
    """,
    unsafe_allow_html=True
)

# Logo zentriert
logo_path = "img/sanaview_logo.png"
if os.path.exists(logo_path):
    st.markdown(f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{base64.b64encode(open(logo_path, "rb").read()).decode()}" width="120"/>
    </div>
    """, unsafe_allow_html=True)

# Begrüßung zentriert
st.markdown("""
<div style="text-align: center;">
    <h1>🧬 Willkommen bei SanaView</h1>
    <p>Diese App hilft Ihnen dabei, Ihre Werte sicher zu speichern – ohne Diagnose, aber mit Überblick.</p>
</div>
""", unsafe_allow_html=True)

# Eingeloggt-Box im Stil von Screenshot 2
st.markdown(f"""
<div style="background-color: #e6f2ff; padding: 12px; border-radius: 8px; margin: 20px 0;">
    👋 <strong>Eingeloggt als:</strong> {username}
</div>
""", unsafe_allow_html=True)

# Autoreninfo
st.markdown("### Autoren")
st.write("""
Diese App wurde im Rahmen des Moduls *Informatik 2* an der **ZHAW** entwickelt von:

- Ana Maria (andraana@students.zhaw.com)  
- Lou-Salomé Frehner (frehnlou@students.zhaw.ch)  
- Cristiana Bastos (pereicri@students.zhaw.ch)
""")
