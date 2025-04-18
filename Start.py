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

# Login-Check
if "authentication_status" not in st.session_state or not st.session_state["authentication_status"]:
    st.warning("🔒 Sie sind nicht eingeloggt. Bitte melden Sie sich an.")
    st.stop()

# Username
username = st.session_state.get("username", "Unbekannt")

# === Logo + Titel nebeneinander ===
col1, col2 = st.columns([1, 5])
with col1:
    if os.path.exists("img/sanaview_logo.png"):
        st.image("img/sanaview_logo.png", width=70)
    else:
        st.warning("⚠️ Logo nicht gefunden.")

with col2:
    st.markdown("## 🧬 Willkommen bei SanaView")
    st.markdown("""
        Diese App hilft Ihnen dabei, Ihre Werte sicher zu speichern – 
        ohne Diagnose, dennoch mit Überblick.
    """)

# === Eingeloggt-Box (hellblau) ===
st.markdown(f"""
<div style="background-color: #e6f2ff; padding: 12px; border-radius: 8px; margin-top: 20px; margin-bottom: 30px;">
    👋 <strong>Eingeloggt als:</strong> {username}
</div>
""", unsafe_allow_html=True)

# === Autorenbereich ===
st.markdown("### 👩‍💻 Autoren")
st.write("""
Diese App wurde im Rahmen des Moduls *Informatik 2* an der **ZHAW** entwickelt von:

- Ana Maria ([andraana@students.zhaw.com](mailto:andraana@students.zhaw.com))  
- Lou-Salomé Frehner ([frehnlou@students.zhaw.ch](mailto:frehnlou@students.zhaw.ch))  
- Cristiana Bastos ([pereicri@students.zhaw.ch](mailto:pereicri@students.zhaw.ch))
""")

