import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation

# --- CONFIGURATION ---
st.set_page_config(page_title="Yamb Connecté", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    h1 { color: #1B5E20 !important; text-align: center; font-size: 45px !important; font-weight: 900; }
    .card-recolte {
        background-color: #FFD600; border: 8px solid #000;
        padding: 20px; border-radius: 20px; text-align: center;
        margin-bottom: 20px;
    }
    .big-card {
        background: #F1F8E9; border: 4px solid #2E7D32;
        padding: 15px; border-radius: 15px; margin-bottom: 10px;
        color: #000000 !important;
    }
    .text-noir { color: #000000 !important; font-weight: bold; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- AFFICHAGE DU LOGO ---
col_l1, col_l2, col_l3 = st.columns([1, 1, 1])
with col_l2:
    # On essaie les deux noms courants pour être sûr
    try:
        st.image("logo.png")
    except:
        try:
            st.image("logo.png.png")
        except:
            st.markdown("<h1>🐝 YAMB CONNECTÉ</h1>", unsafe_allow_html=True)

# --- DÉTECTION GPS ---
loc = get_geolocation()

if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    
    # 1. ALERTE RÉCOLTE
    st.markdown("""<div class='card-recolte'>
        <span style='font-size: 30px; font-weight: 900; color: #000;'>🍯 PRÊT POUR RÉCOLTE (Eucalyptus)</span>
    </div>""", unsafe_allow_html=True)

    # 2. CARTE SATELLITE (GOOGLE EARTH)
    st.markdown("### 🛰️ VUE SATELLITE DU SITE")
    # Création de la carte centrée sur l'apiculteur
    m = folium.Map(location=[lat, lon], zoom_start=16)
    # Ajout de la couche Satellite Google
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr='Google Satellite',
        name='Google Satellite',
        overlay=False,
        control=True
    ).add_to(m)
    folium.Marker([lat, lon], tooltip="Mon Rucher").add_to(m)
    st_folium(m, width="100%", height=400)

    # 3. ANALYSE DE LA DIVERSITÉ FLORISTIQUE (3km)
    st.markdown("### 🌳 Diagnostic de l'Écosystème")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='big-card'><p class='text-noir'>🌳 ARBRES : Fromager, Palmier, Anacardier</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='big-card'><p class='text-noir'>🌡️ MÉTÉO : 28°C | Vent Modéré</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='big-card'><p class='text-noir'>🌿 ARBUSTES & HERBES : Kinkeliba, Liane Madd</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='big-card'><p class='text-noir'>🚜 CULTURES : Riziculture, Vergers</p></div>", unsafe_allow_html=True)

    if st.button("✅ SAUVEGARDER L'EMPLACEMENT"):
        st.balloons()
else:
    st.warning("📡 RECHERCHE DU SIGNAL GPS... Posez le téléphone à plat.")
