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

# --- 2. CHARTE GRAPHIQUE "LISIBILITÉ TOTALE" ---
st.markdown("""
    <style>
    /* Fond crème */
    .stApp { background-color: #FDF5E6; }
    
    /* FORCE LE NOIR SUR TOUS LES TEXTES ET TITRES */
    h1, h2, h3, p, span, label, .stMarkdown {
        color: #000000 !important; 
        font-weight: bold !important;
    }

    /* En-tête contrasté */
    .main-header {
        background: linear-gradient(135deg, #3d1f05 0%, #1a0d02 100%);
        color: #FFC30B !important; 
        padding: 30px; 
        border-radius: 0 0 40px 40px;
        text-align: center; 
        border-bottom: 6px solid #FFC30B;
    }
    .main-header p, .main-header h1 { color: white !important; }

    /* Boîte Verset - Texte Noir Pur */
    .verset-box {
        background: #ffffff;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        border: 2px solid #FFC30B;
        color: #000000 !important;
    }

    /* Correction spécifique pour les titres de sections (Expander/Header) */
    .st-ae, .st-af, .st-ag { color: #000000 !important; }
    
    /* Bouton SOS */
    .sos-btn {
        background: #25D366;
        color: white !important;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        text-decoration: none;
        display: block;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ENTÊTE ---
st.markdown("""
    <div class='main-header'>
        <h1 style='margin:0;'>🐝 YAMB PRO</h1>
        <p style='margin:0;'>Abeilles du Sénégal</p>
    </div>
    """, unsafe_allow_html=True)

# --- 4. VERSET ---
st.markdown("""
    <div class='verset-box'>
        "De leur ventre, sort une liqueur, aux couleurs variées, dans laquelle il y a une guérison pour les gens." 
        <br><br><strong>— Sourate An-Nahl, V. 69</strong>
    </div>
    """, unsafe_allow_html=True)

# --- 5. NAVIGATION ---
tabs = st.tabs(["🌸 FLORE", "🍯 RÉCOLTE", "🚨 SOS"])

loc = get_geolocation()

with tabs[0]:
    st.header("🌸 Floraisons du moment") # Ce titre sera désormais bien NOIR
    if loc:
        st.write("Analyse du rayon de 3 km en cours...")
        # Carte satellite
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        m = folium.Map(location=[lat, lon], zoom_start=14)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        st_folium(m, width="100%", height=300)
    else:
        st.warning("Veuillez activer le GPS.")

with tabs[1]:
    st.header("🍯 Calculateur de récolte") # Ce titre sera désormais bien NOIR
    nb = st.number_input("Nombre de ruches", 1, 100, 10)
    st.metric("Total", f"{nb * 12} kg")

with tabs[2]:
    st.header("🚨 Centre d'alerte") # Ce titre sera désormais bien NOIR
    st.markdown('<a href="https://wa.me/" class="sos-btn">SIGNALER UNE URGENCE</a>', unsafe_allow_html=True)

st.markdown("<p style='text-align:center; padding:20px;'>© 2025 Abeilles du Sénégal</p>", unsafe_allow_html=True)
