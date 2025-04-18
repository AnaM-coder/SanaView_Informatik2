import streamlit as st
import datetime

def show_laborwerte():
    st.title(" Laborwerte – Eingabe")

    # Liste möglicher Laborwerte
    laboroptionen = {
        "CRP": {"einheit": "mg/L", "ref_min": 0, "ref_max": 5},
        "TSH": {"einheit": "mIU/L", "ref_min": 0.4, "ref_max": 4.0},
        "Glucose": {"einheit": "mg/dL", "ref_min": 70, "ref_max": 99}
    }

    # Dropdown Auswahl
    st.subheader("Auswahl des Laborwerts")
    ausgewählt = st.selectbox("Laborwert auswählen", list(laboroptionen.keys()))

    # Automatisch Einheit + Referenzbereich einfüllen
    einheit = laboroptionen[ausgewählt]["einheit"]
    ref_min = laboroptionen[ausgewählt]["ref_min"]
    ref_max = laboroptionen[ausgewählt]["ref_max"]

    # Eingabefelder
    col1, col2 = st.columns(2)
    with col1:
        wert = st.number_input("Wert", min_value=0.0, step=0.1)
        datum = st.date_input("Datum", value=datetime.date.today())
    with col2:
        st.text_input("Einheit", value=einheit, disabled=True)
        st.text_input("Referenzbereich", value=f"{ref_min} - {ref_max} {einheit}", disabled=True)

    # Session-Tabelle vorbereiten
    if "labor_tabelle" not in st.session_state:
        st.session_state.labor_tabelle = []

    # Speichern-Button
    if st.button(" Speichern"):
        # Ampelfarbe bestimmen
        if wert < ref_min:
            ampel = "🟡 (zu niedrig)"
        elif wert > ref_max:
            ampel = "🔴 (zu hoch)"
        else:
            ampel = "🟢 (normal)"

        st.session_state.labor_tabelle.append({
            "Laborwert": ausgewählt,
            "Wert": wert,
            "Einheit": einheit,
            "Datum": datum,
            "Referenz": f"{ref_min}–{ref_max}",
            "Ampel": ampel
        })
        st.success("✅ Eintrag erfolgreich gespeichert!")

    # Tabelle anzeigen
    if st.session_state.labor_tabelle:
        st.markdown("---")
        st.subheader("📁 Ihre bisherigen Einträge")
        st.dataframe(st.session_state.labor_tabelle, use_container_width=True)

# Direkt aufrufen
show_laborwerte()
