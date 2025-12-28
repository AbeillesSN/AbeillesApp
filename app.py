import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import requests
import urllib.parse

# --- CONFIGURATION DU BLINDAGE VISUEL ---
st.set_page_config(page_title="YAMB PRO - ÉLITE", layout="centered")

st.markdown("""
    <style>
    /* Force le fond blanc et le texte noir profond pour éviter le blanc sur blanc */
    .stApp { background-color: #FFFFFF !important; }
    h1, h2, h3, h4, p, span, label, li, div { 
        color: #000000 !important; 
        font-weight: 850 !important; 
    }
    /* Boîtes tactiques à haute visibilité avec bordures épaisses */
    .armor-box {
        background-color: #F8F9FA !important;
        border: 4px solid #000000 !important;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 5px 5px 0px #000000;
    }
    .status-badge {
        background-color: #FFC30B;
        color: black !important;
        padding: 5px 10px;
        border-radius: 5px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ENTÊTE ---
st.markdown("<h1 style='text-align:center;'>🐝 YAMB PRO : TABLEAU DE BORD ÉLITE</h1>", unsafe_allow_html=True)

loc = get_geolocation()

# --- 1. RADAR DE TERRAIN (GPS & SATELLITE) ---
st.markdown("## 🛰️ 1. RADAR DE TERRAIN (RAYON 3KM)")
if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    # Zone de contrôle visuelle
    m = folium.Map(location=[lat, lon], zoom_start=13)
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
    folium.Marker([lat, lon], icon=folium.Icon(color='red', icon='bolt', prefix='fa')).add_to(m)
    folium.Circle([lat, lon], radius=3000, color='#FFC30B', fill=True, fill_opacity=0.2).add_to(m)
    st_folium(m, width="100%", height=350)
else:
    st.info("📍 En attente du signal GPS pour le radar...")

# --- 2. INTELLIGENCE ENVIRONNEMENTALE ---
st.markdown("<div class='armor-box'>", unsafe_allow_html=True)
st.markdown("### 🌿 RESSOURCES & MÉTÉO")
c1, c2 = st.columns(2)
with c1:
    st.write("**FLORE ACTIVE :**")
    st.write("✅ **Kadd** (Plein nectar)")
    st.write("⏳ **Anacarde** (Pré-floraison)")
with c2:
    st.write("**MÉTÉO TACTIQUE :**")
    st.write("🌡️ Temp : 28°C")
    st.write("💨 Vent : 15 km/h (Est)")
st.markdown("</div>", unsafe_allow_html=True)

# --- 3. BIOLOGIE & LUNE ---
st.markdown("<div class='armor-box'>", unsafe_allow_html=True)
st.markdown("### 🌙 ÉTAT DE LA COLONIE")
st.write("**Phase Lunaire :** Premier Croissant")
st.write("**Action Recommandée :** Pose des hausses. Les abeilles sont stimulées par la lune montante.")
st.markdown("</div>", unsafe_allow_html=True)

# --- 4. UNITÉ DE SOINS (PHARMACOPÉE) ---
st.markdown("<div class='armor-box'>", unsafe_allow_html=True)
st.markdown("### 🔬 CLINIQUE APICOLE (BIO)")
maladie = st.selectbox("Scanner une anomalie :", ["Fausse Teigne", "Fourmis", "Varroa"])
if maladie == "Fausse Teigne":
    st.write("**PROTOCOLE NEEM :** Appliquer des feuilles de Neem broyées sur le plateau. Réduit l'infestation de 80%.")
elif maladie == "Fourmis":
    st.write("**PROTOCOLE BARRIÈRE :** Graisse + Cendre sur les supports.")
st.markdown("</div>", unsafe_allow_html=True)

# --- 5. PUISSANCE FINANCIÈRE ---
st.markdown("<div class='armor-box'>", unsafe_allow_html=True)
st.markdown("### 💰 ESTIMATIONS & SOUDURE")
nb_ruches = st.number_input("Nombre de ruches gérées :", 1, 1000, 10)
potentiel_kg = nb_ruches * 15
potentiel_fcfa = potentiel_kg * 4500
st.markdown(f"**VALEUR ESTIMÉE :** <span class='status-badge'>{potentiel_fcfa:,.0f} FCFA</span>", unsafe_allow_html=True)
st.write(f"**ALIMENTATION SOUDURE :** Prévoir {nb_ruches * 5} kg de sucre.")
st.markdown("</div>", unsafe_allow_html=True)

# --- 6. URGENCE SOS ---
st.markdown("### 🚨 LIGNE D'URGENCE GPS")
if st.button("📲 ENVOYER POSITION À L'UNITÉ D'ÉLITE"):
    msg = urllib.parse.quote(f"ALERTE YAMB PRO\nUrgence sur zone\nGPS: {lat if loc else 'N/A'}")
    st.markdown(f'<a href="https://wa.me/221XXXXXX?text={msg}" target="_blank" style="background-color:red; color:white; padding:15px; border-radius:10px; text-decoration:none; display:block; text-align:center;">CONFIRMER L\'ENVOI WHATSAPP</a>', unsafe_allow_html=True)
