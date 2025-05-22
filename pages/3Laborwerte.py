import streamlit as st
import datetime
import pandas as pd
import fitz  # PyMuPDF
import re
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# === Seitenstil ===
st.markdown("""
    <style>
        html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewContainer"] > .main {
            background-color: #d9ecf2 !important;
        }
    </style>
""", unsafe_allow_html=True)

# === Login ===
login_manager = LoginManager(data_manager=DataManager())
if not st.session_state.get("authentication_status", False):
    st.error("⚠️ Kein Benutzer eingeloggt! Anmeldung erforderlich.")
    st.stop()

with st.sidebar:
    login_manager.authenticator.logout("Logout", key="logout_sidebar")

username = st.session_state.get("username")
data_manager = DataManager()

session_key = f"user_data_{username}"
file_name = f"{username}_daten.csv"

data_manager.load_user_data(
    session_state_key=session_key,
    file_name=file_name,
    initial_value=pd.DataFrame(columns=["Datum", "Laborwert", "Wert", "Einheit", "Referenz", "Ampel"])
)

# === Laboroptionen ===
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

# === Eingabe ===
st.title("Laborwerte – Eingabe")
ausgewählt = st.selectbox("Laborwert", sorted(laboroptionen.keys()))
einheit = laboroptionen[ausgewählt]["einheit"]
ref_min = laboroptionen[ausgewählt]["ref_min"]
ref_max = laboroptionen[ausgewählt]["ref_max"]

col1, col2 = st.columns(2)
with col1:
    wert = st.number_input("Wert", min_value=0.0, step=0.1)
    datum = st.date_input("Datum", value=datetime.date.today())
with col2:
    st.text_input("Einheit", value=einheit, disabled=True)
    st.text_input("Referenz", value=f"{ref_min}–{ref_max} {einheit}", disabled=True)

if st.button("Speichern"):
    ampel = "🟢 (normal)"
    if wert < ref_min:
        ampel = "🟡 (niedrig)"
    elif wert > ref_max:
        ampel = "🔴 (hoch)"
    neuer_eintrag = {
        "Datum": datum.strftime("%d.%m.%Y"),
        "Laborwert": ausgewählt,
        "Wert": wert,
        "Einheit": einheit,
        "Referenz": f"{ref_min}–{ref_max}",
        "Ampel": ampel
    }
    data_manager.append_record(session_state_key=session_key, record_dict=neuer_eintrag)
    st.success("Laborwert gespeichert!")

# === PDF Upload ===
st.markdown("### PDF mit Laborwerten hochladen")
pdf = st.file_uploader("PDF auswählen", type="pdf")

if pdf and pdf.name != st.session_state.get("last_pdf_name"):
    st.session_state["last_pdf_name"] = pdf.name
    doc = fitz.open(stream=pdf.read(), filetype="pdf")
    text = "\n".join(page.get_text() for page in doc)

    datum = datetime.date.today().strftime("%d.%m.%Y")
    for zeile in text.split("\n"):
        match = re.search(r"(\d{2}\.\d{2}\.\d{4})", zeile)
        if match:
            datum = match.group(1)
            break

    for key, info in laboroptionen.items():
        match = re.search(rf"{re.escape(key)}\s*[:=]?\s*(-?\d+[.,]?\d*)", text, re.IGNORECASE)
        if match:
            try:
                wert = float(match.group(1).replace(",", "."))
                ampel = "🟢 (normal)"
                if wert < info["ref_min"]:
                    ampel = "🟡 (niedrig)"
                elif wert > info["ref_max"]:
                    ampel = "🔴 (hoch)"
                eintrag = {
                    "Datum": datum,
                    "Laborwert": key,
                    "Wert": wert,
                    "Einheit": info["einheit"],
                    "Referenz": f"{info['ref_min']}–{info['ref_max']}",
                    "Ampel": ampel
                }
                data_manager.append_record(session_state_key=session_key, record_dict=eintrag)
            except:
                continue
    st.success("PDF erfolgreich verarbeitet!")

# === Anzeige & Löschen ===
df = st.session_state[session_key]
if not df.empty:
    st.markdown("---")
    st.subheader("Gespeicherte Laborwerte")
    ansicht = st.radio("Ansicht wählen", ["Gesamttabelle", "Nach Laborwert gruppiert"])

    if ansicht == "Gesamttabelle":
        st.dataframe(df, use_container_width=True)
    else:
        for laborwert in sorted(df["Laborwert"].unique()):
            with st.expander(laborwert):
                st.dataframe(df[df["Laborwert"] == laborwert], use_container_width=True)

    st.markdown("### Eintrag löschen")
    df["Index"] = df.index
    df["Anzeige"] = (
        df["Datum"] + " – " + df["Laborwert"] +
        " (" + df["Wert"].map(lambda x: f"{x:.2f}") + " " + df["Einheit"] + ")"
    )

    auswahl = st.selectbox("Eintrag auswählen", df["Anzeige"])
    if st.button("Eintrag löschen"):
        idx = df[df["Anzeige"] == auswahl]["Index"].values[0]
        df = df.drop(idx).reset_index(drop=True)
        st.session_state[session_key] = df
        data_manager.save_data(session_state_key=session_key, file_name=file_name)
        st.success("Eintrag gelöscht.")
else:
    st.info("Noch keine Laborwerte gespeichert.")
