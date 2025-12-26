import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation

# 1. CONFIGURATION DE L'ONGLET (Le nom en haut du navigateur)
st.set_page_config(page_title="YAMB - Abeilles du Sénégal", layout="wide", page_icon="🐝")

# 2. SUPPRESSION DE L'ANCIEN TITRE ET STYLE DU NOUVEAU
st.markdown("""
    <style>
    /* Cache les éléments qui pourraient afficher l'ancien nom */
    .stApp header {visibility: hidden;}
    
    .yamb-banner {
        background: linear-gradient(135deg, #1B5E20 0%, #004D40 100%);
        color: #FFD600;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }
    .yamb-logo { font-size: 65px; font-weight: 900; margin: 0; }
    .yamb-sub { font-size: 20px; letter-spacing: 2px; text-transform: uppercase; opacity: 0.9; }
    </style>
    """, unsafe_allow_html=True)

# 3. AFFICHAGE DU NOUVEAU TITRE "YAMB"
st.markdown("""
    <div class='yamb-banner'>
        <h1 class='yamb-logo'>🐝 YAMB</h1>
        <div class='yamb-sub'>Identification et Prédiction - Abeilles du Sénégal</div>
    </div>
    """, unsafe_allow_html=True)

# 4. FONCTIONNALITÉS PRÉCISES (3-5 KM)
loc = get_geolocation()

if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    
    col_guide, col_map = st.columns([1, 1])

    with col_guide:
        st.markdown("### 🌳 Guide des Plantes (Rayon 5km)")
        # Utilisation d'une clé unique pour forcer Edge à rafraîchir le composant
        st.multiselect("Sélectionnez les plantes :", 
                       ["Anacardier", "Manguier", "Kad", "Néré"], 
                       default=["Anacardier", "Manguier"],
                       key="yamb_select_expert")
        
        st.info("💡 Analyse de la flore locale en cours pour YAMB...")

    with col_map:
        st.markdown("### 🗺️ Carte d'Analyse (Zone 5km)")
        m = folium.Map(location=[lat, lon], zoom_start=13)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', 
                         attr='Google Satellite').add_to(m)
        # Cercle de précision 5km
        folium.Circle([lat, lon], radius=5000, color='orange', fill=False).add_to(m)
        folium.Marker([lat, lon], popup="Rucher YAMB").add_to(m)
        st_folium(m, width="100%", height=400, key="yamb_map_expert")

else:
    st.warning("📡 Recherche du signal GPS pour activer l'interface YAMB...")
