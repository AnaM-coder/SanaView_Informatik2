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
st.title("Verlauf")

# === Dropdown-Auswahl für Laborwerte und Zeiträume (wenn Daten vorhanden) ===
if not df.empty:
    col1, col2, col3 = st.columns(3)
    with col1:
        ausgewählter_wert = st.selectbox("Laborwert auswählen", df["Laborwert"].unique())
    with col2:
        zeitraum = st.selectbox("Zeitraum", ["Letzte 7", "Letzte 30", "Alle"])
    with col3:
        sortierung = st.selectbox("Sortierung", ["Neueste zuerst", "Älteste zuerst"])

    # === Filterung der Daten ===
    daten = df[df["Laborwert"] == ausgewählter_wert].copy()
    daten["Datum"] = pd.to_datetime(daten["Datum"], format="%d.%m.%Y")
    daten = daten.sort_values("Datum", ascending=(sortierung == "Älteste zuerst"))

    if zeitraum == "Letzte 7":
        daten = daten.tail(7)
    elif zeitraum == "Letzte 30":
        daten = daten.tail(30)

    # === Plots ===
    st.markdown("---")
    col_a, col_b = st.columns(2)
    col_c, col_d = st.columns(2)

    def plot_werte(ax, data, title):
        ax.plot(data["Datum"], data["Wert"], marker='o')
        ax.set_title(title)
        ax.set_ylabel("Wert")
        ax.set_xlabel("Datum")
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True)

    fig1, ax1 = plt.subplots()
    plot_werte(ax1, daten, f"{ausgewählter_wert} Verlauf")

    fig2, ax2 = plt.subplots()
    plot_werte(ax2, daten, "Zoom auf letzte Werte")

    fig3, ax3 = plt.subplots()
    ax3.hist(daten["Wert"], bins=10)
    ax3.set_title("Verteilung")

    fig4, ax4 = plt.subplots()
    ax4.boxplot(daten["Wert"])
    ax4.set_title("Boxplot")

    col_a.pyplot(fig1)
    col_b.pyplot(fig2)
    col_c.pyplot(fig3)
    col_d.pyplot(fig4)

# === Ampelfarb-Legende ===
st.markdown("---")
st.markdown("### 🟢🟡🔴 Ampelfarb-Legende")
st.markdown("""
- 🟢 Normalbereich  
- 🟡 Leicht außerhalb  
- 🔴 Stark abweichend  
""")

else:
    st.info("Noch keine Laborwerte vorhanden. Bitte zuerst Werte eingeben.")