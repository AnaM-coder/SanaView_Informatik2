import streamlit as st
import pandas as pd

def show_labor():
    st.set_page_config(page_title="Laborwerte", layout="centered")  # optional

    st.title("📊 Laborwerte")
    st.subheader("Blutzuckerwert eingeben")

    # Eingabefelder
    datum = st.date_input("Datum")
    wert = st.number_input("Wert (mg/dL)", min_value=0.0, format="%.1f")
    kommentar = st.text_input("Kommentar")

    # Session-State initialisieren
    if "labor_tabelle" not in st.session_state:
        st.session_state.labor_tabelle = pd.DataFrame(columns=["Datum", "Wert", "Kommentar"])

    # Speichern
    if st.button("➕ Wert speichern"):
        neue_zeile = pd.DataFrame([{
            "Datum": datum,
            "Wert": wert,
            "Kommentar": kommentar
        }])
        st.session_state.labor_tabelle = pd.concat([st.session_state.labor_tabelle, neue_zeile], ignore_index=True)
        st.success("✅ Eintrag erfolgreich gespeichert!")

    # Anzeige der Tabelle
    if not st.session_state.labor_tabelle.empty:
        st.markdown("---")
        st.subheader("📁 Ihre bisherigen Einträge")
        st.dataframe(st.session_state.labor_tabelle)
