import streamlit as st
import pandas as pd
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# === Seitenlayout ===
st.set_page_config(page_title="Info-Seite", layout="wide")

# === Login initialisieren & prüfen ===
login_manager = LoginManager(data_manager=DataManager())

if not st.session_state.get("authentication_status", False):
    st.warning("⚠️ Kein Benutzer eingeloggt! Anmeldung erforderlich.")
    st.stop()

# === Logout-Button nur in der Sidebar ===
with st.sidebar:
    login_manager.authenticator.logout("Logout", key="logout_sidebar")

# === Titel & Einleitung ===
st.title("Infoseite")
st.markdown("""
Hier finden Sie Erklärungen und die Referenzwerte zu Ihren Laborwerten.
""")


import streamlit as st
import pandas as pd

# === Laborwerte mit neuen Erklärungen ===
labor_erklärungen = {
    "Albumin": "Ein wichtiges Eiweiss im Blut, das hilft, die Flüssigkeit im Gleichgewicht zu halten.",
    "Anionenlücke": "Eine Rechengrösse, die zeigt, ob bestimmte Salze im Blut im Gleichgewicht sind.",
    "Base Excess": "Zeigt, ob das Blut zu viele oder zu wenige Basen (alkalische Stoffe) enthält.",
    "Bilirubin (gesamt)": "Ein Abfallprodukt, das entsteht, wenn alte rote Blutkörperchen abgebaut werden.",
    "CRP": "Ein Eiweiss, das ansteigt, wenn im Körper eine Entzündung vorliegt.",
    "Calcium (ionisiert)": "Ein Mineral, das für Knochen, Muskeln und Zellen wichtig ist.",
    "Chlorid": "Ein Salz im Blut, das hilft, den Säure-Basen-Haushalt zu steuern.",
    "Fibrinogen": "Ein Eiweiss, das wichtig für die Blutgerinnung ist.",
    "Glukose (nüchtern)": "Der Blutzuckerwert – wird gemessen, wenn man nichts gegessen hat.",
    "Hämoglobin (Frauen)": "Der Farbstoff in roten Blutkörperchen bei Frauen, der Sauerstoff transportiert.",
    "Hämoglobin (Männer)": "Der Farbstoff im Blut von Männern, der Sauerstoff durch den Körper bringt.",
    "Hämatokrit (Frauen)": "Zeigt, wie viel Anteil feste Bestandteile (wie Blutzellen) im Blut bei Frauen haben.",
    "Hämatokrit (Männer)": "Der Anteil fester Bestandteile im Blut bei Männern.",
    "Harnstoff (BUN)": "Ein Stoff, der entsteht, wenn der Körper Eiweiss abbaut.",
    "HCO₃⁻": "Ein Stoff, der hilft, den Säuregehalt im Blut auszugleichen.",
    "INR": "Ein Wert, der zeigt, wie schnell das Blut gerinnt.",
    "Kalium": "Ein Salz, das für Muskeln und Nerven wichtig ist.",
    "Kreatinin": "Ein Abfallprodukt aus den Muskeln – zeigt, wie gut die Nieren arbeiten.",
    "Laktat": "Ein Stoff, der bei körperlicher Anstrengung entsteht.",
    "Leukozyten": "Weisse Blutkörperchen – sie helfen bei der Abwehr von Krankheiten.",
    "Magnesium": "Ein Mineral, das Nerven und viele Körperfunktionen unterstützt.",
    "Natrium": "Ein wichtiges Salz, das den Wasserhaushalt im Körper reguliert.",
    "pCO₂": "Zeigt, wie viel Kohlendioxid im Blut vorhanden ist.",
    "pH (arteriell)": "Misst, ob das Blut eher sauer oder basisch ist.",
    "Procalcitonin": "Ein Eiweiss, das bei bestimmten Infektionen im Körper ansteigt.",
    "PTT (APTT)": "Gibt an, wie lange das Blut braucht, um zu gerinnen.",
    "Thrombozyten": "Blutplättchen – sie helfen, Wunden zu verschließen und Blutungen zu stoppen.",
    "Troponin T/I": "Ein Eiweiss aus den Muskeln – zeigt mögliche Schäden am Herzmuskel an."
}

df_info = pd.DataFrame(labor_erklärungen.items(), columns=["Begriff", "Erklärung"])
st.subheader("Begriffserklärungen")
st.dataframe(df_info, use_container_width=True)

# === Referenzwerte inkl. Kinder ===
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

# DataFrame aufbauen
df_ref = pd.DataFrame([
    {
        "Laborwert": k,
        "Männer": v.get("Männer", "-"),
        "Frauen": v.get("Frauen", "-"),
        "Schwanger": v.get("Schwanger", "-"),
        "Kinder": v.get("Kinder", "-")
    }
    for k, v in referenzwerte.items()
])

st.markdown("### Referenzwerte (nach Personengruppe)")
st.dataframe(df_ref, use_container_width=True)

st.markdown("---")
st.markdown("### Quellen")
st.markdown("""
Die angegebenen Referenzwerte und Erklärungen basieren auf folgenden Quellen:

- **SwissLab** – Schweizer Labornormen und Richtwerte  
- **Unilabs Schweiz** – Laborinformationsdienste für medizinisches Fachpersonal  
- **Ladr Gruppe Medizinische Labore** – Laborwerte und deren Einordnung  
- **Medizinische Lehrbücher** wie *Pschyrembel Klinisches Wörterbuch*, *Thieme Innere Medizin*  
- **Kinderärztliche Leitlinien** (z.B. [pädiatrie-online.de](https://www.paediatrie-online.de))  

*Hinweis: Die Werte und Texte dienen der Orientierung und ersetzen keine ärztliche Beratung.*
""")
