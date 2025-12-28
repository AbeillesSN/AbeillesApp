import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import requests
import urllib.parse

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="YAMB PRO - Dashboard Élite", layout="wide")

# --- 2. STYLE CONTRASTE MAXIMUM (Texte NOIR sur fond BLANC) ---
st.markdown("""
    <style>
    .stApp { background-color: #FDF5E6; }
    h1, h2, h3, h4, p, span, label, li { color: #000000 !important; font-weight: 800 !important; }
    
    /* Blocs de données ultra-lisibles */
    .feature-card {
        background-color: #ffffff !important;
        border: 4px solid #000000 !important;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    }
    
    /* Onglets plus visibles */
    .stTabs [data-baseweb="tab"] { background-color: #e0e0e0; border-radius: 5px; margin: 2px; }
    .stTabs [aria-selected="true"] { background-color: #FFC30B !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIQUE MÉTIER ---
def get_moon_phase(): return "🌓 Premier Quartier (Colonies calmes)"

# --- 4. NAVIGATION PRINCIPALE ---
st.markdown("<h1 style='text-align:center;'>🐝 YAMB PRO : SYSTÈME D'EXPLOITATION APICOLE</h1>", unsafe_allow_html=True)

tabs = st.tabs(["📍 TERRAIN & GPS", "📅 CALENDRIER & LUNE", "🍯 GESTION RÉCOLTE", "📝 JOURNAL DE VISITE", "🚨 SOS & ALERTES"])

loc = get_geolocation()

with tabs[0]:
    st.markdown("### 🛰️ Rayon de Butinage (3 km)")
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        col1, col2 = st.columns([2, 1])
        
        with col1:
            m = folium.Map(location=[lat, lon], zoom_start=13)
            folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
            folium.Marker([lat, lon], popup="RUCHER", icon=folium.Icon(color='red', icon='record')).add_to(m)
            folium.Circle([lat, lon], radius=3000, color='#FFC30B', fill=True, fill_opacity=0.2).add_to(m)
            st_folium(m, width="100%", height=400)
        
        with col2:
            st.markdown("<div class='feature-card'><h4>☁️ MÉTÉO</h4><p>Condition : OPTIMALE<br>Vitesse Vent : 14 km/h<br>Humidité : 45%</p></div>", unsafe_allow_html=True)
            st.markdown("<div class='feature-card'><h4>🌿 FLORE ACTIVE</h4><p>• Kadd (80%)<br>• Eucalyptus (20%)</p></div>", unsafe_allow_html=True)

with tabs[1]:
    st.markdown("### 🌙 Influence Lunaire et Floraison")
    c1, c2 = st.columns(2)
    c1.markdown(f"<div class='feature-card'><h3>🌙 LUNE</h3><p>{get_moon_phase()}</p><small>Conseil : Période idéale pour le transvasement.</small></div>", unsafe_allow_html=True)
    c2.markdown("<div class='feature-card'><h3>🌸 CYCLE FLORAL</h3><p>KADD : Pic de nectar prévu dans 10 jours.<br>ANACARDIER : Fin de floraison.</p></div>", unsafe_allow_html=True)

with tabs[2]:
    st.markdown("### 🍯 Calculateur de Production & Valeur")
    col_a, col_b = st.columns(2)
    with col_a:
        nb_ruches = st.number_input("Nombre de ruches", 1, 1000, 20)
        rendement = st.slider("Rendement par ruche (kg)", 5, 30, 12)
    
    total_kg = nb_ruches * rendement
    valeur_fcfa = total_kg * 4500 # Prix moyen kg miel qualité
    
    st.markdown(f"""
        <div class='feature-card' style='text-align:center;'>
            <h2 style='margin:0;'>PROSPECTION : {total_kg} KG</h2>
            <h1 style='color:green !important;'>{valeur_fcfa:,} FCFA</h1>
        </div>
    """, unsafe_allow_html=True)

with tabs[3]:
    st.markdown("### 📝 Carnet de Visite Numérique")
    with st.form("visite"):
        ruche_id = st.text_input("N° de la Ruche")
        etat = st.select_slider("État de la colonie", options=["Faible", "Moyenne", "Forte", "Excellente"])
        reine = st.radio("Présence Reine / Ponte", ["Oui", "Non", "Cellules Royales"])
        notes = st.text_area("Observations (Maladies, parasites...)")
        if st.form_submit_button("ENREGISTRER LA VISITE"):
            st.success(f"Visite de la ruche {ruche_id} sauvegardée.")

with tabs[4]:
    st.markdown("### 🚨 Centre d'Alerte")
    st.error("🔥 RISQUE FEU DE BROUSSE : ÉLEVÉ dans votre zone.")
    incident = st.selectbox("Type d'urgence", ["Feu constaté", "Vol / Vandalisme", "Attaque de prédateurs"])
    if st.button("📲 APPEL D'URGENCE UNITÉ D'ÉLITE"):
        msg = urllib.parse.quote(f"ALERTE RUCHER\nType : {incident}\nLocalisation : {loc['coords']['latitude'] if loc else 'N/A'}")
        st.markdown(f'<a href="https://wa.me/221XXXXXXXX?text={msg}" style="background:red; color:white; padding:20px; display:block; text-align:center; border-radius:10px;">ENVOYER L\'ALERTE GPS</a>', unsafe_allow_html=True)
