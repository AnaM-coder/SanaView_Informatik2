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
    "Albumin": "Eiweiß im Blut – trägt zum osmotischen Druck bei.",
    "Anionenlücke": "Rechengröße – ergibt sich aus Elektrolyten im Blut.",
    "Base Excess": "Gibt an, ob Basenüberschuss oder -mangel vorliegt.",
    "Bilirubin (gesamt)": "Abbauprodukt des roten Blutfarbstoffs.",
    "CRP": "Eiweiß – Bestandteil der körpereigenen Abwehr.",
    "Calcium (ionisiert)": "Mineralstoff – wichtig für Zellen, Muskeln und Knochen.",
    "Chlorid": "Elektrolyt – unterstützt den Säure-Basen-Haushalt.",
    "Fibrinogen": "Eiweiß – spielt eine Rolle bei der Blutgerinnung.",
    "Glukose (nüchtern)": "Zuckerwert im Blut – wird nüchtern gemessen.",
    "Hämoglobin (Frauen)": "Blutfarbstoff bei Frauen – relevant für den Sauerstofftransport.",
    "Hämoglobin (Männer)": "Blutfarbstoff, der Sauerstoff im Blut transportiert.",
    "Hämatokrit (Frauen)": "Anteil der festen Bestandteile bei Frauen.",
    "Hämatokrit (Männer)": "Anteil der festen Bestandteile bei Männern.",
    "Harnstoff (BUN)": "Stoff, der beim Abbau von Eiweiß entsteht.",
    "HCO₃⁻": "Bikarbonat – ein Puffersystem im Blut.",
    "INR": "Maß für die Blutgerinnung.",
    "Kalium": "Elektrolyt – beteiligt an der Reizweiterleitung und Muskelfunktion.",
    "Kreatinin": "Stoffwechselprodukt – entsteht in der Muskulatur.",
    "Laktat": "Produkt des Stoffwechsels – bildet sich bei Aktivität.",
    "Leukozyten": "Weiße Blutkörperchen – Bestandteil des Immunsystems.",
    "Magnesium": "Mineralstoff – unterstützt Nerven und Enzymprozesse.",
    "Natrium": "Elektrolyt – wichtig für Flüssigkeitshaushalt und Zellfunktion.",
    "pCO₂": "Kohlendioxid-Gehalt im Blut.",
    "pH (arteriell)": "Maß für den Säuregrad des Blutes.",
    "Procalcitonin": "Eiweiß – Bestandteil regulativer Vorgänge im Körper.",
    "PTT (APTT)": "Zeit, die das Blut benötigt, um zu gerinnen.",
    "Thrombozyten": "Blutplättchen – beteiligt an der Blutgerinnung.",
    "Troponin T/I": "Eiweiß – Bestandteil der Muskulatur."
}

df_info = pd.DataFrame(labor_erklärungen.items(), columns=["Begriff", "Erklärung"])
st.subheader("Begriffserklärungen")
st.dataframe(df_info, use_container_width=True)

# === Referenzwerte-Tabelle
st.markdown("### Referenzwerte (Beispielwerte)")

referenzwerte = {
    "Hämoglobin (Männer)": "13.5 – 17.5 g/dl",
    "Hämoglobin (Frauen)": "12.0 – 16.0 g/dl",
    "Hämatokrit (Männer)": "40 – 50 %",
    "Hämatokrit (Frauen)": "36 – 46 %",
    "Leukozyten": "4000 – 10000 /µl",
    "Thrombozyten": "150000 – 400000 /µl",
    "Natrium": "135 – 145 mmol/l",
    "Kalium": "3.5 – 5.0 mmol/l",
    "Chlorid": "98 – 106 mmol/l",
    "Calcium (ionisiert)": "1.15 – 1.30 mmol/l",
    "Magnesium": "0.7 – 1.0 mmol/l",
    "Glukose (nüchtern)": "70 – 100 mg/dl",
    "Kreatinin": "0.6 – 1.2 mg/dl",
    "Harnstoff (BUN)": "7 – 20 mg/dl",
    "Laktat": "0 – 1.5 mmol/l",
    "Troponin T/I": "0 – 0.04 ng/ml",
    "CRP": "0 – 5 mg/l",
    "Procalcitonin": "0 – 0.5 ng/ml",
    "INR": "0.8 – 1.2",
    "PTT (APTT)": "25 – 35 s",
    "Fibrinogen": "200 – 400 mg/dl",
    "pH (arteriell)": "7.35 – 7.45",
    "pCO₂": "35 – 45 mmHg",
    "HCO₃⁻": "22 – 26 mmol/l",
    "Base Excess": "-2 – 2 mmol/l",
    "Anionenlücke": "8 – 16 mmol/l",
    "Albumin": "3.5 – 5.0 g/dl",
    "Bilirubin (gesamt)": "0.1 – 1.2 mg/dl"
}

df_ref = pd.DataFrame(referenzwerte.items(), columns=["Laborwert", "Referenzbereich"])
st.dataframe(df_ref, use_container_width=True)