import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import urllib.parse

# --- CONFIGURATION ET STYLE ---
st.set_page_config(page_title="YAMB - Abeilles du Sénégal", layout="centered")

st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #1B5E20 0%, #051A07 100%);
        color: #FFC107;
        padding: 20px;
        border-radius: 0 0 30px 30px;
        text-align: center;
        border-bottom: 4px solid #FF8F00;
        margin-bottom: 20px;
    }
    .whatsapp-btn {
        background-color: #25D366;
        color: white !important;
        padding: 15px;
        border-radius: 10px;
        text-decoration: none;
        display: block;
        text-align: center;
        font-weight: bold;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-header'><h1>🐝 YAMB</h1><p>UNITÉ D'ÉLITE APICOLE</p></div>", unsafe_allow_html=True)

# --- NAVIGATION ---
tabs = st.tabs(["📊 IA & Flore", "📸 Photo", "🚨 SOS WhatsApp", "📍 Carte"])

with tabs[0]:
    st.subheader("🤖 Estimation IA")
    nb = st.number_input("Nombre de ruches :", min_value=1, value=10)
    st.info(f"Rendement moyen estimé : {nb * 12} kg de miel.")

with tabs[1]:
    st.subheader("📸 Photo Terrain")
    st.camera_input("Prendre une photo de contrôle")

with tabs[2]:
    st.subheader("🚨 Alerte Urgence")
    danger = st.selectbox("Nature du danger :", ["Incendie 🔥", "Vol 🥷", "Maladie 🐝"])
    
    # Message WhatsApp
    msg = f"ALERTE SOS YAMB : {danger} détecté sur le rucher."
    encoded_msg = urllib.parse.quote(msg)
    whatsapp_url = f"https://wa.me/?text={encoded_msg}"
    
    st.markdown(f'<a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">🟢 ENVOYER SUR WHATSAPP</a>', unsafe_allow_html=True)

with tabs[3]:
    st.subheader("📍 Géolocalisation")
    loc = get_geolocation()
    if loc:
        lat = loc['coords']['latitude']
        lon = loc['coords']['longitude']
        m = folium.Map(location=[lat, lon], zoom_start=15)
        folium.Marker([lat, lon], tooltip="Votre position").add_to(m)
        st_folium(m, width="100%", height=300)
    else:
        st.warning("📡 Recherche du signal GPS... (Vérifiez vos permissions)")

st.divider()
st.caption("YAMB v1.1 - Abeilles du Sénégal")
