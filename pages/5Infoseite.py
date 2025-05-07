import streamlit as st
import pandas as pd
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# === Login-Schutz ===
LoginManager().go_to_login("Start.py")

# === Seitenlayout ===
st.set_page_config(page_title="Info-Seite", layout="wide")
st.title("Info – Seite")

st.markdown("""
Hier finden Sie Erklärungen und die Referenzwerte zu Ihren Laborwerten.
""")

# === Laborwerte mit Erklärungen ===
labor_erklärungen = {
    "Albumin": "Eiweiss im Blut – trägt zum osmotischen Druck bei.",
    "Anionenlücke": "Rechengröße – ergibt sich aus Elektrolyten im Blut.",
    "Base Excess": "Gibt an, ob Basenüberschuss oder -mangel vorliegt.",
    "Bilirubin (gesamt)": "Abbauprodukt des roten Blutfarbstoffs.",
    "CRP": "Eiweiss – Bestandteil der körpereigenen Abwehr.",
    "Calcium (ionisiert)": "Mineralstoff – wichtig für Zellen, Muskeln und Knochen.",
    "Chlorid": "Elektrolyt – unterstützt den Säure-Basen-Haushalt.",
    "Fibrinogen": "Eiweiss – spielt eine Rolle bei der Blutgerinnung.",
    "Glukose (nüchtern)": "Zuckerwert im Blut – wird nüchtern gemessen.",
    "Hämoglobin (Frauen)": "Blutfarbstoff bei Frauen – relevant für den Sauerstofftransport.",
    "Hämoglobin (Männer)": "Blutfarbstoff, der Sauerstoff im Blut transportiert.",
    "Hämatokrit (Frauen)": "Anteil der festen Bestandteile bei Frauen.",
    "Hämatokrit (Männer)": "Anteil der festen Bestandteile bei Männern.",
    "Harnstoff (BUN)": "Stoff, der beim Abbau von Eiweiss entsteht.",
    "HCO₃⁻": "Bikarbonat – ein Puffersystem im Blut.",
    "INR": "Mass für die Blutgerinnung.",
    "Kalium": "Elektrolyt – beteiligt an der Reizweiterleitung und Muskelfunktion.",
    "Kreatinin": "Stoffwechselprodukt – entsteht in der Muskulatur.",
    "Laktat": "Produkt des Stoffwechsels – bildet sich bei Aktivität.",
    "Leukozyten": "Weiße Blutkörperchen – Bestandteil des Immunsystems.",
    "Magnesium": "Mineralstoff – unterstützt Nerven und Enzymprozesse.",
    "Natrium": "Elektrolyt – wichtig für Flüssigkeitshaushalt und Zellfunktion.",
    "pCO₂": "Kohlendioxid-Gehalt im Blut.",
    "pH (arteriell)": "Mass für den Säuregrad des Blutes.",
    "Procalcitonin": "Eiweiss – Bestandteil regulativer Vorgänge im Körper.",
    "PTT (APTT)": "Zeit, die das Blut benötigt, um zu gerinnen.",
    "Thrombozyten": "Blutplättchen – beteiligt an der Blutgerinnung.",
    "Troponin T/I": "Eiweiss – Bestandteil der Muskulatur."
}

df_info = pd.DataFrame(labor_erklärungen.items(), columns=["Begriff", "Erklärung"])
st.subheader("Begriffserklärungen")
st.dataframe(df_info, use_container_width=True)

# === Neue strukturierte Referenzwerte
referenzwerte = {
    "Hämoglobin": {"Männer": "13.5 – 17.5 g/dl", "Frauen": "12.0 – 16.0 g/dl", "Schwanger": "-"},
    "Hämatokrit": {"Männer": "40 – 50 %", "Frauen": "36 – 46 %", "Schwanger": "-"},
    "Leukozyten": {"Männer": "4000 – 10000 /µl", "Frauen": "4000 – 10000 /µl", "Schwanger": "6000 – 16000 /µl"},
    "Thrombozyten": {"Männer": "150000 – 400000 /µl", "Frauen": "150000 – 400000 /µl", "Schwanger": "100000 – 400000 /µl"},
    "Natrium": {"Männer": "135 – 145 mmol/l", "Frauen": "135 – 145 mmol/l", "Schwanger": "130 – 145 mmol/l"},
    "Kalium": {"Männer": "3.5 – 5.0 mmol/l", "Frauen": "3.5 – 5.0 mmol/l", "Schwanger": "3.3 – 5.1 mmol/l"},
    "Glukose (nüchtern)": {"Männer": "70 – 100 mg/dl", "Frauen": "70 – 100 mg/dl", "Schwanger": "60 – 90 mg/dl"},
    "Kreatinin": {"Männer": "0.7 – 1.2 mg/dl", "Frauen": "0.6 – 1.1 mg/dl", "Schwanger": "0.4 – 0.8 mg/dl"},
    "CRP": {"Männer": "0 – 5 mg/l", "Frauen": "0 – 5 mg/l", "Schwanger": "<10 mg/l"},
    "pH (arteriell)": {"Männer": "7.35 – 7.45", "Frauen": "7.35 – 7.45", "Schwanger": "7.44 – 7.46"},
    "pCO₂": {"Männer": "35 – 45 mmHg", "Frauen": "35 – 45 mmHg", "Schwanger": "27 – 32 mmHg"},
    "Fibrinogen": {"Männer": "200 – 400 mg/dl", "Frauen": "200 – 400 mg/dl", "Schwanger": "400 – 650 mg/dl"},
    "Troponin T/I": {"Männer": "0 – 0.04 ng/ml", "Frauen": "0 – 0.04 ng/ml", "Schwanger": "0 – 0.04 ng/ml"},
}

# Umwandeln in DataFrame
df_ref = pd.DataFrame([
    {"Laborwert": k, "Männer": v.get("Männer", "-"), "Frauen": v.get("Frauen", "-"), "Schwanger": v.get("Schwanger", "-")}
    for k, v in referenzwerte.items()
])

st.markdown("### Referenzwerte (nach Personengruppe)")
st.dataframe(df_ref, use_container_width=True)
