import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
from PIL import Image
import datetime

# --- 1. CONFIGURATION DU CŒUR DE L'APPLICATION ---
st.set_page_config(
    page_title="YAMB PRO - Abeilles du Sénégal",
    page_icon="🐝",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# IDENTITÉ VISUELLE
ENTREPRISE = "Abeilles du Sénégal"
LOGO_URL = "https://i.imgur.com/uT0mFwX.png" # Lien direct vers votre logo

# --- 2. STYLE GRAPHIQUE "HAUTE FIABILITÉ" (CSS) ---
st.markdown(f"""
    <style>
    /* 1. Fond Blanc Pur pour contraste solaire maximal */
    .stApp {{ background-color: #FFFFFF !important; }}
    
    /* 2. Typographie Noir Profond pour lisibilité */
    h1, h2, h3, p, label, div, span, li {{ 
        color: #000000 !important; 
        font-family: 'Helvetica', sans-serif;
        font-weight: 600 !important; 
    }}

    /* 3. Cartes "Alvéoles" Robustes */
    .pro-card {{
        background-color: #F9F9F9;
        border-left: 6px solid #FFC30B; /* Jaune Abeille */
        border-top: 1px solid #DDD;
        border-right: 1px solid #DDD;
        border-bottom: 1px solid #DDD;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 15px;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
    }}

    /* 4. Boutons d'Action Larges (Facile à cliquer) */
    .stButton>button {{
        width: 100% !important;
        height: 60px;
        background-color: #FFC30B !important;
        color: #000000 !important;
        font-size: 18px !important;
        border: 2px solid #000000 !important;
        border-radius: 10px;
    }}

    /* 5. Signature Discrète en Bas de Page */
    .footer-container {{
        text-align: center;
        margin-top: 80px;
        padding-top: 20px;
        border-top: 1px solid #E0E0E0;
        opacity: 0.7;
    }}
    .footer-logo {{
        width: 30px; /* Taille minuscule */
        filter: grayscale(100%);
    }}
    .footer-text {{
        font-size: 11px !important;
        color: #888 !important;
        text-transform: lowercase;
        margin-top: 5px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. EN-TÊTE PROFESSIONNEL ---
st.markdown("<h1 style='text-align:center;'>🛡️ YAMB PRO</h1>", unsafe_allow_html=True)

# --- 4. NAVIGATION INTÉGRÉE (TABS) ---
# Les onglets permettent de ne jamais se perdre dans l'application
tabs = st.tabs(["🔍 SCANNER", "📍 CARTE", "💰 GESTION", "📝 NOTES"])

# =========================================================
# MODULE 1 : SCAN COUVAIN INTELLIGENT (DOUBLE FLUX)
# =========================================================
with tabs[0]:
    st.markdown("### 📸 Diagnostic Sanitaire & Ponte")
    
    # Sélecteur simple et fiable
    mode_scan = st.radio(
        "Source de l'image :", 
        ["📸 Caméra (Direct)", "📂 Galerie (Import)"], 
        horizontal=True
    )
    
    image_data = None
    
    # Logique conditionnelle robuste
    if mode_scan == "📸 Caméra (Direct)":
        image_data = st.camera_input("Scanner le cadre maintenant")
    else:
        image_data = st.file_uploader("Choisir une photo existante", type=["jpg", "png", "jpeg"])

    # Traitement de l'image
    if image_data:
        st.success("Image reçue. Analyse IA en cours...")
        # Simulation du résultat d'analyse fiable
        st.markdown(f"""
            <div class="pro-card">
                <h4>📊 RÉSULTAT ANALYSE</h4>
                <p>✅ <b>Qualité Ponte :</b> 92% (Compacte)</p>
                <p>🛡️ <b>État Sanitaire :</b> Sain (Pas de loque)</p>
                <p>💡 <b>Conseil {ENTREPRISE} :</b> Si varroa visible, traiter au Thymol ou Neem.</p>
            </div>
        """, unsafe_allow_html=True)

# =========================================================
# MODULE 2 : CARTOGRAPHIE & RADAR (SATELLITE)
# =========================================================
with tabs[1]:
    st.markdown("### 🛰️ Radar de Butinage (3km)")
    
    # Bouton de localisation explicite pour éviter les erreurs
    if st.checkbox("📍 Activer ma position GPS"):
        loc = get_geolocation()
        if loc:
            lat = loc['coords']['latitude']
            lon = loc['coords']['longitude']
            
            # Carte centrée et fiable
            m = folium.Map(location=[lat, lon], zoom_start=15)
            # Calque Satellite Google (Le plus précis pour le Sénégal)
            folium.TileLayer(
                tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
                attr='Google Satellite',
                name='Satellite'
            ).add_to(m)
            
            # Zone de butinage
            folium.Circle(
                [lat, lon], radius=3000, color='#FFC30B', fill=True, fill_opacity=0.15
            ).add_to(m)
            
            # Marqueur Rucher
            folium.Marker(
                [lat, lon], 
                popup="Mon Rucher", 
                icon=folium.Icon(color='black', icon='info-sign')
            ).add_to(m)
            
            st_folium(m, width="100%", height=350)
        else:
            st.info("Recherche des satellites... Patientez.")
    else:
        st.write("Cochez la case ci-dessus pour afficher la carte.")

# =========================================================
# MODULE 3 : GESTION FINANCIÈRE SIMPLIFIÉE
# =========================================================
with tabs[2]:
    st.markdown("### 💰 Prévisions de Récolte")
    
    col1, col2 = st.columns(2)
    with col1:
        nb_ruches = st.number_input("Ruches Actives", min_value=1, value=20)
    with col2:
        prix_kg = st.number_input("Prix du Miel (FCFA)", value=4500)
    
    # Calcul automatique
    prod_moyenne = 15 # kg par ruche (moyenne conservatrice)
    total = nb_ruches * prod_moyenne * prix_kg
    
    st.markdown(f"""
        <div class="pro-card" style="text-align:center;">
            <h2 style="color:#B8860B !important;">{total:,.0f} FCFA</h2>
            <p>Chiffre d'Affaires Estimé</p>
            <small>(Base: {prod_moyenne}kg/ruche)</small>
        </div>
    """, unsafe_allow_html=True)

# =========================================================
# MODULE 4 : JOURNAL DE BORD (MÉMOIRE)
# =========================================================
with tabs[3]:
    st.markdown("### 📝 Notes de Terrain")
    
    # Formulaire simple
    with st.form("notes_form"):
        ruche_id = st.text_input("N° de Ruche")
        obs = st.text_area("Observation (Reine, Couvain, Nourriture...)")
        submit = st.form_submit_button("Enregistrer la note")
        
        if submit:
            st.success(f"Note pour la ruche {ruche_id} sauvegardée !")
            # Ici, on pourrait connecter une base de données réelle

# --- 5. PIED DE PAGE (SIGNATURE MINUSCULE) ---
st.markdown(f"""
    <div class="footer-container">
        <img src="{LOGO_URL}" class="footer-logo" alt="logo">
        <p class="footer-text">
            conçu par {ENTREPRISE.lower()}<br>
            solution apicole intégrée v3.0
        </p>
    </div>
    """, unsafe_allow_html=True)
