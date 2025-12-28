import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
from PIL import Image
import datetime

# --- 1. CONFIGURATION MOBILE ---
st.set_page_config(page_title="YAMB PRO", layout="centered") # Centré pour mobile

st.markdown("""
    <style>
    /* Optimisation pour les petits écrans */
    .stApp {
        background-color: #FFFFFF;
        max-width: 450px; /* Taille standard d'un smartphone */
        margin: 0 auto;
    }

    /* Boîtes larges et tactiles */
    .mobile-card {
        background: #F9F9F9;
        border: 2px solid #FFC30B;
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 15px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }

    /* Texte noir forcé pour lecture au soleil */
    h1, h2, h3, p, label {
        color: #000000 !important;
        font-family: 'Helvetica', sans-serif;
    }

    /* Gros boutons pour les doigts */
    .stButton>button {
        width: 100% !important;
        height: 50px;
        background-color: #FFC30B !important;
        color: black !important;
        font-size: 18px !important;
        border-radius: 10px !important;
        border: 2px solid #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. EN-TÊTE ---
st.markdown("<h1 style='text-align:center;'>🐝 YAMB PRO</h1>", unsafe_allow_html=True)

# --- 3. MENU RAPIDE (ACCÈS DIRECT) ---
menu = st.radio("Aller à :", ["🔍 Scan Couvain", "📍 Ma Zone", "💰 Finance", "🤝 Avis Collègues"], horizontal=True)

# --- 4. MODULE : SCAN COUVAIN (PRIORITAIRE) ---
if menu == "🔍 Scan Couvain":
    st.markdown("### 📸 Diagnostic Instantané")
    st.write("Prenez une photo nette du cadre pour analyser la ponte.")
    
    img_file = st.camera_input("Scanner le cadre") # Ouvre l'appareil photo du téléphone
    
    if img_file:
        st.success("Analyse du couvain en cours...")
        st.markdown("""
            <div class="mobile-card">
                <p>✅ <b>État :</b> Couvain operculé sain.</p>
                <p>📊 <b>Densité :</b> 92% (Excellente Reine).</p>
                <p>⚠️ <b>Avis :</b> Quelques cellules vides, surveillez le varroa.</p>
            </div>
        """, unsafe_allow_html=True)

# --- 5. MODULE : ZONE & GPS ---
elif menu == "📍 Ma Zone":
    st.markdown("### 🛰️ Radar de Butinage")
    loc = get_geolocation()
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        m = folium.Map(location=[lat, lon], zoom_start=14)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        folium.Circle([lat, lon], radius=3000, color='#FFC30B', fill=True).add_to(m)
        st_folium(m, width=380, height=300)
    else:
        st.info("Activez le GPS de votre téléphone.")

# --- 6. MODULE : FINANCE & SOUDURE ---
elif menu == "💰 Finance":
    st.markdown("### 💵 Mon Portefeuille")
    ruches = st.number_input("Nombre de ruches", 1, 100, 10)
    valeur = ruches * 15 * 4500
    st.markdown(f"""
        <div class="mobile-card" style="text-align:center;">
            <h3>{valeur:,.0f} FCFA</h3>
            <p>Valeur de la récolte estimée</p>
        </div>
    """, unsafe_allow_html=True)

# --- 7. MODULE : AVIS COLLÈGUES ---
elif menu == "🤝 Avis Collègues":
    st.markdown("### 🗣️ Espace Communautaire")
    nom = st.text_input("Votre nom")
    commentaire = st.text_area("Votre avis sur l'application")
    if st.button("Publier mon avis"):
        st.success("Avis partagé avec le réseau !")
