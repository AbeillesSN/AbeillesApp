import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import urllib.parse
from datetime import datetime

# --- 1. CONFIGURATION DE LA PAGE & ICÔNE ---
st.set_page_config(
    page_title="YAMB - Abeilles du Sénégal",
    page_icon="🐝",
    layout="centered"
)

# --- 2. STYLE VISUEL (PREMIUM) ---
st.markdown("""
    <style>
    .stApp { background-color: #f9fbf9; }
    .main-header {
        background: linear-gradient(135deg, #1B5E20 0%, #051A07 100%);
        color: #FFC107;
        padding: 25px;
        border-radius: 0 0 30px 30px;
        text-align: center;
        border-bottom: 5px solid #FF8F00;
        margin-bottom: 20px;
    }
    .whatsapp-btn {
        background-color: #25D366;
        color: white !important;
        padding: 18px;
        border-radius: 12px;
        text-decoration: none;
        display: block;
        text-align: center;
        font-weight: bold;
        font-size: 18px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    .audio-btn {
        background-color: #FFC107;
        border: none;
        border-radius: 50%;
        padding: 10px;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. FONCTION AIDE VOCALE ---
def parler(texte):
    composant_audio = f"""
        <script>
        var msg = new SpeechSynthesisUtterance("{texte}");
        msg.lang = 'fr-FR';
        window.speechSynthesis.speak(msg);
        </script>
    """
    st.components.v1.html(composant_audio, height=0)

# --- 4. ENTÊTE ---
st.markdown("<div class='main-header'><h1>🐝 YAMB</h1><p>UNITÉ D'ÉLITE • ADANSONII</p></div>", unsafe_allow_html=True)

# --- 5. NAVIGATION PAR ONGLETS ---
tabs = st.tabs(["📊 IA & Récolte", "📸 Photo Terrain", "📖 Journal", "🚨 SOS WhatsApp"])

with tabs[0]: # DIAGNOSTIC IA
    if st.button("🔊 ÉCOUTER (Aide IA)"):
        parler("Bienvenue. Écrivez le nombre de vos ruches pour connaître votre récolte estimée.")
    st.subheader("🤖 Assistant de Rendement")
    nb = st.number_input("Nombre de ruches :", min_value=1, value=5)
    st.info(f"Rendement estimé : **{nb * 12} kg de miel**")

with tabs[1]: # CAPTURE PHOTO
    if st.button("🔊 ÉCOUTER (Aide Photo)"):
        parler("Appuyez sur le bouton pour prendre une photo d'une fleur ou d'une ruche.")
    st.subheader("📸 Identification Visuelle")
    st.camera_input("Prendre une photo")

with tabs[2]: # JOURNAL DE BORD
    st.subheader("📖 Suivi du Rucher")
    date = st.date_input("Date de visite", datetime.now())
    etat = st.select_slider("Santé des abeilles :", options=["Faible", "Moyenne", "Excellente"])
    st.text_area("Notes (ex: ponte de la reine, parasites...)")

with tabs[3]: # SYSTÈME D'ALERTE
    if st.button("🔊 ÉCOUTER (Aide Urgence)"):
        parler("En cas de vol ou d'incendie, choisissez le danger et appuyez sur le gros bouton vert WhatsApp.")
    st.subheader("🚨 Signalement de Danger")
    type_danger = st.selectbox("Urgence :", ["🔥 Incendie", "🥷 Vol / Vandalisme", "🐝 Mortalité groupée"])
    
    # Préparation WhatsApp
    msg = f"🚨 *ALERTE YAMB*\n⚠️ Danger: {type_danger}\n📍 Localisation: GPS activé."
    whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(msg)}"
    st.markdown(f'<a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">🟢 ENVOYER SUR WHATSAPP</a>', unsafe_allow_html=True)

# --- 6. GÉOLOCALISATION & CARTE ---
st.divider()
st.subheader("📍 Position du Rucher")
loc = get_geolocation()

if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    m = folium.Map(location=[lat, lon], zoom_start=15)
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
    folium.Marker([lat, lon], icon=folium.Icon(color='red', icon='info-sign')).add_to(m)
    st_folium(m, width="100%", height=300)
else:
    st.warning("📡 Recherche du signal GPS... Autorisez la localisation sur votre téléphone.")

st.markdown("<p style='text-align:center; font-size:12px;'>YAMB v1.2 Premium - Abeilles du Sénégal</p>", unsafe_allow_html=True)
