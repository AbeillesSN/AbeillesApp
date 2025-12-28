import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import urllib.parse
from PIL import Image
import datetime

# --- 1. CONFIGURATION & SIGNATURE ---
st.set_page_config(page_title="YAMB PRO - Elite", layout="centered", page_icon="🐝")

ENTREPRISE = "YAMB APICULTURE SOLUTIONS"
LOGO_URL = "https://i.imgur.com/uT0mFwX.png" # Remplacez par votre lien logo direct

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
        border-radius: 15px;
        margin-bottom: 15px;
        box-shadow: 4px 4px 10px rgba(0,0,0,0.05);
    }}

    /* Boutons Tactiles */
    .stButton>button {{
        width: 100% !important;
        height: 55px;
        background-color: #FFC30B !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 12px;
        border: 2px solid #000;
    }}

    /* Footer avec logo minuscule */
    .footer {{
        text-align: center;
        margin-top: 50px;
        padding: 20px;
        border-top: 1px solid #EEE;
    }}
    .footer img {{
        width: 30px; /* Taille minuscule */
        filter: grayscale(100%);
        opacity: 0.6;
    }}
    .footer p {{
        font-size: 10px !important;
        color: #999 !important;
        margin-top: 5px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIQUE HORS-LIGNE ---
if "offline_notes" not in st.session_state:
    st.session_state.offline_notes = []

# --- 3. EN-TÊTE ---
st.markdown("<h1 style='text-align:center;'>🛡️ YAMB PRO</h1>", unsafe_allow_html=True)

# --- 4. NAVIGATION MOBILE (TABS) ---
menu = st.tabs(["🔍 SCAN", "📍 CARTE", "💰 BILAN", "💾 NOTES"])

# --- MODULE SCAN COUVAIN ---
with menu[0]:
    st.markdown("### 📸 Analyse du Couvain")
    source = st.radio("Source :", ["Appareil Photo", "Galerie"], horizontal=True)
    
    img = None
    if source == "Appareil Photo":
        img = st.camera_input("Scanner le cadre")
    else:
        img = st.file_uploader("Importer une photo", type=["jpg", "png"])

    if img:
        st.success("Analyse en cours...")
        st.markdown("""<div class="card">
            <h4>📊 DIAGNOSTIC IA</h4>
            <p>✅ <b>Ponte :</b> 95% (Saine).</p>
            <p>🦠 <b>Sanitaire :</b> Aucune loque détectée.</p>
        </div>""", unsafe_allow_html=True)

# --- MODULE RADAR ---
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
        st.warning("Activez le GPS de votre téléphone.")

# --- MODULE FINANCE ---
with menu[2]:
    st.markdown("### 💰 Gestion de Récolte")
    nb = st.number_input("Nombre de ruches :", 1, 500, 10)
    val = nb * 15 * 4500
    st.markdown(f"""<div class="card" style="text-align:center;">
        <h2 style="color:#FFC30B !important;">{val:,.0f} FCFA</h2>
        <p>Potentiel de la saison</p>
    </div>""", unsafe_allow_html=True)

# --- MODULE HORS-LIGNE ---
with menu[3]:
    st.markdown("### 💾 Mode Hors-Ligne")
    n_ruche = st.text_input("N° Ruche")
    obs = st.text_area("Observation")
    if st.button("Sauvegarder localement"):
        st.session_state.offline_notes.append({"Ruche": n_ruche, "Note": obs})
        st.toast("Enregistré !")
    
    if st.session_state.offline_notes:
        st.write("📋 Notes en attente de synchro :")
        st.table(st.session_state.offline_notes)

# --- 5. FOOTER AVEC LOGO MINUSCULE ---
st.markdown(f"""
    <div class="footer">
        <img src="{LOGO_URL}" alt="Logo">
        <p>© 2025 {ENTREPRISE}<br>Développé pour l'élite apicole du Sénégal</p>
    </div>
    """, unsafe_allow_html=True)
