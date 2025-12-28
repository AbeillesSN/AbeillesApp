import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import requests
import urllib.parse
from datetime import datetime

# --- CONFIGURATION & STYLE ---
st.set_page_config(page_title="YAMB PRO - Élite Sénégal", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #FDF5E6; }
    h1, h2, h3, h4, p, span, label { color: #000000 !important; font-weight: 800 !important; }
    .data-card { background: #ffffff !important; border: 3px solid #000000; padding: 20px; border-radius: 12px; margin-bottom: 15px; }
    .moon-card { background: #1a0d02 !important; color: #FFC30B !important; padding: 15px; border-radius: 10px; text-align: center; }
    .fire-alert { background: #ff4b4b !important; color: white !important; padding: 10px; border-radius: 10px; border: 2px solid black; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
tabs = st.tabs(["📍 TERRAIN", "🌙 LUNE & FLORE", "🍯 RÉCOLTE", "🚨 SOS FEU"])

loc = get_geolocation()

with tabs[0]:
    st.markdown("### 🛰️ Rayon de Butinage (3km)")
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        # Carte Satellite avec Cercle et Marqueur
        m = folium.Map(location=[lat, lon], zoom_start=13)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        folium.Marker([lat, lon], icon=folium.Icon(color='red', icon='leaf')).add_to(m)
        folium.Circle([lat, lon], radius=3000, color='#FFC30B', fill=True, fill_opacity=0.2).add_to(m)
        st_folium(m, width="100%", height=300)
    else:
        st.warning("📍 GPS en attente...")

with tabs[1]:
    st.markdown("### 🌙 Influence Lunaire & Flore")
    # Simulation simplifiée du cycle lunaire
    st.markdown("""
        <div class='moon-card'>
            <h2 style='color:#FFC30B !important;'>🌓 Premier Quartier</h2>
            <p style='color:white !important;'>Phase de stimulation : La reine intensifie la ponte. 
            Moment idéal pour nourrir les colonies faibles.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🌿 Ressources Actuelles")
    st.markdown("<div class='data-card'><h4>🌳 Kadd (Acacia Albida)</h4><p>Pleine floraison. Attention au vent d'Est (Harmattan) qui peut sécher le nectar.</p></div>", unsafe_allow_html=True)

with tabs[2]:
    st.markdown("### 🍯 Estimation de Miellée")
    nb = st.number_input("Nombre de ruches peuplées", 1, 500, 10)
    st.markdown(f"""
        <div class='data-card' style='text-align:center;'>
            <p>POTENTIEL DE PRODUCTION</p>
            <h1 style='font-size:60px;'>{nb * 12} kg</h1>
            <p style='color: #d4af37 !important;'>Miel d'Élite du Sénégal</p>
        </div>
    """, unsafe_allow_html=True)

with tabs[3]:
    st.markdown("### 🚨 Alerte Feu & Sécurité")
    st.markdown("<div class='fire-alert'>⚠️ SAISON SÈCHE : Risque élevé de feux de brousse. Vérifiez vos pare-feux (bande de 5m désherbée).</div>", unsafe_allow_html=True)
    
    incident = st.selectbox("Signaler une urgence", ["Feu de brousse", "Vol de ruches", "Mortalité massive (Pesticides)"])
    if st.button("📲 ENVOYER POSITION À L'UNITÉ D'ÉLITE"):
        gps_url = f"https://www.google.com/maps?q={loc['coords']['latitude']},{loc['coords']['longitude']}" if loc else "GPS Non fourni"
        msg = urllib.parse.quote(f"ALERTE YAMB PRO\nIncident: {incident}\nLieu: {gps_url}")
        st.markdown(f'<a href="https://wa.me/?text={msg}" target="_blank" style="background:green; color:white; padding:15px; border-radius:5px; text-decoration:none;">Envoyer via WhatsApp</a>', unsafe_allow_html=True)
