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

# --- 2. CHARTE GRAPHIQUE : BEIGE, RAYON, RUCHE ---
st.markdown("""
    <style>
    /* Fond Beige Alvéole */
    .stApp { background-color: #FDF5E6; } 

    /* En-tête Bois de Ruche */
    .main-header {
        background: linear-gradient(135deg, #8B4513 0%, #5D2E0A 100%);
        color: #FFC30B;
        padding: 30px;
        border-radius: 0 0 50px 50px;
        text-align: center;
        border-bottom: 8px solid #FFC30B;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }

    /* Boite du Verset Coranique */
    .verset-box {
        background-color: #FFF9E3;
        border-left: 8px solid #FFC30B;
        padding: 20px;
        margin: 25px 0;
        font-style: italic;
        color: #5D2E0A;
        font-size: 1.1em;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }

    /* Affichage de la Production (Haute Lisibilité) */
    div[data-testid="stMetricValue"] {
        color: #8B4513 !important; /* Brun Bois */
        font-size: 3.8rem !important;
        font-weight: 900 !important;
        text-shadow: 2px 2px 0px #FFC30B;
    }
    div[data-testid="stMetricLabel"] {
        color: #5D2E0A !important;
        font-size: 1.4rem !important;
        font-weight: bold !important;
    }

    /* Style des onglets (Beige/Miel) */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #EADDCA;
        border-radius: 15px;
        padding: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #5D2E0A !important;
        font-weight: bold;
    }

    /* Bouton SOS WhatsApp */
    .whatsapp-btn {
        background-color: #25D366;
        color: white !important;
        padding: 20px;
        border-radius: 20px;
        text-decoration: none;
        display: block;
        text-align: center;
        font-weight: 900;
        font-size: 1.3em;
        border: 4px solid #FCD116;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    h1, h2, h3 { color: #5D2E0A !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LECTURE DU VERSET AU DÉMARRAGE ---
def lire_verset_demarrage():
    # Traduction du verset 69 de la Sourate An-Nahl
    verset_audio = "De leur ventre, sort une liqueur, aux couleurs variées, dans laquelle il y a une guérison pour les gens."
    st.components.v1.html(f"""
        <script>
        var msg = new SpeechSynthesisUtterance("{verset_audio}");
        msg.lang = 'fr-FR';
        msg.rate = 0.85; 
        window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

if 'verset_lu' not in st.session_state:
    lire_verset_demarrage()
    st.session_state.verset_lu = True

# --- 4. ENTÊTE PRESTIGE ---
st.markdown("""
    <div class='main-header'>
        <div style='font-size:14px; font-weight:bold; color:#FFC30B; letter-spacing:5px;'>ABEILLES DU SÉNÉGAL</div>
        <h1 style='margin:10px 0; color:white; font-size:55px;'>🐝 YAMB</h1>
        <p style='color:#F5F5DC; margin:0; font-size:18px;'>Unité d'Élite Apicole</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class='verset-box'>
        "De leur ventre, sort une liqueur, aux couleurs variées, dans laquelle il y a une guérison pour les gens." <br>
        <strong style='color:#8B4513; float:right;'>— Sourate An-Nahl, Verset 69</strong>
        <br>
    </div>
    """, unsafe_allow_html=True)

# --- 5. NAVIGATION ---
tabs = st.tabs(["🍯 RÉCOLTE", "📸 PHOTO", "🚨 SOS"])

with tabs[0]:
    st.header("Estimation de production")
    nb = st.number_input("Nombre de ruches :", min_value=1, value=10, step=1)
    
    # Calcul
    production = nb * 12
    st.metric(label="Miel attendu (kg)", value=f"{production} kg", delta="Qualité Premium")
    st.write("**Note :** Moyenne Abeilles du Sénégal : 12kg/ruche.")

with tabs[1]:
    st.header("Suivi du Rucher")
    st.camera_input("Capturer l'état des cadres")

with tabs[2]:
    st.header("Signalement Urgence")
    danger = st.selectbox("Type d'incident :", ["🔥 Incendie", "🥷 Vol / Vandalisme", "🐝 Mortalité groupée"])
    
    msg = f"🚨 *ALERTE ABEILLES DU SÉNÉGAL*\n⚠️ Problème : {danger}\n📍 Localisation via YAMB."
    url = f"https://wa.me/?text={urllib.parse.quote(msg)}"
    st.markdown(f'<a href="{url}" target="_blank" class="whatsapp-btn">🟢 ENVOYER L\'ALERTE WHATSAPP</a>', unsafe_allow_html=True)

# --- 6. GÉOLOCALISATION ---
st.divider()
st.subheader("📍 Position du Rucher")
loc = get_geolocation()
if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    m = folium.Map(location=[lat, lon], zoom_start=17)
    # Fond Satellite Google
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
    folium.Marker([lat, lon], popup="Mon Rucher", icon=folium.Icon(color='orange', icon='leaf')).add_to(m)
    st_folium(m, width="100%", height=300)
else:
    st.info("📡 GPS en attente de signal... Vérifiez vos autorisations.")

# --- 7. PIED DE PAGE ---
st.markdown("<p style='text-align:center; padding:30px; font-weight:bold; color:#5D2E0A;'>© 2025 Abeilles du Sénégal - YAMB Version Finale</p>", unsafe_allow_html=True)
