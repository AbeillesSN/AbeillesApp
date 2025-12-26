import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
from datetime import datetime

# --- CONFIGURATION ÉCRAN MOBILE ---
st.set_page_config(page_title="YAMB - Dashboard", layout="centered", page_icon="🐝")

st.markdown("""
    <style>
    /* Global App Style */
    .stApp { background-color: #F0F2F5; }
    header {visibility: hidden;}
    
    /* Bannière d'accueil */
    .welcome-banner {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
        color: white;
        padding: 30px 20px;
        border-radius: 0 0 30px 30px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    /* Cartes de statistiques (KPI) */
    .kpi-container { display: flex; justify-content: space-between; gap: 10px; margin-bottom: 20px; }
    .kpi-card {
        background: white;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        flex: 1;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border-bottom: 4px solid #FFD600;
    }
    .kpi-value { font-size: 20px; font-weight: bold; color: #1B5E20; display: block; }
    .kpi-label { font-size: 12px; color: #666; }

    /* Menu Actions Rapides */
    .action-card {
        background: white;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        transition: transform 0.2s;
        border: 1px solid #E0E0E0;
    }
    .action-icon { font-size: 30px; margin-right: 20px; }
    .action-text b { font-size: 18px; color: #1B5E20; }
    .action-text p { margin: 0; color: #757575; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. BANNIÈRE DE BIENVENUE ---
st.markdown(f"""
    <div class='welcome-banner'>
        <h1 style='margin:0;'>Jërëjëf, YAMB !</h1>
        <p style='opacity:0.9;'>{datetime.now().strftime('%d %B %Y')}</p>
    </div>
    """, unsafe_allow_html=True)

loc = get_geolocation()

if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']

    # --- 2. TABLEAU DE BORD (STATISTIQUES) ---
    st.markdown("""
        <div class='kpi-container'>
            <div class='kpi-card'><span class='kpi-value'>32°C</span><span class='kpi-label'>🌡️ Météo</span></div>
            <div class='kpi-card'><span class='kpi-value'>85%</span><span class='kpi-label'>🌸 Flore</span></div>
            <div class='kpi-card'><span class='kpi-value'>3 km</span><span class='kpi-label'>🛰️ Portée</span></div>
        </div>
    """, unsafe_allow_html=True)

    # --- 3. ACTIONS RAPIDES (L'UX Play Store) ---
    st.markdown("### ⚡ Actions Rapides")

    # Onglet Flore
    with st.expander("🌳 **IDENTIFIER LA FLORE LOCALE**", expanded=True):
        st.write("Quels arbres voyez-vous dans vos 5 km ?")
        col1, col2 = st.columns(2)
        with col1:
            st.button("🥭 Manguier")
            st.button("🥜 Arachide")
        with col2:
            st.button("🌳 Anacardier")
            st.button("🌿 Kinkeliba")

    # Carte interactive
    with st.expander("📍 **SURVEILLER MA ZONE**"):
        m = folium.Map(location=[lat, lon], zoom_start=14)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        folium.Circle([lat, lon], radius=3000, color='green', fill=True, opacity=0.1).add_to(m)
        folium.Circle([lat, lon], radius=5000, color='red', fill=False).add_to(m)
        st_folium(m, width=330, height=300)

    # Export
    st.markdown("---")
    if st.button("📊 GÉNÉRER MON BILAN D'EXPERTISE"):
        st.balloons()
        st.success("Rapport PDF YAMB prêt !")

else:
    st.markdown("""
        <div style='text-align:center; padding:50px;'>
            <div style='font-size:50px;'>🛰️</div>
            <b>YAMB recherche votre position...</b><br>
            <small>Veuillez autoriser le GPS pour l'expertise du site.</small>
        </div>
    """, unsafe_allow_html=True)
