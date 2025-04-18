import streamlit as st

def show_laborwerte():
    st.title("📊 Laborwerte")
    st.subheader("Blutzuckerwert eingeben")

    datum = st.date_input("Datum")
    wert = st.number_input("Wert (mg/dL)", min_value=0)
    kommentar = st.text_input("Kommentar")

    if "labor_tabelle" not in st.session_state:
        st.session_state.labor_tabelle = []

    if st.button("➕ Wert speichern"):
        st.session_state.labor_tabelle.append({
            "Datum": datum,
            "Wert": wert,
            "Kommentar": kommentar
        })
        st.success("✅ Wert erfolgreich gespeichert!")

    if st.session_state.labor_tabelle:
        st.markdown("---")
        st.subheader("📁 Ihre bisherigen Einträge")
        st.dataframe(st.session_state.labor_tabelle)

# automatisch starten bei Aufruf
show_laborwerte()
