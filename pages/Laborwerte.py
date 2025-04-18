import streamlit as st
import pandas as pd
from datetime import datetime

def show_labor():
    st.title("🧪 Laborwerte erfassen")

    st.markdown("Bitte wählen Sie den Laborwert-Typ und geben Sie Ihre Messung ein:")

    # Beispiel: Liste von Laborwerten
    laboroptionen = ["Blutzucker", "Cholesterin", "HbA1c", "Leukozyten"]
    labortyp = st.selectbox("Laborwert-Typ", laboroptionen)

    col1, col2 = st.columns(2)
    with col1:
        datum = st.date_input("Datum", value=datetime.today())
    with col2:
        wert = st.number_input("Wert", min_value=0.0, format="%.2f")

    kommentar = st.text_area("Kommentar")

    # Initialisiere DataFrame in Session (einmalig)
    if "labor_tabelle" not in st.session_state:
        st.session_state.labor_tabelle = pd.DataFrame(columns=["Datum", "Typ", "Wert", "Kommentar"])

    # Speichern
    if st.button(" Wert hinzufügen"):
        neue_zeile = {
            "Datum": datum.strftime("%Y-%m-%d"),
            "Typ": labortyp,
            "Wert": wert,
            "Kommentar": kommentar
        }
        st.session_state.labor_tabelle = pd.concat(
            [st.session_state.labor_tabelle, pd.DataFrame([neue_zeile])],
            ignore_index=True
        )
        st.success("✅ Wert erfolgreich hinzugefügt.")

    st.markdown("---")
    st.subheader("🗂️ Ihre bisherigen Einträge")
    st.dataframe(st.session_state.labor_tabelle, use_container_width=True)