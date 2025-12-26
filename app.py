import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import base64
from datetime import datetime

# --- CONFIGURATION STYLE "APP MOBILE" ---
st.set_page_config(page_title="YAMB App", layout="centered")

st.markdown("""
    <style>
    /* Style pour ressembler à une application Play Store */
    .stApp { background-color: #F8F9FA; }
    header {visibility: hidden;}
    
    .nav-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: white;
        display: flex;
        justify-content: space-around;
        padding: 10px 0;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
        z-index: 1000;
    }
    
    .app-header {
        background: #1B5E20;
        color: #FFD600;
        padding: 15px;
        text-align: center;
        border-radius: 0 0 20px 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    .mobile-card {
        background: white;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid #E0E0E0;
    }

    .status-active { color: #2E7D32; font-weight: bold; font-size: 14px; }
    
    /* Gros boutons pour pouces */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 50px;
        background-color: #1B5E20 !important;
        color: white !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ENTÊTE DE L'APPLICATION ---
st.markdown("""
    <div class='app-header'>
        <h1 style='margin:0; font-size:24px;'>🐝 YAMB</h1>
        <small>Abeilles du Sénégal - Expert</small>
    </div>
    """, unsafe_allow_html=True)

# --- NAVIGATION PAR ONGLETS (Simulé) ---
tabs = st.tabs(["🏠 Accueil", "🌳 Flore", "📍 Carte", "📄 Rapport"])

loc = get_geolocation()

with tabs[0]: # ACCUEIL
    st.markdown("### 👋 Bonjour !")
    if loc:
        st.success("📍 GPS Connecté")
        st.markdown(f"""
            <div class='mobile-card'>
                <b>Météo Locale</b><br>
                🌡️ 32°C | 💨 14 km/h<br>
                <span class='status-active'>✓ Conditions idéales pour le butinage</span>
            </div>
        """, unsafe_allow_html=True)
        
        st.warning("⚠️ Alerte : Fin de floraison Manguiers dans 5 jours.")
    else:
        st.info("Recherche de votre position...")

with tabs[1]: # FLORE (VISUEL)
    st.markdown("### 🌸 Identification")
    st.write("Cliquez sur les fleurs présentes :")
    
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Anacardium_occidentale_2.jpg/400px-Anacardium_occidentale_2.jpg")
        st.checkbox("Anacardier (Dahaba)")
        
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Mangifera_indica_%28Mango%29_Flower_in_Hyderabad%2C_India.jpg/400px-Mangifera_indica_%28Mango%29_Flower_in_Hyderabad%2C_India.jpg")
        st.checkbox("Manguier (Mango)")
        
    with col2:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Combretum_micranthum.jpg/400px-Combretum_micranthum.jpg")
        st.checkbox("Kinkeliba (Sékéw)")
        
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Vachellia_seyal_in_flower_in_Ethiopia.jpg/400px-Vachellia_seyal_in_flower_in_Ethiopia.jpg")
        st.checkbox("Kad (Acacia)")

with tabs[2]: # CARTE
    st.markdown("### 📍 Zone de 5 KM")
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        m = folium.Map(location=[lat, lon], zoom_start=13, control_scale=True)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        folium.Circle([lat, lon], radius=5000, color='orange', fill=False).add_to(m)
        folium.Marker([lat, lon]).add_to(m)
        st_folium(m, width=350, height=400)

with tabs[3]: # RAPPORT PDF
    st.markdown("### 📄 Dossier Expert")
    st.write("Générez le document pour la direction ou l'université.")
    
    if st.button("📥 TÉLÉCHARGER LE RAPPORT PDF"):
        st.balloons()
        st.success("Rapport enregistré dans vos téléchargements.")
    
    st.markdown("---")
    st.write("Partager sur :")
    st.button("🟢 Envoyer par WhatsApp")
