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

# --- 2. CHARTE GRAPHIQUE "ZÉRO BLANC" (Contraste Maximum) ---
st.markdown("""
    <style>
    .stApp { background-color: #FDF5E6; }
    
    /* FORCER LE NOIR SUR TOUT CE QUI ÉTAIT ILLISIBLE */
    h1, h2, h3, p, span, label, .stMetric, [data-testid="stMetricValue"], [data-testid="stText"] {
        color: #000000 !important;
        font-weight: 700 !important;
    }

    /* Fond blanc pour les blocs de données pour une lecture parfaite */
    .data-block {
        background-color: #ffffff;
        border: 3px solid #000000;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    }

    /* Header très sombre */
    .main-header {
        background: #1a0d02;
        padding: 30px;
        text-align: center;
        border-bottom: 5px solid #FFC30B;
        border-radius: 0 0 30px 30px;
    }
    
    /* Bouton SOS Rouge Alerte */
    .sos-final {
        background: #CC0000;
        color: white !important;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        display: block;
        text-decoration: none;
        font-size: 1.3em;
        border: 4px solid #000000;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIQUE MÉTIER ---
flore_riche = [
    {"nom": "Kadd", "miel": "Miel clair médicinal", "mois": [11, 12, 1, 2, 3]},
    {"nom": "Anacardier", "miel": "Ambré et fruité", "mois": [12, 1, 2, 3]},
    {"nom": "Acacia Sénégal", "miel": "Qualité Export (Gomme)", "mois": [8, 9, 10]}
]

# --- 4. HEADER ---
st.markdown("""
    <div class='main-header'>
        <h1 style='color: #FFC30B !important; margin:0;'>🐝 YAMB PRO</h1>
        <p style='color: white !important; margin:0;'>UNITÉ D'ÉLITE - ABEILLES DU SÉNÉGAL</p>
    </div>
    """, unsafe_allow_html=True)

tabs = st.tabs(["🌸 TERRAIN", "🍯 RÉCOLTE", "🚨 SOS DÉTAILLÉ"])

loc = get_geolocation()
mois = datetime.now().month

with tabs[0]:
    st.markdown("## 📍 Analyse Environnementale")
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        
        # MÉTÉO EN BLOCS BLANCS (LISIBILITÉ 100%)
        try:
            w = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true").json()['current_weather']
            col1, col2 = st.columns(2)
            col1.markdown(f"<div class='data-block'><small>TEMPÉRATURE</small><br><span style='font-size:30px;'>{w['temperature']}°C</span></div>", unsafe_allow_html=True)
            col2.markdown(f"<div class='data-block'><small>VENT</small><br><span style='font-size:30px;'>{w['windspeed']} km/h</span></div>", unsafe_allow_html=True)
        except: pass

        st.markdown("### 🌿 Ressources Florales Actuelles")
        actives = [f for f in flore_riche if mois in f['mois']]
        for f in actives:
            st.markdown(f"<div class='data-block'><b>{f['nom']}</b><br>Type de miel : {f['miel']}</div>", unsafe_allow_html=True)
            
        m = folium.Map(location=[lat, lon], zoom_start=14)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        st_folium(m, width="100%", height=300)
    else:
        st.warning("Veuillez autoriser le GPS pour lire les données.")

with tabs[1]:
    st.markdown("## 🍯 Estimation Production")
    nb = st.number_input("Nombre de ruches", 1, 500, 10)
    # Affichage du résultat dans un bloc blanc géant
    st.markdown(f"""
        <div class='data-block' style='text-align:center;'>
            <p style='margin:0; font-size:20px;'>POTENTIEL DE RÉCOLTE</p>
            <h1 style='font-size:60px; margin:0;'>{nb * 12} kg</h1>
            <p style='color: green !important;'>Miel Bio Sénégal</p>
        </div>
    """, unsafe_allow_html=True)

with tabs[2]:
    st.markdown("## 🚨 Rapport d'Urgence Unité d'Élite")
    st.markdown("Détaillez l'incident pour une intervention rapide :")
    
    with st.form("sos_form"):
        type_incident = st.selectbox("Nature de l'urgence", ["🔥 Incendie", "🕵️ Vol / Vandalisme", "🐝 Mortalité massive", "☠️ Intoxication Pesticides"])
        gravite = st.select_slider("Gravité", options=["Faible", "Moyenne", "CRITIQUE"])
        details = st.text_area("Précisions (Lieu exact, nombre de ruches touchées...)")
        
        submit = st.form_submit_button("PRÉPARER L'ALERTE")
        
        if submit:
            gps_link = f"https://www.google.com/maps?q={loc['coords']['latitude']},{loc['coords']['longitude']}" if loc else "GPS Non fourni"
            message = f"*URGENCE YAMB PRO*\n\n*Type:* {type_incident}\n*Gravité:* {gravite}\n*Lieu:* {gps_link}\n*Détails:* {details}"
            whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(message)}"
            st.markdown(f'<a href="{whatsapp_url}" target="_blank" class="sos-final">📲 ENVOYER L\'ALERTE À L\'UNITÉ D\'ÉLITE</a>', unsafe_allow_html=True)

st.markdown("<p style='text-align:center; padding:20px;'>© 2025 Abeilles du Sénégal</p>", unsafe_allow_html=True)
