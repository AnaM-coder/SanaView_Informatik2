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

# === CSV-Dateipfad im Switch Drive ===
profil_pfad = r"Z:\sanaView2\profil.csv"

# === Session Keys initialisieren ===
session_key = "profil_daten"
if "profil_gespeichert" not in st.session_state:
    st.session_state.profil_gespeichert = False
if "bearbeiten_modus" not in st.session_state:
    st.session_state.bearbeiten_modus = False

# === DataManager initialisieren ===
data_manager = DataManager()
data_manager.load_user_data(
    session_state_key=session_key,
    file_name=profil_pfad,
    initial_value=pd.DataFrame(columns=[
        "Benutzername", "Name", "Vorname", "Geburtsdatum", "Geschlecht", "Schwanger",
        "Herkunft", "Vorerkrankung", "Medikamente", "Allergien"
    ])
)

# === Profil aus Session State laden
profil_df = st.session_state.get(session_key, pd.DataFrame())

# 💡 Sicherstellen, dass 'Benutzername' existiert
if "Benutzername" not in profil_df.columns:
    profil_df["Benutzername"] = ""

profil_eintrag = profil_df[profil_df["Benutzername"] == username] if not profil_df.empty else pd.DataFrame()

# === Falls vorhanden: als geladen markieren
if not profil_eintrag.empty and not st.session_state.profil_gespeichert:
    st.session_state.profil_daten_anzeige = profil_eintrag.iloc[-1].to_dict()
    st.session_state.profil_gespeichert = True

# === Formular anzeigen ===
if not st.session_state.profil_gespeichert or st.session_state.bearbeiten_modus:
    st.title("Profil bearbeiten" if st.session_state.bearbeiten_modus else "Profilverwaltung")
    st.subheader("Persönliche Angaben")

    daten = st.session_state.get("profil_daten_anzeige", {})

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name*", value=daten.get("Name", ""), help="Pflichtfeld")
        geburtsdatum = st.date_input(
            "Geburtsdatum*",
            value=pd.to_datetime(daten.get("Geburtsdatum", "2000-01-01"), dayfirst=True),
            min_value=date(1940, 1, 1),
            max_value=date.today(),
            help="Pflichtfeld"
        )
    with col2:
        vorname = st.text_input("Vorname*", value=daten.get("Vorname", ""), help="Pflichtfeld")
        geschlecht = st.radio("Geschlecht*", ["Weiblich", "Männlich"],
                              index=["Weiblich", "Männlich"].index(daten.get("Geschlecht", "Weiblich")),
                              horizontal=True, help="Pflichtfeld")

    schwanger = st.radio("Schwanger*", ["Ja", "Nein", "Weiss nicht"],
                         index=["Ja", "Nein", "Weiss nicht"].index(daten.get("Schwanger", "Nein")),
                         horizontal=True, help="Pflichtfeld")

    herkunft = st.text_input(
        "Herkunft / ethnischer Hintergrund",
        value=daten.get("Herkunft", ""),
        help="Ihr ethnischer Hintergrund kann die medizinische Bewertung beeinflussen. Die Angaben dienen nur der individuellen Einschätzung und werden vertraulich behandelt."
    )

    st.subheader("Gesundheit")
    vorerkrankung = st.text_area("Vorerkrankung", value=daten.get("Vorerkrankung", ""))
    medikamente = st.text_area("Medikamente", value=daten.get("Medikamente", ""))
    allergien = st.text_area("Allergien / Besonderheiten", value=daten.get("Allergien", ""))

    if st.button("Speichern"):
        if not name or not vorname or not geschlecht or not schwanger:
            st.error("❌ Bitte füllen Sie alle mit * markierten Pflichtfelder aus.")
        else:
            eintrag = {
                "Benutzername": username,
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

            # Alten Eintrag ersetzen
            updated_df = profil_df[profil_df["Benutzername"] != username]
            updated_df = pd.concat([updated_df, pd.DataFrame([eintrag])], ignore_index=True)
            st.session_state[session_key] = updated_df

            data_manager.save_data(session_state_key=session_key)
            st.session_state.profil_daten_anzeige = eintrag
            st.session_state.profil_gespeichert = True
            st.session_state.bearbeiten_modus = False
            st.rerun()

# === Profilansicht anzeigen ===
else:
    st.title("🧾 Ihr Profil")
    st.success("✅ Ihr Profil wurde gespeichert.")

    daten = st.session_state.profil_daten_anzeige

    with st.container():
        st.markdown(f"**👤 Name:** {daten['Vorname']} {daten['Name']}")
        st.markdown(f"**🎂 Geburtsdatum:** {daten['Geburtsdatum']}")
        st.markdown(f"**🚻 Geschlecht:** {daten['Geschlecht']}")
        st.markdown(f"**🤰 Schwanger:** {daten['Schwanger']}")
        st.markdown(f"**🌍 Herkunft:** {daten['Herkunft']}")
        st.markdown(f"**🩺 Vorerkrankung:** {daten['Vorerkrankung']}")
        st.markdown(f"**💊 Medikamente:** {daten['Medikamente']}")
        st.markdown(f"**⚠️ Allergien:** {daten['Allergien']}")

    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Profil bearbeiten"):
            st.session_state.bearbeiten_modus = True
            st.rerun()
    with col2:
        if st.button("Zurück zur Startseite"):
            st.switch_page("Start.py")
