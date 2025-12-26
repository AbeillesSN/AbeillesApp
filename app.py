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

# --- 2. CHARTE GRAPHIQUE "ULTRA-LISIBLE" ---
st.markdown("""
    <style>
    /* Fond de page plus sombre pour éviter l'éblouissement */
    .stApp { background-color: #F5F5DC; } 

    /* FORCER TOUT LE TEXTE EN NOIR PUR */
    h1, h2, h3, p, span, label, .stMarkdown, .stText {
        color: #000000 !important; 
        font-weight: 500;
    }

    /* En-tête avec texte contrasté */
    .main-header {
        background: linear-gradient(135deg, #3d1f05 0%, #1a0d02 100%);
        color: #FFC30B; padding: 25px; border-radius: 0 0 30px 30px;
        text-align: center; border-bottom: 6px solid #FFC30B;
    }

    /* Boîte Verset - Texte Noir */
    .verset-box {
        background-color: #ffffff;
        border-left: 8px solid #FFC30B;
        padding: 20px; margin: 20px 0;
        color: #000000 !important;
        font-style: italic; font-size: 1.15em;
        border-radius: 10px; border: 1px solid #dcdcdc;
    }

    /* Chiffres Production & Météo - Noir Éclatant */
    div[data-testid="stMetricValue"] {
        color: #000000 !important;
        font-size: 3.2rem !important;
        font-weight: 900 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #3d1f05 !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
    }

    /* Onglets - Amélioration du contraste */
    .stTabs [data-baseweb="tab-list"] { background-color: #e0e0e0; border-radius: 10px; }
    .stTabs [data-baseweb="tab"] { color: #000000 !important; font-weight: bold; }
    
    /* Cartes Flore Mellifère */
    .flore-card {
        background-color: #ffffff;
        border: 2px solid #8B4513;
        padding: 15px; border-radius: 12px;
        margin-bottom: 10px;
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DONNÉES FLORE MELLIFÈRE ---
flore_nationale = [
    {"nom": "Kadd (Faidherbia)", "debut": 11, "fin": 3, "desc": "Saison sèche - Miel clair et prisé"},
    {"nom": "Anacardier (Cajou)", "debut": 12, "fin": 3, "desc": "Niayes/Sud - Miellée abondante"},
    {"nom": "Manguier", "debut": 1, "fin": 3, "desc": "National - Source majeure de nectar"},
    {"nom": "Eucalyptus", "debut": 3, "fin": 6, "desc": "Littoral - Miel ambré médicinal"},
    {"nom": "Acacia Sénégal", "debut": 8, "fin": 10, "desc": "Nord/Centre - Gomme et nectar"},
    {"nom": "Baobab", "debut": 5, "fin": 7, "desc": "Hivernage - Pollen pour le couvain"},
    {"nom": "Néré", "debut": 1, "fin": 4, "desc": "Est/Sud - Très attractif"}
]
df_flore = pd.DataFrame(flore_nationale)

# --- 4. ACCUEIL ET VERSET ---
st.markdown("<div class='main-header'><div style='font-size:12px; font-weight:bold; color:#FFC30B; letter-spacing:3px;'>ABEILLES DU SÉNÉGAL</div><h1 style='margin:0; color:white;'>🐝 YAMB PRO</h1></div>", unsafe_allow_html=True)

st.markdown("""
    <div class='verset-box'>
        "De leur ventre, sort une liqueur, aux couleurs variées, dans laquelle il y a une guérison pour les gens." <br>
        <strong style='color:#3d1f05;'>— Sourate An-Nahl, Verset 69</strong>
    </div>
    """, unsafe_allow_html=True)

# --- 5. LOGIQUE MÉTIER ---
tabs = st.tabs(["🌸 FLORE & MÉTÉO", "🍯 RÉCOLTE", "🚨 SOS"])

loc = get_geolocation()
mois_actuel = datetime.now().month

with tabs[0]:
    st.markdown("## État du Butinage")
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        
        # MÉTÉO EN NOIR
        try:
            w = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true").json()['current_weather']
            col1, col2 = st.columns(2)
            col1.metric("TEMPÉRATURE", f"{w['temperature']}°C")
            col2.metric("VENT", f"{w['windspeed']} km/h")
        except: st.write("Météo indisponible")

        st.markdown("### 🌿 Plantes en fleur ce mois-ci")
        fleurs = df_flore[(df_flore['debut'] <= mois_actuel) & (df_flore['fin'] >= mois_actuel)]
        
        for _, r in fleurs.iterrows():
            st.markdown(f"<div class='flore-card'><strong>{r['nom']}</strong><br>{r['desc']}</div>", unsafe_allow_html=True)
        
        # CARTE SATELLITE
        st.markdown("### 🛰️ Rayon de 3 km")
        m = folium.Map(location=[lat, lon], zoom_start=14)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        folium.Circle([lat, lon], radius=3000, color='#FFC30B', fill=True, fill_opacity=0.2).add_to(m)
        st_folium(m, width="100%", height=300)
    else:
        st.warning("⚠️ Activez le GPS pour voir la flore autour de vos ruches.")

with tabs[1]:
    st.markdown("## Estimation de Récolte")
    nb = st.number_input("Nombre de ruches :", 1, 1000, 10)
    st.metric("TOTAL ESTIMÉ", f"{nb * 12} kg", "Miel de Qualité")

with tabs[2]:
    st.markdown("## Module d'Urgence")
    danger = st.selectbox("Type d'alerte", ["Feu de brousse", "Vol / Vandalisme", "Mortalité Abeilles"])
    msg = urllib.parse.quote(f"🚨 URGENCE ABEILLES DU SÉNÉGAL : {danger} détecté.")
    st.markdown(f'<a href="https://wa.me/?text={msg}" target="_blank" style="display:block; background:#25D366; color:white; padding:20px; text-align:center; border-radius:15px; text-decoration:none; font-weight:bold; border: 4px solid #128C7E;">📲 ENVOYER L\'ALERTE WHATSAPP</a>', unsafe_allow_html=True)

st.markdown("<p style='text-align:center; padding-top:30px; font-weight:bold; color:#000000;'>© 2025 Abeilles du Sénégal</p>", unsafe_allow_html=True)
