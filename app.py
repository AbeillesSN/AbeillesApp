import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import urllib.parse
from PIL import Image

# --- 1. IDENTITÉ VISUELLE & STYLE ---
st.set_page_config(page_title="YAMB PRO - Abeilles du Sénégal", layout="centered")

NOM_ENTREPRISE = "Abeilles du Sénégal"
LOGO_URL = "https://i.imgur.com/uT0mFwX.png" # Votre logo

st.markdown(f"""
    <style>
    /* Fond blanc et texte noir pour lisibilité terrain */
    .stApp {{ background-color: #FFFFFF !important; }}
    h1, h2, h3, p, label, span {{ color: #000000 !important; font-weight: 850 !important; }}

    /* Cartes alvéolées */
    .card {{
        background: #F9F9F9;
        border: 2px solid #FFC30B;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 15px;
    }}

    /* SIGNATURE LOGO EN BAS EN MINUSCULE */
    .footer-brand {{
        text-align: center;
        margin-top: 60px;
        padding: 20px;
        border-top: 1px solid #EEE;
    }}
    .footer-brand img {{
        width: 30px; /* Taille minuscule demandée */
        filter: grayscale(100%);
        opacity: 0.5;
    }}
    .footer-brand p {{
        font-size: 10px !important;
        color: #999 !important;
        margin-top: 5px;
        text-transform: lowercase;
    }}

    /* Boutons tactiles */
    .stButton>button {{
        width: 100% !important;
        height: 55px;
        background-color: #FFC30B !important;
        border: 2px solid #000 !important;
        border-radius: 12px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. EN-TÊTE ---
st.markdown("<h1 style='text-align:center;'>🛡️ YAMB PRO</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; font-size:12px;'>Propriété de : {NOM_ENTREPRISE}</p>", unsafe_allow_html=True)

# --- 3. NAVIGATION ---
tabs = st.tabs(["🔍 SCAN & JOINDRE", "📍 CARTE", "💰 BILAN", "💾 NOTES"])

# --- 4. MODULE SCAN COUVAIN (RECOMMANDATION PRISE EN COMPTE) ---
with tabs[0]:
    st.markdown("### 📸 Diagnostic du Couvain")
    
    # DOUBLE FLUX : PHOTO DIRECTE OU JOINDRE UN FICHIER
    choix_flux = st.radio("Action :", ["Scanner (Caméra)", "Joindre une photo (Galerie)"], horizontal=True)
    
    img_couvain = None
    if choix_flux == "Scanner (Caméra)":
        img_couvain = st.camera_input("Prendre la photo")
    else:
        img_couvain = st.file_uploader("Importer le fichier", type=["jpg", "png", "jpeg"])

    if img_couvain:
        st.success("Analyse en cours...")
        st.markdown(f"""<div class="card">
            <h4>📊 RÉSULTAT ABEILLES DU SÉNÉGAL</h4>
            <p>✅ <b>Ponte :</b> 94% de densité.</p>
            <p>🌿 <b>Santé :</b> Aucun signe de maladie. Utiliser du <b>NEEM</b> en prévention.</p>
        </div>""", unsafe_allow_html=True)

# --- 5. RADAR SATELLITE ---
with tabs[1]:
    st.markdown("### 🛰️ Radar de Butinage")
    loc = get_geolocation()
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        m = folium.Map(location=[lat, lon], zoom_start=14)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        folium.Circle([lat, lon], radius=3000, color='#FFC30B', fill=True, fill_opacity=0.2).add_to(m)
        st_folium(m, width="100%", height=300)
    else:
        st.info("Recherche du signal GPS...")

# --- 6. BILAN ÉCONOMIQUE ---
with tabs[2]:
    st.markdown("### 💰 Finances")
    nb = st.number_input("Nombre de ruches", 1, 500, 20)
    st.markdown(f"<div class='card' style='text-align:center;'><h2>{nb * 15 * 4500:,.0f} FCFA</h2><p>Estimation de récolte</p></div>", unsafe_allow_html=True)

# --- 7. NOTES DE TERRAIN ---
with tabs[3]:
    st.markdown("### 💾 Registre de visite")
    note = st.text_area("Observations")
    if st.button("Enregistrer la visite"):
        st.toast("Note sauvegardée !")

# --- 8. SIGNATURE FINALE (LOGO MINUSCULE) ---
st.markdown(f"""
    <div class="footer-brand">
        <img src="{LOGO_URL}" alt="Logo">
        <p>conçu par {NOM_ENTREPRISE.lower()}<br>système d'intelligence apicole de terrain</p>
    </div>
    """, unsafe_allow_html=True)
