import streamlit as st
import os
import time
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# === Seitenlayout===
st.set_page_config(page_title="Info-Seite", layout="wide")

st.markdown("""
    <style>
        html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewContainer"] > .main {
            background-color: #d9ecf2 !important;
        }
    </style>
""", unsafe_allow_html=True)

# === Login initialisieren ===
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="SanaView2")
login_manager = LoginManager(data_manager)

# === Authentifizierung (Login & Registrierung)
if not st.session_state.get("authentication_status"):
    login_tab, register_tab = st.tabs(["Login", "Registrieren"])
    with login_tab:
        login_manager.login(stop=False)
    with register_tab:
        login_manager.register()
    st.stop()

# === Logout-Button nur in der Sidebar anzeigen ===
with st.sidebar:
    login_manager.authenticator.logout("Logout", key="logout_sidebar")

# === Logo zentriert und gross ===
if os.path.exists("img/sanaview_logo.png"):
    col1, col2, col3 = st.columns([2, 4, 1])
    with col2:
        st.image("img/sanaview_logo.png", width=360)
else:
    st.warning("⚠️ Logo nicht gefunden.")

# === Titel & Beschreibung zentriert ===
st.markdown("<h1 style='text-align: center;'>Willkommen bei SanaView</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:18px; color:gray;'>Ihre Werte sicher gespeichert – ohne Diagnose, dennoch mit Überblick.</p>", unsafe_allow_html=True)

# === Beschreibung zur App hinzufügen ===
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

# === Autoren-Info ===
st.markdown("### Autoren")
st.write("""
Diese App wurde im Rahmen des Moduls *Informatik 2* an der **ZHAW** entwickelt von:

- Ana Maria Andrade (andraana@students.zhaw.com)  
- Lou-Salomé Frehner (frehnlou@students.zhaw.ch)  
- Cristiana Pereira Bastos (pereicri@students.zhaw.ch)
""")

col1, col2, col3 = st.columns([2,1,2])
with col2:
    st.markdown("""
        <style>
        div[data-testid="arrow-button"] button {
            font-size: 300px !important;
            height: 320px !important;
            width: 320px !important;
            border-radius: 60px;
            padding: 0;
            background: none;
            border: none;
        }
        </style>
        <div data-testid="arrow-button">
    """, unsafe_allow_html=True)
    if st.button("➡️", key="goto_mainmenu", help="Weiter zum Hauptmenü"):
        st.switch_page("pages/1Hauptmenü.py")
    st.markdown("</div>", unsafe_allow_html=True)