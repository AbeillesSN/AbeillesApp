import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import urllib.parse
from datetime import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="YAMB - Abeilles du Sénégal",
    page_icon="🐝",
    layout="centered"
)

# --- 2. STYLE HAUTE LISIBILITÉ (CORRIGÉ) ---
st.markdown("""
    <style>
    /* Fond de page blanc pur pour le contraste */
    .stApp { background-color: #FFFFFF; }
    
    /* En-tête vert profond Abeilles du Sénégal */
    .main-header {
        background-color: #004d26;
        color: #FCD116;
        padding: 25px;
        border-radius: 0 0 30px 30px;
        text-align: center;
        border-bottom: 5px solid #FCD116;
        margin-bottom: 20px;
    }

    /* Texte de production (CORRECTION LISIBILITÉ) */
    .stMetric label {
        color: #000000 !important; /* Texte noir pour l'étiquette */
        font-weight: bold !important;
        font-size: 1.2rem !important;
    }
    div[data-testid="stMetricValue"] {
        color: #004d26 !important; /* Vert foncé pour le chiffre */
        font-size: 3rem !important;
        font-weight: 800 !important;
    }
    div[data-testid="stMetricDelta"] {
        color: #00853f !important; /* Vert clair pour le delta */
        background-color: #e8f5e9;
        padding: 5px;
        border-radius: 5px;
    }

    /* Titres noirs */
    h1, h2, h3 { color: #000000 !important; }
    
    .whatsapp-btn {
        background-color: #25D366;
        color: white !important;
        padding: 20px;
        border-radius: 15px;
        text-decoration: none;
        display: block;
        text-align: center;
        font-weight: 900;
        font-size: 1.2em;
        border: 3px solid #075E54;
    }
    </style>
    """, unsafe_allow_html=True)

def parler(texte):
    st.components.v1.html(f"""<script>var msg = new SpeechSynthesisUtterance("{texte}"); msg.lang = 'fr-FR'; window.speechSynthesis.speak(msg);</script>""", height=0)

# --- 3. ENTÊTE ---
st.markdown("""
    <div class='main-header'>
        <div style='font-size:12px; font-weight:bold; color:white;'>ABEILLES DU SÉNÉGAL</div>
        <h1 style='margin:0; color:#FCD116;'>YAMB</h1>
        <p style='color:white; margin:0;'>Unité d'Élite Apicole</p>
    </div>
    """, unsafe_allow_html=True)

# --- 4. NAVIGATION ---
tabs = st.tabs(["🍯 RÉCOLTE", "📸 TERRAIN", "🚨 SOS"])

with tabs[0]:
    if st.button("🔊 ÉCOUTER (Aide Récolte)"):
        parler("Calculateur Abeilles du Sénégal. Indiquez le nombre de ruches pour voir votre production.")
    
    st.header("Estimation de la production")
    
    # Sélecteur de ruches
    nb_ruches = st.number_input("Combien de ruches avez-vous ?", min_value=1, value=10, step=1)
    
    # Calcul et Affichage (LISIBILITÉ MAXIMALE)
    production = nb_ruches * 12
    st.metric(label="Récolte prévue (kg)", value=f"{production} kg", delta="Miel 100% Bio")
    
    st.markdown("---")
    st.write("**Conseil :** Cette estimation se base sur une moyenne de 12kg par ruche.")

with tabs[1]:
    st.header("Photo Terrain")
    st.camera_input("Prendre une photo")

with tabs[2]:
    st.header("Signalement Urgent")
    danger = st.selectbox("Urgence :", ["🔥 Incendie", "🥷 Vol", "🐝 Mortalité"])
    msg = f"🚨 *ABEILLES DU SÉNÉGAL* : {danger} signalé via YAMB."
    url = f"https://wa.me/?text={urllib.parse.quote(msg)}"
    st.markdown(f'<a href="{url}" target="_blank" class="whatsapp-btn">🟢 ENVOYER L\'ALERTE</a>', unsafe_allow_html=True)

# --- 5. CARTE ---
st.markdown("### 📍 Emplacement de vos ruches")
loc = get_geolocation()
if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    m = folium.Map(location=[lat, lon], zoom_start=16)
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
    folium.Marker([lat, lon], icon=folium.Icon(color='green')).add_to(m)
    st_folium(m, width="100%", height=300)
else:
    st.info("📡 GPS en attente de signal...")

st.markdown("<p style='text-align:center; font-weight:bold; color:#004d26;'>© 2025 Abeilles du Sénégal</p>", unsafe_allow_html=True)
