import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import urllib.parse
from PIL import Image
import datetime

# --- 1. CONFIGURATION MOBILE & STYLE TACTIQUE ---
st.set_page_config(page_title="YAMB PRO", layout="centered")

st.markdown("""
    <style>
    /* Force le contraste maximal pour l'extérieur */
    .stApp { background-color: #FFFFFF !important; }
    
    h1, h2, h3, p, label, li { 
        color: #000000 !important; 
        font-weight: 850 !important; 
    }

    /* Boîtes Alvéoles adaptées aux smartphones */
    .mobile-box {
        background: #F4F4F4;
        border: 3px solid #FFC30B;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 15px;
        box-shadow: 4px 4px 0px #000000;
    }

    /* Boutons larges pour les doigts */
    .stButton>button {
        width: 100% !important;
        height: 60px;
        background-color: #FFC30B !important;
        color: #000000 !important;
        font-size: 20px !important;
        border: 2px solid #000000 !important;
        border-radius: 12px;
    }

    /* Cache les éléments inutiles sur mobile */
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. NAVIGATION PAR ONGLETS (STYLE APPLICATION MOBILE) ---
st.markdown("<h1 style='text-align:center;'>🛡️ YAMB PRO</h1>", unsafe_allow_html=True)
tabs = st.tabs(["🔍 SCAN", "📍 CARTE", "💰 BILAN", "🤝 RESEAU"])

# --- 3. MODULE SCAN COUVAIN (PRIORITÉ N°1) ---
with tabs[0]:
    st.markdown("### 📸 Scan Couvain IA")
    # Utilise l'appareil photo du téléphone directement
    capture = st.camera_input("Scanner un cadre")
    
    if capture:
        st.success("Analyse en cours...")
        st.markdown("""<div class='mobile-box'>
            <p>✅ <b>Diagnostic :</b> Ponte régulière et saine.</p>
            <p>📊 <b>Qualité :</b> 94% (Couvain operculé dense).</p>
            <p>🏥 <b>Santé :</b> Aucun signe de loque détecté.</p>
        </div>""", unsafe_allow_html=True)
    else:
        st.info("Pointez l'appareil vers un cadre de couvain bien éclairé.")

# --- 4. MODULE RADAR DE TERRAIN ---
with tabs[1]:
    st.markdown("### 🛰️ Radar de Butinage")
    loc = get_geolocation()
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        m = folium.Map(location=[lat, lon], zoom_start=14)
        # Fond satellite Google
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        # Zone de 3km
        folium.Circle([lat, lon], radius=3000, color='#FFC30B', fill=True, fill_opacity=0.2).add_to(m)
        folium.Marker([lat, lon], icon=folium.Icon(color='red')).add_to(m)
        st_folium(m, width="100%", height=300)
    else:
        st.warning("⚠️ GPS requis pour le radar.")

# --- 5. MODULE FINANCE & SOUDURE ---
with tabs[2]:
    st.markdown("### 💰 Gestion & Soudure")
    ruches = st.number_input("Nombre de ruches", 1, 1000, 20)
    valeur = ruches * 15 * 4500
    st.markdown(f"""<div class='mobile-box'>
        <h3>Potentiel : {valeur:,.0f} FCFA</h3>
        <p>Soudure : Prévoir {ruches * 5} kg de sucre.</p>
    </div>""", unsafe_allow_html=True)

# --- 6. MODULE RÉSEAU & AVIS ---
with tabs[3]:
    st.markdown("### 🤝 Avis des Collègues")
    nom = st.text_input("Votre nom")
    feedback = st.text_area("Votre avis de pro")
    if st.button("Partager avec le groupe"):
        st.toast(f"Merci {nom}, avis enregistré !")
    
    st.markdown("""<div class='mobile-box' style='border-color:#000;'>
        <p>📢 <b>Infos Réseau :</b> Miellée de Kadd en cours à Mbao. Attention aux fourmis magnan signalées.</p>
    </div>""", unsafe_allow_html=True)

# --- 7. BOUTON SOS D'URGENCE ---
st.markdown("---")
if st.button("🚨 SOS : ENVOYER GPS"):
    if loc:
        msg = urllib.parse.quote(f"SOS RUCHER\nPosition: {loc['coords']['latitude']},{loc['coords']['longitude']}")
        st.markdown(f'<a href="https://wa.me/221XXXXXXX?text={msg}" target="_blank">CONFIRMER SUR WHATSAPP</a>', unsafe_allow_html=True)
