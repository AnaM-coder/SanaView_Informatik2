import streamlit as st
import os
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# === Seitenlayout: Muss ganz am Anfang stehen ===
st.set_page_config(page_title="SanaView", layout="wide")

# === Login-Manager & DataManager (WebDAV) ===
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="SanaView2")
login_manager = LoginManager(data_manager=data_manager)

# === Wenn eingeloggt, Logout anzeigen ===
if st.session_state.get("authentication_status"):
    login_manager.authenticator.logout("🚪 Logout", "sidebar")

# === Wenn nicht eingeloggt → Login-Seite anzeigen ===
if not st.session_state.get("authentication_status"):
    login_manager.go_to_login("Start.py")
    st.stop()

# === Logo oben links ===
if os.path.exists("img/sanaview_logo.png"):
    st.image("img/sanaview_logo.png", width=250)
else:
    st.warning("⚠️ Logo nicht gefunden.")

# === Begrüßungstitel zentriert ===
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

# === Nutzername-Anzeige ===
username = st.session_state.get("username", "Unbekannt")
st.markdown(f"""
<div style="background-color: #e6f2ff; padding: 12px; border-radius: 10px; margin-top: 25px; margin-bottom: 30px;">
    👋 <strong>Eingeloggt als:</strong> {username}
</div>
""", unsafe_allow_html=True)

# === Autoren-Info ===
st.markdown("### Autoren")
st.write("""
Diese App wurde im Rahmen des Moduls *Informatik 2* an der **ZHAW** entwickelt von:

- Ana Maria Andrade (andraana@students.zhaw.com)  
- Lou-Salomé Frehner (frehnlou@students.zhaw.ch)  
- Cristiana Pereira Bastos (pereicri@students.zhaw.ch)
""")
