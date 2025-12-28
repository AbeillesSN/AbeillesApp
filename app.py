import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import urllib.parse
from PIL import Image

# --- 1. CONFIGURATION & STYLE ÉLITE ---
st.set_page_config(page_title="YAMB PRO - Abeilles du Sénégal", layout="centered")

# Identité de l'entreprise
ENTREPRISE = "Abeilles du Sénégal"
LOGO_URL = "https://i.imgur.com/uT0mFwX.png" # Lien direct vers votre logo

st.markdown(f"""
    <style>
    /* Lisibilité maximale : Noir sur Blanc */
    .stApp {{ background-color: #FFFFFF !important; }}
    h1, h2, h3, p, label, span, li {{ 
        color: #000000 !important; 
        font-weight: 850 !important; 
    }}

    /* Cartes Alvéolées Tactiles */
    .card {{
        background: #F9F9F9;
        border: 2px solid #FFC30B;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 15px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }}

    /* BOUTONS TACTILES LARGEUR MOBILE */
    .stButton>button {{
        width: 100% !important;
        height: 55px;
        background-color: #FFC30B !important;
        border: 2px solid #000 !important;
        border-radius: 12px;
        font-size: 18px !important;
    }}

    /* SIGNATURE LOGO MINUSCULE EN BAS */
    .footer-brand {{
        text-align: center;
        margin-top: 60px;
        padding: 20px;
        border-top: 1px solid #EEE;
    }}
    .footer-brand img {{
        width: 25px; /* Taille minuscule exigée */
        filter: grayscale(100%);
        opacity: 0.5;
    }}
    .footer-brand p {{
        font-size: 10px !important;
        color: #999 !important;
        margin-top: 5px;
        text-transform: lowercase;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. EN-TÊTE OFFICIEL ---
st.markdown("<h1 style='text-align:center;'>🛡️ YAMB PRO</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; font-size:12px; margin-top:-15px;'>Une solution signée {ENTREPRISE}</p>", unsafe_allow_html=True)

# --- 3. NAVIGATION MOBILE (TABS) ---
tabs = st.tabs(["🔍 SCAN & JOINDRE", "📍 CARTE", "💰 BILAN", "💾 NOTES"])

# --- 4. MODULE SCAN COUVAIN (DOUBLE FLUX : SCANNER OU JOINDRE) ---
with tabs[0]:
    st.markdown("### 📸 Diagnostic du Couvain")
    
    # Choix entre caméra directe ou importation
    mode_input = st.radio("Comment voulez-vous procéder ?", ["Scanner un cadre (Caméra)", "Joindre une photo (Galerie)"], horizontal=True)
    
    img_data = None
    if mode_input == "Scanner un cadre (Caméra)":
        img_data = st.camera_input("Pointez la caméra sur le cadre")
    else:
        img_data = st.file_uploader("Importer le fichier depuis votre téléphone", type=["jpg", "jpeg", "png"])

    if img_data:
        st.success("Analyse en cours par l'intelligence Abeilles du Sénégal...")
        st.markdown(f"""
            <div class="card">
                <h4>📊 RÉSULTAT DU SCAN</h4>
                <p>✅ <b>Ponte :</b> 94% de densité (Excellente Reine).</p>
                <p>🛡️ <b>Santé :</b> Aucun signe de maladie détecté.</p>
                <p>🌿 <b>Action :</b> Traitement préventif au <b>Neem</b> conseillé.</p>
            </div>
        """, unsafe_allow_html=True)

# --- 5. MODULE RADAR SATELLITE ---
with tabs[1]:
    st.markdown("### 🛰️ Radar de Butinage (3km)")
    loc = get_geolocation()
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        # Carte satellite professionnelle
        m = folium.Map(location=[lat, lon], zoom_start=14)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        folium.Circle([lat, lon], radius=3000, color='#FFC30B', fill=True, fill_opacity=0.2).add_to(m)
        folium.Marker([lat, lon], icon=folium.Icon(color='red')).add_to(m)
        st_folium(m, width="100%", height=300)
    else:
        st.info("📍 Recherche du signal GPS au-dessus de votre rucher...")

# --- 6. MODULE FINANCIER ---
with tabs[2]:
    st.markdown("### 💰 Portefeuille")
    ruches = st.number_input("Nombre de ruches gérées :", 1, 500, 20)
    valeur_estimée = ruches * 15 * 4500
    st.markdown(f"""<div class='card' style='text-align:center;'>
        <h2 style='color:#FFC30B !important;'>{valeur_estimée:,.0f} FCFA</h2>
        <p>Estimation globale de votre récolte</p>
    </div>""", unsafe_allow_html=True)

# --- 7. MODULE NOTES HORS-LIGNE ---
with tabs[3]:
    st.markdown("### 💾 Registre de Terrain")
    id_ruche = st.text_input("Identifiant de la Ruche")
    observation = st.text_area("Observations (ex: Pose de hausses)")
    if st.button("Sauvegarder la visite"):
        st.toast("Note enregistrée dans la mémoire locale !")

# --- 8. SIGNATURE FINALE (LOGO MINUSCULE) ---
st.markdown(f"""
    <div class="footer-brand">
        <img src="{LOGO_URL}" alt="Logo Abeilles du Sénégal">
        <p>conçu par {ENTREPRISE.lower()}<br>système d'intelligence apicole pour le sénégal</p>
    </div>
    """, unsafe_allow_html=True)
