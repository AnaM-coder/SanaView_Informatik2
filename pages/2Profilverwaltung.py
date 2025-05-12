import streamlit as st
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# === Login & Logout ===
login_manager = LoginManager(data_manager=DataManager())

# Nur wenn eingeloggt, Logout anzeigen
if st.session_state.get("authentication_status", False):
    with st.sidebar:
        login_manager.authenticator.logout("Logout", key="logout_sidebar")
else:
    st.error("⚠️ Kein Benutzer eingeloggt! Anmeldung erforderlich.")
    st.stop()

# === Login absichern ===
username = st.session_state.get("username")
if not username:
    st.stop()

# === Session Key (benutzerspezifisch)
session_key = f"profil_daten_{username}"

# === Session init
st.session_state.setdefault("profil_gespeichert", False)
st.session_state.setdefault("bearbeiten_modus", False)

# === WebDAV DataManager
data_manager = DataManager(fs_protocol="webdav", fs_root_folder="SanaView2")
file_name = "profil.csv"

# === CSV laden
data_manager.load_user_data(
    session_state_key=session_key,
    file_name=file_name,
    initial_value=pd.DataFrame(columns=[
        "Benutzername", "Name", "Vorname", "Geburtsdatum", "Geschlecht", "Schwanger",
        "Herkunft", "Vorerkrankung", "Medikamente", "Allergien", "Avatar",
        "Eltern_Name", "Eltern_Kontakt"
    ])
)
profil_df = st.session_state.get(session_key, pd.DataFrame())
profil_df["Benutzername"] = profil_df.get("Benutzername", "")

# === Vorheriges Profil löschen, wenn es nicht zum aktuellen Benutzer gehört
if "profil_daten_anzeige" in st.session_state:
    if st.session_state.profil_daten_anzeige.get("Benutzername") != username:
        del st.session_state["profil_daten_anzeige"]
        st.session_state["profil_gespeichert"] = False

# === Profil automatisch laden
if not st.session_state.profil_gespeichert:
    if username in profil_df["Benutzername"].values:
        eintrag = profil_df[profil_df["Benutzername"] == username].iloc[-1].to_dict()
        st.session_state.profil_daten_anzeige = eintrag
        st.session_state.profil_gespeichert = True

