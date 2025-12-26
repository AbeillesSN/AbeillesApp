import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import urllib.parse
from datetime import datetime
from PIL import Image

# --- CONFIGURATION DE L'APPLICATION ---
st.set_page_config(page_title="YAMB - Abeilles du Sénégal", layout="centered", page_icon="🐝")

# --- CHARTE GRAPHIQUE PRESTIGE (Mode Nuit Auto) ---
st.markdown("""
    <style>
    :root { --yamb-gold: #FFC107; --yamb-green: #1B5E20; --yamb-amber: #FF8F00; }
    @media (prefers-color-scheme: dark) { 
        .stApp { background-color: #0E1117; color: #E0E0E0; }
    }
    .premium-header {
        background: linear-gradient(135deg, #1B5E20 0%, #051A07 100%);
        color: var(--yamb-gold);
        padding: 30px;
        border-radius: 0 0 40px 40px;
        text-align: center;
        border-bottom: 5px solid var(--yamb-amber);
        margin-bottom: 20px;
    }
    .whatsapp-btn {
        background-color: #25D366;
        color: white !important;
        padding: 15px;
        border-radius: 12px;
        text-decoration: none;
        display: block;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# --- DONNÉES IA ---
potentials = {"Anacardier": 15, "Manguier": 10, "Kad": 20, "Néré": 12, "Flore Sauvage": 8}

# --- ENTÊTE ---
st.markdown("<div class='premium-header'><h1>🐝 YAMB</h1><p>UNITÉ D'ÉLITE APICOLE • SÉNÉGAL</p></div>", unsafe_allow_html=True)

loc = get_geolocation()

if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    
    # NAVIGATION
    tabs = st.tabs(["📊 Diagnostic & IA", "📸 Terrain", "📖 Journal", "🚨 SOS"])

    with tabs[0]: # DIAGNOSTIC & IA
        st.subheader("🤖 Conseiller IA")
        nb = st.number_input("Nombre de ruches :", min_value=1, value=10)
        flore = st.multiselect("Flore détectée :", list(potentials.keys()), default=["Anacardier"])
        if flore:
            rendement = (sum([potentials[p] for p in flore]) / len(flore)) * nb
            st.info(f"🚀 Rendement estimé : **{rendement:.1f} kg de miel**")

    with tabs[1]: # PHOTO & FLORE
        st.subheader("📸 Identification Visuelle")
        photo_expert = st.camera_input("Prendre une photo (fleur/ruche)")
        if photo_expert: st.success("Photo enregistrée dans le rapport.")

    with tabs[2]: # JOURNAL
        st.subheader("📖 Journal de Bord")
        st.date_input("Date", datetime.now())
        st.select_slider("État de la reine", options=["Mauvais", "Moyen", "Excellent"])
        st.text_area("Observations libres")

    with tabs[3]: # ALERTE SOS
        st.subheader("🚨 Al
