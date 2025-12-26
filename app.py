import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="YAMB - Abeilles du Sénégal", layout="wide")

# --- STYLE POUR TOUS LES PROFILS ---
st.markdown("""
    <style>
    /* Design adapté : Couleurs vives pour repérage rapide */
    .yamb-header { background: #1B5E20; color: #FFD600; padding: 20px; border-radius: 15px; text-align: center; }
    .profile-box { padding: 10px; border-radius: 10px; text-align: center; font-weight: bold; margin-bottom: 10px; }
    .expert-card { background: #ffffff; border-left: 10px solid #FFD600; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 15px; }
    .icon-text { font-size: 24px; vertical-align: middle; margin-right: 10px; }
    .btn-green { background-color: #2E7D32; color: white; padding: 15px; border-radius: 10px; text-decoration: none; display: block; text-align: center; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='yamb-header'><h1>🐝 YAMB</h1><p>Sénégal Apiculture : Outil pour Tous</p></div>", unsafe_allow_html=True)

loc = get_geolocation()

if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    
    # --- NAVIGATION PAR PROFIL ---
    st.write("### 👤 Qui utilise l'outil aujourd'hui ?")
    profil = st.radio("Sélectionnez votre profil :", 
                     ["Traditionnel (Images & Couleurs)", "Étudiant / Universitaire (Données)", "Professionnel (Bilan)"], 
                     horizontal=True)

    st.divider()

    col_atlas, col_map = st.columns([1.2, 1])

    with col_atlas:
        if "Traditionnel" in profil:
            st.info("🟡 **Guide par l'image :** Regardez les fleurs et cliquez sur ce que vous voyez autour de vous.")
            
            # Affichage simplifié par grandes icônes pour les analphabètes
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🌳 DAHABA (Anacardier)"): st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Anacardium_occidentale_2.jpg/400px-Anacardium_occidentale_2.jpg")
                if st.button("🌳 MANGO (Manguier)"): st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Mangifera_indica_%28Mango%29_Flower_in_Hyderabad%2C_India.jpg/400px-Mangifera_indica_%28Mango%29_Flower_in_Hyderabad%2C_India.jpg")
            with col2:
                if st.button("🌿 SÉKÉW (Kinkeliba)"): st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Combretum_micranthum.jpg/400px-Combretum_micranthum.jpg")
                if st.button("🌳 KAD (Acacia)"): st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Vachellia_seyal_in_flower_in_Ethiopia.jpg/400px-Vachellia_seyal_in_flower_in_Ethiopia.jpg")

        else:
            # Affichage détaillé pour Étudiants/Pros
            st.write("### 🔬 Inventaire Scientifique (Rayon 5km)")
            options = st.multiselect("Valider les espèces présentes :", 
                                    ["Anacardium occidentale (Dahaba)", "Mangifera indica (Mango)", "Parkia biglobosa (Néré)", "Combretum micranthum (Sékéw)"])
            
            for opt in options:
                st.markdown(f"<div class='expert-card'><span class='icon-text'>✅</span> <b>{opt}</b><br>Statut : Floraison active | Potentiel : Élevé</div>", unsafe_allow_html=True)

    with col_map:
        st.write("### 🗺️ Carte (Où sont vos abeilles ?)")
        m = folium.Map(location=[lat, lon], zoom_start=14)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        
        # Le cercle Vert (3km) = Miel / Le cercle Rouge (5km) = Danger/Limite
        folium.Circle([lat, lon], radius=3000, color='green', fill=True, opacity=0.1, tooltip="Zone Miel").add_to(m)
        folium.Circle([lat, lon], radius=5000, color='red', fill=False, tooltip="Zone Limite").add_to(m)
        folium.Marker([lat, lon], popup="Rucher Central").add_to(m)
        st_folium(m, width="100%", height=450)

    # --- LE BILAN (L'action finale) ---
    st.divider()
    st.markdown("### 📋 Rapport Final")
    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
        st.markdown('<a href="#" class="btn-green">📥 TÉLÉCHARGER LE PDF (Pour l\'école ou la banque)</a>', unsafe_allow_html=True)
    with c_btn2:
        st.markdown('<a href="#" class="btn-green" style="background:#1976D2;">📤 ENVOYER PAR WHATSAPP (Pour les collègues)</a>', unsafe_allow_html=True)

else:
    st.warning("📡 YAMB cherche votre position sur la carte...")
