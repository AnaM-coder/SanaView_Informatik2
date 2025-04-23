import streamlit as st
import pandas as pd
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# === Login-Schutz ===
LoginManager().go_to_login("Start.py")

# === DataManager initialisieren ===
data_manager = DataManager()

# === Daten laden
username = st.session_state.get("username")
session_key = "laborwerte"
file_name = f"{username}_daten.csv"

data_manager.load_user_data(
    session_state_key=session_key,
    file_name=file_name
)

df = st.session_state[session_key]

st.title("📈 Verlauf Ihrer Laborwerte")

# === Auswahl
if not df.empty:
    df["Datum"] = pd.to_datetime(df["Datum"], format="%d.%m.%Y")
    ausgewählter_wert = st.selectbox("Laborwert auswählen", df["Laborwert"].unique())

    daten = df[df["Laborwert"] == ausgewählter_wert].sort_values("Datum")

    # === Referenzbereiche berechnen
    import re
    ref_clean = re.sub(r"[–—−]", "-", daten["Referenz"].iloc[0])
    ref_min, ref_max = map(float, ref_clean.split("-"))

    # Farben zuordnen
    def ampel_farbe(w):
        if w < ref_min:
            return "🟡"
        elif w > ref_max:
            return "🔴"
        else:
            return "🟢"

    daten["Ampel"] = daten["Wert"].apply(ampel_farbe)

    # In Gruppen teilen
    grün = daten[daten["Ampel"] == "🟢"]
    gelb = daten[daten["Ampel"] == "🟡"]
    rot = daten[daten["Ampel"] == "🔴"]

    # === 4 Diagramme nebeneinander ===
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    col1.subheader("Alle Werte")
    col1.line_chart(daten.set_index("Datum")["Wert"])

    col2.subheader("🟢 Normalbereich")
    if not grün.empty:
        col2.line_chart(grün.set_index("Datum")["Wert"])
    else:
        col2.info("Keine Werte im Normalbereich.")

    col3.subheader("🟡 Leicht außerhalb")
    if not gelb.empty:
        col3.line_chart(gelb.set_index("Datum")["Wert"])
    else:
        col3.info("Keine leicht abweichenden Werte.")

    col4.subheader("🔴 Stark abweichend")
    if not rot.empty:
        col4.line_chart(rot.set_index("Datum")["Wert"])
    else:
        col4.info("Keine stark abweichenden Werte.")

    st.markdown("---")
    st.markdown("### Ampelfarb-Legende")
    st.markdown("""
    - 🟢 Normalbereich  
    - 🟡 Leicht außerhalb  
    - 🔴 Stark abweichend  
    """)

else:
    st.info("Noch keine Laborwerte vorhanden.")
