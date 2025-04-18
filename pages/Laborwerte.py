import streamlit as st
import pandas as pd
import datetime
import os

# === CSV-Dateipfad ===
csv_path = "laborwerte.csv"

# === Bestehende Tabelle laden oder neu starten ===
if os.path.exists(csv_path):
    labor_tabelle = pd.read_csv(csv_path)
else:
    labor_tabelle = pd.DataFrame(columns=["Laborwert", "Wert", "Einheit", "Datum", "Referenz", "Ampel"])

st.title("🧪 Laborwerte – Eingabe")

# === Laboroptionen ===
laboroptionen = {
    "CRP": {"einheit": "mg/L", "ref_min": 0, "ref_max": 5},
    "TSH": {"einheit": "mIU/L", "ref_min": 0.4, "ref_max": 4.0},
    "Glucose": {"einheit": "mg/dL", "ref_min": 70, "ref_max": 99}
}

# === Auswahl
st.subheader("Auswahl des Laborwerts")
ausgewählt = st.selectbox("Laborwert auswählen", list(laboroptionen.keys()))
einheit = laboroptionen[ausgewählt]["einheit"]
ref_min = laboroptionen[ausgewählt]["ref_min"]
ref_max = laboroptionen[ausgewählt]["ref_max"]

# === Eingabe
col1, col2 = st.columns(2)
with col1:
    wert = st.number_input("Wert", min_value=0.0, step=0.1)
    datum = st.date_input("Datum", value=datetime.date.today())
with col2:
    st.text_input("Einheit", value=einheit, disabled=True)
    st.text_input("Referenzbereich", value=f"{ref_min} – {ref_max} {einheit}", disabled=True)

# === Speichern
if st.button(" Speichern"):
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

    # An Tabelle anhängen und speichern
    labor_tabelle = pd.concat([labor_tabelle, pd.DataFrame([neuer_eintrag])], ignore_index=True)
    labor_tabelle.to_csv(csv_path, index=False)

    st.success("✅ Eintrag gespeichert (dauerhaft in CSV)!")

# === Tabelle anzeigen
if not labor_tabelle.empty:
    st.markdown("---")
    st.subheader(" Ihre bisherigen Einträge")
    st.dataframe(labor_tabelle.sort_values("Datum", ascending=False), use_container_width=True)