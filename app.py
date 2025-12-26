import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
from datetime import datetime

# --- CONFIGURATION ÉCRAN ---
st.set_page_config(page_title="YAMB - Abeilles du Sénégal", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #FDFCF0; }
    header {visibility: hidden;}

    /* Style Alvéoles et Header */
    .yamb-header {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
        color: #FFD600;
        padding: 20px;
        border-radius: 0 0 40px 40px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .logo-container {
        background: white;
        width: 80px;
        height: 80px;
        border-radius: 50%;
        margin: -40px auto 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border: 3px solid #FFD600;
    }

    /* Tableau de Bord Alvéolaire */
    .hex-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 15px;
        margin-top: 20px;
    }

    .hex-card {
        width: 100px;
        height: 115px;
        background: white;
        clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        border: 2px solid #FFD600;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }

    .hex-icon { font-size: 30px; margin-bottom: 5px; }
    .hex-label { font-size: 10px; font-weight: bold; color: #1B5E20; text-transform: uppercase; }

    /* Section Mobile Cards */
    .mobile-card {
        background: white;
        border-radius: 20px;
        padding: 20px;
        margin-top: 20px;
        border: 1px solid #FFD600;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. HEADER AVEC LOGO ---
st.markdown("""
    <div class='yamb-header'>
        <h1 style='margin:0; font-size:28px;'>🐝 YAMB</h1>
        <p style='font-size:14px;'>Expertise Apicole du Sénégal</p>
    </div>
    <div class='logo-container'>
        <img src="https://images.unsplash.com/photo-1589648751789-c87882269550?q=80&w=100&auto=format&fit=crop" width="60" style="border-radius:50%;">
    </div>
    """, unsafe_allow_html=True)

loc = get_geolocation()

if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']

    # --- 2. TABLEAU DE BORD ALVÉOLAIRE (Hexagones) ---
    st.markdown("<h4 style='text-align:center; color:#1B5E20;'>📊 État du Rucher</h4>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class='hex-container'>
            <div class='hex-card'>
                <span class='hex-icon'>🐝</span>
                <span class='hex-label'>Activités<br>Abeilles</span>
            </div>
            <div class='hex-card'>
                <span class='hex-icon'>🏠</span>
                <span class='hex-label'>État<br>Ruches</span>
            </div>
            <div class='hex-card'>
                <span class='hex-icon'>🌸</span>
                <span class='hex-label'>Flore<br>Mellifère</span>
            </div>
            <div class='hex-card'>
                <span class='hex-icon'>🌡️</span>
                <span class='hex-label'>31°C<br>Météo</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- 3. ACTIONS PRINCIPALES ---
    st.markdown("### 🛠️ Actions Terrain")
    
    with st.expander("🐝 **SURVEILLANCE DES ABEILLES**"):
        st.write("Observation du comportement au trou de vol :")
        st.select_slider("Intensité de butinage", options=["Faible", "Moyenne", "Forte", "Exceptionnelle"])
        st.image("https://images.unsplash.com/photo-1559440666-489ca64d852c?q=80&w=400&auto=format&fit=crop", caption="Abeilles en activité")

    with st.expander("🌸 **ANALYSE DE LA FLORE**"):
        st.write("Cochez les ressources disponibles dans les 5 km :")
        st.checkbox("🌳 Anacardier (Dahaba)")
        st.checkbox("🌳 Manguier (Mango)")
        st.checkbox("🌿 Flore Sauvage")

    with st.expander("📍 **CARTE SATELLITE**"):
        m = folium.Map(location=[lat, lon], zoom_start=14)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        folium.Circle([lat, lon], radius=3000, color='green', fill=True, opacity=0.1).add_to(m)
        folium.Marker([lat, lon], icon=folium.Icon(color='green', icon='home')).add_to(m)
        st_folium(m, width=320, height=300)

    # --- PIED DE PAGE ---
    st.markdown("---")
    if st.button("💾 ENREGISTRER LE RAPPORT YAMB"):
        st.balloons()
        st.success("Rapport d'expertise transmis à Abeilles du Sénégal.")

else:
    st.markdown("""
        <div style='text-align:center; padding:50px;'>
            <h1 style='font-size:80px;'>🐝</h1>
            <p><b>YAMB active ses capteurs...</b></p>
            <p style='font-size:12px;'>Veuillez accepter la localisation pour l'expert.</p>
        </div>
    """, unsafe_allow_html=True)
