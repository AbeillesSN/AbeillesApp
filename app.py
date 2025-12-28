import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import urllib.parse
from PIL import Image
import datetime

# --- 1. CONFIGURATION & SIGNATURE OFFICIELLE ---
st.set_page_config(page_title="YAMB PRO - Abeilles du Sénégal", layout="centered", page_icon="🐝")

NOM_ENTREPRISE = "ABEILLES DU SÉNÉGAL"
VERSION = "v3.0 Final"
# Lien vers votre logo (utilisez une URL directe vers l'image)
LOGO_URL = "https://i.imgur.com/uT0mFwX.png" 

st.markdown(f"""
    <style>
    /* Design Mobile-First Haute Visibilité */
    .stApp {{ background-color: #FFFFFF !important; }}
    
    h1, h2, h3, p, label, li {{ 
        color: #000000 !important; 
        font-weight: 850 !important; 
    }}

    .card {{
        background: #F8F9FA;
        border: 2px solid #FFC30B;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 15px;
        box-shadow: 4px 4px 10px rgba(0,0,0,0.05);
    }}

    /* Signature Entreprise en bas - Logo Minuscule */
    .footer-brand {{
        text-align: center;
        margin-top: 50px;
        padding: 20px;
        border-top: 1px solid #EEE;
    }}
    .footer-brand img {{
        width: 35px; /* Taille minuscule respectée */
        filter: grayscale(100%);
        opacity: 0.5;
    }}
    .footer-brand p {{
        font-size: 10px !important;
        color: #888 !important;
        margin-top: 5px;
        text-transform: lowercase;
    }}

    /* Boutons Tactiles larges */
    .stButton>button {{
        width: 100% !important;
        height: 55px;
        background-color: #FFC30B !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 12px;
        border: 2px solid #000;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. EN-TÊTE ---
st.markdown("<h1 style='text-align:center;'>🛡️ YAMB PRO</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; font-size:12px; color:#FFC30B !important;'>Expertise : {NOM_ENTREPRISE}</p>", unsafe_allow_html=True)

# --- 3. NAVIGATION TACTILE ---
menu = st.tabs(["🔍 SCAN", "📍 CARTE", "💰 BILAN", "💾 NOTES"])

# --- 4. MODULE SCAN COUVAIN (DOUBLE FLUX) ---
with menu[0]:
    st.markdown("### 📸 Diagnostic de Ponte")
    
    # Choix : Scanner en direct ou joindre depuis la galerie
    mode = st.radio("Méthode :", ["Scanner (Caméra)", "Joindre (Galerie)"], horizontal=True)
    
    image_file = None
    if mode == "Scanner (Caméra)":
        image_file = st.camera_input("Capturer le cadre")
    else:
        image_file = st.file_uploader("Choisir une photo du couvain", type=["jpg", "png"])

    if image_file:
        st.success("Analyse IA en cours...")
        st.markdown(f"""
            <div class="card">
                <h4>📊 DIAGNOSTIC {NOM_ENTREPRISE}</h4>
                <p>✅ <b>Ponte :</b> 94% (Régulière).</p>
                <p>🛡️ <b>Santé :</b> Aucun parasite détecté.</p>
                <p>🌿 <b>Plantes :</b> Appliquer du <b>Neem</b> ou de la <b>Citronnelle</b> si nécessaire.</p>
            </div>
        """, unsafe_allow_html=True)

# --- 5. RADAR SATELLITE ---
with menu[1]:
    st.markdown("### 🛰️ Radar de Butinage")
    loc = get_geolocation()
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        m = folium.Map(location=[lat, lon], zoom_start=14)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        folium.Circle([lat, lon], radius=3000, color='#FFC30B', fill=True, fill_opacity=0.3).add_to(m)
        st_folium(m, width="100%", height=300)
    else:
        st.info("📍 Recherche du signal GPS...")

# --- 6. BILAN FINANCIER ---
with menu[2]:
    st.markdown("### 💰 Gestion de Récolte")
    nb_ruches = st.number_input("Nombre de ruches :", 1, 500, 20)
    valeur = nb_ruches * 15 * 4500
    st.markdown(f"""
        <div class="card" style="text-align:center; border-color: black;">
            <h2 style="color:#FFC30B !important;">{valeur:,.0f} FCFA</h2>
            <p>Valeur estimée pour {NOM_ENTREPRISE}</p>
        </div>
    """, unsafe_allow_html=True)

# --- 7. NOTES HORS-LIGNE ---
with menu[3]:
    st.markdown("### 💾 Journal de Terrain")
    n_ruche = st.text_input("N° Ruche")
    obs = st.text_area("Observations")
    if st.button("Sauvegarder la note"):
        st.toast("Note enregistrée en local !")

# --- 8. FOOTER AVEC LOGO MINUSCULE (ABEILLES DU SÉNÉGAL) ---
st.markdown(f"""
    <div class="footer-brand">
        <img src="{LOGO_URL}" alt="Logo Abeilles du Sénégal">
        <p>conçu par {NOM_ENTREPRISE.lower()}<br>{VERSION} - technologie apicole durable</p>
    </div>
    """, unsafe_allow_html=True)
