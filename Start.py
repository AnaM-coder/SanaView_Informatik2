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

# ==== Kopfbereich: Logo + Logout nebeneinander ====
col1, col2 = st.columns([8, 1])
with col1:
    if os.path.exists("img/sanaview_logo.png"):
        st.image("img/sanaview_logo.png", width=160)
    else:
        st.warning("⚠️ Logo nicht gefunden.")
with col2:
    if st.button("Logout"):
        login_manager.logout()

# ==== Begrüßung in der Mitte ====
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
st.markdown("## 🧬 Willkommen bei SanaView", unsafe_allow_html=True)
st.markdown(
    "Ihre Werte sicher gespeichert – ohne Diagnose, dennoch mit Überblick.",
    unsafe_allow_html=True
)
st.markdown("</div>", unsafe_allow_html=True)

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