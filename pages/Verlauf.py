import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# === Login-Schutz ===
LoginManager().go_to_login("Start.py")

# === DataManager initialisieren ===
data_manager = DataManager()

# === Session-Key & Datei laden ===
session_key = "laborwerte"
username = st.session_state.get("username")
file_name = f"{username}_daten.csv"
data_manager.load_user_data(session_state_key=session_key, file_name=file_name)

df = st.session_state[session_key]

# === Seite Titel ===
st.title("📈 Verlauf")

# === Wenn Daten vorhanden sind ===
if not df.empty:
    # Vorbereitung der Daten
    df["Datum"] = pd.to_datetime(df["Datum"], format="%d.%m.%Y")
    df = df.sort_values("Datum", ascending=True)

    # Auswahl des Laborwertes
    ausgewählter_wert = st.selectbox("Laborwert auswählen", df["Laborwert"].unique())
    daten = df[df["Laborwert"] == ausgewählter_wert].copy()

    # Referenzbereich extrahieren
    ref_min, ref_max = map(float, daten["Referenz"].iloc[0].split("–"))

    # Ampelfarben zuweisen
    def get_ampelfarbe(wert):
        if wert < ref_min:
            return "gelb"
        elif wert > ref_max:
            return "rot"
        return "grün"

    daten["Farbe"] = daten["Wert"].apply(get_ampelfarbe)

    # === Diagramm-Funktion ===
    def zeichne_liniendiagramm(data, title, farbe="gray"):
        fig, ax = plt.subplots()
        ax.plot(data["Datum"], data["Wert"], marker="o", color=farbe)
        ax.set_title(title)
        ax.set_xlabel("Datum")
        ax.set_ylabel("Wert")
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True)
        return fig

    # === Layout für 4 Diagramme ===
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    col1.pyplot(zeichne_liniendiagramm(daten, "Alle Werte", farbe="black"))
    col2.pyplot(zeichne_liniendiagramm(daten[daten["Farbe"] == "grün"], "Normalbereich (🟢)", farbe="green"))
    col3.pyplot(zeichne_liniendiagramm(daten[daten["Farbe"] == "gelb"], "Leicht außerhalb (🟡)", farbe="gold"))
    col4.pyplot(zeichne_liniendiagramm(daten[daten["Farbe"] == "rot"], "Stark abweichend (🔴)", farbe="red"))

    # === Legende ===
    st.markdown("---")
    st.markdown("### 🟢🟡🔴 Ampelfarb-Legende")
    st.markdown("""
    - 🟢 Normalbereich  
    - 🟡 Leicht außerhalb  
    - 🔴 Stark abweichend  
    """)
else:
    st.info("Noch keine Laborwerte vorhanden. Bitte zuerst Werte eingeben.")
