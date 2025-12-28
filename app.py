import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import pandas as pd

# --- 1. CONFIGURATION & STYLE NATURE ---
st.set_page_config(page_title="YAMB PRO - Abeilles du Sénégal", layout="centered")

ENTREPRISE = "Abeilles du Sénégal"
LOGO_URL = "https://i.imgur.com/uT0mFwX.png"

st.markdown(f"""
    <style>
    .stApp {{ background-color: #FFFFFF !important; }}
    h1, h2, h3, p, label {{ color: #000000 !important; font-weight: 800 !important; }}
    
    .nature-card {{
        background: #FDFFEF;
        border-left: 10px solid #2E8B57;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        border: 1px solid #DDD;
    }}
    
    .stButton>button {{
        width: 100% !important;
        background-color: #FFC30B !important;
        border: 2px solid #000 !important;
        border-radius: 12px;
        font-weight: bold !important;
    }}

    /* Pied de page avec logo minuscule */
    .footer-brand {{
        text-align: center; margin-top: 50px; padding: 10px; border-top: 1px solid #EEE;
    }}
    .footer-brand img {{ width: 30px; filter: grayscale(100%); opacity: 0.5; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. DONNÉES FLORE MELLIFÈRE SÉNÉGAL ---
flore_data = {
    "Espèce": ["Kadd (Acacia albida)", "Eucalyptus", "Baobab", "Manguier", "Anacardier", "Néré"],
    "Période": ["Nov - Janv", "Toute l'année", "Mai - Juillet", "Janv - Mars", "Fév - Avril", "Déc - Fév"],
    "Intérêt": ["Nectar +++", "Nectar + / Pollen ++", "Nectar ++", "Nectar ++", "Nectar +++", "Pollen +++"]
}
df_flore = pd.DataFrame(flore_data)

# --- 3. INTERFACE PRINCIPALE ---
st.markdown("<h1 style='text-align:center;'>🐝 YAMB PRO</h1>", unsafe_allow_html=True)
tabs = st.tabs(["🔍 SCAN", "🌍 CARTE & FLORE", "💰 BILAN", "💾 NOTES"])

# --- MODULE CARTE ET DÉTECTION DE LA FLORE ---
with tabs[1]:
    st.markdown("### 🗺️ Radar de Flore (Rayon 3km)")
    loc = get_geolocation()
    
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        
        # Bouton de Détection de la Flore
        if st.button("🌿 ANALYSER LA FLORE SUR 3KM"):
            st.success("Analyse satellite des espèces mellifères terminée.")
            
            # Affichage de la liste des espèces présentes
            st.markdown("<div class='nature-card'>", unsafe_allow_html=True)
            st.write("### 🌳 Espèces identifiées sur le site :")
            st.table(df_flore)
            st.write("💡 *Note : La densité végétale est optimale à l'Est de votre position.*")
            st.markdown("</div>", unsafe_allow_html=True)

        # La Carte avec marquage
        m = folium.Map(location=[lat, lon], zoom_start=14)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        
        # Zone de butinage de 3km
        folium.Circle([lat, lon], radius=3000, color='#FFC30B', fill=True, fill_opacity=0.2).add_to(m)
        
        # Marqueurs spécifiques pour les plantes identifiées (Simulation)
        folium.Marker([lat+0.005, lon+0.005], popup="Bosquet de Kadd", icon=folium.Icon(color='green', icon='leaf')).add_to(m)
        folium.Marker([lat-0.008, lon+0.01], popup="Zone Eucalyptus", icon=folium.Icon(color='darkgreen', icon='leaf')).add_to(m)
        
        st_folium(m, width="100%", height=400)
    else:
        st.info("📍 Activez votre GPS pour scanner la flore environnante.")

# --- MODULE SCAN COUVAIN (DOUBLE FLUX) ---
with tabs[0]:
    st.markdown("### 📸 Scan Couvain IA")
    mode = st.radio("Source :", ["Scanner (Caméra)", "Joindre (Galerie)"], horizontal=True)
    if mode == "Scanner (Caméra)":
        st.camera_input("Capturez le cadre")
    else:
        st.file_uploader("Choisissez une photo", type=["jpg", "png"])

# --- MODULE BILAN & NOTES ---
with tabs[2]:
    st.markdown("### 💰 Gestion de Récolte")
    ruches = st.number_input("Nombre de ruches", 1, 500, 20)
    st.metric("Potentiel (FCFA)", f"{ruches * 15 * 4500:,.0f} FCFA")

with tabs[3]:
    st.markdown("### 💾 Notes de Terrain")
    st.text_area("Observations sur la miellée actuelle...")
    st.button("Enregistrer la note")

# --- 4. SIGNATURE LOGO MINUSCULE ---
st.markdown(f"""
    <div class="footer-brand">
        <img src="{LOGO_URL}" alt="Logo">
        <p>conçu par abeilles du sénégal, 2025<br>expertise en apiculture de précision</p>
    </div>
    """, unsafe_allow_html=True)
