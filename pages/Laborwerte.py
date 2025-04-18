import streamlit as st
import pandas as pd
import datetime
import os

# === CSV-Dateipfad ===
csv_path = "laborwerte.csv"

# === Bestehende Tabelle laden oder neu erstellen ===
if os.path.exists(csv_path):
    try:
        labor_tabelle = pd.read_csv(csv_path)
    except Exception as e:
        st.error(f"Fehler beim Laden der CSV-Datei: {e}")
        labor_tabelle = pd.DataFrame(columns=["Laborwert", "Wert", "Einheit", "Datum", "Referenz", "Ampel"])
else:
    labor_tabelle = pd.DataFrame(columns=["Laborwert", "Wert", "Einheit", "Datum", "Referenz", "Ampel"])

# === Titel
st.title("🧪 Laborwerte – Eingabe")

# === Optionen
laboroptionen = {
    "CRP": {"einheit": "mg/L", "ref_min": 0, "ref_max": 5},
    "TSH": {"einheit": "mIU/L", "ref_min": 0.4, "ref_max": 4.0},
    "Glucose": {"einheit": "mg/dL", "ref_min": 70, "ref_max": 99}
}

# Auswahl
st.subheader("Laborwert auswählen")
ausgewählt = st.selectbox("Laborwert", list(laboroptionen.keys()))
einheit = laboroptionen[ausgewählt]["einheit"]
ref_min = laboroptionen[ausgewählt]["ref_min"]
ref_max = laboroptionen[ausgewählt]["ref_max"]

# Eingabe
col1, col2 = st.columns(2)
with col1:
    wert = st.number_input("Wert", min_value=0.0, step=0.1)
    datum = st.date_input("Datum", value=datetime.date.today())
with col2:
    st.text_input("Einheit", value=einheit, disabled=True)
    st.text_input("Referenz", value=f"{ref_min}–{ref_max} {einheit}", disabled=True)

# Speichern
if st.button("💾 Speichern"):
    if wert < ref_min:
        ampel = "🟡 (zu niedrig)"
    elif wert > ref_max:
        ampel = "🔴 (zu hoch)"
    else:
        ampel = "🟢 (normal)"

    neuer_eintrag = {
        "Laborwert": ausgewählt,
        "Wert": wert,
        "Einheit": einheit,
        "Datum": datum.strftime("%d.%m.%Y"),
        "Referenz": f"{ref_min}–{ref_max}",
        "Ampel": ampel
    }

    labor_tabelle = pd.concat([labor_tabelle, pd.DataFrame([neuer_eintrag])], ignore_index=True)

    try:
        labor_tabelle.to_csv(csv_path, index=False)
        st.success("✅ Dauerhaft gespeichert in 'laborwerte.csv'")
    except Exception as e:
        st.error(f"Fehler beim Speichern der CSV: {e}")

# Anzeige
if not labor_tabelle.empty:
    st.markdown("---")
    st.subheader("📋 Gespeicherte Laborwerte")
    st.dataframe(labor_tabelle, use_container_width=True)