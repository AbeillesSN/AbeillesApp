import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import pandas as pd
from datetime import datetime
import requests

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="YAMB PRO - Abeilles du Sénégal", page_icon="🐝", layout="centered")

# --- 2. STYLE "LUXE & CONTRASTE" ---
st.markdown("""
    <style>
    .stApp { background-color: #FDF5E6; }
    
    /* Titres Noirs et Dorés */
    h1, h2, h3 { color: #000000 !important; font-family: 'Playfair Display', serif; }
    p, span, label { color: #1a1a1a !important; font-weight: 500; }

    /* Header Signature */
    .main-header {
        background: linear-gradient(135deg, #3d1f05 0%, #1a0d02 100%);
        padding: 40px 20px; border-radius: 0 0 50px 50px;
        text-align: center; border-bottom: 8px solid #FFC30B;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }

    /* Cartes de Flore Riches */
    .flore-card {
        background: #ffffff;
        border-radius: 20px; padding: 20px;
        margin-bottom: 20px; border-left: 10px solid #FFC30B;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Indicateur de Saison */
    .season-tag {
        background: #FFC30B; color: #000000;
        padding: 5px 15px; border-radius: 50px;
        font-weight: bold; font-size: 0.8em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DONNÉES RICHE : LA FLORE DU SÉNÉGAL ---
# Données basées sur les cycles soudano-sahéliens
flore_db = [
    {"espèce": "Kadd (Faidherbia albida)", "type": "Arbre", "mois": [11, 12, 1, 2, 3], "miel": "Clair, très doux", "zone": "National"},
    {"espèce": "Anacardier (Pomme Cajou)", "type": "Arbre fruitier", "mois": [12, 1, 2, 3], "miel": "Ambré, fruité", "zone": "Casamance / Niayes"},
    {"espèce": "Acacia Sénégal (Gommier)", "type": "Arbre", "mois": [8, 9, 10], "miel": "Prestigieux, rare", "zone": "Zone Sylvopastorale"},
    {"espèce": "Manguier", "type": "Arbre fruitier", "mois": [1, 2, 3], "miel": "Dense, floral", "zone": "Littoral / Sud"},
    {"espèce": "Eucalyptus", "type": "Arbre", "mois": [3, 4, 5, 6], "miel": "Mentholé, médicinal", "zone": "Niayes"},
    {"espèce": "Baobab", "type": "Arbre", "mois": [5, 6, 7], "miel": "Pollen riche", "zone": "National"},
    {"espèce": "Néré (Parkia biglobosa)", "type": "Arbre", "mois": [1, 2, 3, 4], "miel": "Sombre, puissant", "zone": "Sud / Est"}
]

# --- 4. HEADER & VERSET ---
st.markdown("""
    <div class='main-header'>
        <h1 style='color: white !important; margin:0; font-size: 45px;'>🐝 YAMB PRO</h1>
        <p style='color: #FFC30B !important; letter-spacing: 3px; font-weight: bold;'>ABEILLES DU SÉNÉGAL</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- 5. NAVIGATION ---
tabs = st.tabs(["📊 TERRAIN & FLORE", "🍯 PRODUCTION", "🚨 SOS"])

loc = get_geolocation()
mois_actuel = datetime.now().month

with tabs[0]:
    st.header("🔍 Analyse du Rayon de 3 km")
    
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        
        # BLOC MÉTÉO RICHE
        try:
            w_res = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true").json()['current_weather']
            col1, col2, col3 = st.columns(3)
            col1.metric("TEMPÉRATURE", f"{w_res['temperature']}°C")
            col2.metric("VENT", f"{w_res['windspeed']} km/h")
            col3.metric("CONDITION", "Optimale" if w_res['windspeed'] < 20 else "Difficile")
        except: pass

        st.divider()

        # BLOC FLORE RICHE
        st.subheader("🌸 Calendrier de Floraison Actuel")
        fleurs_actives = [f for f in flore_db if mois_actuel in f['mois']]
        
        for f in fleurs_actives:
            st.markdown(f"""
                <div class='flore-card'>
                    <span class='season-tag'>{f['type']}</span>
                    <h3 style='margin: 10px 0 5px 0;'>{f['espèce']}</h3>
                    <p style='margin:0;'>🎯 <b>Zone:</b> {f['zone']}</p>
                    <p style='margin:0;'>🍯 <b>Miel attendu:</b> {f['miel']}</p>
                </div>
            """, unsafe_allow_html=True)

        # CARTE SATELLITE
        st.subheader("🛰️ Vue Satellite & Zone de Vol")
        m = folium.Map(location=[lat, lon], zoom_start=14)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        folium.Circle([lat, lon], radius=3000, color='#FFC30B', fill=True, fill_opacity=0.1).add_to(m)
        st_folium(m, width="100%", height=400)
    else:
        st.info("📍 Activez le GPS pour charger les données de votre zone.")

with tabs[1]:
    st.header("🍯 Gestion de la Récolte")
    nb = st.slider("Nombre de ruches en production", 1, 100, 10)
    st.metric("Potentiel de Récolte", f"{nb * 12} kg", "Miel Bio Sénégal")
    
    st.markdown("""
        ### 📋 Conseils de saison
        * Vérifiez l'espace dans les hausses (Floraison du Kadd en cours).
        * Assurez un point d'eau propre à moins de 500m.
    """)

with tabs[2]:
    st.header("🚨 Assistance d'Urgence")
    st.markdown('<a href="https://wa.me/" class="sos-btn" style="display:block; background:#25D366; color:white; padding:20px; text-align:center; border-radius:15px; text-decoration:none; font-weight:bold;">📲 CONTACTER L\'UNITÉ D\'ÉLITE</a>', unsafe_allow_html=True)

st.markdown("<p style='text-align:center; padding:40px; color:#3d1f05;'>© 2025 Abeilles du Sénégal - Expertises Nationales</p>", unsafe_allow_html=True)
