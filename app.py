import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import requests
import urllib.parse

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="YAMB ARMURE ÉLITE", layout="centered")

# --- 2. STYLE INVERSÉ (ANTI-ÉBLOUISSEMENT & LISIBILITÉ TOTALE) ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; }
    
    /* BOITES NOIRES TEXTE BLANC / DORÉ */
    .armor-box {
        background-color: #1A1C24 !important;
        border: 2px solid #FFC30B !important;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 25px;
    }
    
    h1, h2, h3, h4, p, span, label, li { 
        color: #FFFFFF !important; 
        font-weight: bold !important; 
    }
    
    .gold-title { color: #FFC30B !important; text-transform: uppercase; letter-spacing: 2px; }
    .status-alert { background-color: #FF4B4B; color: white; padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ENTÊTE ---
st.markdown("<h1 style='text-align:center; color:#FFC30B !important;'>🛡️ YAMB ARMURE ÉLITE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Arsenal Complet de l'Apiculteur Sénégalais</p>", unsafe_allow_html=True)

loc = get_geolocation()

# --- 4. TOUTES LES FONCTIONS SUR UNE PAGE ---

# A. CARTOGRAPHIE TACTIQUE
st.markdown("<h2 class='gold-title'>📍 Localisation & Rayon 3km</h2>", unsafe_allow_html=True)
if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    m = folium.Map(location=[lat, lon], zoom_start=13)
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
    folium.Marker([lat, lon], icon=folium.Icon(color='red')).add_to(m)
    folium.Circle([lat, lon], radius=3000, color='#FFC30B', fill=True, fill_opacity=0.2).add_to(m)
    st_folium(m, width="100%", height=350)
else:
    st.info("Recherche du signal GPS...")

# B. MÉTÉO & FLORE
st.markdown("<div class='armor-box'>", unsafe_allow_html=True)
st.markdown("<h3 class='gold-title'>🌿 Environnement Direct</h3>", unsafe_allow_html=True)
st.write("• **Flore dominante :** Kadd (Floraison massive), Anacardier (Début)")
st.write("• **Météo :** 24°C | Vent 18 km/h (Vigilance Harmattan)")
st.markdown("</div>", unsafe_allow_html=True)

# C. BIO-STRATÉGIE (LUNE)
st.markdown("<div class='armor-box'>", unsafe_allow_html=True)
st.markdown("<h3 class='gold-title'>🌙 Biologie Lunaire</h3>", unsafe_allow_html=True)
st.write("**Phase :** Premier Quartier")
st.write("**Impact :** Ponte active de la reine. Colonies calmes. Période idéale pour l'inspection des cadres.")
st.markdown("</div>", unsafe_allow_html=True)

# D. SANTÉ & PHARMACOPÉE (NEEM)
st.markdown("<div class='armor-box'>", unsafe_allow_html=True)
st.markdown("<h3 class='gold-title'>🔬 Clinique du Rucher</h3>", unsafe_allow_html=True)
maladie = st.selectbox("Symptôme observé :", ["Fausse Teigne", "Fourmis Magnan", "Varroa"])
if maladie == "Fausse Teigne":
    st.write("**Traitement :** Placer des feuilles de **NEEM** fraîches sur les têtes de cadres. Réduire l'entrée de la ruche.")
elif maladie == "Fourmis Magnan":
    st.write("**Traitement :** Graisse mécanique + cendre sur les pieds des supports.")
st.markdown("</div>", unsafe_allow_html=True)

# E. ÉCONOMIE & SOUDURE
st.markdown("<div class='armor-box'>", unsafe_allow_html=True)
st.markdown("<h3 class='gold-title'>💰 Calculateur de Puissance</h3>", unsafe_allow_html=True)
ruches = st.number_input("Nombre de ruches :", 1, 1000, 20)
st.write(f"• **Valeur Récolte :** {(ruches * 15 * 4500):,} FCFA")
st.write(f"• **Achat Sucre (Soudure) :** {ruches * 5} kg nécessaires")
st.markdown("</div>", unsafe_allow_html=True)

# F. URGENCE SOS
st.markdown("<div class='armor-box' style='border-color:red !important;'>", unsafe_allow_html=True)
st.markdown("<h3 style='color:red !important;'>🚨 SIGNAL D'URGENCE</h3>", unsafe_allow_html=True)
if st.button("📲 ENVOYER ALERTE GPS À L'UNITÉ D'ÉLITE"):
    msg = urllib.parse.quote(f"URGENCE RUCHER\nGPS: {lat if loc else 'N/A'},{lon if loc else 'N/A'}")
    st.markdown(f'<a href="https://wa.me/221XXXXXX?text={msg}" target="_blank" style="color:white;">CLIQUEZ ICI POUR VALIDER</a>', unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
