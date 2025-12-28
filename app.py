import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import requests
import urllib.parse
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="YAMB PRO - Élite Sénégal", layout="centered")

# --- STYLE VISUEL FORCÉ ---
st.markdown("""
    <style>
    .stApp { background-color: #FDF5E6; }
    h1, h2, h3, h4, p, span, label { color: #000000 !important; font-weight: 800 !important; }
    .data-card { background: #ffffff !important; border: 3px solid #000000; padding: 15px; border-radius: 12px; margin-bottom: 10px; }
    .stMetric { background: white; border: 1px solid black; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- MÉMOIRE GPS ---
if 'rucher_save' not in st.session_state: st.session_state['rucher_save'] = None

# --- NAVIGATION ---
tabs = st.tabs(["🌸 FLORE & MÉTÉO", "🍯 RÉCOLTE", "💾 MÉMOIRE", "🚨 SOS"])

loc = get_geolocation()

with tabs[0]:
    st.markdown("### 🛰️ Analyse Terrain (Rayon 3km)")
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        
        # Météo
        try:
            w = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true").json()['current_weather']
            col1, col2 = st.columns(2)
            col1.metric("TEMPÉRATURE", f"{w['temperature']}°C")
            col2.metric("VENT", f"{w['windspeed']} km/h")
        except: pass

        # Flore
        st.markdown("<div class='data-card'><h4>🌳 Kadd & Anacardier</h4><p>Floraison active en Décembre/Janvier. Miel clair et fruité.</p></div>", unsafe_allow_html=True)
        
        # Carte
        m = folium.Map(location=[lat, lon], zoom_start=13)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        folium.Marker([lat, lon], icon=folium.Icon(color='red')).add_to(m)
        folium.Circle([lat, lon], radius=3000, color='#FFC30B', fill=True, fill_opacity=0.2).add_to(m)
        st_folium(m, width="100%", height=300)

with tabs[1]:
    st.markdown("### 🍯 Calculateur de Récolte")
    nb = st.number_input("Nombre de ruches", 1, 500, 10)
    st.markdown(f"<div class='data-card'><h1 style='text-align:center;'>{nb * 12} kg</h1><p style='text-align:center; color:green !important;'>Potentiel Miel Bio</p></div>", unsafe_allow_html=True)

with tabs[2]:
    st.markdown("### 💾 Sauvegarde Rucher")
    if loc:
        if st.button("💾 ENREGISTRER CETTE POSITION"):
            st.session_state['rucher_save'] = {"lat": loc['coords']['latitude'], "lon": loc['coords']['longitude']}
            st.success("Position enregistrée !")

with tabs[3]:
    st.markdown("### 🚨 Urgence Unité d'Élite")
    incident = st.text_input("Détail de l'incident (ex: Feu, Vol)")
    if st.button("📲 ENVOYER ALERTE WHATSAPP"):
        msg = urllib.parse.quote(f"URGENCE YAMB PRO\nIncident: {incident}\nPosition: https://maps.google.com/?q={loc['coords']['latitude']},{loc['coords']['longitude']}")
        st.markdown(f'<a href="https://wa.me/?text={msg}" target="_blank">Cliquez ici pour envoyer</a>', unsafe_allow_html=True)
