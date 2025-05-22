import streamlit as st
import os
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# === Seitenlayout ===
st.set_page_config(page_title="SanaView – Hauptmenü", layout="wide")

st.markdown("""
    <style>
        html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewContainer"] > .main {
            background-color: #d9ecf2 !important;
        }
    </style>
""", unsafe_allow_html=True)

# === Login prüfen ===
login_manager = LoginManager(data_manager=DataManager())

if not st.session_state.get("authentication_status", False):
    st.error("⚠️ Kein Benutzer eingeloggt! Anmeldung erforderlich.")
    st.stop()

# === Logout nur in der Sidebar ===
with st.sidebar:
    login_manager.authenticator.logout("Logout", key="logout_sidebar")

# === Logo links oben ===
if os.path.exists("img/sanaview_logo.png"):
    st.image("img/sanaview_logo.png", width=180)
else:
    st.warning("⚠️ Logo nicht gefunden.")

# === Haupttitel & Begrüssung ===
st.markdown("## Willkommen auf dem Hauptmenü")
st.markdown("#### Liebe Nutzerinnen und Nutzer 🧬")

# === Beschreibung ===
st.markdown("Mit der **SanaView App** können Sie:")

st.markdown("""
<ul style='font-size:18px; line-height: 1.8;'>
    <li>Laborwerte erfassen</li>
    <li>Verlauf grafisch anzeigen</li>
    <li>Ampelsystem zur Bewertung nutzen</li>
    <li>Laborwerte verstehen – mit Erklärungen und Referenzwerten</li>
    <li>Ihr Gesundheitsprofil verwalten</li>
    <li>Laborberichte als PDF hochladen</li>
</ul>
""", unsafe_allow_html=True)

# === Abschluss ===
st.markdown("<p style='margin-top: 25px; font-size:18px;'><strong>Behalten Sie Ihre Gesundheit im Blick – einfach, sicher und übersichtlich ✨.</strong></p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Laborwerte erfassen"):
        st.switch_page("pages/3Laborwerte.py")
    if st.button("Verlauf anzeigen"):
        st.switch_page("pages/4Verlauf.py")
with col2:
    if st.button("Profil verwalten"):
        st.switch_page("pages/2Profilverwaltung.py")
    if st.button("Infoseite"):
        st.switch_page("pages/5Infoseite.py")
with col3:
    if st.button("Laborbericht (PDF) hochladen"):
        st.switch_page("pages/3Laborwerte.py")  # oder eigene Upload-Seite
