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

# === Seitentitel ===
st.title("Verlauf Ihrer Laborwerte")

# === Filterauswahl nur wenn Daten vorhanden ===
if not df.empty:
    col1, col2, col3 = st.columns(3)
    with col1:
        ausgewählt = st.selectbox("Laborwert", df["Laborwert"].unique())
    with col2:
        sortierung = st.selectbox("Sortierung", ["Neueste zuerst", "Älteste zuerst"])
    with col3:
        anzahl = st.selectbox("Anzahl Werte", ["Alle", "Letzte 10", "Letzte 30"])

    # === Daten filtern & sortieren ===
    daten = df[df["Laborwert"] == ausgewählt].copy()
    daten["Datum"] = pd.to_datetime(daten["Datum"], format="%d.%m.%Y")
    daten = daten.sort_values("Datum", ascending=(sortierung == "Älteste zuerst"))

    if anzahl == "Letzte 10":
        daten = daten.tail(10)
    elif anzahl == "Letzte 30":
        daten = daten.tail(30)

    # === Farben zuweisen basierend auf Ampeltext ===
    def farbe(ampel):
        if "normal" in ampel:
            return "limegreen"
        elif "niedrig" in ampel:
            return "gold"
        elif "hoch" in ampel:
            return "red"
        else:
            return "gray"

    daten["Farbe"] = daten["Ampel"].apply(farbe)

    # === Plots ===
    def linien_plot(daten):
        fig, ax = plt.subplots()
        ax.scatter(daten["Datum"], daten["Wert"], c=daten["Farbe"], s=80)
        ax.plot(daten["Datum"], daten["Wert"], alpha=0.3)
        ax.set_title("Zeitlicher Verlauf")
        ax.set_xlabel("Datum")
        ax.set_ylabel("Wert")
        ax.grid(True)
        fig.autofmt_xdate()
        return fig

    def balken_plot(daten):
        fig, ax = plt.subplots()
        ax.bar(daten["Datum"].astype(str), daten["Wert"], color=daten["Farbe"])
        ax.set_title("Balkendiagramm")
        ax.set_xlabel("Datum")
        ax.set_ylabel("Wert")
        fig.autofmt_xdate()
        return fig

    def box_plot(daten):
        fig, ax = plt.subplots()
        ax.boxplot(daten["Wert"])
        ax.set_title("Boxplot")
        return fig

    def histogramm_plot(daten):
        fig, ax = plt.subplots()
        ax.hist(daten["Wert"], bins=10, color="skyblue", edgecolor="black")
        ax.set_title("Histogramm")
        return fig

    # === Anzeigen in 2x2 Layout ===
    colA1, colA2 = st.columns(2)
    with colA1:
        st.pyplot(linien_plot(daten))
    with colA2:
        st.pyplot(balken_plot(daten))

    colB1, colB2 = st.columns(2)
    with colB1:
        st.pyplot(histogramm_plot(daten))
    with colB2:
        st.pyplot(box_plot(daten))

    # === Legende
    st.markdown("---")
    st.markdown("### Ampelfarben-Legende")
    st.markdown("""
    <div style='font-size: 18px;'>
        <span style='color: limegreen;'>🟢 Normalbereich</span><br>
        <span style='color: gold;'>🟡 Leicht außerhalb</span><br>
        <span style='color: red;'>🔴 Stark abweichend</span>
    </div>
    """, unsafe_allow_html=True)

else:
    st.info("Noch keine Laborwerte gespeichert. Bitte zuerst Daten erfassen.")
