import streamlit as st
import pandas as pd
from datetime import date
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# === Login absichern ===
LoginManager().go_to_login("Start.py")
username = st.session_state.get("username")
if not username:
    st.stop()

# === Pfad zur CSV im Switch Drive ===
profil_pfad = r"Z:\sanaView2\profil.csv"

# === DataManager & SessionState ===
session_key = "profil_daten"
data_manager = DataManager()

data_manager.load_user_data(
    session_state_key=session_key,
    file_name=profil_pfad,
    initial_value=pd.DataFrame(columns=[
        "Name", "Vorname", "Geburtsdatum", "Geschlecht", "Schwanger",
        "Herkunft", "Vorerkrankung", "Medikamente", "Allergien"
    ])
)

# === Daten aus Session State laden (korrekt mit get_user_data) ===
profil_df = data_manager.get_user_data(session_state_key=session_key)
profil_eintrag = profil_df[profil_df["Name"] == username] if username else pd.DataFrame()

if not profil_eintrag.empty and "profil_gespeichert" not in st.session_state:
    st.session_state.profil_daten_anzeige = profil_eintrag.iloc[0].to_dict()
    st.session_state.profil_gespeichert = True

if "profil_gespeichert" not in st.session_state:
    st.session_state.profil_gespeichert = False

# === Formular anzeigen ===
if not st.session_state.profil_gespeichert:
    st.title("Profilverwaltung")
    st.subheader("Persönliche Angaben")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name*", help="Pflichtfeld")
        geburtsdatum = st.date_input(
            "Geburtsdatum*",
            value=date(2000, 1, 1),
            min_value=date(1940, 1, 1),
            max_value=date.today(),
            help="Pflichtfeld"
        )
    with col2:
        vorname = st.text_input("Vorname*", help="Pflichtfeld")
        geschlecht = st.radio("Geschlecht*", ["Weiblich", "Männlich"], horizontal=True, help="Pflichtfeld")

    schwanger = st.radio("Schwanger*", ["Ja", "Nein", "Weiss nicht"], horizontal=True, help="Pflichtfeld")

    herkunft = st.text_input(
        "Herkunft / ethnischer Hintergrund",
        help="Ihr ethnischer Hintergrund kann die medizinische Bewertung beeinflussen. Die Angaben dienen nur der individuellen Einschätzung und werden vertraulich behandelt."
    )

    st.subheader("Gesundheit")
    vorerkrankung = st.text_area("Vorerkrankung")
    medikamente = st.text_area("Medikamente")
    allergien = st.text_area("Allergien / Besonderheiten")

    if st.button("Profil speichern"):
        if not name or not vorname or not geschlecht or not schwanger:
            st.error("❌ Bitte füllen Sie alle mit * markierten Pflichtfelder aus.")
        else:
            eintrag = {
                "Name": name,
                "Vorname": vorname,
                "Geburtsdatum": geburtsdatum.strftime("%d.%m.%Y"),
                "Geschlecht": geschlecht,
                "Schwanger": schwanger,
                "Herkunft": herkunft,
                "Vorerkrankung": vorerkrankung,
                "Medikamente": medikamente,
                "Allergien": allergien
            }

            data_manager.append_record(session_state_key=session_key, record_dict=eintrag)
            st.session_state.profil_daten_anzeige = eintrag
            st.session_state.profil_gespeichert = True
            st.experimental_rerun()

# === Nach dem Speichern: Profilanzeige ===
else:
    st.success("✅ Profil erfolgreich gespeichert!")
    st.subheader("🧾 Ihr Profil")

    bild = st.file_uploader("Profilbild hochladen", type=["png", "jpg", "jpeg"])
    if bild:
        st.image(bild, width=150)

    daten = st.session_state.profil_daten_anzeige
    st.markdown(f"**👤 Name:** {daten['Vorname']} {daten['Name']}")
    st.markdown(f"**🎂 Geburtsdatum:** {daten['Geburtsdatum']}")
    st.markdown(f"**🚻 Geschlecht:** {daten['Geschlecht']}")
    st.markdown(f"**🤰 Schwanger:** {daten['Schwanger']}")
    st.markdown(f"**🌍 Herkunft:** {daten['Herkunft']}")
    st.markdown(f"**🩺 Vorerkrankung:** {daten['Vorerkrankung']}")
    st.markdown(f"**💊 Medikamente:** {daten['Medikamente']}")
    st.markdown(f"**⚠️ Allergien:** {daten['Allergien']}")

    if st.button("Zurück zur Startseite"):
        st.switch_page("Start.py")
