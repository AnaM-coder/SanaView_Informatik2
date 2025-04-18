import streamlit as st
import pandas as pd

st.set_page_config(page_title="Laborwerte", layout="centered")

st.title("🧪 Laborwerte eingeben")

# Beispielhafte Felder
wert = st.text_input("Laborwert")
kommentar = st.text_area("Kommentar")

if "labor_tabelle" not in st.session_state:
    st.session_state.labor_tabelle = pd.DataFrame(columns=["Wert", "Kommentar"])

if st.button("➕ Wert hinzufügen"):
    neue_zeile = {"Wert": wert, "Kommentar": kommentar}
    st.session_state.labor_tabelle = pd.concat(
        [st.session_state.labor_tabelle, pd.DataFrame([neue_zeile])],
        ignore_index=True
    )
    st.success("✅ Wert erfolgreich hinzugefügt!")

# Zeige Tabelle
st.markdown("---")
st.subheader("📁 Ihre bisherigen Einträge")
st.dataframe(st.session_state.labor_tabelle)
