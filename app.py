import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import requests
import urllib.parse
from datetime import datetime

# --- 1. CONFIGURATION & DESIGN HAUTE VISIBILITÉ ---
st.set_page_config(page_title="YAMB PRO - ÉLITE", layout="wide")

st.markdown("""
    <style>
    /* Fond neutre et texte noir profond pour lecture sous le soleil */
    .stApp { background-color: #FFFFFF; }
    h1, h2, h3, h4, p, span, label, li { color: #000000 !important; font-weight: 900 !important; }
    
    /* Blocs de combat (Cartes d'info) */
    .tactical-card {
        border: 4px solid #000000;
        padding: 20px;
        margin-bottom: 20px;
        background-color: #F9F9F9;
        border-radius: 10px;
    }
    
    /* Boutons et alertes */
    .stButton>button { background-color: #000000 !important; color: #FFC30B !important; width: 100%; border-radius: 10px; font-weight: bold; }
    .health-tip { color: #006400 !important; border-left: 5px solid #006400; padding-left: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIQUE MÉTIER ---
def calculate_syrup(nb_ruches):
    # Pour l'hivernage : 5kg de sucre par ruche pour la soudure
    total_sucre = nb_ruches * 5
    total_eau = total_sucre * 0.5
    return total_sucre, total_eau

# --- 3. INTERFACE PRINCIPALE ---
st.markdown("<h1 style='text-align:center;'>🛡️ YAMB PRO : ARSENAL APICOLE SÉNÉGAL</h1>", unsafe_allow_html=True)

loc = get_geolocation()
tabs = st.tabs(["🎯 TERRAIN & GPS", "🌙 BIOLOGIE & LUNE", "🔬 SANTÉ & NEEM", "🍯 ÉCONOMIE", "🚨 SOS"])

with tabs[0]:
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### 🛰️ Rayon de Butinage (3 km)")
            m = folium.Map(location=[lat, lon], zoom_start=13)
            folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
            # Marqueur rouge (Position exacte)
            folium.Marker([lat, lon], icon=folium.Icon(color='red', icon='bolt', prefix='fa')).add_to(m)
            # Rayon de 3km (Zone de travail)
            folium.Circle([lat, lon], radius=3000, color='#FFC30B', fill=True, fill_opacity=0.2).add_to(m)
            st_folium(m, width="100%", height=400)
        with col2:
            st.markdown("<div class='tactical-card'><h4>🌳 FLORE ACTUELLE</h4><p>• KADD : 85%<br>• ANACARDE : 15%</p><hr><h4>💨 MÉTÉO</h4><p>Vitesse : 18 km/h<br>Direction : Nord-Est</p></div>", unsafe_allow_html=True)

with tabs[1]:
    st.markdown("### 🌙 Stratégie Lunaire")
    st.markdown("""
        <div class='tactical-card'>
            <h2>🌓 Premier Quartier</h2>
            <p><b>Impact :</b> Développement de la ponte. Les ouvrières sont plus douces.</p>
            <p class='health-tip'>CONSEIL : Idéal pour diviser vos colonies ou introduire une nouvelle reine.</p>
        </div>
    """, unsafe_allow_html=True)

with tabs[2]:
    st.markdown("### 🔬 Pharmacopée & Santé")
    maladie = st.selectbox("Identifier un problème :", ["Fausse Teigne", "Fourmis Magnan", "Varroa"])
    
    if maladie == "Fausse Teigne":
        st.markdown("""<div class='tactical-card'><h3>🌿 Remède au NEEM</h3>
        <p>1. Nettoyer les déchets de cire au fond de la ruche.<br>
        2. Placer des feuilles de <b>Neem fraîches</b> sur les couvre-cadres.<br>
        3. Réduire l'entrée pour aider les abeilles à garder la ruche.</p></div>""", unsafe_allow_html=True)
    elif maladie == "Fourmis Magnan":
        st.markdown("""<div class='tactical-card'><h3>🛡️ Barrière Physique</h3>
        <p>Enduire les supports de la ruche avec un mélange de <b>graisse</b> et de <b>cendre</b>.</p></div>""", unsafe_allow_html=True)

with tabs[3]:
    st.markdown("### 💰 Gestion de la Richesse")
    nb_ruches = st.number_input("Nombre de ruches gérées :", 1, 1000, 20)
    sucre, eau = calculate_syrup(nb_ruches)
    
    col_a, col_b = st.columns(2)
    col_a.markdown(f"<div class='tactical-card'><h4>🍞 SOUDURE (Hivernage)</h4><p>Sucre : {sucre} kg<br>Eau : {eau} litres</p></div>", unsafe_allow_html=True)
    
    total_valeur = nb_ruches * 15 * 4500 # Moyenne 15kg/ruche à 4500 FCFA
    col_b.markdown(f"<div class='tactical-card'><h4>💎 POTENTIEL</h4><h1>{total_valeur:,.0f} FCFA</h1></div>", unsafe_allow_html=True)

with tabs[4]:
    st.markdown("### 🚨 SOS - Intervention d'Élite")
    st.error("🔥 ALERTE FEU : Saison sèche critique. Pare-feux de 5 mètres obligatoires.")
    incident = st.selectbox("Signaler :", ["Feu de brousse", "Vol de ruche", "Mortalité massive"])
    if st.button("📲 ENVOYER ALERTE WHATSAPP"):
        gps = f"{loc['coords']['latitude']},{loc['coords']['longitude']}" if loc else "N/A"
        msg = urllib.parse.quote(f"🚨 URGENCE YAMB PRO\nIncident: {incident}\nLocalisation: http://maps.google.com/?q={gps}")
        st.markdown(f'<a href="https://wa.me/221XXXXXXX?text={msg}" target="_blank">Cliquez ici pour confirmer l\'envoi</a>', unsafe_allow_html=True)
