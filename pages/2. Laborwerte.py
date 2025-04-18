import streamlit as st
import pandas as pd

st.set_page_config(page_title="Laborwerte", layout="centered")

st.title("📊 Laborwerte eingeben, ansehen & verwalten")

if "labor_tabelle" not in st.session_state:
    st.session_state.labor_tabelle = pd.DataFrame(columns=["Wert", "Kommentar"])

wert = st.text_input("Wert")
kommentar = st.text_input("Kommentar")

if st.button("💾 Speichern"):
    new_entry = {"Wert": wert, "Kommentar": kommentar}
    st.session_state.labor_tabelle = pd.concat(
        [st.session_state.labor_tabelle, pd.DataFrame([new_entry])],
        ignore_index=True
    )
    st.success("✅ Wert erfolgreich gespeichert!")

st.markdown("---")
st.subheader("📁 Ihre bisherigen Einträge")

if not st.session_state.labor_tabelle.empty:
    st.dataframe(st.session_state.labor_tabelle)
else:
    st.info("Noch keine Werte gespeichert.")
