import streamlit as st
import pandas as pd
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

# Titel & Begrüssung
col1, col2 = st.columns([1, 8])
with col1:
    st.image("img/sanaview_logo.png", width=100)  # Pfad ggf. anpassen
with col2:
    st.markdown("### 🧬 Willkommen bei SanaView")
    st.markdown("Diese App hilft Ihnen dabei, Ihre Werte sicher zu speichern – ohne Diagnose, aber mit Überblick.")

# Angemeldet als...
st.markdown("""
<div style="border: 2px solid #00cc99; border-radius: 8px; padding: 8px; margin-top: 20px; background-color: #eafff5;">
<b>✅ Angemeldet als:</b> <span style='color: green; font-weight: bold;'>{}</span>
</div>
""".format(username), unsafe_allow_html=True)

# Autoreninfo
st.markdown("### Autoren")
st.write("""
Diese App wurde im Rahmen des Moduls *Informatik 2* an der **ZHAW** entwickelt von:

- Ana Maria (andraana@students.zhaw.com)  
- Lou-Salomé Frehner (frehnlou@students.zhaw.ch)  
- Cristiana Bastos (pereicri@students.zhaw.ch)
""")

# Logout-Button
if st.button("Logout"):
    login_manager.logout()
