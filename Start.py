import streamlit as st
import os
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# === Seitenlayout ===
st.set_page_config(page_title="SanaView", layout="wide")

# === Login initialisieren ===
data_manager = DataManager(fs_protocol="webdav", fs_root_folder="SanaView2")
login_manager = LoginManager(data_manager=data_manager)

# === Login durchführen ===
login_manager.authenticator.login(location="main")

# === Wenn nicht eingeloggt → abbrechen ===
if not st.session_state.get("authentication_status"):
    st.stop()

# === Logout anzeigen ===
login_manager.authenticator.logout("Logout", "sidebar")

# === Logo links oben ===
col_logo, _ = st.columns([1, 10])
with col_logo:
    if os.path.exists("img/sanaview_logo.png"):
        st.image("img/sanaview_logo.png", width=250)
    else:
        st.warning("⚠️ Logo nicht gefunden.")

# === Begrüßung – LINKS ausgerichtet ===
st.markdown("## Willkommen bei SanaView")
st.markdown("*Ihre Werte sicher gespeichert – ohne Diagnose, dennoch mit Überblick.*")

# === Beschreibung – ebenfalls linksbündig ===
st.markdown("""
Diese App unterstützt Sie dabei, Ihre medizinischen Werte sicher zu speichern 
und den Verlauf über einen längeren Zeitraum im Blick zu behalten – etwa im Rahmen einer Behandlung. 
Ergänzend erhalten Sie hilfreiche Informationen zu verschiedenen Analysewerten – 
**ohne dabei medizinische Diagnosen zu ersetzen**.
""")

# === Login-Hinweis — bleibt mittig formatiert, zur Betonung ===
username = st.session_state.get("username", "Unbekannt")
st.markdown(f"""
<div style="background-color: #e6f2ff; padding: 12px; border-radius: 10px; margin-top: 25px; margin-bottom: 30px;">
    👋 <strong>Eingeloggt als:</strong> {username}
</div>
""", unsafe_allow_html=True)

# === Autoren ===
st.markdown("### Autoren")
st.write("""
Diese App wurde im Rahmen des Moduls *Informatik 2* an der **ZHAW** entwickelt von:

- Ana Maria Andrade (andraana@students.zhaw.com)  
- Lou-Salomé Frehner (frehnlou@students.zhaw.ch)  
- Cristiana Pereira Bastos (pereicri@students.zhaw.ch)
""")