# === Formular anzeigen
if not st.session_state.profil_gespeichert or st.session_state.bearbeiten_modus:
    st.title("Profilverwaltung")
    st.subheader("Persönliche Angaben")
    daten = st.session_state.get("profil_daten_anzeige", {})

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name*", value=daten.get("Name", ""))
        geburtsdatum = st.date_input(
            "Geburtsdatum*",
            value=pd.to_datetime(daten.get("Geburtsdatum", "2000-01-01"), dayfirst=True),
            min_value=date(1940, 1, 1),
            max_value=date.today()
        )
    with col2:
        vorname = st.text_input("Vorname*", value=daten.get("Vorname", ""))
        geschlecht = st.radio("Geschlecht*", ["Weiblich", "Männlich"],
                              index=["Weiblich", "Männlich"].index(daten.get("Geschlecht", "Weiblich")),
                              horizontal=True)

    schwanger = st.radio("Schwanger*", ["Ja", "Nein", "Weiss nicht"],
                         index=["Ja", "Nein", "Weiss nicht"].index(daten.get("Schwanger", "Nein")),
                         horizontal=True)

    herkunft = st.text_input(
        "Herkunft / ethnischer Hintergrund",
        value=daten.get("Herkunft", ""),
        help="Für eine medizinisch fundierte Einordnung Ihrer Werte können Faktoren wie ethnischer Hintergrund, genetische Veranlagung oder regionale Besonderheiten eine Rolle spielen. Diese Daten dienen ausschliesslich der individuellen Bewertung und werden vertraulich behandelt."
    )

    # === Alter berechnen
    alter = relativedelta(date.today(), geburtsdatum).years

    # === Angaben Elternteil bei Minderjährigen
    if alter < 18:
        st.subheader("Angaben eines Elternteils (bei Minderjährigen)")
        eltern_name = st.text_input("Name des Elternteils*", value=daten.get("Eltern_Name", ""))
        eltern_kontakt = st.text_input("Kontakt (Telefon oder E-Mail)*", value=daten.get("Eltern_Kontakt", ""))
    else:
        eltern_name = ""
        eltern_kontakt = ""

    # === Avatar-Auswahl
    st.subheader("Avatar auswählen")
    tier_auswahl = {
        "🦋 Schmetterling": "🦋", "🦄 Einhorn": "🦄", "🐶 Hund": "🐶", "🦊 Fuchs": "🦊",
        "🐯 Tiger": "🐯", "🦁 Löwe": "🦁", "🐻 Bär": "🐻", "🐱 Katze": "🐱", "🐭 Maus": "🐭",
        "🐼 Panda": "🐼", "🐻‍❄️ Eisbär": "🐻‍❄️", "🐰 Hase": "🐰", "🐨 Koala": "🐨",
        "🐸 Frosch": "🐸", "🐢 Schildkröte": "🐢", "🦉 Eule": "🦉", "🐺 Wolf": "🐺"
    }
    avatar_key = st.selectbox("Tier-Avatar wählen", list(tier_auswahl.keys()), index=0)
    avatar_symbol = tier_auswahl[avatar_key]

    st.subheader("Gesundheit")
    vorerkrankung = st.text_area("Vorerkrankung", value=daten.get("Vorerkrankung", ""))
    medikamente = st.text_area("Medikamente", value=daten.get("Medikamente", ""))
    allergien = st.text_area("Allergien / Besonderheiten", value=daten.get("Allergien", ""))

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Speichern"):
            if not name or not vorname:
                st.error("❌ Bitte Pflichtfelder ausfüllen.")
            elif alter < 18 and (not eltern_name or not eltern_kontakt):
                st.error("❌ Angaben des Elternteils erforderlich für Minderjährige.")
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
                    "Allergien": allergien,
                    "Avatar": avatar_symbol,
                    "Eltern_Name": eltern_name,
                    "Eltern_Kontakt": eltern_kontakt
                }

                updated_df = profil_df[profil_df["Benutzername"] != username]
                updated_df = pd.concat([updated_df, pd.DataFrame([eintrag])], ignore_index=True)
                st.session_state[session_key] = updated_df

                data_manager.save_data(session_state_key=session_key)
                st.session_state.profil_daten_anzeige = eintrag
                st.session_state.profil_gespeichert = True
                st.success("✅ Profil gespeichert!")

    with col2:
        if st.button("Profil anzeigen"):
            st.session_state.bearbeiten_modus = False
            st.rerun()

# === Profilansicht
else:
    st.title("Ihr Profil")
    st.success("Ihr Profil wurde geladen.")
    daten = st.session_state.profil_daten_anzeige
    geburtsdatum = pd.to_datetime(daten["Geburtsdatum"], dayfirst=True)
    alter = relativedelta(date.today(), geburtsdatum).years

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"**Benutzername**: {daten['Benutzername']}")
        st.markdown(f"**Name, Vorname**: {daten['Name']} {daten['Vorname']}")
        st.markdown(f"**Geburtsdatum**: {daten['Geburtsdatum']} ({alter} Jahre)")
        st.markdown(f"**Geschlecht**: {daten['Geschlecht']}")
        st.markdown(f"**Schwanger**: {daten['Schwanger']}")
        st.markdown(f"**Herkunft**: {daten['Herkunft']}")
        st.markdown(f"**Vorerkrankung**: {daten['Vorerkrankung']}")
        st.markdown(f"**Medikamente**: {daten['Medikamente']}")
        st.markdown(f"**Allergien**: {daten['Allergien']}")
        if alter < 18:
            st.markdown(f"**Elternteil**: {daten.get('Eltern_Name', '')}")
            st.markdown(f"**Kontakt Elternteil**: {daten.get('Eltern_Kontakt', '')}")

    with col2:
        if "Avatar" in daten:
            st.markdown(
                f"""
                <div style='background-color:#f0f0f0; width:140px; height:140px;
                border-radius:70px; display:flex; align-items:center; justify-content:center;
                font-size:80px; margin:auto; border:2px solid #ccc;'>
                    {daten['Avatar']}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Profil bearbeiten"):
            st.session_state.bearbeiten_modus = True
            st.rerun()
    with col2:
        if st.button("Zurück zur Startseite"):
            st.switch_page("Start.py")

