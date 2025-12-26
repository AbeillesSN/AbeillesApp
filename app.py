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

# --- 2. CHARTE GRAPHIQUE HAUTE LISIBILITÉ ---
st.markdown("""
    <style>
    /* Fond crème plus saturé pour réduire l'éblouissement */
    .stApp { background-color: #FDF5E6; }
    
    /* En-tête Bois Sombre */
    .main-header {
        background: linear-gradient(135deg, #4b2c0f 0%, #2b1808 100%);
        color: #FFC30B; padding: 25px; border-radius: 0 0 30px 30px;
        text-align: center; border-bottom: 6px solid #FFC30B;
    }

    /* FORCER LE TEXTE EN NOIR (CORRECTION LISIBILITÉ) */
    h1, h2, h3, p, span, label {
        color: #1a1a1a !important; /* Noir profond */
    }
    
    .verset-box {
        background-color: #FFF9E3;
        border-left: 8px solid #FFC30B;
        padding: 20px; margin: 20px 0;
        color: #1a1a1a !important;
        font-style: italic; font-size: 1.1em;
        border-radius: 10px; border: 1px solid #EADDCA;
    }

    /* Métriques de production et météo */
    div[data-testid="stMetricValue"] {
        color: #1a1a1a !important;
        font-size: 3rem !important;
        font-weight: 900 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #4b2c0f !important;
        font-weight: bold !important;
    }

    /* Cartes de Flore */
    .flore-card {
        background-color: #ffffff;
        border: 2px solid #FFC30B;
        padding: 15px; border-radius: 12px;
        margin-bottom: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DONNÉES FLORE NATIONALE ---
flore_nationale = [
    {"nom": "Kadd (Faidherbia)", "debut": 11, "fin": 3, "desc": "Saison sèche - Miel clair"},
    {"nom": "Anacardier (Cajou)", "debut": 12, "fin": 3, "desc": "Niayes/Sud - Très mellifère"},
    {"nom": "Manguier", "debut": 1, "fin": 3, "desc": "National - Miellée intense"},
    {"nom": "Eucalyptus", "debut": 3, "fin": 6, "desc": "Littoral - Miel ambré"},
    {"nom": "Acacia Sénégal", "debut": 8, "fin": 10, "desc": "Nord/Centre - Qualité export"},
    {"nom": "Baobab", "debut": 5, "fin": 7, "desc": "Hivernage - Pollen abondant"},
    {"nom": "Néré", "debut": 1, "fin": 4, "desc": "Est/Sud - Ressource majeure"}
]
df_flore = pd.DataFrame(flore_nationale)

# --- 4. ACCUEIL VOCAL ---
if 'init' not in st.session_state:
    verset = "De leur ventre, sort une liqueur, aux couleurs variées, dans laquelle il y a une guérison pour les gens."
    st.components.v1.html(f"<script>var m=new SpeechSynthesisUtterance('{verset}'); m.lang='fr-FR'; window.speechSynthesis.speak(m);</script>", height=0)
    st.session_state.init = True

# --- 5. INTERFACE ---
st.markdown("<div class='main-header'><div style='font-size:12px; font-weight:bold; color:#FFC30B; letter-spacing:3px;'>ABEILLES DU SÉNÉGAL</div><h1 style='margin:0; color:white;'>🐝 YAMB PRO</h1></div>", unsafe_allow_html=True)

tabs = st.tabs(["🌸 FLORE & MÉTÉO", "🍯 RÉCOLTE", "🚨 SOS"])

loc = get_geolocation()
mois_actuel = datetime.now().month

with tabs[0]:
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        
        # MÉTÉO LISIBLE
        try:
            w = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true").json()['current_weather']
            c1, c2 = st.columns(2)
            c1.metric("Température", f"{w['temperature']}°C")
            c2.metric("Vent", f"{w['windspeed']} km/h")
        except: st.write("Chargement météo...")

        st.markdown("### 🌿 Flore en floraison actuellement")
        # Filtrer la flore du mois
        fleurs = df_flore[(df_flore['debut'] <= mois_actuel) & (df_flore['fin'] >= mois_actuel)]
        
        if not fleurs.empty:
            for _, r in fleurs.iterrows():
                st.markdown(f"<div class='flore-card'><strong>{r['nom']}</strong><br><small>{r['desc']}</small></div>", unsafe_allow_html=True)
        
        # CARTE 3KM AVEC SATELLITE
        st.markdown("### 🛰️ Rayon de butinage (3 km)")
        m = folium.Map(location=[lat, lon], zoom_start=14)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        folium.Circle([lat, lon], radius=3000, color='#FFC30B', fill=True, fill_opacity=0.1).add_to(m)
        st_folium(m, width="100%", height=300)
    else:
        st.warning("⚠️ Activez le GPS pour voir la flore et la météo.")

with tabs[1]:
    st.markdown("### Estimation de la production")
    nb = st.number_input("Nombre de ruches exploitées :", 1, 1000, 10)
    st.metric("Rendement total", f"{nb * 12} kg", "Miel Bio")

with tabs[2]:
    st.markdown("### Signalement d'urgence")
    danger = st.selectbox("Nature du problème", ["Feu de brousse", "Vol de ruches", "Mortalité massive"])
    msg = urllib.parse.quote(f"🚨 ALERTE YAMB - {danger} détecté sur mon rucher.")
    st.markdown(f'<a href="https://wa.me/?text={msg}" target="_blank" style="background-color:#25D366; color:white; padding:20px; border-radius:15px; text-decoration:none; display:block; text-align:center; font-weight:bold; border: 3px solid #128C7E;">📲 ENVOYER L\'ALERTE WHATSAPP</a>', unsafe_allow_html=True)

st.markdown("<p style='text-align:center; padding-top:20px; color:#4b2c0f; font-weight:bold;'>© 2025 Abeilles du Sénégal</p>", unsafe_allow_html=True)
