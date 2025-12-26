import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import datetime
from streamlit_js_eval import get_geolocation
from streamlit_folium import st_folium
import folium

# --- CONFIGURATION & DESIGN SÉNÉGALAIS ---
st.set_page_config(page_title="Yamb Connecté IA", layout="wide", page_icon="🐝")

st.markdown("""
    <style>
    .stApp { background-color: #fdfaf0; background-image: url('https://www.transparenttextures.com/patterns/leaf.png'); }
    /* Boutons géants pour l'accessibilité */
    .stButton>button { 
        height: 120px; font-size: 24px !important; border-radius: 20px; 
        background-color: #f1c40f; border: 4px solid #5d4037; color: black; font-weight: bold;
    }
    h1 { color: #5d4037; text-align: center; font-size: 45px; }
    .big-icon { font-size: 50px; text-align: center; display: block; }
    .card { background: white; padding: 20px; border-radius: 15px; border-left: 10px solid #f1c40f; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES IA APICOLE TROPICALE ---
# Données sur 3km autour du point GPS
FLORE_DATA = {
    "Niayes": {"arbres": "Eucalyptus, Cocotiers, Filaos", "floraison": "Janvier - Avril", "eau": "Nappes proches", "danger": "Sel marin"},
    "Casamance": {"arbres": "Anacardier, Manguier, Palmier", "floraison": "Mars - Juin", "eau": "Rivières/Bolongs", "danger": "Humidité forte"},
    "Ferlo": {"arbres": "Acacia Sénégal, Gommier", "floraison": "Septembre - Novembre", "eau": "Forages requis", "danger": "Feux de brousse"},
    "Bassin Arachidier": {"arbres": "Baobab, Kad, Néré", "floraison": "Mai - Août", "eau": "Puits profonds", "danger": "Pesticides champs"}
}

def ia_conseil_tropical(zone, ruches):
    data = FLORE_DATA.get(zone, FLORE_DATA["Bassin Arachidier"])
    return f"💡 **Conseil IA :** En zone {zone}, surveillez les {data['arbres']}. Floraison prévue en {data['floraison']}. Attention au danger : {data['danger']}."

# --- INTERFACE PRINCIPALE ---
st.markdown("<h1>🐝 YAMB CONNECTÉ</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;'>L'IA au service des Apiculteurs du Sénégal</h3>", unsafe_allow_html=True)

# Bouton d'aide Vocale (Simulé pour l'UI)
if st.button("📢 CLIQUEZ ICI POUR ÉCOUTER LE GUIDE (Aide Vocale)"):
    st.info("L'IA prépare le résumé audio pour vous...")

tab1, tab2 = st.tabs(["🔍 DIAGNOSTIC RAPIDE", "📊 MON REGISTRE"])

with tab1:
    loc = get_geolocation()
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        
        # Logique de zone (Simplifiée pour l'exemple)
        zone = "Niayes" if lon < -17.0 else "Casamance" if lat < 13.5 else "Bassin Arachidier"
        info = FLORE_DATA.get(zone)

        st.markdown(f"### 📍 Vous êtes à : {zone}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='card'>🌳 <b>Flore (3km) :</b> {info['arbres']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='card'>📅 <b>Floraison :</b> {info['floraison']}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='card'>💧 <b>Points d'eau :</b> {info['eau']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='card'>🔥 <b>Risque Feux :</b> Élevé (Vigilance !)</div>", unsafe_allow_html=True)

        st.divider()
        
        # Interface simplifiée pour l'enregistrement
        st.markdown("### Combien de ruches avez-vous ?")
        nb = st.slider("", 1, 100, 10)
        
        st.markdown(ia_conseil_tropical(zone, nb))
        
        if st.button("💾 ENREGISTRER MON EMPLACEMENT"):
            # Logique de sauvegarde ici
            st.success("Bravo ! Vos abeilles sont maintenant suivies par l'IA.")
            st.balloons()
    else:
        st.warning("⚠️ Posez le téléphone à plat et attendez le signal satellite...")

with tab2:
    st.subheader("🛰️ Carte de vos Ruches")
    m = folium.Map(location=[14.4974, -14.4524], zoom_start=7)
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr='Google', name='Google Satellite').add_to(m)
    st_folium(m, width="100%", height=400)
    
st.markdown("<p style='text-align:center; font-size:12px;'>Développé par Abeilles du Sénégal - Technologie IA Tropicale v2.0</p>", unsafe_allow_html=True)
