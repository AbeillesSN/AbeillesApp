import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import base64
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="YAMB - Abeilles du Sénégal", layout="wide", page_icon="🐝")

# --- BASE DE DONNÉES BOTANIQUE STRUCTURÉE ---
# Catégories : Arbres (Strate Haute), Arbustes (Moyenne), Herbes/Cultures (Basse)
flora_yamb = {
    "Arbres (Grandes tailles)": {
        "Anacardier (Dahaba)": {"mois": [1, 2, 3, 4], "miel": "Clair", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Anacardium_occidentale_2.jpg/800px-Anacardium_occidentale_2.jpg"},
        "Manguier (Mango)": {"mois": [12, 1, 2, 3], "miel": "Ambré", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Mangifera_indica_%28Mango%29_Flower_in_Hyderabad%2C_India.jpg/800px-Mangifera_indica_%28Mango%29_Flower_in_Hyderabad%2C_India.jpg"},
        "Néré (Néré)": {"mois": [2, 3, 4], "miel": "Sombre", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Parkia_biglobosa_Kigoma.jpg/800px-Parkia_biglobosa_Kigoma.jpg"},
        "Kad (Acacia seyal)": {"mois": [11, 12, 1], "miel": "Très clair", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Vachellia_seyal_in_flower_in_Ethiopia.jpg/800px-Vachellia_seyal_in_flower_in_Ethiopia.jpg"},
        "Fromager (Bentennier)": {"mois": [1, 2, 3], "miel": "Léger", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Ceiba_pentandra_flower.jpg/800px-Ceiba_pentandra_flower.jpg"}
    },
    "Arbustes et Buissons": {
        "Kinkeliba (Sékéw)": {"mois": [7, 8, 9], "miel": "Sauvage", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Combretum_micranthum.jpg/800px-Combretum_micranthum.jpg"},
        "Zizyphus (Siddem)": {"mois": [8, 9, 10], "miel": "Rare/Sidr", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Ziziphus_mauritiana_leaves_and_fruit.jpg/800px-Ziziphus_mauritiana_leaves_and_fruit.jpg"},
        "Mélaleuca (Tea Tree)": {"mois": [5, 6, 7], "miel": "Médicinal", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Melaleuca_alternifolia_-_Australian_Native_Plant_2022-07-06.jpg/800px-Melaleuca_alternifolia_-_Australian_Native_Plant_2022-07-06.jpg"}
    },
    "Herbes et Cultures": {
        "Mil (Dugub)": {"mois": [8, 9, 10], "miel": "Pollen uniquement", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Pennisetum_glaucum_n02.jpg/800px-Pennisetum_glaucum_n02.jpg"},
        "Arachide (Guerté)": {"mois": [8, 9], "miel": "Polyfloral", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Peanut_9417.jpg/800px-Peanut_9417.jpg"},
        "Tournesol": {"mois": [10, 11, 12], "miel": "Jaune vif", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/A_sunflower.jpg/800px-A_sunflower.jpg"}
    }
}

st.markdown("""
    <style>
    .yamb-header { background: #1B5E20; color: #FFD600; padding: 20px; border-radius: 15px; text-align: center; }
    .cate-title { background: #eee; padding: 5px 15px; border-radius: 5px; color: #333; font-weight: bold; margin-top: 15px; }
    .plant-box { display: flex; align-items: center; background: white; border: 1px solid #ddd; padding: 10px; border-radius: 10px; margin-bottom: 8px; }
    .plant-box img { border-radius: 5px; margin-right: 15px; border: 2px solid #1B5E20; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='yamb-header'><h1>🐝 YAMB - CATALOGUE BOTANIQUE</h1><p>Abeilles du Sénégal : Arbres, Arbustes et Cultures</p></div>", unsafe_allow_html=True)

loc = get_geolocation()

if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    mois_actuel = datetime.now().month

    col_atlas, col_map = st.columns([1.2, 1])

    with col_atlas:
        st.write("### 🔍 Inventaire de la Flore Locale")
        
        # Parcours des catégories
        for categorie, plantes in flora_yamb.items():
            st.markdown(f"<div class='cate-title'>{categorie}</div>", unsafe_allow_html=True)
            
            # Pour chaque plante dans la catégorie
            for nom, data in plantes.items():
                # On vérifie si elle est en fleurs
                en_fleurs = mois_actuel in data['mois']
                status = "🌸 EN FLEURS" if en_fleurs else "⏳ REPOS"
                color = "#1B5E20" if en_fleurs else "#999"
                
                # Case à cocher pour l'expert
                if st.checkbox(f"Confirmer présence : {nom}", key=nom):
                    st.markdown(f"""
                        <div class='plant-box'>
                            <img src="{data['img']}" width="70">
                            <div>
                                <b>{nom}</b><br>
                                <span style='color:{color}; font-size:12px; font-weight:bold;'>{status}</span><br>
                                <small>Type de miel : {data['miel']}</small>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

    with col_map:
        st.write("### 🗺️ Rayon d'action (5km)")
        m = folium.Map(location=[lat, lon], zoom_start=13)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        folium.Circle([lat, lon], radius=5000, color='orange', fill=False).add_to(m)
        folium.Marker([lat, lon], popup="Rucher YAMB").add_to(m)
        st_folium(m, width="100%", height=500)

else:
    st.warning("📡 Recherche du signal GPS YAMB...")
