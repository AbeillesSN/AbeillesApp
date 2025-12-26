import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_js_eval import get_geolocation
from streamlit_folium import st_folium
import folium

# --- CONFIGURATION ---
st.set_page_config(page_title="Yamb Connecté", layout="wide", page_icon="🐝")

# CSS CORRECTIF POUR LA LISIBILITÉ (Contraste Élevé)
st.markdown("""
    <style>
    .stApp { background-color: #fdfaf0; }
    
    /* Titres en Marron très foncé */
    h1 { color: #3e2723 !important; text-align: center; font-size: 45px !important; font-weight: bold; }
    h3 { color: #d35400 !important; text-align: center; font-weight: bold; }
    
    /* Correction du texte dans les cartes : NOIR PUR pour la lecture */
    .info-card { 
        background: #ffffff; 
        padding: 20px; 
        border-radius: 15px; 
        border: 3px solid #5d4037; 
        margin: 10px 0px; 
        text-align: center; 
        box-shadow: 4px 4px 0px #5d4037;
    }
    .icon-label { font-size: 50px; display: block; margin-bottom: 5px; }
    .text-title { font-size: 22px; font-weight: bold; color: #3e2723; text-decoration: underline; }
    .text-value { font-size: 20px; font-weight: 900; color: #000000 !important; display: block; margin-top: 10px; }
    
    /* Bouton d'aide vocale jaune vif */
    .stButton>button { 
        height: 90px; font-size: 22px !important; border-radius: 15px; 
        background-color: #f1c40f !important; color: #000000 !important; 
        border: 4px solid #3e2723; font-weight: bold;
    }
    
    /* Texte général */
    .stMarkdown, p, span { color: #000000 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- DONNÉES IA TROPICALE ---
ZONES_IA = {
    "Niayes": {"flore": "Eucalyptus, Agrumes, Maraîchage", "cal": "Janvier à Mai", "eau": "Céanes / Bassins", "feu": "Risque Faible"},
    "Casamance": {"flore": "Anacardier, Manguier, Palmier", "cal": "Mars à Juin", "eau": "Rivières / Bolongs", "feu": "Risque Moyen"},
    "Ferlo": {"flore": "Acacia Sénégal, Siddem", "cal": "Sept à Nov", "eau": "Forages / Abreuvoirs", "feu": "RISQUE TRÈS ÉLEVÉ"},
    "Bassin Arachidier": {"flore": "Baobab, Kad, Néré", "cal": "Mai à Août", "eau": "Puits profonds", "feu": "Risque Moyen"}
}

# --- EN-TÊTE ---
col_logo_1, col_logo_2, col_logo_3 = st.columns([1, 2, 1])
with col_logo_2:
    if os.path.exists("logo.png.png"):
        st.image("logo.png.png", use_container_width=True)
    st.markdown("<h1>YAMB CONNECTÉ</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#5d4037; font-size:18px;'>L'IA Apicole par Abeilles du Sénégal</p>", unsafe_allow_html=True)

if st.button("📢 CLIQUEZ ICI POUR ÉCOUTER (Aide Vocale)"):
    st.success("Lecture en cours... (Simulé)")

# --- DIAGNOSTIC ---
loc = get_geolocation()
if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    zone = "Niayes" if lon < -16.8 else "Casamance" if lat < 13.5 else "Bassin Arachidier"
    info = ZONES_IA.get(zone)

    st.markdown(f"<h2 style='text-align:center; color:white; background:#d35400; padding:10px; border-radius:10px;'>📍 ZONE : {zone.upper()}</h2>", unsafe_allow_html=True)

    # GRILLE D'INFORMATION HAUTE LISIBILITÉ
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class='info-card'>
            <span class='icon-label'>🌳</span>
            <span class='text-title'>FLORE (3km)</span>
            <span class='text-value'>{info['flore']}</span>
        </div>""", unsafe_allow_html=True)
        st.markdown(f"""<div class='info-card'>
            <span class='icon-label'>📅</span>
            <span class='text-title'>FLORAISON</span>
            <span class='text-value'>{info['cal']}</span>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class='info-card'>
            <span class='icon-label'>💧</span>
            <span class='text-title'>POINTS D'EAU</span>
            <span class='text-value'>{info['eau']}</span>
        </div>""", unsafe_allow_html=True)
        st.markdown(f"""<div class='info-card'>
            <span class='icon-label'>🔥</span>
            <span class='text-title'>ALERTE FEU</span>
            <span class='text-value'>{info['feu']}</span>
        </div>""", unsafe_allow_html=True)

    st.divider()
    
    if st.button("✅ ENREGISTRER MA POSITION MAINTENANT"):
        st.balloons()
        st.success("POSITION SAUVEGARDÉE !")
else:
    st.warning("⚠️ RECHERCHE DU GPS... MERCI DE PATIENTER AU SOLEIL.")
