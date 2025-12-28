import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import requests
import urllib.parse

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="YAMB PRO", layout="centered")

# --- 2. STYLE "LUMINOSITÉ MAXIMALE" ---
st.markdown("""
    <style>
    .stApp { background-color: #FDF5E6; }
    h1, h2, h3, h4, p, span, label { color: #000000 !important; font-weight: 800 !important; }
    
    .flore-card-fix {
        background-color: #ffffff !important;
        border: 3px solid #000000 !important;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
    }
    
    .save-btn {
        background-color: #FFC30B !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. GESTION DE LA MÉMOIRE (COORDONNÉES) ---
if 'rucher_lat' not in st.session_state:
    st.session_state['rucher_lat'] = None
    st.session_state['rucher_lon'] = None

# --- 4. INTERFACE ---
st.title("🐝 YAMB PRO - Gestion Rucher")

tabs = st.tabs(["📍 CARTE & FLORE", "💾 MES RUCHERS"])

with tabs[0]:
    loc = get_geolocation()
    
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        
        st.markdown("### 🛰️ Localisation en temps réel")
        
        # Bouton de sauvegarde
        if st.button("💾 SAUVEGARDER CE RUCHER COMME PRINCIPAL"):
            st.session_state['rucher_lat'] = lat
            st.session_state['rucher_lon'] = lon
            st.success(f"Position enregistrée : {lat:.4f}, {lon:.4f}")

        # Carte
        m = folium.Map(location=[lat, lon], zoom_start=13)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        folium.Marker([lat, lon], tooltip="Position Actuelle", icon=folium.Icon(color='red')).add_to(m)
        folium.Circle([lat, lon], radius=3000, color='#FFC30B', fill=True, fill_opacity=0.2).add_to(m)
        st_folium(m, width="100%", height=400)
        
        # Ressources Florales
        st.markdown("### 🌿 Ressources Florales")
        st.markdown("""
            <div class='flore-card-fix'>
                <h4>🌳 Kadd</h4>
                <p><b>Miel attendu :</b> Miel clair médicinal</p>
            </div>
            <div class='flore-card-fix'>
                <h4>🍎 Anacardier</h4>
                <p><b>Miel attendu :</b> Ambré et fruité</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Recherche du signal GPS...")

with tabs[1]:
    st.subheader("🏠 Rucher Sauvegardé")
    if st.session_state['rucher_lat']:
        st.write(f"**Coordonnées enregistrées :**")
        st.code(f"Lat: {st.session_state['rucher_lat']}\nLon: {st.session_state['rucher_lon']}")
        
        if st.button("VOIR LE RUCHER ENREGISTRÉ"):
            m_saved = folium.Map(location=[st.session_state['rucher_lat'], st.session_state['rucher_lon']], zoom_start=14)
            folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m_saved)
            folium.Marker([st.session_state['rucher_lat'], st.session_state['rucher_lon']], icon=folium.Icon(color='green')).add_to(m_saved)
            st_folium(m_saved, width="100%", height=300)
    else:
        st.write("Aucun rucher n'a encore été sauvegardé.")
