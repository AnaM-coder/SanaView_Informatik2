import streamlit as st
import os
import base64
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

# Logout-Button oben rechts
logout_placeholder = st.empty()
with logout_placeholder.container():
    cols = st.columns([10, 1])
    with cols[1]:
        if st.button("🔓 Logout"):
            login_manager.logout()

# === GROSSER HEADER mit Logo, Begrüßung, Beschreibung ===
logo_path = "img/sanaview_logo.png"
if os.path.exists(logo_path):
    with open(logo_path, "rb") as image_file:
        encoded_logo = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f"""
        <div style='text-align: center; margin-top: 40px; margin-bottom: 20px;'>
            <img src="data:image/png;base64,{encoded_logo}" alt="SanaView Logo" style="max-width: 100%; width: 150px; height: auto;" />
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    """
    <div style='text-align: center; margin-bottom: 30px;'>
        <h1 style='font-size: 36px;'>Willkommen bei SanaView</h1>
        <p style='font-size: 18px;'>Mit dieser App können Sie Ihre Gesundheitswerte im Blick behalten.</p>
        <button style='background-color: #1e90ff; color: white; padding: 10px 20px; border: none; border-radius: 8px; font-size: 16px; cursor: pointer;'>Jetzt starten</button>
    </div>
    """,
    unsafe_allow_html=True
)

# === 4 Hauptbereiche (Infokarten) ===
st.markdown(
    """
    <div style='display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-top: 30px;'>

        <div style='flex: 1 1 200px; background-color: #f9f9f9; border-radius: 12px; padding: 20px; text-align: center;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1); min-width: 180px;'>
            <h4 style='margin-bottom: 8px;'>🧪 Laborwerte</h4>
            <p>Ihre medizinischen Werte eingeben und verwalten.</p>
        </div>

        <div style='flex: 1 1 200px; background-color: #f9f9f9; border-radius: 12px; padding: 20px; text-align: center;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1); min