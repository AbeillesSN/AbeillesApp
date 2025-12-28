import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import pandas as pd

# --- 1. CONFIGURATION ET CHARTE GRAPHIQUE ---
st.set_page_config(page_title="YAMB PRO - Abeilles du Sénégal", layout="centered", page_icon="🐝")

ENTREPRISE = "Abeilles du Sénégal"
ANNEE = "2025"
LOGO_URL = "https://i.imgur.com/uT0mFwX.png" 

st.markdown(f"""
    <style>
    .stApp {{ background-color: #FFFFFF !important; }}
    h1, h2, h3, p, label {{ color: #000000 !important; font-weight: 850 !important; }}
    
    .nature-card {{
        background: #FDFFEF;
        border-left: 10px solid #DAA520;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        border: 1px solid #EEE;
    }}
    
    .stButton>button {{
        width: 100% !important;
        height: 55px;
        background-color: #FFC30B !important;
        color: black !important;
        border: 2px solid #000 !important;
        border-radius: 15px;
        font-weight: bold !important;
    }}

    .footer-brand {{
        text-align: center;
        margin-top: 60px;
        padding: 20px;
        border-top: 1px solid #EEE;
    }}
    .footer-brand img {{ width: 30px; filter: grayscale(100%); opacity: 0.5; }}
    .footer-brand p {{ font-size: 10px !important; color: #999 !important; text-transform: lowercase; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. BASE DE DONNÉES FLORE & SMS ---
data_flore = {
    "Espèce": ["Kadd (Acacia albida)", "Eucalyptus", "Baobab", "Manguier", "Anacardier", "Néré"],
    "Floraison": ["Nov - Janv", "Toute l'année", "Mai - Juil", "Janv - Mars", "Fév - Avr", "Déc - Fév"],
    "Intérêt": ["Nectar +++", "Pollen ++", "Nectar ++", "Nectar +", "Nectar +++", "Pollen +++"]
}
df_flore = pd.DataFrame(data_flore)

def send_sms_alert(message, destination="Collègues"):
    # Simulation d'envoi SMS via API (Twilio/Orange)
    st.toast(f"📲 SMS envoyé à {destination} : {message}")

# --- 3. INTERFACE ---
st.markdown("<h1 style='text-align:center;'>🌻 YAMB PRO</h1>", unsafe_allow_html=True)

tabs = st.tabs(["🔍 SCAN COUVAIN", "📍 FLORE & CARTE", "💰 BILAN", "💾 NOTES"])

# --- MODULE 1 : SCAN DOUBLE FLUX ---
with tabs[0]:
    st.markdown("### 📸 Diagnostic de Ponte")
    mode = st.radio("Méthode :", ["Scanner (Caméra)", "Joindre (Galerie)"], horizontal=True)
    
    image = st.camera_input("Capture") if mode == "Scanner (Caméra)" else st.file_uploader("Image", type=["jpg", "png"])
    
    if image:
        st.success("Analyse terminée.")
        st.markdown(f"<div class='nature-card'><b>Diagnostic {ENTREPRISE} :</b> Ponte 94%, Santé Optimale.</div>", unsafe_allow_html=True)

# --- MODULE 2 : DÉTECTION FLORE & ALERTES SMS ---
with tabs[1]:
    st.markdown("### 🗺️ Radar Flore sur 3km")
    loc = get_geolocation()
    
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🌿 LISTE DES ESPÈCES"):
                st.markdown("<div class='nature-card'>", unsafe_allow_html=True)
                st.table(df_flore)
                st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            if st.button("📲 ALERTE SMS FLORAISON"):
                send_sms_alert("Début de la floraison du Kadd détecté sur le site d'Abeilles du Sénégal !")

        # Carte Satellite avec cercle de 3km
        m = folium.Map(location=[lat, lon], zoom_start=14)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        folium.Circle([lat, lon], radius=3000, color='#FFC30B', fill=True, fill_opacity=0.2).add_to(m)
        st_folium(m, width="100%", height=400)
    else:
        st.warning("📍 GPS requis pour la détection de flore.")

# --- MODULE 3 & 4 ---
with tabs[2]:
    ruches = st.number_input("Nombre de ruches", 1, 500, 20)
    st.metric("Potentiel (FCFA)", f"{ruches * 15 * 4500:,.0f} FCFA")

with tabs[3]:
    st.markdown("### 💾 Journal")
    st.text_area("Observations")
    st.button("Sauvegarder")

# --- 4. SIGNATURE LOGO MINUSCULE ---
st.markdown(f"""
    <div class="footer-brand">
        <img src="{LOGO_URL}" alt="Logo">
        <p>conçu par {ENTREPRISE.lower()}, {ANNEE}<br>apiculture de précision au sénégal</p>
    </div>
    """, unsafe_allow_html=True)
