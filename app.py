import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import base64
from datetime import datetime
import urllib.parse

# --- BASE DE DONNÉES BOTANIQUE COMPLÈTE AVEC IMAGES ---
plantes_melliferes = {
    "Anacardier (Pomme Cajou)": {
        "floraison": [1, 2, 3, 4], "miel": "Clair, goût fruité", "potentiel": "⭐⭐⭐⭐⭐",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Anacardium_occidentale_2.jpg/800px-Anacardium_occidentale_2.jpg"
    },
    "Manguier": {
        "floraison": [12, 1, 2, 3], "miel": "Ambré, très parfumé", "potentiel": "⭐⭐⭐⭐",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Mangifera_indica_%28Mango%29_Flower_in_Hyderabad%2C_India.jpg/800px-Mangifera_indica_%28Mango%29_Flower_in_Hyderabad%2C_India.jpg"
    },
    "Eucalyptus": {
        "floraison": [9, 10, 11, 12], "miel": "Mentholé, médicinal", "potentiel": "⭐⭐⭐⭐⭐",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Eucalyptus_globulus_flower_001.jpg/800px-Eucalyptus_globulus_flower_001.jpg"
    },
    "Néré (Parkia biglobosa)": {
        "floraison": [2, 3, 4], "miel": "Sombre, riche en minéraux", "potentiel": "⭐⭐⭐⭐",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Parkia_biglobosa_Kigoma.jpg/800px-Parkia_biglobosa_Kigoma.jpg"
    },
    "Fromager (Ceiba pentandra)": {
        "floraison": [1, 2, 3], "miel": "Léger, liquide", "potentiel": "⭐⭐⭐",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Ceiba_pentandra_flower.jpg/800px-Ceiba_pentandra_flower.jpg"
    },
    "Zizyphus (Maure)": {
        "floraison": [8, 9, 10], "miel": "Rare, très prisé (Sidr)", "potentiel": "⭐⭐⭐⭐⭐",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Ziziphus_mauritiana_leaves_and_fruit.jpg/800px-Ziziphus_mauritiana_leaves_and_fruit.jpg"
    },
    "Acacia (Kad/Sedd)": {
        "floraison": [11, 12, 1], "miel": "Très clair, cristallise peu", "potentiel": "⭐⭐⭐⭐⭐",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Vachellia_seyal_in_flower_in_Ethiopia.jpg/800px-Vachellia_seyal_in_flower_in_Ethiopia.jpg"
    },
    "Palmier à huile": {
        "floraison": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "miel": "Source de pollen constante", "potentiel": "⭐⭐",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Oil_palm_%28Elaeis_guineensis%29_in_Blantyre%2C_Malawi_01.jpg/800px-Oil_palm_%28Elaeis_guineensis%29_in_Blantyre%2C_Malawi_01.jpg"
    },
    "Kinkeliba": {
        "floraison": [7, 8, 9], "miel": "Miel sauvage de brousse", "potentiel": "⭐⭐⭐",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Combretum_micranthum.jpg/800px-Combretum_micranthum.jpg"
    },
    "Mélaleuca (Tea Tree)": {
        "floraison": [5, 6, 7], "miel": "Puissant, antibactérien", "potentiel": "⭐⭐⭐⭐",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Melaleuca_alternifolia_-_Australian_Native_Plant_2022-07-06.jpg/800px-Melaleuca_alternifolia_-_Australian_Native_Plant_2022-07-06.jpg"
    }
}

