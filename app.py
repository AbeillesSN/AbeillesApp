import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import requests
import urllib.parse

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="YAMB ÉLITE", layout="centered")

# --- 2. STYLE "ANTI-ÉBLOUISSEMENT" (FORCE LE NOIR SUR BLANC) ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    
    /* FORCE LE NOIR SUR TOUT LE TEXTE */
    h1, h2, h3, h4, p, span, label, li, div { 
        color: #000000 !important; 
        font-weight: 800 !important; 
    }
    
    /* BLOCS DE DONNÉES À HAUT CONTRASTE */
    .tactical-box {
        background-color: #F0F2F6 !important;
        border: 3px solid #000000 !important;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    
    /* BOUTON D'URGENCE */
    .stButton>button {
        background-color: #FF0000 !important;
        color: white !important;
        font-weight: bold !important;
        border: 2px solid #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ENTÊTE ---
st.markdown("<h1 style='text-align:center;'>🛡️ YAMB ARMURE : UNITÉ D'ÉLITE</h1>", unsafe_allow_html=True)

loc = get_geolocation()

# --- 4. NAVIGATION PAR SECTION (TOUT VISIBLE) ---
st.markdown("---")

# SECTION A : TERRAIN & GPS
st.markdown("### 🎯 ZONE DE BUTINAGE (3 KM)")
if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    m = folium.Map(location=[lat, lon], zoom_start=14)
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
    folium.Marker([lat, lon], icon=folium.Icon(color='red', icon='bolt', prefix='fa')).add_to(m)
    folium.Circle([lat, lon], radius=3000, color='yellow', fill=True, fill_opacity=0.3).add_to(m)
    st_folium(m, width="100%", height=350)
else:
    st.warning("⚠️ POSITION GPS EN ATTENTE...")

# SECTION B : SANTÉ & PHARMACOPÉE (NEEM)
st.markdown("<div class='tactical-box'>", unsafe_allow_html=True)
st.markdown("### 🔬 CLINIQUE : TRAITEMENT AU NEEM")
st.write("**Problème :** Fausse Teigne ou parasites.")
st.write("**Remède d'Élite :** Tapisser le fond de la ruche de feuilles de **NEEM** fraîches. La teneur en azadirachtine repousse naturellement les prédateurs sans nuire aux abeilles.")
st.markdown("</div>", unsafe_allow_html=True)

# SECTION C : STRATÉGIE LUNAIRE
st.markdown("<div class='tactical-box'>", unsafe_allow_html=True)
st.markdown("### 🌙 CYCLE LUNAIRE")
st.write("**Phase :** Premier Quartier")
st.write("**Tactique :** Les colonies sont en pleine extension. Vérifiez l'espace dans les hausses pour éviter l'essaimage non désiré.")
st.markdown("</div>", unsafe_allow_html=True)

# SECTION D : ÉCONOMIE (FCFA)
st.markdown("<div class='tactical-box' style='border-color: #FFD700 !important;'>", unsafe_allow_html=True)
st.markdown("### 💰 VALEUR DE LA RÉCOLTE")
nb_ruches = st.number_input("Nombre de ruches", 1, 1000, 20)
total_kg = nb_ruches * 15
valeur_fcfa = total_kg * 4500
st.markdown(f"<h2 style='text-align:center;'>{valeur_fcfa:,} FCFA</h2>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# SECTION E : SOS URGENCE
st.markdown("### 🚨 ASSISTANCE D'URGENCE")
if st.button("📲 SIGNALER UN INCIDENT (FEU / VOL)"):
    msg = urllib.parse.quote(f"ALERTE UNITÉ ÉLITE\nPosition: {lat if loc else 'Inconnue'}")
    st.markdown(f'<a href="https://wa.me/221XXXXXX?text={msg}" target="_blank" style="color:red; font-size:20px;">CONFIRMER L\'ALERTE PAR WHATSAPP</a>', unsafe_allow_html=True)
