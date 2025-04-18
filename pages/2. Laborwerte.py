import streamlit as st

def show_labor():
    st.title("📊 Laborwerte")
    st.write("Hier können Sie Ihre Blutzuckerwerte eintragen oder anschauen.")

    # Beispiel-Dataframe
    data = {
        "Datum": ["2025-04-18"],
        "Wert (mg/dL)": [120],
        "Kommentar": ["Morgens nüchtern"]
    }

    st.dataframe(data)
