import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import urllib.parse

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="YAMB - Abeilles du Sénégal",
    page_icon="🐝",
    layout="centered"
)

# --- 2. CHARTE GRAPHIQUE ALVÉOLES & BOIS ---
st.markdown("""
    <style>
    .stApp { background-color: #FDF5E6; } /* Beige Cire */
    .main-header {
        background: linear-gradient(135deg, #8B4513 0%, #5D2E0A 100%); /* Bois de ruche */
        color: #FFC30B; /* Or Miel */
        padding: 30px;
        border-radius: 0 0 50px 50px;
        text-align: center;
        border-bottom: 8px solid #FFC30B;
    }
    .verset-box {
        background-color: #FFF9E3;
        border-left: 5px solid #FFC30B;
        padding: 20px;
        margin: 20px 0;
        font-style: italic;
        color: #5D2E0A;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    div[data-testid="stMetricValue"] {
        color: #8B4513 !important;
        font-weight: 900 !important;
    }
    .whatsapp-btn {
        background-color: #25D366;
        color: white !important;
        padding: 20px;
        border-radius: 15px;
        text-decoration: none;
        display: block;
        text-align: center;
        font-weight: bold;
        border: 4px solid #FCD116;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LECTURE AUTOMATIQUE DU VERSET ---
def lire_verset_demarrage():
    verset = "De leur ventre, sort une liqueur, aux couleurs variées, dans laquelle il y a une guérison pour les gens."
    st.components.v1.html(f"""
        <script>
        var msg = new SpeechSynthesisUtterance("{verset}");
        msg.lang = 'fr-FR';
        msg.rate = 0.85; 
        window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

if 'verset_fait' not in st.session_state:
    lire_verset_demarrage()
    st.session_state.verset_fait = True

# --- 4. ENTÊTE ---
st.markdown("""
    <div class='main-header'>
        <div style='font-size:12px; font-weight:bold; color:#FFC30B; letter-spacing:4px;'>ABEILLES DU SÉNÉGAL</div>
        <h1 style='margin:10px 0; color:white; font-size:45px;'>🐝 YAMB</h1>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class='verset-box'>
        "De leur ventre, sort une liqueur, aux couleurs variées, dans laquelle il y a une guérison pour les gens." <br>
        <strong style='color:#8B4513;'>— Sourate An-Nahl, Verset 69</strong>
    </div>
    """, unsafe_allow_html=True)

# --- 5. ONGLETS ---
tabs = st.tabs(["🍯 RÉCOLTE", "📸 PHOTO", "🚨 SOS"])

with tabs[0]:
    st.subheader("Estimation de production")
    nb = st.number_input("Nombre de ruches :", min_value=1, value=10)
    st.metric(label="Miel estimé", value=f"{nb * 12} kg", delta="Pureté Adansonii")

with tabs[1]:
    st.subheader("Suivi des rayons")
    st.camera_input("Prendre une photo")

with tabs[2]:
    st.subheader("Signaler une urgence")
    danger = st.selectbox("Problème :", ["🔥 Incendie", "🥷 Vol", "🐝 Maladie"])
    msg = f"🚨 *URGENCE ABEILLES DU SÉNÉGAL*\nIncident : {danger}."
    url = f"https://wa.me/?text={urllib.parse.quote(msg)}"
    st.markdown(f'<a href="{url}" target="_blank" class="whatsapp-btn">🟢 ENVOYER L\'ALERTE WHATSAPP</a>', unsafe_allow_html=True)

# --- 6. CARTE ---
st.divider()
loc = get_geolocation()
if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    m = folium.Map(location=[lat, lon], zoom_start=17)
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
    folium.Marker([lat, lon], icon=folium.Icon(color='orange')).add_to(m)
    st_folium(m, width="100%", height=250)

st.markdown("<p style='text-align:center; padding:20px; font-weight:bold;'>© 2025 Abeilles du Sénégal</p>", unsafe_allow_html=True)
