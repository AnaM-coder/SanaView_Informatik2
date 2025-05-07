import streamlit as st
import pandas as pd
from datetime import date
from webdav4.client import Client
from io import StringIO, BytesIO

# === WebDAV-Konfiguration ===
webdav_url = "https://deinserver.de/remote.php/webdav/"
webdav_user = "dein_benutzername"
webdav_password = "dein_passwort"
remote_path = "sanaView2/profil.csv"

client = Client(webdav_url, auth=(webdav_user, webdav_password))

# === Funktion: CSV von WebDAV laden ===
def load_csv_from_webdav():
    try:
        if client.exists(remote_path):
            with client.open(remote_path, "rb") as f:
                return pd.read_csv(f)
        else:
            return pd.DataFrame(columns=[
                "Name", "Vorname", "Geburtsdatum", "Geschlecht", "Schwanger",
                "Herkunft", "Vorerkrankung", "Medikamente", "Allergien"
            ])
    except Exception as e:
        st.error(f"Fehler beim Laden der Daten: {e}")
        return pd.DataFrame()

# === Funktion: CSV zu WebDAV speichern ===
def save_csv_to_webdav(df):
    try:
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        client.upload_fileobj(BytesIO(csv_buffer.getvalue().encode("utf-8")), remote_path)
    except Exception as e:
        st.error(f"Fehler beim Speichern: {e}")

# === Session State Setup ===
if "profil_gespeichert" not in st.session_state:
    st.session_state.profil_gespeichert = False

# === Benutzername (z. B. durch Login festgelegt) ===
username = st.session_state.get("username", "demo_user")

# === Daten laden ===
profil_df = load_csv_from_webdav()
profil_eintrag = profil_df[profil_df["Name"] == username] if username else pd.DataFrame()

if not profil_eintrag.empty and not st.session_state.profil_gespeichert:
    st.session_state.profil_daten_anzeige = profil_eintrag.iloc[0].to_dict()
    st.session_state.profil_gespeichert = True

# === Formular anzeigen ===
if not st.session_state.profil_gespeichert:
    st.title("Profilverwaltung")
    st.subheader("Persönliche Angaben")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name*", value=username, help="Pflichtfeld")
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
            neuer_eintrag = {
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

            # Eintrag anhängen und speichern
            profil_df = profil_df[profil_df["Name"] != name]  # alten ggf. löschen
            profil_df = pd.concat([profil_df, pd.DataFrame([neuer_eintrag])], ignore_index=True)
            save_csv_to_webdav(profil_df)

            st.session_state.profil_daten_anzeige = neuer_eintrag
            st.session_state.profil_gespeichert = True
            st.experimental_rerun()

# === Profil anzeigen ===
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
