import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_js_eval import get_geolocation
from streamlit_folium import st_folium
import folium

# --- CONFIGURATION ---
st.set_page_config(page_title="Yamb Connecté", layout="wide")

# CSS : DÉCOR NATURE & CONTRASTE MAXIMUM
st.markdown("""
    <style>
    /* Fond avec rappel de la nature */
    .stApp { 
        background-color: #ffffff; 
        background-image: url('https://www.transparenttextures.com/patterns/leaf.png');
    }
    
    /* Titre Géant */
    h1 { color: #2e7d32 !important; text-align: center; font-size: 65px !important; font-weight: 900; margin-bottom: 0px; }
    .sub { text-align: center; color: #5d4037; font-size: 25px; font-weight: bold; margin-bottom: 30px; }

    /* Cartes Visuelles (Flore Casamance) */
    .nature-card {
        background: #ffffff;
        border: 8px solid #2e7d32; /* Vert forêt */
        padding: 20px;
        margin: 10px;
        border-radius: 30px;
        text-align: center;
        box-shadow: 10px 10px 0px #f1c40f; /* Ombre jaune miel */
    }
    
    .label-visuel { font-size: 35px; font-weight: 900; color: #000000; display: block; }
    .emoji-geant { font-size: 70px; display: block; }

    /* BOUTON D'ACTION (Gros et Jaune) */
    .stButton>button {
        height: 150px !important;
        background-color: #f1c40f !important;
        color: #000000 !important;
        font-size: 40px !important;
        font-weight: 900 !important;
        border: 8px solid #5d4037 !important;
        border-radius: 40px !important;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.3);
    }
    
    /* Alerte Rouge pour les Feux */
    .alerte-feu {
        background-color: #ff0000;
        color: #ffffff;
        padding: 20px;
        font-size: 40px;
        text-align: center;
        font-weight: 900;
        border-radius: 20px;
        border: 5px solid #000000;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES VISUELLE ---
FLORE_CASAMANCE = {
    "Arbres": "🌳 Anacardier, Manguier, Palmier",
    "Fleurs": "🌸 Floraison : Mars à Juin",
    "Eau": "💧 Rivières et Bolongs",
    "Feu": "🔥 ATTENTION AUX FEUX"
}

# --- EN-TÊTE ---
st.markdown("<h1>🐝 YAMB CONNECTÉ</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub'>Abeilles du Sénégal - Expertise Casamance</p>", unsafe_allow_html=True)

# --- GÉOLOCALISATION ---
loc = get_geolocation()

if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    
    # Affichage Visuel des ressources
    st.markdown("<div style='background:#f1c40f; padding:10px; border-radius:15px; text-align:center; font-size:30px; font-weight:900;'>📍 VOTRE EMPLACEMENT EST PRÊT</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""<div class='nature-card'>
            <span class='emoji-geant'>🌳</span>
            <span class='label-visuel'>{FLORE_CASAMANCE['Arbres']}</span>
        </div>""", unsafe_allow_html=True)
        
        st.markdown(f"""<div class='nature-card'>
            <span class='emoji-geant'>📅</span>
            <span class='label-visuel'>{FLORE_CASAMANCE['Fleurs']}</span>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""<div class='nature-card'>
            <span class='emoji-geant'>💧</span>
            <span class='label-visuel'>{FLORE_CASAMANCE['Eau']}</span>
        </div>""", unsafe_allow_html=True)
        
        st.markdown(f"""<div class='alerte-feu'>
            {FLORE_CASAMANCE['Feu']}
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Gros bouton de validation
    if st.button("✅ ENREGISTRER"):
        st.balloons()
        st.success("C'EST FAIT ! MERCI.")
else:
    st.markdown("<h2 style='text-align:center; color:#3e2723;'>📡 RECHERCHE DU SIGNAL... Posez le téléphone à plat.</h2>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; margin-top:50px;'>🍯 Abeilles du Sénégal - Protégeons nos forêts.</p>", unsafe_allow_html=True)
