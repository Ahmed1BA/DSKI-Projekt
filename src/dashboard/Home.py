import streamlit as st
from PIL import Image
import base64
import os






st.set_page_config(
    page_title="Fussball Dashboard",
    page_icon="⚽",
    layout="wide"
)




logo_path = "src/dashboard/pages/logo.png"

col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.empty()
with col2:
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
        st.image(logo, use_container_width=True)
    else:
        st.warning("Logo nicht gefunden.")
    st.markdown("<h1 style='text-align: center;'>⚽ Willkommen im Fussball Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Analyse. Vergleich. Leidenschaft.</h3>", unsafe_allow_html=True)
    
with col3:
    st.empty()

st.markdown("""
Tauche ein in die Welt des Fußballs – mit leistungsstarken Tools zur Datenanalyse, Visualisierung und Historienvergleichen.  
Dieses Dashboard hilft dir dabei, Spiele, Spieler und Taktiken besser zu verstehen und zu vergleichen.
""")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📊 Datenanzeigen")
    st.write("Erkunde Spielstatistiken, Teamleistungen und Spielerprofile.")

with col2:
    st.subheader("🎯 Possession Analyse")
    st.write("Sieh dir an, wie das nächste Duell ausgeht.")

with col3:
    st.subheader("📅  Vergleich")
    st.write("Vergleiche Teams und Spieler über verschiedene Spielzeiten hinweg.")

st.markdown("---")

st.markdown("#### 🚀 Los geht’s:")
st.markdown("""
👉 **Wähle eine Funktion in der Seitenleiste**, um mit der Analyse zu starten.  
Oder klicke direkt auf einen Bereich:
""")


col4, col5, col6 = st.columns(3)
with col4:
    if st.button("📊 Team Daten"):
        st.switch_page("pages/Team.py")
with col5:
    if st.button("🎯 Poisson Analyse"):
        st.switch_page("pages/Possession_Analyse.py")
with col6:
    if st.button("Vergleich"):
        st.switch_page("pages/Vergleich.py")

