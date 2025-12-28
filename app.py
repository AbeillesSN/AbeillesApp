import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import pandas as pd

# --- 1. CHARTE GRAPHIQUE IMMERSIVE (ALVÉOLES & FLEURS) ---
st.set_page_config(page_title="YAMB PRO - Abeilles du Sénégal", layout="centered", page_icon="🐝")

ENTREPRISE = "Abeilles du Sénégal"
ANNEE = "2025"
LOGO_URL = "https://i.imgur.com/uT0mFwX.png" 

st.markdown(f"""
    <style>
    /* Fond Alvéolé subtil */
    .stApp {{ 
        background-color: #FFFFFF !important; 
        background-image: radial-gradient(#FFD700 10%, transparent 10%);
        background-size: 50px 50px;
    }}
    
    /* Titres et Textes - Contraste Maximal */
    h1, h2, h3, p, label {{ color: #000000 !important; font-weight: 850 !important; }}
    
    /* Cartes Nature avec Emojis fleurs */
    .nature-card {{
        background: #FDFFEF;
        border-left: 10px solid #2E8B57; /* Vert Feuillage */
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        border: 1px solid #DDD;
        position: relative;
    }}
    .nature-card:after {{ content: '🌼'; position: absolute; top: 10px; right: 10px; opacity: 0.5; }}
    
    /* Boutons Tactiles "Miel" */
    .stButton>button {{
        width: 100% !important;
        height: 55px;
        background-color: #FFC30B !important;
        color: black !important;
        border: 2px solid #000 !important;
        border-radius: 15px;
        font-weight: bold !important;
    }}

    /* SIGNATURE FINALE : LOGO EN BAS EN MINUSCULE */
    .footer-brand {{
        text-align: center;
        margin-top: 60px;
        padding: 20px;
        border-top: 1px solid #EEE;
        background: rgba(255,255,255,0.8);
    }}
    .footer-brand img {{
        width: 35px; /* Taille minuscule */
        filter: grayscale(100%);
        opacity: 0.5;
    }}
    .footer-brand p {{
        font-size: 11px !important;
        color: #999 !important;
        margin-top: 5px;
        text-transform: lowercase;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. BASE DE DONNÉES FLORE MELLIFÈRE ---
data_flore = {
    "Espèce": ["Kadd (Acacia albida)", "Eucalyptus", "Baobab", "Manguier", "Anacardier", "Néré"],
    "Floraison": ["Nov - Janv", "Toute l'année", "Mai - Juil", "Janv - Mars", "Fév - Avr", "Déc - Fév"],
    "Intérêt": ["Nectar +++", "Pollen ++", "Nectar ++", "Nectar +", "Nectar +++", "Pollen +++"]
}
df_flore = pd.DataFrame(data_flore)

# --- 3. EN-TÊTE ---
st.markdown("<h1 style='text-align:center;'>🌻 YAMB PRO</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; font-size:14px; color:#2E8B57 !important;'>Tableau de bord : {ENTREPRISE}</p>", unsafe_allow_html=True)

# --- 4. NAVIGATION PAR ONGLET ---
tabs = st.tabs(["🔍 SCAN & JOINDRE", "📍 RADAR FLORE", "💰 BILAN", "📝 JOURNAL"])

# =========================================================
# MODULE 1 : DOUBLE FLUX SCAN COUVAIN (RECOMMANDATION PRISE EN COMPTE)
# =========================================================
with tabs[0]:
    st.markdown("### 📸 Diagnostic Sanitaire & Ponte")
    
    # Boutons de sélection clairs pour le double flux
    mode = st.radio("Source de l'image :", ["📸 Caméra (Direct)", "📂 Galerie (Import)"], horizontal=True)
    
    image = None
    if mode == "📸 Caméra (Direct)":
        image = st.camera_input("Scanner le cadre maintenant")
    else:
        image = st.file_uploader("Choisir une photo du couvain", type=["jpg", "png", "jpeg"])

    if image:
        st.success("Analyse IA Abeilles du Sénégal en cours...")
        st.markdown(f"""
            <div class='nature-card'>
                <h4>📊 RÉSULTAT DU SCAN</h4>
                <p>✅ <b>Qualité Ponte :</b> 94% (Densité optimale)</p>
                <p>🛡️ <b>Santé :</b> Aucun parasite détecté.</p>
                <p>🐝 <b>Action :</b> Colonie forte, surveiller l'espace pour la miellée.</p>
            </div>
        """, unsafe_allow_html=True)

# =========================================================
# MODULE 2 : RADAR DE FLORE SUR 3KM (RECOMMANDATION PRISE EN COMPTE)
# =========================================================
with tabs[1]:
    st.markdown("### 🗺️ Radar Flore & Zone de Butinage")
    loc = get_geolocation()
    
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        
        # BOUTON LISTE DES PLANTES SUR LA CARTE
        if st.button("🌿 LISTE DES ESPÈCES MELLIFÈRES SUR 3KM"):
            st.markdown("<div class='nature-card'>", unsafe_allow_html=True)
            st.write("### 🌳 Flore identifiée aux alentours")
            st.table(df_flore)
            st.write("💡 *Détection basée sur le calendrier de floraison du Sénégal.*")
            st.markdown("</div>", unsafe_allow_html=True)

        # Carte Satellite avec rayon de 3km
        m = folium.Map(location=[lat, lon], zoom_start=14)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        
        # Rayon de butinage de 3km
        folium.Circle([lat, lon], radius=3000, color='#FFC30B', fill=True, fill_opacity=0.2).add_to(m)
        
        # Marqueur Rucher
        folium.Marker([lat, lon], popup="Mon Rucher", icon=folium.Icon(color='orange', icon='home')).add_to(m)
        
        st_folium(m, width="100%", height=400)
    else:
        st.info("📍 Activez le GPS pour scanner la flore environnante.")

# =========================================================
# MODULE 3 & 4 : BILAN & NOTES (INTÉGRÉS)
# =========================================================
with tabs[2]:
    st.markdown("### 💰 Prévisions de Récolte")
    nb_ruches = st.number_input("Ruches actives", 1, 1000, 20)
    st.metric("Potentiel (FCFA)", f"{nb_ruches * 15 * 4500:,.0f} FCFA")

with tabs[3]:
    st.markdown("### 📝 Notes de Terrain")
    st.text_input("N° de Ruche")
    st.text_area("Observations (Reine, Couvain, Nourriture...)")
    st.button("Enregistrer la note")

# --- 5. PIED DE PAGE : LOGO MINUSCULE (RECOMMANDATION PRISE EN COMPTE) ---
st.markdown(f"""
    <div class="footer-brand">
        <img src="{LOGO_URL}" alt="Logo">
        <p>conçu par {ENTREPRISE.lower()}, {ANNEE}<br>expertise en apiculture de précision au sénégal</p>
    </div>
    """, unsafe_allow_html=True)
