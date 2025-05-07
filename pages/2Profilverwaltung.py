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

# === WebDAV DataManager
data_manager = DataManager(fs_protocol="webdav", fs_root_folder="SanaView2")
file_name = "profil.csv"
session_key = "profil_daten"

# === Session init
if "profil_gespeichert" not in st.session_state:
    st.session_state.profil_gespeichert = False
if "bearbeiten_modus" not in st.session_state:
    st.session_state.bearbeiten_modus = False

# === CSV laden
data_manager.load_user_data(
    session_state_key=session_key,
    file_name=file_name,
    initial_value=pd.DataFrame(columns=[
        "Benutzername", "Name", "Vorname", "Geburtsdatum", "Geschlecht", "Schwanger",
        "Herkunft", "Vorerkrankung", "Medikamente", "Allergien", "Avatar"
    ])
)
profil_df = st.session_state.get(session_key, pd.DataFrame())
if "Benutzername" not in profil_df.columns:
    profil_df["Benutzername"] = ""

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
                              horizontal=True)

    schwanger = st.radio("Schwanger*", ["Ja", "Nein", "Weiss nicht"],
                         index=["Ja", "Nein", "Weiss nicht"].index(daten.get("Schwanger", "Nein")),
                         horizontal=True)

    herkunft = st.text_input(
        "Herkunft / ethnischer Hintergrund",
        value=daten.get("Herkunft", ""),
        help="Ihr ethnischer Hintergrund kann die medizinische Bewertung beeinflussen."
    )

    # === Avatar-Auswahl (17 Tiere)
    st.subheader("Avatar auswählen")
    tier_auswahl = {
        "🦋 Schmetterling": "🦋", "🦄 Einhorn": "🦄", "🐶 Hund": "🐶", "🦊 Fuchs": "🦊",
        "🐯 Tiger": "🐯", "🦁 Löwe": "🦁", "🐻 Bär": "🐻", "🐱 Katze": "🐱", "🐭 Maus": "🐭",
        "🐼 Panda": "🐼", "🐻‍❄️ Eisbär": "🐻‍❄️", "🐰 Hase": "🐰", "🐨 Koala": "🐨",
        "🐸 Frosch": "🐸", "🐢 Schildkröte": "🐢", "🦉 Eule": "🦉", "🐺 Wolf": "🐺"
    }
    avatar_key = st.selectbox("Tier-Avatar wählen", list(tier_auswahl.keys()), index=0)
    avatar_symbol = tier_auswahl[avatar_key]

    # === Gesundheitsdaten
    st.subheader("Gesundheit")
    vorerkrankung = st.text_area("Vorerkrankung", value=daten.get("Vorerkrankung", ""))
    medikamente = st.text_area("Medikamente", value=daten.get("Medikamente", ""))
    allergien = st.text_area("Allergien / Besonderheiten", value=daten.get("Allergien", ""))

    # === Speichern & Anzeigen
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Speichern"):
            if not name or not vorname or not geschlecht or not schwanger:
                st.error("❌ Bitte Pflichtfelder ausfüllen.")
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
                    "Avatar": avatar_symbol
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
            gespeicherte_daten = st.session_state.get("profil_daten_anzeige", {})
            aktuelle_daten = {
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
                "Avatar": avatar_symbol
            }

            if gespeicherte_daten and aktuelle_daten != gespeicherte_daten:
                st.warning("⚠️ Änderungen wurden vorgenommen, aber nicht gespeichert.")
            elif gespeicherte_daten:
                st.session_state.bearbeiten_modus = False
                st.rerun()
            else:
                st.warning("⚠️ Bitte zuerst speichern.")

# === Profilansicht
else:
    st.title("Ihr Profil")
    st.success("Ihr Profil wurde gespeichert und geladen.")
    daten = st.session_state.profil_daten_anzeige

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f"*👤 **Name, Vorname**:* {daten['Vorname']} {daten['Name']}")
        st.markdown(f"*🎂 **Geburtsdatum**:* {daten['Geburtsdatum']}")
        st.markdown(f"*🚻 **Geschlecht**:* {daten['Geschlecht']}")
        st.markdown(f"*🤰 **Schwanger**:* {daten['Schwanger']}")
        st.markdown(f"*🌍 **Herkunft**:* {daten['Herkunft']}")
        st.markdown(f"*🩺 **Vorerkrankung**:* {daten['Vorerkrankung']}")
        st.markdown(f"*💊 **Medikamente**:* {daten['Medikamente']}")
        st.markdown(f"*⚠️ **Allergien**:* {daten['Allergien']}")

    with col2:
        if "Avatar" in daten:
            st.markdown(
                f"""
                <div style='
                    background-color:#f0f0f0;
                    width:220px;
                    height:220px;
                    border-radius:110px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-size:140px;
                    margin:auto;
                    border:4px solid #ccc;
                '>
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