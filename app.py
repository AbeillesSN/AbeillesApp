import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import urllib.parse
from datetime import datetime

# --- 1. CONFIGURATION ÉLITE ---
st.set_page_config(
    page_title="YAMB - Abeilles du Sénégal",
    page_icon="🐝",
    layout="centered"
)

# --- 2. CHARTE GRAPHIQUE "ABEILLES DU SÉNÉGAL" ---
st.markdown("""
    <style>
    /* Couleurs : Vert Sénégal (#00853F), Or Miel (#FCD116), Rouge Alerte (#E31B23) */
    .stApp { background-color: #F4F7F4; }
    
    .main-header {
        background: linear-gradient(135deg, #004d26 0%, #00853f 100%);
        color: #FCD116;
        padding: 30px;
        border-radius: 0 0 50px 50px;
        text-align: center;
        border-bottom: 6px solid #FCD116;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    .company-name {
        font-size: 14px;
        letter-spacing: 2px;
        font-weight: bold;
        color: #FFFFFF;
        margin-bottom: 5px;
    }
    .whatsapp-btn {
        background-color: #25D366;
        color: white !important;
        padding: 20px;
        border-radius: 15px;
        text-decoration: none;
        display: block;
        text-align: center;
        font-weight: 900;
        font-size: 20px;
        border: 2px solid #128C7E;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #004d26;
        padding: 10px;
        border-radius: 15px;
    }
    .stTabs [data-baseweb="tab"] {
        color: white !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FONCTION AUDIO ---
def parler(texte):
    st.components.v1.html(f"""
        <script>
        var msg = new SpeechSynthesisUtterance("{texte}");
        msg.lang = 'fr-FR';
        window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

# --- 4. ENTÊTE OFFICIEL ---
st.markdown("""
    <div class='main-header'>
        <div class='company-name'>ABEILLES DU SÉNÉGAL PRÉSENTE</div>
        <h1 style='margin:0;'>🐝 YAMB</h1>
        <p style='color:white; font-style:italic;'>La technologie au service de l'apiculture</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. NAVIGATION ---
tabs = st.tabs(["🍯 RÉCOLTE", "📸 TERRAIN", "🚨 SOS"])

with tabs[0]:
    if st.button("🔊 Aide Vocale"):
        parler("Abeilles du Sénégal vous aide à calculer votre récolte. Tapez le nombre de ruches.")
    st.subheader("🤖 Calculateur de Miel")
    nb = st.number_input("Nombre de ruches exploitées :", min_value=1, value=10)
    st.metric("Potentiel de production", f"{nb * 12} kg", delta="Miel pur")

with tabs[1]:
    if st.button("🔊 Aide Photo"):
        parler("Prenez une photo pour le suivi d'Abeilles du Sénégal.")
    st.subheader("📸 Suivi Visuel")
    st.camera_input("Scanner une ruche ou une fleur")

with tabs[2]:
    if st.button("🔊 Aide Urgence"):
        parler("Urgence. Choisissez le problème et envoyez l'alerte WhatsApp à Abeilles du Sénégal.")
    st.subheader("🚨 Alerte de Sécurité")
    danger = st.selectbox("Type d'incident :", ["🔥 Feu de brousse", "🥷 Vol de ruches", "💀 Mortalité anormale"])
    
    msg = f"🚨 *URGENCE ABEILLES DU SÉNÉGAL*\n📍 Un incident de type [{danger}] est signalé sur un rucher YAMB."
    url = f"https://wa.me/?text={urllib.parse.quote(msg)}"
    st.markdown(f'<a href="{url}" target="_blank" class="whatsapp-btn">🟢 SIGNALER L\'INCIDENT</a>', unsafe_allow_html=True)

# --- 6. CARTE SATELLITE ---
st.divider()
st.markdown("### 📍 Géolocalisation du Rucher")
loc = get_geolocation()
if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    m = folium.Map(location=[lat, lon], zoom_start=16)
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
    folium.Marker([lat, lon], popup="Rucher Abeilles du Sénégal", icon=folium.Icon(color='green')).add_to(m)
    st_folium(m, width="100%", height=300)
else:
    st.warning("📡 Recherche GPS... Activez la localisation pour Abeilles du Sénégal.")

# --- 7. PIED DE PAGE ---
st.markdown("""
    <div style='text-align:center; padding:20px; color:#004d26; font-weight:bold;'>
        © 2025 Abeilles du Sénégal - Tous droits réservés
    </div>
    """, unsafe_allow_html=True)
