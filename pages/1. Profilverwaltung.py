import streamlit as st

st.set_page_config(page_title="Profilverwaltung", layout="centered")

st.title("🧾 Profilverwaltung")
st.subheader("Persönliche Angaben")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Name")
    geschlecht = st.radio("Geschlecht", ["Weiblich", "Männlich", "Divers"])
    schwanger = st.radio("Schwanger", ["Ja", "Nein", "Weiss nicht"])

with col2:
    vorname = st.text_input("Vorname")
    geburtsdatum = st.date_input("Geburtsdatum")

herkunft = st.text_input("Herkunft / ethnischer Hintergrund")

st.subheader("Gesundheit")
vorerkrankung = st.text_area("Vorerkrankungen")
medikamente = st.text_area("Medikamente")
allergien = st.text_area("Allergien / Besonderheiten")

col1, col2 = st.columns(2)
with col1:
    if st.button("💾 Profil speichern"):
        st.success("✅ Profil erfolgreich gespeichert!")
with col2:
    st.info("↩️ Zurück zur Startseite oben im Menü")
