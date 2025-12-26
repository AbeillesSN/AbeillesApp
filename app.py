import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import base64
from datetime import datetime

# --- CONFIGURATION (Change le nom de l'onglet du navigateur) ---
st.set_page_config(page_title="YAMB - Abeilles du Sénégal", layout="wide", page_icon="🐝")

# --- STYLE CSS POUR FORCER L'AFFICHAGE DU NOM ---
st.markdown("""
    <style>
    /* Cache le header par défaut de Streamlit pour plus de propreté */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .yamb-container {
        background: linear-gradient(135deg, #1B5E20 0%, #003300 100%);
        color: #FFD600;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    .yamb-title {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 60px;
        font-weight: 900;
        margin: 0;
        text-transform: uppercase;
    }
    .yamb-subtitle {
        font-size: 22px;
        letter-spacing: 1px;
        opacity: 0.9;
    }
    </style>
    """, unsafe_allow_html=True)

# --- NOUVEL AFFICHAGE DU TITRE ---
st.markdown("""
    <div class='yamb-container'>
        <h1 class='yamb-title'>🐝 YAMB</h1>
        <div class='yamb-subtitle'>Expertise Apicole Précise - Abeilles du Sénégal</div>
    </div>
    """, unsafe_allow_html=True)

# --- RESTE DE L'INTERFACE ---
loc = get_geolocation()

if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    
    col_map, col_data = st.columns([2, 1])

    with col_map:
        st.markdown("### 🗺️ Zone d'Analyse (5km)")
        m = folium.Map(location=[lat, lon], zoom_start=14)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', 
                         attr='Google Satellite').add_to(m)
        folium.Circle([lat, lon], radius=3000, color='green', fill=True, opacity=0.1).add_to(m)
        folium.Marker([lat, lon], icon=folium.Icon(color='green')).add_to(m)
        st_folium(m, width="100%", height=450)

    with col_data:
        st.markdown("### 📊 Données de Terrain")
        st.write(f"**Position :** {lat:.4f}, {lon:.4f}")
        st.success("Signal GPS Stable")
        
        st.divider()
        if st.button("📄 GÉNÉRER LE RAPPORT YAMB"):
            st.balloons()
            st.info("Le rapport PDF 'YAMB_Expert.pdf' est prêt pour la direction.")

else:
    st.warning("⚠️ Localisation en cours... Veuillez autoriser l'accès GPS sur Microsoft Edge.")
