import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import urllib.parse
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="YAMB - Abeilles du Sénégal", layout="centered")

st.markdown("""
    <style>
    .premium-header {
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
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='premium-header'><h1>🐝 YAMB</h1><p>UNITÉ D'ÉLITE</p></div>", unsafe_allow_html=True)

# --- NAVIGATION ---
tabs = st.tabs(["📊 IA & Flore", "📸 Photo", "🚨 SOS WhatsApp"])

with tabs[0]:
    st.subheader("🤖 Estimation IA")
    nb = st.number_input("Nombre de ruches :", min_value=1, value=10)
    st.info(f"Potentiel estimé : {nb * 12} kg de miel (moyenne).")

with tabs[1]:
    st.subheader("📸 Photo Terrain")
    st.camera_input("Prendre une photo")

with tabs[2]:
    st.subheader("🚨 Alerte Urgence")
    danger = st.selectbox("Type :", ["Incendie", "Vol", "Maladie"])
    
    # Bouton WhatsApp simple
    msg = f"ALERTE YAMB: {danger} détecté sur le rucher."
    whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(msg)}"
    st.markdown(f'<a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">Envoyer Alerte WhatsApp</a>', unsafe_allow_html=True)

# --- GÉOLOCALISATION ---
st.divider()
st.subheader("📍 Localisation du Rucher")
loc = get_geolocation()

if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    m = folium.Map(location=[lat, lon], zoom_start=14)
    folium.Marker([lat, lon], icon=folium.Icon(color='red')).add_to(m)
    st_folium(m, width="100%", height=300)
else:
    st.info("Recherche de la position GPS... (Vérifiez que la localisation est activée sur votre téléphone)")
