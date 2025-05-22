import streamlit as st
import base64
import datetime
import pandas as pd
import fitz  # PyMuPDF
import re
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# === Hintergrundbild aus img-Ordner als Base64 einbinden ===
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_path = "img/labor_bg.png"
img_base64 = get_base64_of_bin_file(img_path)

st.markdown(
    f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{img_base64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

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

# === Referenzwerte inkl. Kinder, Frauen, Männer, Schwangere ===
referenzwerte = {
    "Albumin": {"Männer": "3.5 – 5.0 g/dl", "Frauen": "3.5 – 5.0 g/dl", "Schwanger": "3.0 – 4.5 g/dl", "Kinder": "3.8 – 5.4 g/dl"},
    "Anionenlücke": {"Männer": "8 – 16 mmol/l", "Frauen": "8 – 16 mmol/l", "Schwanger": "8 – 16 mmol/l", "Kinder": "10 – 18 mmol/l"},
    "Base Excess": {"Männer": "-2 – 2 mmol/l", "Frauen": "-2 – 2 mmol/l", "Schwanger": "-2 – 2 mmol/l", "Kinder": "-3 – 3 mmol/l"},
    "Bilirubin (gesamt)": {"Männer": "0.1 – 1.2 mg/dl", "Frauen": "0.1 – 1.2 mg/dl", "Schwanger": "0.1 – 1.0 mg/dl", "Kinder": "0.2 – 1.0 mg/dl"},
    "CRP": {"Männer": "0 – 5 mg/l", "Frauen": "0 – 5 mg/l", "Schwanger": "0 – 5 mg/l", "Kinder": "0 – 5 mg/l"},
    "Calcium (ionisiert)": {"Männer": "1.15 – 1.30 mmol/l", "Frauen": "1.15 – 1.30 mmol/l", "Schwanger": "1.10 – 1.25 mmol/l", "Kinder": "1.00 – 1.30 mmol/l"},
    "Chlorid": {"Männer": "98 – 106 mmol/l", "Frauen": "98 – 106 mmol/l", "Schwanger": "98 – 106 mmol/l", "Kinder": "98 – 106 mmol/l"},
    "Fibrinogen": {"Männer": "200 – 400 mg/dl", "Frauen": "200 – 400 mg/dl", "Schwanger": "400 – 650 mg/dl", "Kinder": "150 – 400 mg/dl"},
    "Glukose (nüchtern)": {"Männer": "70 – 100 mg/dl", "Frauen": "70 – 100 mg/dl", "Schwanger": "60 – 90 mg/dl", "Kinder": "70 – 110 mg/dl"},
    "Hämoglobin": {"Männer": "13.5 – 17.5 g/dl", "Frauen": "12.0 – 16.0 g/dl", "Schwanger": "≥11.0 g/dl", "Kinder": "11.5 – 14.5 g/dl"},
    "Hämatokrit": {"Männer": "40 – 50 %", "Frauen": "36 – 46 %", "Schwanger": "33 – 43 %", "Kinder": "34 – 40 %"},
    "Harnstoff (BUN)": {"Männer": "8 – 24 mg/dl", "Frauen": "7 – 20 mg/dl", "Schwanger": "3 – 13 mg/dl", "Kinder": "5 – 18 mg/dl"},
    "HCO₃⁻": {"Männer": "22 – 26 mmol/l", "Frauen": "22 – 26 mmol/l", "Schwanger": "18 – 22 mmol/l", "Kinder": "20 – 28 mmol/l"},
    "INR": {"Männer": "0.8 – 1.2", "Frauen": "0.8 – 1.2", "Schwanger": "0.8 – 1.2", "Kinder": "0.8 – 1.2"},
    "Kalium": {"Männer": "3.5 – 5.1 mmol/l", "Frauen": "3.5 – 5.1 mmol/l", "Schwanger": "3.3 – 5.1 mmol/l", "Kinder": "3.5 – 5.0 mmol/l"},
    "Kreatinin": {"Männer": "0.7 – 1.2 mg/dl", "Frauen": "0.6 – 1.1 mg/dl", "Schwanger": "0.4 – 0.8 mg/dl", "Kinder": "0.3 – 0.7 mg/dl"},
    "Laktat": {"Männer": "0 – 1.5 mmol/l", "Frauen": "0 – 1.5 mmol/l", "Schwanger": "0 – 1.5 mmol/l", "Kinder": "0.5 – 2.2 mmol/l"},
    "Leukozyten": {"Männer": "4000 – 10000 /µl", "Frauen": "4000 – 10000 /µl", "Schwanger": "6000 – 16000 /µl", "Kinder": "5000 – 15000 /µl"},
    "Magnesium": {"Männer": "0.7 – 1.0 mmol/l", "Frauen": "0.7 – 1.0 mmol/l", "Schwanger": "0.7 – 1.0 mmol/l", "Kinder": "0.70 – 1.1 mmol/l"},
    "Natrium": {"Männer": "135 – 145 mmol/l", "Frauen": "135 – 145 mmol/l", "Schwanger": "130 – 145 mmol/l", "Kinder": "135 – 145 mmol/l"},
    "pCO₂": {"Männer": "35 – 45 mmHg", "Frauen": "35 – 45 mmHg", "Schwanger": "27 – 32 mmHg", "Kinder": "30 – 40 mmHg"},
    "pH (arteriell)": {"Männer": "7.35 – 7.45", "Frauen": "7.35 – 7.45", "Schwanger": "7.44 – 7.46", "Kinder": "7.36 – 7.44"},
    "Procalcitonin": {"Männer": "0 – 0.5 ng/ml", "Frauen": "0 – 0.5 ng/ml", "Schwanger": "0 – 0.5 ng/ml", "Kinder": "0 – 0.5 ng/ml"},
    "PTT (APTT)": {"Männer": "25 – 35 s", "Frauen": "25 – 35 s", "Schwanger": "17 – 33 s", "Kinder": "25 – 35 s"},
    "Thrombozyten": {"Männer": "150000 – 400000 /µl", "Frauen": "150000 – 400000 /µl", "Schwanger": "100000 – 400000 /µl", "Kinder": "150000 – 450000 /µl"},
    "Troponin T/I": {"Männer": "0 – 0.04 ng/ml", "Frauen": "0 – 0.04 ng/ml", "Schwanger": "0 – 0.04 ng/ml", "Kinder": "0 – 0.03 ng/ml"}
}

# === Profildaten aus Profilverwaltung laden ===
profil_key = f"profil_daten_{username}"
profil_df = st.session_state.get(profil_key)
profil_daten = {}
if profil_df is not None and not profil_df.empty:
    eintrag = profil_df[profil_df["Benutzername"] == username]
    if not eintrag.empty:
        profil_daten = eintrag.iloc[-1].to_dict()

geschlecht = profil_daten.get("Geschlecht", "Männlich")
geburtsdatum = profil_daten.get("Geburtsdatum", "01.01.1980")
schwanger = profil_daten.get("Schwanger", "Nein")

try:
    geburtsdatum_dt = datetime.datetime.strptime(geburtsdatum, "%d.%m.%Y").date()
    alter = (datetime.date.today() - geburtsdatum_dt).days // 365
except:
    alter = 30  # Fallback

# Robuste Schwanger-Erkennung
if alter < 18:
    profil = "Kinder"
elif geschlecht.lower() == "weiblich" and str(schwanger).strip().lower() in ["ja", "true", "1"]:
    profil = "Schwanger"
elif geschlecht.lower() == "weiblich":
    profil = "Frauen"
else:
    profil = "Männer"

# === Eingabe (ohne sichtbare Profilfelder) ===
st.title(" 🩸 Laborwerte – Eingabe")

ausgewählt = st.selectbox("Laborwert", sorted(referenzwerte.keys()))
ref_string = referenzwerte[ausgewählt][profil]
einheit = ref_string.split()[-1]

# Referenzbereich für das gewählte Profil extrahieren
ref_min, ref_max = None, None
if "≥" in ref_string:
    ref_min = float(ref_string.replace("≥", "").replace(einheit, "").strip().replace(",", "."))
    ref_max = None
elif "–" in ref_string:
    ref_min, ref_max = [float(x.replace(einheit, "").replace(",", ".").strip()) for x in ref_string.split("–")]
else:
    ref_min = None
    ref_max = None

col1, col2 = st.columns(2)
with col1:
    wert = st.number_input("Wert", min_value=0.0, step=0.1)
    datum = st.date_input("Datum", value=datetime.date.today())
with col2:
    st.text_input("Einheit", value=einheit, disabled=True)
    st.text_input("Referenz", value=ref_string, disabled=True)

if st.button("Speichern"):
    ampel = "🟢 (normal)"
    if ref_min is not None and wert < ref_min:
        ampel = "🟡 (niedrig)"
    if ref_max is not None and wert > ref_max:
        ampel = "🔴 (hoch)"
    neuer_eintrag = {
        "Datum": datum.strftime("%d.%m.%Y"),
        "Laborwert": ausgewählt,
        "Wert": wert,
        "Einheit": einheit,
        "Referenz": ref_string,
        "Ampel": ampel
    }
    data_manager.append_record(session_state_key=session_key, record_dict=neuer_eintrag)
    data_manager.save_data(session_state_key=session_key)
    st.success("Laborwert erfolgreich gespeichert!")

# === Automatische Profilerkennung aus PDF ===
def bestimme_profil(text):
    if re.search(r'\bkind(er)?\b', text, re.IGNORECASE) or re.search(r'\balter\s*[:=]?\s*\d{1,2}\s*(Jahre|J\.|Jahre alt)', text, re.IGNORECASE):
        return "Kinder"
    if re.search(r'\bschwanger\b', text, re.IGNORECASE):
        return "Schwanger"
    if re.search(r'\bweiblich\b', text, re.IGNORECASE) or re.search(r'\bfrau\b', text, re.IGNORECASE):
        return "Frauen"
    if re.search(r'\bmännlich\b', text, re.IGNORECASE) or re.search(r'\bmann\b', text, re.IGNORECASE):
        return "Männer"
    return "Männer"  # Standard

# === PDF Upload (Datum aus PDF suchen, alle Werte erkennen, Profil automatisch) ===
st.markdown("### PDF mit Laborwerten hochladen")
pdf = st.file_uploader("PDF auswählen", type="pdf")

if pdf and pdf.name != st.session_state.get("last_pdf_name"):
    st.session_state["last_pdf_name"] = pdf.name

    doc = fitz.open(stream=pdf.read(), filetype="pdf")
    text = "\n".join(page.get_text() for page in doc)

    # Profil automatisch bestimmen
    auto_profil = bestimme_profil(text)
    st.info(f"Automatisch erkanntes Profil: {auto_profil}")

    # Datum suchen (erste Zeile mit Entnahme/Befunddatum/Datum)
    extrahiertes_datum = None
    for zeile in text.split("\n"):
        if any(x in zeile.lower() for x in ["entnahme", "befunddatum", "datum"]):
            match = re.search(r"\b(\d{2}\.\d{2}\.\d{4})\b", zeile)
            if match:
                extrahiertes_datum = match.group(1)
                break

    datum = extrahiertes_datum or datetime.date.today().strftime("%d.%m.%Y")
    gefunden = []

    for key in referenzwerte.keys():
        pattern = rf"{re.escape(key)}\s*[:=]?\s*(-?\d+[.,]?\d*)"
        for match in re.finditer(pattern, text, re.IGNORECASE):
            try:
                wert = float(match.group(1).replace(",", "."))
                ref_string = referenzwerte[key][auto_profil]
                einheit = ref_string.split()[-1]
                ref_min, ref_max = None, None
                if "≥" in ref_string:
                    ref_min = float(ref_string.replace("≥", "").replace(einheit, "").strip().replace(",", "."))
                    ref_max = None
                elif "–" in ref_string:
                    ref_min, ref_max = [float(x.replace(einheit, "").replace(",", ".").strip()) for x in ref_string.split("–")]
                ampel = "🟢 (normal)"
                if ref_min is not None and wert < ref_min:
                    ampel = "🟡 (niedrig)"
                if ref_max is not None and wert > ref_max:
                    ampel = "🔴 (hoch)"
                eintrag = {
                    "Datum": datum,
                    "Laborwert": key,
                    "Wert": wert,
                    "Einheit": einheit,
                    "Referenz": ref_string,
                    "Ampel": ampel
                }
                data_manager.append_record(session_state_key=session_key, record_dict=eintrag)
                gefunden.append(key)
            except:
                continue

    data_manager.save_data(session_state_key=session_key)
    if gefunden:
        st.success(f"Erkannte und gespeicherte Laborwerte: {', '.join(gefunden)}")
    else:
        st.warning("Keine bekannten Laborwerte im PDF erkannt.")
elif pdf:
    st.info("PDF wurde bereits verarbeitet. Bitte eine andere Datei auswählen.")

# ...vorheriger Code...

# === Anzeige & Löschen
df = st.session_state[session_key]
df = df[[c for c in df.columns if c in ["Datum", "Laborwert", "Wert", "Einheit", "Referenz", "Ampel"]]]
st.session_state[session_key] = df

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

    # Deutliche Warnung und roter Button für Löschen
    st.markdown("### 🗑️ Eintrag löschen")
    if len(df) > 0:
        optionen = df.apply(lambda row: f"{row['Datum']} – {row['Laborwert']} ({row['Wert']:.2f} {row['Einheit']})", axis=1).tolist()
        auswahl = st.selectbox("Eintrag auswählen", optionen)
        st.markdown('<div style="margin-top: 10px"></div>', unsafe_allow_html=True)

        if "delete_confirm" not in st.session_state:
            st.session_state["delete_confirm"] = False
        if "delete_result" not in st.session_state:
            st.session_state["delete_result"] = None

        if st.button("Eintrag löschen", type="primary", key="delete_button"):
            st.session_state["delete_confirm"] = True
            st.session_state["delete_result"] = None

        if st.session_state.get("delete_confirm"):
            st.warning("Sind Sie sicher, dass Sie diesen Eintrag löschen möchten?")
            aktion = st.selectbox("Bitte wählen:", ["", "Ja", "Nein"], key="delete_action")
            if aktion == "Ja":
                maske = df.apply(lambda row: f"{row['Datum']} – {row['Laborwert']} ({row['Wert']:.2f} {row['Einheit']})", axis=1) == auswahl
                df = df[~maske].reset_index(drop=True)
                st.session_state[session_key] = df
                data_manager.save_data(session_state_key=session_key)
                st.session_state["delete_confirm"] = False
                st.session_state["delete_result"] = "success"
                st.experimental_rerun()
            elif aktion == "Nein":
                st.session_state["delete_confirm"] = False
                st.session_state["delete_result"] = "cancel"
                st.experimental_rerun()

        if st.session_state.get("delete_result") == "success":
            st.success("Eintrag erfolgreich gelöscht!")
            st.session_state["delete_result"] = None
        elif st.session_state.get("delete_result") == "cancel":
            st.info("Eintrag nicht gelöscht.")
            st.session_state["delete_result"] = None
    else:
        st.info("Keine Einträge zum Löschen vorhanden.")

# === Navigations-Buttons am Schluss ===
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("Profil"):
        st.switch_page("pages/2Profilverwaltung.py")
with col2:
    if st.button("Verlauf"):
        st.switch_page("pages/4Verlauf.py")
with col3:
    if st.button("Infoseite"):
        st.switch_page("pages/5Infoseite.py")
with col4:
    if st.button("Hauptmenü"):
        st.switch_page("pages/1Hauptmenü.py")
with col5:
    if st.button("Start"):
        st.switch_page("Start.py")