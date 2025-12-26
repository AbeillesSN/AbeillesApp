import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import base64
from datetime import datetime
import urllib.parse

# --- CONFIGURATION PRESTIGE ---
st.set_page_config(page_title="YAMB - Expertise Apicole", layout="wide", page_icon="🐝")

# --- BASE DE DONNÉES BOTANIQUE ---
plantes_melliferes = {
    "Anacardier (Pomme Cajou)": {
        "floraison": [1, 2, 3, 4], "miel": "Clair, fruité", "potentiel": "⭐⭐⭐⭐⭐",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Anacardium_occidentale_2.jpg/800px-Anacardium_occidentale_2.jpg"
    },
    "Manguier": {
        "floraison": [12, 1, 2, 3], "miel": "Ambré, parfumé", "potentiel": "⭐⭐⭐⭐",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Mangifera_indica_%28Mango%29_Flower_in_Hyderabad%2C_India.jpg/800px-Mangifera_indica_%28Mango%29_Flower_in_Hyderabad%2C_India.jpg"
    },
    "Eucalyptus": {
        "floraison": [9, 10, 11, 12], "miel": "Mentholé", "potentiel": "⭐⭐⭐⭐⭐",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Eucalyptus_globulus_flower_001.jpg/800px-Eucalyptus_globulus_flower_001.jpg"
    },
    "Néré (Parkia biglobosa)": {
        "floraison": [2, 3, 4], "miel": "Sombre, minéral", "potentiel": "⭐⭐⭐⭐",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Parkia_biglobosa_Kigoma.jpg/800px-Parkia_biglobosa_Kigoma.jpg"
    },
    "Acacia (Kad / Sedd)": {
        "floraison": [11, 12, 1], "miel": "Très clair", "potentiel": "⭐⭐⭐⭐⭐",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Vachellia_seyal_in_flower_in_Ethiopia.jpg/800px-Vachellia_seyal_in_flower_in_Ethiopia.jpg"
    }
}

st.markdown("""
    <style>
    .main-header { background: linear-gradient(135deg, #1B5E20, #003300); color: #FFD600; padding: 25px; border-radius: 15px; text-align: center; }
    .yamb-card { background: #F1F8E9; border: 1px solid #C8E6C9; padding: 10px; border-radius: 10px; margin-bottom: 10px; display: flex; align-items: center; }
    .yamb-card img { border-radius: 8px; margin-right: 15px; border: 2px solid #FFD600; }
    .alert-harvest { background: #FFD600; color: black; padding: 15px; border-radius: 10px; font-weight: bold; border: 2px solid black; text-align: center; }
    .btn-action { color: white !important; padding: 15px; border-radius: 10px; text-align: center; display: block; text-decoration: none; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER YAMB ---
st.markdown("<div class='main-header'><h1>🐝 YAMB - ABEILLES DU SÉNÉGAL</h1><p>VOTRE ASSISTANT D'EXPERTISE APICOLE LOCALE</p></div>", unsafe_allow_html=True)

loc = get_geolocation()

if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    mois_actuel = datetime.now().month

    col_flora, col_map = st.columns([1, 1])

    with col_flora:
        st.markdown("### 🌳 Guide Visuel de la Flore (Rayon 5km)")
        selection = st.multiselect("Identifiez les plantes présentes :", list(plantes_melliferes.keys()), default=["Manguier"])
        
        for p in selection:
            info = plantes_melliferes[p]
            en_fleurs = mois_actuel in info['floraison']
            status = "🌸 EN FLORAISON ACTUELLE" if en_fleurs else "⏳ REPOS (Prochainement)"
            color = "#1B5E20" if en_fleurs else "#666"
            
            st.markdown(f"""
                <div class='yamb-card'>
                    <img src="{info['image']}" width="110">
                    <div>
                        <b style='font-size:18px;'>{p}</b><br>
                        <span style='color:{color}; font-weight:bold;'>{status}</span><br>
                        <small>Miel : {info['miel']} | Potentiel : {info['potentiel']}</small>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    with col_map:
        st.markdown("### 🛰️ Carte Satellite du Rucher")
        m = folium.Map(location=[lat, lon], zoom_start=14)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        folium.Circle([lat, lon], radius=3000, color='green', fill=True, opacity=0.1).add_to(m)
        folium.Marker([lat, lon], icon=folium.Icon(color='green', icon='info-sign')).add_to(m)
        st_folium(m, width="100%", height=450)

    # --- ALERTES RÉCOLTE ---
    floraison_active = [p for p in selection if mois_actuel in plantes_melliferes[p]['floraison']]
    if floraison_active:
        st.markdown(f"<div class='alert-harvest'>🍯 MIEL DE {', '.join(floraison_active).upper()} : RÉCOLTE IMMINENTE !</div>", unsafe_allow_html=True)

    # --- TRANSMISSION ---
    st.divider()
    st.markdown("### 📄 Rapport Certifié & Envoi Direction")
    
    rapport = f"RAPPORT YAMB - EXPERTISE DU {datetime.now().strftime('%d/%m/%Y')}\nPosition : {lat}, {lon}\nFlore validée : {selection}"
    b64 = base64.b64encode(rapport.encode()).decode()
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<a href="data:file/txt;base64,{b64}" download="Rapport_YAMB.pdf" class="btn-action" style="background:#D32F2F;">📄 TÉLÉCHARGER LE RAPPORT PDF</a>', unsafe_allow_html=True)
    with c2:
        sujet = urllib.parse.quote("Expertise YAMB - Abeilles du Sénégal")
        corps = urllib.parse.quote(rapport)
        st.markdown(f'<a href="mailto:direction@abeillesdusenegal.sn?subject={sujet}&body={corps}" class="btn-action" style="background:#1976D2;">📧 ENVOYER PAR EMAIL</a>', unsafe_allow_html=True)

else:
    st.info("📡 Recherche du signal YAMB (GPS)... Veuillez patienter.")
