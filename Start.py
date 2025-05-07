import streamlit as st
import os
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# === Seitenlayout: Muss ganz oben stehen ===
st.set_page_config(page_title="SanaView", layout="wide")

# === DataManager & LoginManager initialisieren ===
data_manager = DataManager(fs_protocol="webdav", fs_root_folder="SanaView2")
login_manager = LoginManager(data_manager=data_manager)

# === Login-Fenster anzeigen (zentral) ===
login_manager.authenticator.login(location="main")

# === Wenn nicht eingeloggt → stoppen ===
if not st.session_state.get("authentication_status"):
    st.stop()

# === Logout-Button in Sidebar ===
login_manager.authenticator.logout("Logout", "sidebar")

# === Zentriertes Logo anzeigen ===
st.markdown("""
<div style='text-align: center; margin-top: 30px; margin-bottom: 30px;'>
    <img src='img/sanaview_logo.png' style='width: 250px;' alt='SanaView Logo'>
</div>
""", unsafe_allow_html=True)

# === Titel & Begrüssung ===
st.markdown("<h1 style='text-align: center;'>Willkommen bei SanaView</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:18px; color:gray;'>Ihre Werte sicher gespeichert – ohne Diagnose, dennoch mit Überblick.</p>", unsafe_allow_html=True)

# === Beschreibung ===
st.markdown("""
<div style='margin: 30px 0; font-size: 17px; line-height: 1.6;'>
    Diese App unterstützt Sie dabei, Ihre medizinischen Werte sicher zu speichern 
    und den Verlauf über einen längeren Zeitraum im Blick zu behalten – etwa im Rahmen einer Behandlung. 
    Ergänzend erhalten Sie hilfreiche Informationen zu verschiedenen Analysewerten – 
    <strong>ohne dabei medizinische Diagnosen zu ersetzen</strong>.
</div>
""", unsafe_allow_html=True)

# === Eingeloggt-Hinweis ===
username = st.session_state.get("username", "Unbekannt")
st.markdown(f"""
<div style="background-color: #e6f2ff; padding: 12px; border-radius: 10px; margin-top: 25px; margin-bottom: 30px;">
    👋 <strong>Eingeloggt als:</strong> {username}
</div>
""", unsafe_allow_html=True)

# === Autoren-Infos ===
st.markdown("### Autoren")
st.write("""
Diese App wurde im Rahmen des Moduls *Informatik 2* an der **ZHAW** entwickelt von:

- Ana Maria Andrade (andraana@students.zhaw.com)  
- Lou-Salomé Frehner (frehnlou@students.zhaw.ch)  
- Cristiana Pereira Bastos (pereicri@students.zhaw.ch)
""")
