import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_js_eval import get_geolocation

# --- CONFIGURATION FINALE ---
st.set_page_config(page_title="Yamb Connecté - Expert", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    h1 { color: #1B5E20 !important; text-align: center; font-size: 50px !important; font-weight: 900; }
    
    /* Carte d'Alerte Récolte Clignotante */
    .harvest-alert {
        background-color: #FFD600;
        border: 10px solid #000;
        padding: 25px;
        border-radius: 30px;
        text-align: center;
        animation: blinker 1.5s linear infinite;
    }
    @keyframes blinker { 50% { opacity: 0.6; } }

    .card { background: #F1F8E9; border: 4px solid #2E7D32; padding: 15px; border-radius: 20px; margin-bottom: 15px; }
    .titre { font-size: 24px; font-weight: 900; color: #1B5E20; text-decoration: underline; }
    .info { font-size: 22px; font-weight: bold; color: #000; }
    
    .stButton>button {
        height: 100px !important; background-color: #000 !important; color: #FFF !important;
        font-size: 30px !important; font-weight: 900 !important; border-radius: 30px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES IA ---
DATA_ZONE = {
    "Niayes": {
        "miels": "Eucalyptus, Maraîchage",
        "meteo": "🌡️ 24°C | 🌬️ Vent Fort",
        "recolte": "✅ PRÊT POUR RÉCOLTE (Fin de floraison Eucalyptus)",
        "flore": "Eucalyptus, Filaos, Légumes"
    },
    "Casamance": {
        "miels": "Mangrove, Anacardier, Forêt",
        "meteo": "🌡️ 31°C | 🌧️ Risque Pluie",
        "recolte": "⏳ ATTENDRE (Floraison Anacardier en cours)",
        "flore": "Fromager, Palmier, Madd"
    },
    "Bassin Arachidier": {
        "miels": "Kad, Baobab, Mil",
        "meteo": "🌡️ 36°C | ☀️ Très Sec",
        "recolte": "🔔 SURVEILLER (Début floraison Kad)",
        "flore": "Baobab, Kad, Néré"
    }
}

st.markdown("<h1>🐝 YAMB CONNECTÉ</h1>", unsafe_allow_html=True)

loc = get_geolocation()
if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    z = "Niayes" if lon < -16.8 else "Casamance" if lat < 13.5 else "Bassin Arachidier"
    d = DATA_ZONE[z]

    # --- MODULE ALERTE RÉCOLTE ---
    st.markdown(f"""
        <div class='harvest-alert'>
            <span style='font-size:40px;'>🍯</span><br>
            <span style='font-size:30px; font-weight:900; color:#000;'>{d['recolte']}</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- INFOS COMPLÉMENTAIRES ---
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<div class='card'><span class='titre'>☁️ MÉTÉO DU JOUR</span><br><span class='info'>{d['meteo']}</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='card'><span class='titre'>🍯 TYPES DE MIEL</span><br><span class='info'>{d['miels']}</span></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='card'><span class='titre'>🌳 ÉCOSYSTÈME</span><br><span class='info'>{d['flore']}</span></div>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:black;'>📸 SCANNER PLANTE</h3>", unsafe_allow_html=True)
        st.camera_input("")

    if st.button("💾 ENREGISTRER LE SITE"):
        st.balloons()
        st.success("Diagnostic complet enregistré !")
else:
    st.markdown("<h2 style='text-align:center;'>🛰️ Recherche GPS...</h2>", unsafe_allow_html=True)
