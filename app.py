import streamlit as st
from streamlit_js_eval import get_geolocation

st.set_page_config(page_title="Yamb Connecté", layout="wide")

# CSS pour forcer l'écriture en NOIR sur fond BLANC
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    h1 { color: #000000 !important; text-align: center; font-size: 50px !important; }
    .big-card {
        background: #F1F8E9;
        border: 5px solid #2E7D32;
        padding: 20px;
        margin: 10px 0px;
        border-radius: 20px;
        color: #000000 !important;
    }
    .text-noir { color: #000000 !important; font-weight: bold; font-size: 22px; }
    .stButton>button {
        height: 100px !important; background-color: #FFD600 !important;
        color: #000 !important; font-size: 25px !important; font-weight: 900 !important;
        border: 4px solid #000 !important; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🐝 YAMB CONNECTÉ</h1>", unsafe_allow_html=True)

loc = get_geolocation()
if loc:
    st.success("✅ GPS ACTIVÉ")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='big-card'><p class='text-noir'>🌳 FLORE : Anacardier, Mangue, Fleurs de brousse</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='big-card'><p class='text-noir'>🌡️ MÉTÉO : Chaud et Sec</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='big-card'><p class='text-noir'>💧 EAU : Bolongs et Puits proches</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='big-card'><p class='text-noir'>🍯 MIEL : Mangrove et Forêt</p></div>", unsafe_allow_html=True)
    
    if st.button("💾 ENREGISTRER MON RUCHER"):
        st.balloons()
else:
    st.info("📡 Recherche du signal GPS... Posez le téléphone à plat au soleil.")