st.markdown("""
    <style>
    .main-header { background: linear-gradient(135deg, #1B5E20, #004D40); color: #FFD600; padding: 25px; border-radius: 15px; text-align: center; }
    .plant-card-visual { background: #F1F8E9; border: 1px solid #C8E6C9; padding: 10px; border-radius: 10px; margin-bottom: 10px; display: flex; align-items: center; }
    .plant-card-visual img { border-radius: 5px; margin-right: 10px; }
    .current-bloom { color: #1B5E20; font-weight: bold; }
    .next-bloom { color: #666; font-weight: bold; }
    .stButton>button { background-color: #1B5E20 !important; color: white !important; font-weight: bold; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-header'><h1>🐝 ATLAS MELLIFÈRE VISUEL</h1><p>IDENTIFICATION ET PRÉDICTION</p></div>", unsafe_allow_html=True)

loc = get_geolocation()

if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    mois_actuel = datetime.now().month

    col_flora, col_map = st.columns([1, 1])

    with col_flora:
        st.markdown("### 🌳 Guide des Plantes (Rayon 5km)")
        selection = st.multiselect("Sélectionnez les plantes mellifères pour les visualiser :", 
                                 list(plantes_melliferes.keys()), 
                                 default=["Anacardier (Pomme Cajou)", "Manguier"])
        
        st.markdown("---")
        for p in selection:
            info = plantes_melliferes[p]
            status_text = ""
            status_class = ""
            if mois_actuel in info['floraison']:
                status_text = "🌸 STATUT : EN FLORAISON ACTUELLE"
                status_class = "current-bloom"
            else:
                prochain_mois = [m for m in info['floraison'] if m > mois_actuel]
                if not prochain_mois: # Si floraison passée pour cette année, on prend le premier mois de l'année suivante
                    prochain_mois = [info['floraison'][0]]
                status_text = f"⏳ STATUT : Prochaine floraison en mois {prochain_mois[0]}"
                status_class = "next-bloom"
            
            st.markdown(f"""
                <div class='plant-card-visual'>
                    <img src="{info['image']}" width="100">
                    <div>
                        <b style='font-size:18px;'>{p}</b><br>
                        <span class='{status_class}'>{status_text}</span><br>
                        <small>Miel : {info['miel']} | Potentiel : {info['potentiel']}</small>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    with col_map:
        st.markdown("### 🗺️ Carte d'Analyse (Zone 5km)")
        m = folium.Map(location=[lat, lon], zoom_start=14)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        folium.Circle([lat, lon], radius=3000, color='green', fill=True, opacity=0.1).add_to(m)
        folium.Circle([lat, lon], radius=5000, color='orange', fill=False).add_to(m)
        folium.Marker([lat, lon], icon=folium.Icon(color='green')).add_to(m)
        st_folium(m, width="100%", height=500)

    # --- ALERTE RÉCOLTE DYNAMIQUE ---
    floraison_active = [p for p in selection if mois_actuel in plantes_melliferes[p]['floraison']]
    if floraison_active:
        st.markdown(f"""
            <div style='background: #FFD600; color: black; padding: 15px; border-radius: 10px; font-weight: bold; border: 2px solid black; margin-top:20px;'>
                🔔 ALERTE ACTIVE : Miellée en cours sur {', '.join(floraison_active)} ! Préparez la récolte.
            </div>
        """, unsafe_allow_html=True)
    
    # --- TRANSMISSION DES DONNÉES ---
    st.divider()
    c1, c2 = st.columns(2)
    
    rapport = f"RAPPORT EXPERT - {lat}, {lon}\nPlantes détectées : {selection}\nMois : {mois_actuel}"
    
    with c1:
        b64 = base64.b64encode(rapport.encode()).decode()
        st.markdown(f'<a href="data:file/txt;base64,{b64}" download="Rapport_Visuel_Flore.pdf" style="text-decoration:none;"><div style="background-color:#D32F2F; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold;">📄 TÉLÉCHARGER LE RAPPORT PDF</div></a>', unsafe_allow_html=True)
    
    with c2:
        sujet = urllib.parse.quote("Rapport de Flore Visuel - Abeilles du Sénégal")
        corps = urllib.parse.quote(rapport)
        st.markdown(f'<a href="mailto:direction@abeillesdusenegal.sn?subject={sujet}&body={corps}" style="text-decoration:none;"><div style="background-color:#1976D2; color:white; padding:15px; border-radius:10px; text-align:center; font-weight:bold;">📧 ENVOYER À LA DIRECTION</div></a>', unsafe_allow_html=True)

else:
    st.info("ℹ️ Info : Synchronisation GPS pour la dernière précision...")
