import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import pandas as pd
from datetime import datetime
import requests
import urllib.parse

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="YAMB PRO - Abeilles du Sénégal", page_icon="🐝", layout="centered")

# --- 2. CHARTE GRAPHIQUE PRESTIGE (Alvéoles & Relief) ---
st.markdown("""
    <style>
    /* Fond dégradé doux "Cire d'abeille" */
    .stApp { 
        background: radial-gradient(circle, #FDF5E6 0%, #F5F5DC 100%); 
    }
    
    /* Header Royal */
    .main-header {
        background: linear-gradient(135deg, #3d1f05 0%, #1a0d02 100%);
        color: #FFC30B; 
        padding: 40px 20px; 
        border-radius: 0 0 60px 60px;
        text-align: center; 
        border-bottom: 8px solid #FFC30B;
        box-shadow: 0 15px 30px rgba(0,0,0,0.3);
        margin-bottom: 30px;
    }

    /* Boîte Verset stylisée */
    .verset-box {
        background: #ffffff;
        border-radius: 20px;
        padding: 25px;
        margin: -40px 20px 30px 20px; /* Chevauchement élégant sur le header */
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        border: 1px solid #FFC30B;
        position: relative;
        z-index: 10;
    }

    /* Style des Metrics (Chiffres) */
    div[data-testid="stMetricValue"] {
        color: #1a1a1a !important;
        font-family: 'Georgia', serif;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
    }
    
    /* Cartes Flore Mellifère avec effet relief */
    .flore-card {
        background: #ffffff;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 12px;
        border: 1px solid #EADDCA;
        box-shadow: 5px 5px 0px #FFC30B; /* Ombre décalée style moderne */
    }

    /* Onglets personnalisés */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent;
        gap: 15px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        border: 1px solid #EADDCA;
        color: #3d1f05 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFC30B !important;
        border: 1px solid #FFC30B !important;
    }

    /* Bouton SOS */
    .sos-btn {
        background: linear-gradient(90deg, #25D366 0%, #128C7E 100%);
        color: white !important;
        padding: 20px;
        border-radius: 50px;
        text-align: center;
        text-decoration: none;
        display: block;
        font-weight: bold;
        font-size: 1.2em;
        box-shadow: 0 10px 20px rgba(37, 211, 102, 0.3);
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ACCUEIL ET VERSET ---
st.markdown("""
    <div class='main-header'>
        <p style='font-size:14px; font-weight:bold; color:#FFC30B; letter-spacing:5px; margin-bottom:5px;'>ABEILLES DU SÉNÉGAL</p>
        <h1 style='margin:0; color:white; font-size:50px;'>🐝 YAMB PRO</h1>
        <p style='color:#F5F5DC; font-style:italic; opacity:0.8;'>L'excellence de la ruche sénégalaise</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class='verset-box'>
        <p style='color:#1a1a1a; font-size:1.1em; line-height:1.6; text-align:center; margin:0;'>
        "De leur ventre, sort une liqueur, aux couleurs variées, dans laquelle il y a une guérison pour les gens."
        </p>
        <p style='text-align:right; color:#8B4513; font-weight:bold; margin-top:10px; margin-bottom:0;'>
        — Sourate An-Nahl, V. 69
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- 4. NAVIGATION ---
tabs = st.tabs(["📊 ANALYSE TERRAIN", "🍯 PRODUCTION", "🚨 SOS"])

loc = get_geolocation()
mois_actuel = datetime.now().month

with tabs[0]:
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        
        # Météo
        try:
            w = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true").json()['current_weather']
            c1, c2 = st.columns(2)
            c1.metric("TEMPÉRATURE", f"{w['temperature']}°C")
            c2.metric("VENT", f"{w['windspeed']} km/h")
        except: pass

        st.markdown("### 🌸 Floraisons du moment")
        # Base de données simplifiée pour l'exemple
        fleurs = [
            {"nom": "Kadd", "desc": "Floraison intense - Miel de brousse"},
            {"nom": "Anacardier", "desc": "Nectar abondant - Miellée en cours"}
        ]
        for f in fleurs:
            st.markdown(f"<div class='flore-card'><strong>{f['nom']}</strong><br><small style='color:#5D2E0A;'>{f['desc']}</small></div>", unsafe_allow_html=True)
        
        # Carte
        m = folium.Map(location=[lat, lon], zoom_start=14)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        folium.Circle([lat, lon], radius=3000, color='#FFC30B', fill=True, fill_opacity=0.15).add_to(m)
        st_folium(m, width="100%", height=300)
    else:
        st.warning("📍 Veuillez autoriser la localisation pour activer l'analyse 360°.")

with tabs[1]:
    st.markdown("### 🍯 Calculateur de récolte")
    nb_ruches = st.slider("Nombre de ruches", 1, 100, 10)
    recolte = nb_ruches * 12
    st.metric("PRODUCTION ESTIMÉE", f"{recolte} KG")
    st.info("💡 Basé sur le rendement moyen des colonies d'Abeilles du Sénégal.")

with tabs[2]:
    st.markdown("### 🚨 Centre d'alerte")
    st.write("En cas d'incident grave sur le rucher, prévenez immédiatement le siège.")
    msg = urllib.parse.quote("🚨 URGENCE YAMB : Intervention nécessaire sur mon rucher.")
    st.markdown(f'<a href="https://wa.me/?text={msg}" target="_blank" class="sos-btn">🟢 CONTACTER L\'UNITÉ D\'ÉLITE</a>', unsafe_allow_html=True)

st.markdown("<p style='text-align:center; padding:40px 0; color:#8B4513; font-size:0.9em;'>© 2025 Abeilles du Sénégal • Fait avec passion</p>", unsafe_allow_html=True)
