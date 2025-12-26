import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import urllib.parse
from datetime import datetime

# --- 1. CONFIGURATION ÉLITE ---
st.set_page_config(
    page_title="YAMB - Abeilles du Sénégal",
    page_icon="🐝",
    layout="centered"
)

# --- 2. CHARTE GRAPHIQUE HAUTE LISIBILITÉ ---
st.markdown("""
    <style>
    /* Fond très clair pour lecture au soleil */
    .stApp { background-color: #FFFFFF; color: #000000; }
    
    /* En-tête Prestige Abeilles du Sénégal */
    .main-header {
        background-color: #004d26; /* Vert profond */
        color: #FCD116; /* Or pur */
        padding: 25px;
        border-radius: 0 0 30px 30px;
        text-align: center;
        border-bottom: 5px solid #FCD116;
        margin-bottom: 20px;
    }
    .company-name {
        font-size: 12px;
        letter-spacing: 2px;
        font-weight: bold;
        color: #FFFFFF;
        text-transform: uppercase;
    }
    
    /* Boutons et éléments de navigation */
    .stButton>button {
        background-color: #004d26 !important;
        color: white !important;
        border-radius: 10px;
        border: 2px solid #FCD116;
        font-weight: bold;
        width: 100%;
    }
    
    /* Style Spécial Bouton SOS */
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
        margin-top: 10px;
    }
    
    /* Tabs lisibles */
    .stTabs [data-baseweb="tab-list"] { background-color: #f1f1f1; border-radius: 10px; }
    .stTabs [data-baseweb="tab"] { color: #004d26 !important; font-size: 16px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FONCTION AIDE VOCALE ---
def parler(texte):
    st.components.v1.html(f"""
        <script>
        var msg = new SpeechSynthesisUtterance("{texte}");
        msg.lang = 'fr-FR';
        window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

# --- 4. ENTÊTE OFFICIEL ---
st.markdown("""
    <div class='main-header'>
        <div class='company-name'>Abeilles du Sénégal</div>
        <h1 style='margin:0; font-size: 40px;'>YAMB</h1>
        <p style='color:white; margin:0;'>L'assistant apicole intelligent</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. NAVIGATION ---
tabs = st.tabs(["🍯 RÉCOLTE", "📸 TERRAIN", "🚨 SOS"])

with tabs[0]:
    if st.button("🔊 ÉCOUTER LES INSTRUCTIONS (RÉCOLTE)"):
        parler("Calculateur de récolte Abeilles du Sénégal. Écrivez le nombre de vos ruches.")
    st.subheader("Estimation de la production")
    nb = st.number_input("Combien de ruches ?", min_value=1, value=10)
    st.metric("Récolte prévue", f"{nb * 12} kg", "Miel Bio")

with tabs[1]:
    if st.button("🔊 ÉCOUTER LES INSTRUCTIONS (PHOTO)"):
        parler("Prenez une photo de votre rucher pour le suivi technique.")
    st.subheader("Photo de contrôle")
    st.camera_input("Scanner la ruche")

with tabs[2]:
    if st.button("🔊 ÉCOUTER LES INSTRUCTIONS (URGENCE)"):
        parler("Alerte urgence. Choisissez le problème et appuyez sur le bouton vert pour prévenir Abeilles du Sénégal.")
    st.subheader("Signaler une urgence")
    danger = st.selectbox("Quel est le problème ?", ["🔥 Feu", "🥷 Vol", "🐝 Maladie"])
    
    msg = f"🚨 *ALERTE ABEILLES DU SÉNÉGAL*\n📍 Problème : {danger}\nLocalisation envoyée via l'application YAMB."
    url = f"https://wa.me/?text={urllib.parse.quote(msg)}"
    st.markdown(f'<a href="{url}" target="_blank" class="whatsapp-btn">🟢 ENVOYER ALERTE WHATSAPP</a>', unsafe_allow_html=True)

# --- 6. CARTE SATELLITE ---
st.divider()
st.markdown("### 📍 Emplacement de vos ruches")
loc = get_geolocation()
if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    m = folium.Map(location=[lat, lon], zoom_start=16)
    # Couche Satellite Google pour voir les arbres
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
    folium.Marker([lat, lon], popup="Mon Rucher", icon=folium.Icon(color='green')).add_to(m)
    st_folium(m, width="100%", height=300)
else:
    st.info("📡 GPS en attente... Cliquez sur 'Autoriser' si votre téléphone le demande.")

# --- 7. PIED DE PAGE ---
st.markdown("<p style='text-align:center; padding:20px; font-weight:bold;'>© 2025 Abeilles du Sénégal</p>", unsafe_allow_html=True)
