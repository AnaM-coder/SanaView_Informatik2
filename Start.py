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

# === Nur wenn eingeloggt: Logout + Inhalt ===
if not st.session_state.get("authentication_status"):
    st.stop()

login_manager.authenticator.logout("Logout", "sidebar")

# === Logo links anzeigen ===
col_logo, col_rest = st.columns([1, 8])
with col_logo:
    if os.path.exists("img/sanaview_logo.png"):
        st.image("img/sanaview_logo.png", width=200)
    else:
        st.warning("⚠️ Logo nicht gefunden.")

# === Texte zentriert anzeigen ===
with col_rest:
    st.markdown("<h1 style='text-align: center;'>Willkommen bei SanaView</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size:18px; color:gray;'>Ihre Werte sicher gespeichert – ohne Diagnose, dennoch mit Überblick.</p>", unsafe_allow_html=True)

    st.markdown("""
    <div style='margin: 30px auto; font-size: 17px; line-height: 1.6; text-align: center; max-width: 700px;'>
        Diese App unterstützt Sie dabei, Ihre medizinischen Werte sicher zu speichern 
        und den Verlauf über einen längeren Zeitraum im Blick zu behalten – etwa im Rahmen einer Behandlung. 
        Ergänzend erhalten Sie hilfreiche Informationen zu verschiedenen Analysewerten – 
        <strong>ohne dabei medizinische Diagnosen zu ersetzen</strong>.
    </div>
    """, unsafe_allow_html=True)

    username = st.session_state.get("username", "Unbekannt")
    st.markdown(f"""
    <div style="background-color: #e6f2ff; padding: 12px; border-radius: 10px; margin-top: 25px; margin-bottom: 30px; text-align: center;">
        👋 <strong>Eingeloggt als:</strong> {username}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Autoren", unsafe_allow_html=True)
    st.write("""
    Diese App wurde im Rahmen des Moduls *Informatik 2* an der **ZHAW** entwickelt von:

    - Ana Maria Andrade (andraana@students.zhaw.com)  
    - Lou-Salomé Frehner (frehnlou@students.zhaw.ch)  
    - Cristiana Pereira Bastos (pereicri@students.zhaw.ch)
    """)
