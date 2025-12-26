import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
from datetime import datetime

# --- CONFIGURATION PRESTIGE ---
st.set_page_config(page_title="YAMB - Dark Mode Auto", layout="centered")

# --- LOGIQUE DE COULEURS DYNAMIQUES ---
# Le mode nuit s'active automatiquement selon l'heure ou les paramètres système
st.markdown("""
    <style>
    :root {
        --yamb-green: #1B5E20;
        --yamb-gold: #FFC107;
        --yamb-amber: #FF8F00;
        --bg-color: #FDFBF7;
        --card-bg: #FFFFFF;
        --text-color: #1B5E20;
    }

    @media (prefers-color-scheme: dark) {
        :root {
            --bg-color: #0E1117;
            --card-bg: #1A1C23;
            --text-color: #E0E0E0;
        }
    }

    .stApp { background-color: var(--bg-color); }
    header {visibility: hidden;}

    /* Header Adaptatif */
    .premium-header {
        background: linear-gradient(135deg, #1B5E20 0%, #051A07 100%);
        color: var(--yamb-gold);
        padding: 40px 20px;
        border-radius: 0 0 50px 50px;
        text-align: center;
        border-bottom: 5px solid var(--yamb-amber);
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }

    /* Grille Alvéolaire Adaptative */
    .alveole-card {
        background: var(--card-bg);
        border: 1px solid var(--yamb-gold);
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        color: var(--text-color);
    }
    
    .alveole-title { color: var(--yamb-gold); font-weight: 800; font-size: 12px; }

    /* Boutons YAMB */
    .stButton>button {
        background: linear-gradient(to right, #1B5E20, #2E7D32) !important;
        color: var(--yamb-gold) !important;
        border-radius: 15px !important;
        border: 1px solid var(--yamb-gold) !important;
        height: 50px;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER & LOGO ---
st.markdown("""
    <div class='premium-header'>
        <h1 style='margin:0; font-weight:900;'>YAMB</h1>
        <p style='margin:0; opacity:0.8; font-size:12px;'>ABEILLES DU SÉNÉGAL • INTELLIGENCE CONNECTÉE</p>
    </div>
    """, unsafe_allow_html=True)

loc = get_geolocation()

if loc:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- DASHBOARD HEXAGONAL ---
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""<div class='alveole-card'><span style='font-size:30px;'>🐝</span><br><span class='alveole-title'>ACTIVITÉ</span></div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""<div class='alveole-card'><span style='font-size:30px;'>🏠</span><br><span class='alveole-title'>RUCHERS</span></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class='alveole-card'><span style='font-size:30px;'>🌸</span><br><span class='alveole-title'>FLORE</span></div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""<div class='alveole-card'><span style='font-size:30px;'>🛰️</span><br><span class='alveole-title'>ZONE 5KM</span></div>""", unsafe_allow_html=True)

    # --- CARTE SATELLITE ---
    st.markdown("### 📍 Localisation Stratégique")
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    
    # Choix du style de carte selon le mode
    m = folium.Map(location=[lat, lon], zoom_start=14)
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
    
    # Zone de butinage (3km vert, 5km orange)
    folium.Circle([lat, lon], radius=3000, color='#2E7D32', fill=True, opacity=0.1).add_to(m)
    folium.Circle([lat, lon], radius=5000, color='#FF8F00', fill=False, dash_array='10').add_to(m)
    folium.Marker([lat, lon], icon=folium.Icon(color='green', icon='bolt', prefix='fa')).add_to(m)
    
    st_folium(m, width="100%", height=350)

    # --- ACTIONS ---
    st.markdown("---")
    if st.button("📊 GÉNÉRER LE RAPPORT D'EXPERTISE"):
        st.balloons()
        st.success("Expertise enregistrée sous le numéro : YAMB-2025-SN")

else:
    st.markdown("""
        <div style='text-align:center; padding:100px;'>
            <h2 style='color:#1B5E20;'>🛰️ Synchronisation...</h2>
            <p>YAMB prépare votre environnement de travail.</p>
        </div>
    """, unsafe_allow_html=True)
