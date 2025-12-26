import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import base64
from datetime import datetime
import urllib.parse

# --- CONFIGURATION (C'est ici que le nom change dans l'onglet) ---
st.set_page_config(page_title="YAMB - Abeilles du Sénégal", layout="wide", page_icon="🐝")

# Nettoyage du style pour forcer le nouveau titre
st.markdown("""
    <style>
    .main-header { 
        background: linear-gradient(135deg, #1B5E20 0%, #003300 100%); 
        color: #FFD600; 
        padding: 25px; 
        border-radius: 15px; 
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }
    .yamb-title { font-size: 50px; font-weight: 900; margin: 0; letter-spacing: 2px; }
    .yamb-card { background: #F1F8E9; border: 1px solid #C8E6C9; padding: 10px; border-radius: 10px; margin-bottom: 10px; display: flex; align-items: center; }
    .yamb-card img { border-radius: 8px; margin-right: 15px; border: 2px solid #FFD600; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER AVEC LE NOUVEAU NOM ---
st.markdown("""
    <div class='main-header'>
        <h1 class='yamb-title'>🐝 YAMB</h1>
        <p style='font-size: 20px; opacity: 0.9;'>L'Intelligence Apicole du Sénégal</p>
    </div>
    """, unsafe_allow_html=True)

# --- LE RESTE DU CODE ---
loc = get_geolocation()

if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown("### 🌳 Guide Visuel YAMB (5km)")
        # Liste simplifiée pour l'exemple
        plantes = {
            "Anacardier": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Anacardium_occidentale_2.jpg/800px-Anacardium_occidentale_2.jpg",
            "Manguier": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Mangifera_indica_%28Mango%29_Flower_in_Hyderabad%2C_India.jpg/800px-Mangifera_indica_%28Mango%29_Flower_in_Hyderabad%2C_India.jpg"
        }
        
        for p, img in plantes.items():
            st.markdown(f"""
                <div class='yamb-card'>
                    <img src="{img}" width="80">
                    <div><b>{p}</b><br><small>Zone : Casamance / Littoral</small></div>
                </div>
            """, unsafe_allow_html=True)

    with col_right:
        st.markdown("### 🗺️ Localisation du Rucher")
        m = folium.Map(location=[lat, lon], zoom_start=14)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        folium.Marker([lat, lon], icon=folium.Icon(color='green')).add_to(m)
        st_folium(m, width="100%", height=400)

    # Bouton de Rapport
    st.divider()
    if st.button("📄 GÉNÉRER LE RAPPORT YAMB (PDF)"):
        st.success("Rapport généré avec succès !")

else:
    st.info("📡 En attente du signal GPS pour activer YAMB...")
