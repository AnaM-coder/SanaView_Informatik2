import streamlit as st
import base64
import datetime
import pandas as pd
import fitz  # PyMuPDF
import re
import time
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# ... (dein bisheriger Code bleibt unverändert bis zum Löschbereich) ...

# === Eintrag löschen ===
st.markdown("### 🗑️ Eintrag löschen")

if len(df) > 0:
    optionen = df.apply(
        lambda row: f"{row['Datum']} – {row['Laborwert']} ({row['Wert']:.2f} {row['Einheit']})", axis=1
    ).tolist()
    auswahl = st.selectbox("Eintrag auswählen", optionen)

    # Stil für roten "Eintrag löschen"-Button
    st.markdown("""
        <style>
        div[data-testid="stButton"] > button[kind="primary"] {
            background-color: #dc3545 !important;
            color: white !important;
            font-weight: bold;
            font-size: 1.1em;
            border-radius: 8px;
            border: none;
            padding: 0.6em 2em;
            margin-top: 1em;
            margin-bottom: 2em;
        }
        </style>
    """, unsafe_allow_html=True)

    # Session-State init
    if "delete_confirm" not in st.session_state:
        st.session_state["delete_confirm"] = False
    if "delete_result" not in st.session_state:
        st.session_state["delete_result"] = None

    # Löschbutton
    if st.button("Eintrag löschen", type="primary", key="delete_button"):
        st.session_state["delete_confirm"] = True
        st.session_state["delete_result"] = None

    # Bestätigungsbox mit Ja / Nein nebeneinander
    if st.session_state["delete_confirm"]:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown("""
                <div style='background-color: #e0f7fa; padding: 1em; border-radius: 10px;
                            font-weight: bold; color: #004d40; font-size: 1.05em; margin-bottom: 3em;'>
                    Sind Sie sicher, dass Sie diesen Eintrag löschen möchten?
                </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("✅ Ja", key="delete_yes"):
                maske = df.apply(
                    lambda row: f"{row['Datum']} – {row['Laborwert']} ({row['Wert']:.2f} {row['Einheit']})", axis=1
                ) == auswahl
                df = df[~maske].reset_index(drop=True)
                st.session_state[session_key] = df
                data_manager.save_data(session_state_key=session_key)
                st.session_state["delete_confirm"] = False
                st.session_state["delete_result"] = "success"
                st.experimental_rerun()
        with col3:
            if st.button("❌ Nein", key="delete_no"):
                st.session_state["delete_confirm"] = False
                st.session_state["delete_result"] = "cancel"
                st.experimental_rerun()

    # Nach dem Rerun: Erfolgs- oder Abbruchmeldung anzeigen
    if st.session_state.get("delete_result") == "success":
        st.success("Eintrag erfolgreich gelöscht.")
        time.sleep(4)
        st.session_state["delete_result"] = None
        st.experimental_rerun()
    elif st.session_state.get("delete_result") == "cancel":
        st.info("Löschvorgang abgebrochen.")
        time.sleep(4)
        st.session_state["delete_result"] = None
        st.experimental_rerun()

else:
    st.info("Keine Einträge zum Löschen vorhanden.")

# === Navigations-Buttons am Schluss ===
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("Start"):
        st.switch_page("Start.py")
with col2:
    if st.button("Hauptmenü"):
        st.switch_page("pages/1Hauptmenü.py")
with col3:
    if st.button("Profil"):
        st.switch_page("pages/2Profilverwaltung.py")
with col4:
    if st.button("Infoseite"):
        st.switch_page("pages/5Infoseite.py")
with col5:
    if st.button("Verlauf"):
        st.switch_page("pages/4Verlauf.py")