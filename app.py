import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import urllib.parse
import requests
import pandas as pd
from datetime import datetime

# --- 1. CONFIGURATION & DESIGN ---
st.set_page_config(page_title="YAMB PRO - Abeilles du Sénégal", page_icon="🐝", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #FDF5E6; }
    .main-header {
        background: linear-gradient(135deg, #8B4513 0%, #5D2E0A 100%);
        color: #FFC30B; padding: 25px; border-radius: 0 0 40px 40px;
        text-align: center; border-bottom: 6px solid #FFC30B;
    }
    .region-tag {
        background-color: #FFC30B; color: #5D2E0A;
        padding: 5px 15px; border-radius: 20px;
        font-weight: bold; font-size: 14px; margin-bottom: 10px; display: inline-block;
    }
    .flore-card {
        background-color: #FFF9E3; border-left: 5px solid #8B4513;
        padding: 12px; margin: 8px 0; border-radius: 8px; border: 1px solid #EADDCA;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BASE DE DONNÉES EXPERTE : FLORE PAR RÉGION ---
flore_nationale = [
    # Arbres de Savane (Partout)
    {"nom": "Kadd (Faidherbia)", "zones": ["Nord", "Centre", "Est"], "debut": 11, "fin": 3, "type": "Arbre"},
    {"nom": "Acacia Sénégal (Gommier)", "zones": ["Nord", "Centre"], "debut": 8, "fin : 10, "type": "Arbre"},
    
    # Zone des Niayes / Littoral
    {"nom": "Eucalyptus", "zones": ["Niayes"], "debut": 3, "fin": 6, "type": "Arbre"},
    {"nom": "Agrumes & Maraîchage", "zones": ["Niayes", "Centre"], "debut": 2, "fin": 4, "type": "Culture"},
    
    # Casamance & Sénégal Oriental
    {"nom": "Néré (Parkia)", "zones": ["Sud", "Est"], "debut": 1, "fin": 4, "type": "Arbre"},
    {"nom": "Fromager (Ceiba)", "zones": ["Sud"], "debut": 12, "fin": 2, "type": "Arbre"},
    {"nom": "Manguier & Anacardier", "zones": ["Sud", "Niayes", "Centre"], "debut": 12, "fin": 3, "type": "Culture"},
    
    # Bassin Arachidier / Centre
    {"nom": "Ziziphus (Sidem/Jujubier)", "zones": ["Centre", "Nord"], "debut": 9, "fin": 11, "type": "Arbuste"},
    {"nom": "Baobab", "zones": ["Centre", "Sud", "Est"], "debut": 5, "fin": 7, "type": "Arbre"}
]
df_flore = pd.DataFrame(flore_nationale)

# --- 3. LOGIQUE DE DÉTECTION DE ZONE ---
def obtenir_zone(lat):
    if lat > 15.5: return "Nord"
    elif 13.5 < lat <= 15.5: return "Centre"
    elif lat <= 13.5: return "Sud"
    return "Est" # Simplification par latitude

# --- 4. ACCUEIL & VERSET ---
if 'init' not in st.session_state:
    verset = "De leur ventre, sort une liqueur, aux couleurs variées, dans laquelle il y a une guérison pour les gens."
    st.components.v1.html(f"<script>var m = new SpeechSynthesisUtterance('{verset}'); m.lang='fr-FR'; window.speechSynthesis.speak(m);</script>", height=0)
    st.session_state.init = True

st.markdown("<div class='main-header'><div style='font-size:12px; font-weight:bold; color:#FFC30B;'>ABEILLES DU SÉNÉGAL</div><h1 style='margin:0; color:white;'>🐝 YAMB NATIONAL</h1></div>", unsafe_allow_html=True)

# --- 5. MODULES PRINCIPAUX ---
tabs = st.tabs(["🌸 FLORE & MÉTÉO", "🍯 RÉCOLTE", "🚨 SOS"])

loc = get_geolocation()
mois = datetime.now().month

with tabs[0]:
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        zone = obtenir_zone(lat)
        
        st.markdown(f"<div class='region-tag'>📍 Zone détectée : {zone} Sénégal</div>", unsafe_allow_html=True)
        
        # Météo
        try:
            w = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true").json()['current_weather']
            col1, col2 = st.columns(2)
            col1.metric("Température", f"{w['temperature']}°C")
            col2.metric("Vent", f"{w['windspeed']} km/h")
        except: pass

        st.divider()
        
        # Flore spécifique à la zone et au mois
        st.subheader(f"Inventaire Mellifère - Mois de {datetime.now().strftime('%B')}")
        fleurs_zone = df_flore[df_flore['zones'].apply(lambda x: zone in x)]
        en_fleur = fleurs_zone[(fleurs_zone['debut'] <= mois) & (fleurs_zone['fin'] >= mois)]
        
        if not en_fleur.empty:
            for _, r in en_fleur.iterrows():
                st.markdown(f"<div class='flore-card'><strong>{r['nom']}</strong> ({r['type']})<br>Période propice pour ce secteur.</div>", unsafe_allow_html=True)
        else:
            st.warning("Période de repos floral. Vérifiez les apports en eau.")

        # Carte 3km
        m = folium.Map(location=[lat, lon], zoom_start=14)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        folium.Circle([lat, lon], radius=3000, color='#FFC30B', fill=True, opacity=0.3).add_to(m)
        st_folium(m, width="100%", height=300)
    else:
        st.info("📡 Veuillez autoriser la localisation pour analyser votre zone (Niayes, Casamance, etc.)")

with tabs[1]:
    st.subheader("Calculateur de Production")
    nb = st.number_input("Nombre de ruches", min_value=1, value=5)
    st.metric("Estimation (Moyenne Nationale)", f"{nb * 12} kg", "Miel Pur")

with tabs[2]:
    st.subheader("Alerte Sécurité")
    type_a = st.selectbox("Urgence", ["Incendie", "Vol", "Intoxication (Pesticides)"])
    msg = f"ALERTE ABEILLES DU SENEGAL - {type_a} au rucher."
    st.markdown(f'<a href="https://wa.me/?text={msg}" target="_blank" style="display:block; background:#25D366; color:white; padding:20px; text-align:center; border-radius:15px; text-decoration:none; font-weight:bold;">📲 SIGNALER VIA WHATSAPP</a>', unsafe_allow_html=True)

st.markdown("<p style='text-align:center; padding:30px; font-weight:bold; color:#5D2E0A;'>© 2025 Abeilles du Sénégal • Expertise Nationale</p>", unsafe_allow_html=True)
