import streamlit as st
import datetime
import pandas as pd
import fitz  # PyMuPDF
import re
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# === Login-Schutz ===
LoginManager().go_to_login('Start.py')

# === Nutzername prüfen ===
username = st.session_state.get("username")
if not username:
    st.error("⚠️ Kein Benutzer eingeloggt! Anmeldung erforderlich.")
    st.stop()

data_manager = DataManager()
session_key = f"user_data_{username}"
file_name = f"{username}_daten.csv"

data_manager.load_user_data(
    session_state_key=session_key,
    file_name=file_name,
    initial_value=pd.DataFrame(columns=["Datum", "Laborwert", "Wert", "Einheit", "Referenz", "Ampel"])
)

# === Laboroptionen 
laboroptionen = {
    "Albumin": {"einheit": "g/dl", "ref_min": 3.5, "ref_max": 5.0},
    "Anionenlücke": {"einheit": "mmol/l", "ref_min": 8, "ref_max": 16},
    "Base Excess": {"einheit": "mmol/l", "ref_min": -2, "ref_max": 2},
    "Bilirubin (gesamt)": {"einheit": "mg/dl", "ref_min": 0.1, "ref_max": 1.2},
    "CRP": {"einheit": "mg/l", "ref_min": 0, "ref_max": 5},
    "Calcium (ionisiert)": {"einheit": "mmol/l", "ref_min": 1.15, "ref_max": 1.30},
    "Chlorid": {"einheit": "mmol/l", "ref_min": 98, "ref_max": 106},
    "Fibrinogen": {"einheit": "mg/dl", "ref_min": 200, "ref_max": 400},
    "Glukose (nüchtern)": {"einheit": "mg/dl", "ref_min": 70, "ref_max": 100},
    "HBA1c": {"einheit": "%", "ref_min": 4.0, "ref_max": 6.0},
    "HCO₃⁻": {"einheit": "mmol/l", "ref_min": 22, "ref_max": 26},
    "Harnstoff (BUN)": {"einheit": "mg/dl", "ref_min": 7, "ref_max": 20},
    "Hämatokrit (Frauen)": {"einheit": "%", "ref_min": 36, "ref_max": 46},
    "Hämatokrit (Männer)": {"einheit": "%", "ref_min": 40, "ref_max": 50},
    "Hämoglobin (Frauen)": {"einheit": "g/dl", "ref_min": 12.0, "ref_max": 16.0},
    "Hämoglobin (Männer)": {"einheit": "g/dl", "ref_min": 13.5, "ref_max": 17.5},
    "INR": {"einheit": "-", "ref_min": 0.8, "ref_max": 1.2},
    "Kalium": {"einheit": "mmol/l", "ref_min": 3.5, "ref_max": 5.0},
    "Kreatinin": {"einheit": "mg/dl", "ref_min": 0.6, "ref_max": 1.2},
    "Laktat": {"einheit": "mmol/l", "ref_min": 0, "ref_max": 1.5},
    "Leukozyten": {"einheit": "/µl", "ref_min": 4000, "ref_max": 10000},
    "Magnesium": {"einheit": "mmol/l", "ref_min": 0.7, "ref_max": 1.0},
    "Natrium": {"einheit": "mmol/l", "ref_min": 135, "ref_max": 145},
    "PTT (APTT)": {"einheit": "s", "ref_min": 25, "ref_max": 35},
    "Procalcitonin": {"einheit": "ng/ml", "ref_min": 0, "ref_max": 0.5},
    "TSH": {"einheit": "mIU/L", "ref_min": 0.4, "ref_max": 4.0},
    "Thrombozyten": {"einheit": "/µl", "ref_min": 150000, "ref_max": 400000},
    "Troponin T/I": {"einheit": "ng/ml", "ref_min": 0, "ref_max": 0.04},
    "pCO₂": {"einheit": "mmHg", "ref_min": 35, "ref_max": 45},
    "pH (arteriell)": {"einheit": "", "ref_min": 7.35, "ref_max": 7.45}
}

# === Eingabeformular
st.title("Laborwerte – Eingabe")
ausgewählt = st.selectbox("Laborwert", sorted(laboroptionen.keys()))
info = laboroptionen[ausgewählt]

col1, col2 = st.columns(2)
with col1:
    wert = st.number_input("Wert", min_value=0.0, step=0.1)
    datum = st.date_input("Datum", value=datetime.date.today())
with col2:
    st.text_input("Einheit", value=info["einheit"], disabled=True)
    st.text_input("Referenz", value=f"{info['ref_min']}–{info['ref_max']} {info['einheit']}", disabled=True)

if st.button("Speichern"):
    if wert < info["ref_min"]:
        ampel = "🟡 (niedrig)"
    elif wert > info["ref_max"]:
        ampel = "🔴 (hoch)"
    else:
        ampel = "🟢 (normal)"

    neuer_eintrag = {
        "Datum": datum.strftime("%d.%m.%Y"),
        "Laborwert": ausgewählt,
        "Wert": wert,
        "Einheit": info["einheit"],
        "Referenz": f"{info['ref_min']}–{info['ref_max']}",
        "Ampel": ampel
    }
    data_manager.append_record(session_state_key=session_key, record_dict=neuer_eintrag)
    st.success("Laborwert erfolgreich gespeichert!")

# === PDF Upload
st.markdown("### PDF mit Laborwerten hochladen")
pdf = st.file_uploader("PDF auswählen", type="pdf")

if pdf:
    doc = fitz.open(stream=pdf.read(), filetype="pdf")
    text = "\n".join(page.get_text() for page in doc)

    # Entnahmedatum suchen (z. B. "04.05.2025")
    date_match = re.search(r"\b(\d{2}\.\d{2}\.\d{4})\b", text)
    try:
        entnahmedatum = datetime.datetime.strptime(date_match.group(1), "%d.%m.%Y").strftime("%d.%m.%Y") if date_match else datetime.date.today().strftime("%d.%m.%Y")
    except:
        entnahmedatum = datetime.date.today().strftime("%d.%m.%Y")

    gefunden = []
    for key, info in laboroptionen.items():
        pattern = rf"{re.escape(key)}\s*[:=]?\s*(-?\d+[.,]?\d*)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                value = float(match.group(1).replace(",", "."))
                if value < info["ref_min"]:
                    ampel = "🟡 (niedrig)"
                elif value > info["ref_max"]:
                    ampel = "🔴 (hoch)"
                else:
                    ampel = "🟢 (normal)"

                eintrag = {
                    "Datum": entnahmedatum,
                    "Laborwert": key,
                    "Wert": value,
                    "Einheit": info["einheit"],
                    "Referenz": f"{info['ref_min']}–{info['ref_max']}",
                    "Ampel": ampel
                }
                data_manager.append_record(session_state_key=session_key, record_dict=eintrag)
                gefunden.append(key)
            except:
                continue

    if gefunden:
        st.success(f"Erkannt & gespeichert: {', '.join(gefunden)}")
    else:
        st.warning("Keine Laborwerte erkannt.")

# === Tabelle
if not st.session_state[session_key].empty:
    st.markdown("---")
    st.subheader("Ihre gespeicherten Laborwerte")
    st.dataframe(st.session_state[session_key], use_container_width=True)