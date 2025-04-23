import streamlit as st

# Seitenlayout
st.set_page_config(page_title="SanaView – Hauptmenü", layout="wide")

# Haupttitel
st.markdown("##Hauptmenü")

# Willkommen mit grünem Highlight
st.markdown("""
<div style='background-color: #90ee90; padding: 10px; border-radius: 8px; width: fit-content;'>
    <h3 style='margin: 0;'>Willkommen</h3>
</div>
""", unsafe_allow_html=True)

# Einleitung
st.write("Mit **SanaView App** können Sie:")

# Checkliste
punkte = [
    "Laborwerte erfassen",
    "Verlauf grafisch anzeigen",
    "Ampelfarben",
    "Referenzwerte individuell anzeigen"
]

for punkt in punkte:
    st.markdown(f"- [ ] {punkt}")
