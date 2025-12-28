import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import requests
import urllib.parse

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="YAMB PRO - Sénégal", layout="centered")

# --- 2. STYLE HAUTE VISIBILITÉ (Correction définitive du blanc sur blanc) ---
st.markdown("""
    <style>
    /* Fond de page crème pour reposer les yeux */
    .stApp { background-color: #FDF5E6; }
    
    /* FORCE LE NOIR SUR ABSOLUMENT TOUT LE TEXTE */
    h1, h2, h3, h4, p, span, label, li, div {
        color: #000000 !important;
        font-weight: 800 !important;
    }

    /* Cartes d'information avec bordures noires épaisses */
    .info-box {
        background-color: #ffffff !important;
        border: 4px solid #000000 !important;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 8px 8px 0px #FFC30B;
    }

    /* Titres dorés dans les boites */
    .info-box h3 { color: #8B4513 !important; margin-top: 0; }
    
    /* Alerte Rouge pour les dangers */
    .danger-box {
        background-color: #FFEBEB !important;
        border: 4px solid #CC0000 !important;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ENTÊTE ---
st.markdown("<h1 style='text-align:center;'>🐝 YAMB PRO - ÉLITE</h1>", unsafe_allow_html=True)

# --- 4. NAVIGATION ---
tabs = st.tabs(["📊 TERRAIN", "🌙 LUNE & FLORE", "🍯 PRODUCTION", "🚨 SOS"])

loc = get_geolocation()

with tabs[0]:
    st.markdown("## 🛰️ Analyse du Rayon de 3 km")
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        
        # Météo en texte brut noir (plus sûr que les metrics Streamlit)
        try:
            w = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true").json()['current_weather']
            st.markdown(f"""
                <div class='info-box'>
                    <h3>☁️ MÉTÉO ACTUELLE</h3>
                    <p style='font-size:20px;'>Température : {w['temperature']}°C</p>
                    <p style='font-size:20px;'>Vent : {w['windspeed']} km/h</p>
                </div>
            """, unsafe_allow_html=True)
        except: pass

        # Carte avec Marqueur Rouge et Cercle Jaune
        m = folium.Map(location=[lat, lon], zoom_start=13)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        folium.Marker([lat, lon], popup="Mon Rucher", icon=folium.Icon(color='red', icon='home')).add_to(m)
        folium.Circle([lat, lon], radius=3000, color='#FFC30B', fill=True, fill_opacity=0.3).add_to(m)
        st_folium(m, width="100%", height=350)
    else:
        st.warning("⚠️ Activez le GPS pour voir votre zone de butinage.")

with tabs[1]:
    st.markdown("## 🌙 Cycle Lunaire & Flore")
    # Calendrier Lunaire simplifié pour l'apiculture
    st.markdown("""
        <div class='info-box' style='background-color:#1a0d02 !important;'>
            <h3 style='color:#FFC30B !important;'>🌒 Premier Croissant</h3>
            <p style='color:white !important;'>Période de développement : Les colonies sont calmes. Idéal pour les inspections de santé.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("## 🌿 Floraisons du Moment")
    st.markdown("""
        <div class='info-box'>
            <h3>🌳 Kadd (Faidherbia)</h3>
            <p>Pleine floraison. Nectar abondant mais sensible à l'Harmattan.</p>
        </div>
        <div class='info-box'>
            <h3>🍎 Anacardier</h3>
            <p>Début de floraison dans les zones côtières.</p>
        </div>
    """, unsafe_allow_html=True)

with tabs[2]:
    st.markdown("## 🍯 Calculateur de Récolte")
    nb = st.number_input("Nombre de ruches productives", 1, 500, 10)
    recolte_estimee = nb * 12
    st.markdown(f"""
        <div class='info-box' style='text-align:center;'>
            <p>ESTIMATION TOTALE</p>
            <h1 style='font-size:70px; margin:10px 0;'>{recolte_estimee} kg</h1>
            <p style='color:green !important;'>Label : Miel Bio du Sénégal</p>
        </div>
    """, unsafe_allow_html=True)

with tabs[3]:
    st.markdown("## 🚨 Centre d'Urgence Unité d'Élite")
    st.markdown("""<div class='danger-box'>⚠️ RISQUE FEU : La brousse est très sèche. Vos pare-feux doivent être dégagés sur 5 mètres.</div>""", unsafe_allow_html=True)
    
    incident = st.selectbox("Type d'urgence", ["Feu de brousse", "Vol de ruches", "Mortalité massive"])
    if st.button("📲 SIGNALER L'URGENCE VIA WHATSAPP"):
        gps = f"{loc['coords']['latitude']},{loc['coords']['longitude']}" if loc else "Non disponible"
        msg = urllib.parse.quote(f"🚨 URGENCE YAMB PRO\nIncident: {incident}\nLocalisation GPS: https://www.google.com/maps?q={gps}")
        st.markdown(f'<a href="https://wa.me/221XXXXXXX?text={msg}" target="_blank" style="display:block; background:green; color:white; padding:20px; text-align:center; border-radius:10px; text-decoration:none;">VALIDER L\'ENVOI WHATSAPP</a>', unsafe_allow_html=True)
