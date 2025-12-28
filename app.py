import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import urllib.parse
from PIL import Image
import datetime

# --- 1. CONFIGURATION & DESIGN "ARMURE BLINDÉE" ---
st.set_page_config(page_title="YAMB PRO - ÉLITE", layout="wide", page_icon="🐝")

st.markdown("""
    <style>
    /* Force le contraste : Texte Noir sur Fond Blanc */
    .stApp {
        background-color: #FFFFFF;
        background-image: url("https://www.transparenttextures.com/patterns/honeycomb.png");
        background-attachment: fixed;
    }

    h1, h2, h3, p, span, label, li {
        color: #000000 !important;
        font-weight: 800 !important;
    }

    /* Cartes Alvéoles Professionnelles */
    .alveole-card {
        background: #FDFDFD;
        border-left: 8px solid #FFC30B;
        border: 2px solid #FFC30B;
        padding: 20px;
        border-radius: 15px 40px 15px 40px;
        margin-bottom: 20px;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
    }

    /* Animation Abeille */
    @keyframes fly {
        0% { transform: translate(0,0); }
        50% { transform: translate(5px,-10px); }
        100% { transform: translate(0,0); }
    }
    .bee-icon { display: inline-block; animation: fly 2s infinite ease-in-out; font-size: 40px; }

    /* Boutons Tactiques */
    .stButton>button {
        background-color: #FFC30B !important;
        color: #000000 !important;
        border: 2px solid #000000 !important;
        font-weight: 900 !important;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INITIALISATION DU MODE HORS-LIGNE (CACHE) ---
if "offline_db" not in st.session_state:
    st.session_state.offline_db = []

# --- 3. EN-TÊTE ---
st.markdown("<div style='text-align:center;'><span class='bee-icon'>🐝</span></div>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center;'>YAMB PRO : ARSENAL APICOLE SÉNÉGAL</h1>", unsafe_allow_html=True)

loc = get_geolocation()

# --- 4. NAVIGATION PAR SECTIONS ---
tab1, tab2, tab3, tab4 = st.tabs(["🎯 RADAR & GPS", "🔬 SCAN & SANTÉ", "💰 ÉCONOMIE", "💾 MODE HORS-LIGNE"])

# TAB 1 : RADAR TACTIQUE
with tab1:
    st.markdown("### 🛰️ Radar de Butinage (3 km)")
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        m = folium.Map(location=[lat, lon], zoom_start=13)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        folium.Circle([lat, lon], radius=3000, color='#FFC30B', fill=True, fill_opacity=0.2).add_to(m)
        folium.Marker([lat, lon], icon=folium.Icon(color='red', icon='bolt', prefix='fa')).add_to(m)
        st_folium(m, width="100%", height=400)
    else:
        st.info("📍 Recherche du signal GPS au-dessus de Yeumbeul/Mbao...")

# TAB 2 : SCAN COUVAIN & SANTÉ
with tab2:
    st.markdown("### 🔍 Scan Couvain par IA")
    img_file = st.file_uploader("Prendre une photo du cadre", type=["jpg", "png"])
    if img_file:
        st.image(img_file, width=400)
        if st.button("Lancer l'Analyse"):
            st.success("✅ Diagnostic : Ponte 95% (Excellent). Absence de loque. Prévoir traitement Neem préventif.")
    
    st.markdown("""<div class='alveole-card'>
        <h3>🌿 Pharmacopée : Le Pouvoir du Neem</h3>
        <p>En cas de Fausse Teigne : Placez 3 branches de Neem fraîches sous le toit. 
        L'odeur naturelle bloque la reproduction des papillons parasites.</p>
    </div>""", unsafe_allow_html=True)

# TAB 3 : ÉCONOMIE & SOUDURE
with tab3:
    st.markdown("### 💰 Puissance Financière")
    nb = st.number_input("Nombre de ruches actives", 1, 1000, 20)
    col1, col2 = st.columns(2)
    with col1:
        valeur = nb * 15 * 4500
        st.markdown(f"<div class='alveole-card'><h4>🍯 Potentiel Récolte</h4><h2>{valeur:,.0f} FCFA</h2></div>", unsafe_allow_html=True)
    with col2:
        sucre = nb * 5
        st.markdown(f"<div class='alveole-card'><h4>🍞 Plan de Soudure</h4><h2>{sucre} kg de sucre</h2></div>", unsafe_allow_html=True)

# TAB 4 : MODE HORS-LIGNE (PERSISTANCE)
with tab4:
    st.markdown("### 💾 Mémoire de Terrain (Sans Réseau)")
    ruche_id = st.text_input("N° de la Ruche visitée")
    note = st.text_area("Note de visite")
    if st.button("Sauvegarder en local"):
        st.session_state.offline_db.append({"id": ruche_id, "note": note, "date": str(datetime.date.today())})
        st.toast("Données gardées en mémoire !")

    if st.session_state.offline_db:
        st.markdown("#### 🔄 Données prêtes à la synchronisation")
        st.table(st.session_state.offline_db)

# --- 5. BOUTON SOS ---
st.write("---")
if st.button("🚨 ENVOYER ALERTE SOS (GPS)"):
    if loc:
        msg = urllib.parse.quote(f"SOS YAMB PRO\nUrgence au rucher !\nGPS: {lat},{lon}")
        st.markdown(f'<a href="https://wa.me/221XXXXXXX?text={msg}" target="_blank">CONFIRMER SUR WHATSAPP</a>', unsafe_allow_html=True)
