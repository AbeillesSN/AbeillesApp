import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import requests
import urllib.parse

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="YAMB ARMURE", layout="wide")

# --- 2. STYLE TACTIQUE (FORCE LE CONTRASTE NOIR/BLANC) ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    h1, h2, h3, h4, p, span, label, li { color: #000000 !important; font-weight: 900 !important; }
    
    /* Cartes d'information avec fond noir pour texte blanc ou inversement */
    .black-card {
        background-color: #1a1a1a !important;
        border: 4px solid #FFC30B;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    .black-card h3, .black-card h4, .black-card p, .black-card li { 
        color: #FFFFFF !important; 
    }
    
    .gold-text { color: #FFC30B !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. NAVIGATION ---
st.title("🛡️ YAMB ARMURE : ARSENAL COMPLET")
tabs = st.tabs(["🎯 TERRAIN", "🌙 BIO-STRATÉGIE", "🔬 SANTÉ (NEEM)", "💰 ÉCONOMIE", "🚨 SOS"])

loc = get_geolocation()

with tabs[0]:
    st.markdown("## 🛰️ Zone de Contrôle (3 km)")
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        col1, col2 = st.columns([2, 1])
        with col1:
            m = folium.Map(location=[lat, lon], zoom_start=14)
            folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
            folium.Marker([lat, lon], icon=folium.Icon(color='red', icon='bolt', prefix='fa')).add_to(m)
            folium.Circle([lat, lon], radius=3000, color='yellow', fill=True, fill_opacity=0.2).add_to(m)
            st_folium(m, width="100%", height=400)
        with col2:
            st.markdown(f"""<div class='black-card'>
                <h3 class='gold-text'>🌿 FLORE ACTIVE</h3>
                <ul><li>KADD (Pleine floraison)</li><li>ANACARDIER (Début)</li></ul>
                <h3 class='gold-text'>☁️ MÉTÉO</h3>
                <p>Vent : 16 km/h (Harmattan)<br>Condition : Optimale</p>
            </div>""", unsafe_allow_html=True)

with tabs[1]:
    st.markdown("## 🌙 Calendrier Lunaire & Gestion")
    st.markdown("""<div class='black-card'>
        <h3 class='gold-text'>🌓 Premier Quartier</h3>
        <p>Les colonies sont en phase de construction. La reine intensifie la ponte.</p>
        <p><b>CONSEIL :</b> Période parfaite pour agrandir le nid ou poser des hausses.</p>
    </div>""", unsafe_allow_html=True)

with tabs[2]:
    st.markdown("## 🔬 Pharmacopée Africaine (Remèdes Locaux)")
    maladie = st.selectbox("Anomalie détectée :", ["Fausse Teigne", "Fourmis Magnan", "Varroa"])
    if maladie == "Fausse Teigne":
        st.markdown("""<div class='black-card'>
            <h3 class='gold-text'>🦋 Remède : NEEM (Azadirachta indica)</h3>
            <p>1. Brûler légèrement des feuilles de Neem sèches dans l'enfumoir.</p>
            <p>2. Tapisser le fond de la ruche de feuilles fraîches.</p>
            <p><b>Effet :</b> Répulsif naturel contre les larves de cire.</p>
        </div>""", unsafe_allow_html=True)
    elif maladie == "Fourmis Magnan":
        st.markdown("<div class='black-card'><p>Utiliser de la <b>graisse de moteur</b> sur les supports.</p></div>", unsafe_allow_html=True)

with tabs[3]:
    st.markdown("## 💰 Puissance Financière & Soudure")
    ruches = st.number_input("Nombre de ruches :", 1, 500, 20)
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"""<div class='black-card'>
            <h4 class='gold-text'>🍯 RÉCOLTE ESTIMÉE</h4>
            <p style='font-size:30px;'>{ruches * 15} KG</p>
            <h2 class='gold-text'>{(ruches * 15 * 4500):,} FCFA</h2>
        </div>""", unsafe_allow_html=True)
    with col_b:
        st.markdown(f"""<div class='black-card'>
            <h4 class='gold-text'>🥣 NOURRISSEMENT (Soudure)</h4>
            <p>Sucre nécessaire : {ruches * 5} kg</p>
            <p>Eau : {ruches * 2.5} litres</p>
        </div>""", unsafe_allow_html=True)

with tabs[4]:
    st.markdown("## 🚨 Unité d'Urgence")
    st.error("🔥 RISQUE INCENDIE ÉLEVÉ : Vérifiez vos pare-feux.")
    if st.button("📲 ENVOYER ALERTE GPS (WHATSAPP)"):
        msg = urllib.parse.quote(f"ALERTE RUCHER\nPosition: {loc['coords']['latitude'] if loc else 'N/A'}")
        st.markdown(f'<a href="https://wa.me/221XXXXXX?text={msg}" target="_blank">CONFIRMER ENVOI</a>', unsafe_allow_html=True)
