import streamlit as st
import os
from utils.data_manager import DataManager
from utils.login_manager import LoginManager


# === Seitenlayout: Muss das erste Streamlit-Kommando sein ===
st.set_page_config(page_title="SanaView", layout="wide")

# === DataManager & LoginManager initialisieren ===
data_manager = DataManager(fs_protocol="webdav", fs_root_folder="SanaView2")
login_manager = LoginManager(data_manager=data_manager)

# === Login-Fenster anzeigen (im Hauptbereich) ===
login_manager.authenticator.login(location="main")

# === Wenn nicht eingeloggt → Login abbrechen ===
if not st.session_state.get("authentication_status"):
    st.stop()

# === Logout-Button in der Sidebar anzeigen ===
login_manager.authenticator.logout("Logout", "sidebar")

# === Logo anzeigen (klein) ===
zeige_logo(breite=250)

# === Begrüssung & Info ===
st.markdown("<h1 style='text-align: center;'>Willkommen bei SanaView</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:18px; color:gray;'>Ihre Werte sicher gespeichert – ohne Diagnose, dennoch mit Überblick.</p>", unsafe_allow_html=True)

st.markdown("""
<div style='margin: 30px 0; font-size: 17px; line-height: 1.6;'>
    Diese App unterstützt Sie dabei, Ihre medizinischen Werte sicher zu speichern 
    und den Verlauf über einen längeren Zeitraum im Blick zu behalten – etwa im Rahmen einer Behandlung. 
    Ergänzend erhalten Sie hilfreiche Informationen zu verschiedenen Analysewerten – 
    <strong>ohne dabei medizinische Diagnosen zu ersetzen</strong>.
</div>
""", unsafe_allow_html=True)

username = st.session_state.get("username", "Unbekannt")
st.markdown(f"""
<div style="background-color: #e6f2ff; padding: 12px; border-radius: 10px; margin-top: 25px; margin-bottom: 30px;">
    👋 <strong>Eingeloggt als:</strong> {username}
</div>
""", unsafe_allow_html=True)

st.markdown("### Autoren")
st.write("""
Diese App wurde im Rahmen des Moduls *Informatik 2* an der **ZHAW** entwickelt von:

- Ana Maria Andrade (andraana@students.zhaw.com)  
- Lou-Salomé Frehner (frehnlou@students.zhaw.ch)  
- Cristiana Pereira Bastos (pereicri@students.zhaw.ch)
""")

