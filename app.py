import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import requests
import urllib.parse
from datetime import datetime

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="YAMB PRO - Abeilles du Sénégal", layout="centered")

# --- 2. CHARTE GRAPHIQUE HAUTE VISIBILITÉ ---
st.markdown("""
    <style>
    /* Fond de l'application */
    .stApp { background-color: #FDF5E6; }
    
    /* FORCE LE NOIR ABSOLU SUR TOUS LES TEXTES */
    h1, h2, h3, h4, p, span, label, li, .stMarkdown {
        color: #000000 !important; 
        font-weight: bold !important;
    }

    /* Header Sombre pour le contraste */
    .main-header {
        background: #1a0d02;
        padding: 25px;
        text-align: center;
        border-bottom: 5px solid #FFC30B;
        border-radius: 0 0 30px 30px;
        margin-bottom: 20px;
    }

    /* BLOCS DE DONNÉES BLANCS (Pour une lecture parfaite) */
    .data-card {
        background-color: #ffffff !important;
        border: 3px solid #000000 !important;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        box-shadow: 5px 5px 0px #FFC30B;
    }

    /* Style des onglets */
    button[data-baseweb="tab"] { background-color: #f0f0f0 !important; }
    button[aria-selected="true"] { background-color: #FFC30B !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ENTÊTE ---
st.markdown("""
    <div class='main-header'>
        <h1 style='color: #FFC30B !important; margin:0;'>🐝 YAMB PRO</h1>
        <p style='color: white !important; margin:0;'>Unité d'Élite Apicole - Sénégal</p>
    </div>
    """, unsafe_allow_html=True)

# --- 4. LOGIQUE DE LOCALISATION ET ANALYSE ---
loc = get_geolocation()
mois_actuel = datetime.now().strftime("%B")

tabs = st.tabs(["🌸 TERRAIN", "🍯 RÉCOLTE", "🚨 SOS"])

with tabs[0]:
    st.subheader(f"📍 Analyse du Rayon (3 km) - {mois_actuel}")
    
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        
        # Météo
        try:
            w = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true").json()['current_weather']
            col1, col2 = st.columns(2)
            col1.markdown(f"<div class='data-card'><small>TEMPÉRATURE</small><br><span style='font-size:25px;'>{w['temperature']}°C</span></div>", unsafe_allow_html=True)
            col2.markdown(f"<div class='data-card'><small>VENT</small><br><span style='font-size:25px;'>{w['windspeed']} km/h</span></div>", unsafe_allow_html=True)
        except: st.write("Données météo indisponibles.")

        # Ressources Florales (ENFIN LISIBLES)
        st.markdown("### 🌿 Ressources Florales Actuelles")
        st.markdown("""
            <div class='data-card'>
                <h4 style='margin:0;'>🌳 Kadd</h4>
                <p style='margin:0;'>Type de miel : Miel clair médicinal</p>
            </div>
            <div class='data-card'>
                <h4 style='margin:0;'>🍎 Anacardier</h4>
                <p style='margin:0;'>Type de miel : Ambré et fruité</p>
            </div>
        """, unsafe_allow_html=True)

        # Carte avec Marqueur et Rayon
        st.markdown("### 🛰️ Carte de Butinage")
        m = folium.Map(location=[lat, lon], zoom_start=13)
        
        # Couche Satellite Google
        folium.TileLayer(
            tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
            attr='Google Satellite',
            name='Satellite'
        ).add_to(m)

        # MARQUEUR ROUGE (Le Rucher)
        folium.Marker([lat, lon], tooltip="Position du Rucher", icon=folium.Icon(color='red')).add_to(m)

        # CERCLE JAUNE (Rayon de 3 km)
        folium.Circle(
            location=[lat, lon],
            radius=3000,
            color='#FFC30B',
            fill=True,
            fill_opacity=0.2
        ).add_to(m)

        st_folium(m, width="100%", height=400)
    else:
        st.info("📍 Recherche de votre position GPS... Veuillez autoriser l'accès.")

with tabs[1]:
    st.subheader("🍯 Calculateur de production")
    nb_ruches = st.number_input("Combien de ruches avez-vous ?", 1, 1000, 10)
    recolte = nb_ruches * 12
    st.markdown(f"""
        <div class='data-card' style='text-align:center;'>
            <p style='margin:0;'>POTENTIEL DE RÉCOLTE</p>
            <h1 style='font-size:50px; margin:0;'>{recolte} kg</h1>
            <p style='color: green !important;'>Miel Bio Sénégal</p>
        </div>
    """, unsafe_allow_html=True)

with tabs[2]:
    st.subheader("🚨 Assistance d'Urgence")
    st.write("Détaillez le problème pour l'Unité d'Élite :")
    incident = st.selectbox("Type d'incident", ["Incendie", "Vol", "Maladie", "Pesticides"])
    msg = urllib.parse.quote(f"🚨 ALERTE YAMB PRO\nIncident : {incident}\nLocalisation : {loc['coords']['latitude'] if loc else 'Inconnue'},{loc['coords']['longitude'] if loc else 'Inconnue'}")
    st.markdown(f'<a href="https://wa.me/?text={msg}" target="_blank" style="display:block; background:#25D366; color:white; padding:20px; text-align:center; border-radius:15px; text-decoration:none; font-weight:bold; border: 4px solid #128C7E;">📲 ENVOYER L\'ALERTE WHATSAPP</a>', unsafe_allow_html=True)
