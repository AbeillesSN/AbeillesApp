import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="YAMB - Expertise Flore", layout="wide", page_icon="🐝")

# --- BASE DE DONNÉES APICOLE (Noms complets) ---
flora_apicole = {
    "🌳 STRATE HAUTE (Arbres majeurs)": {
        "Anacardier (Dahaba / Anacardium occidentale)": {"mois": [1, 2, 3, 4], "apport": "Nectar & Pollen", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Anacardium_occidentale_2.jpg/800px-Anacardium_occidentale_2.jpg"},
        "Manguier (Mango / Mangifera indica)": {"mois": [12, 1, 2, 3], "apport": "Nectar ++", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Mangifera_indica_%28Mango%29_Flower_in_Hyderabad%2C_India.jpg/800px-Mangifera_indica_%28Mango%29_Flower_in_Hyderabad%2C_India.jpg"},
        "Néré (Néré / Parkia biglobosa)": {"mois": [2, 3, 4], "apport": "Nectar (Miel sombre)", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Parkia_biglobosa_Kigoma.jpg/800px-Parkia_biglobosa_Kigoma.jpg"},
        "Kad (Acacia seyal)": {"mois": [11, 12, 1], "apport": "Nectar +++", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Vachellia_seyal_in_flower_in_Ethiopia.jpg/800px-Vachellia_seyal_in_flower_in_Ethiopia.jpg"},
        "Eucalyptus (Gommier)": {"mois": [9, 10, 11, 12], "apport": "Nectar & Miellat", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Eucalyptus_globulus_flower_001.jpg/800px-Eucalyptus_globulus_flower_001.jpg"}
    },
    "🌿 STRATE MOYENNE (Arbustes & Buissons)": {
        "Kinkeliba (Sékéw / Combretum micranthum)": {"mois": [7, 8, 9], "apport": "Pollen & Nectar", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Combretum_micranthum.jpg/800px-Combretum_micranthum.jpg"},
        "Zizyphus (Siddem / Juju)": {"mois": [8, 9, 10], "apport": "Nectar (Miel Sidr)", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Ziziphus_mauritiana_leaves_and_fruit.jpg/800px-Ziziphus_mauritiana_leaves_and_fruit.jpg"},
        "Mélaleuca (Tea Tree)": {"mois": [5, 6, 7], "apport": "Nectar Médicinal", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Melaleuca_alternifolia_-_Australian_Native_Plant_2022-07-06.jpg/800px-Melaleuca_alternifolia_-_Australian_Native_Plant_2022-07-06.jpg"}
    },
    "🌱 STRATE BASSE (Herbes & Cultures)": {
        "Arachide (Guerté / Arachis hypogaea)": {"mois": [8, 9], "apport": "Pollen", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Peanut_9417.jpg/800px-Peanut_9417.jpg"},
        "Mil (Dugub / Pennisetum)": {"mois": [8, 9, 10], "apport": "Pollen important", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Pennisetum_glaucum_n02.jpg/800px-Pennisetum_glaucum_n02.jpg"},
        "Tournesol (Solaire)": {"mois": [10, 11, 12], "apport": "Nectar & Pollen ++", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/A_sunflower.jpg/800px-A_sunflower.jpg"}
    }
}

# --- STYLE CSS ---
st.markdown("""
    <style>
    .yamb-banner { background: #1B5E20; color: #FFD600; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px;}
    .section-title { color: #1B5E20; border-bottom: 2px solid #FFD600; padding-bottom: 5px; margin-top: 20px; font-weight: bold; }
    .plant-card { background: white; border: 1px solid #eee; border-radius: 10px; padding: 15px; margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .status-badge { padding: 3px 8px; border-radius: 5px; font-size: 11px; font-weight: bold; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='yamb-banner'><h1>🐝 YAMB EXPERT</h1><p>Diagnostic de la Ressource Mellifère (Rayon 5km)</p></div>", unsafe_allow_html=True)

loc = get_geolocation()

if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    mois_actuel = datetime.now().month

    col_atlas, col_map = st.columns([1.3, 1])

    with col_atlas:
        st.subheader("📋 Inventaire Botanique du Rucher")
        
        for cate, plantes in flora_apicole.items():
            st.markdown(f"<div class='section-title'>{cate}</div>", unsafe_allow_html=True)
            
            for nom, data in plantes.items():
                en_fleurs = mois_actuel in data['mois']
                badge_color = "#2E7D32" if en_fleurs else "#757575"
                badge_text = "FLORAISON ACTIVE" if en_fleurs else "HORS FLORAISON"
                
                # Checkbox pour sélection expert
                if st.checkbox(f"Valider présence : {nom}", key=nom):
                    st.markdown(f"""
                        <div class='plant-card'>
                            <div style="display: flex; align-items: center;">
                                <img src="{data['img']}" width="80" style="border-radius: 5px; margin-right: 15px;">
                                <div>
                                    <b style="font-size: 16px;">{nom}</b><br>
                                    <span class='status-badge' style='background-color:{badge_color};'>{badge_text}</span><br>
                                    <span style="color: #555; font-size: 13px;">Apport : {data['apport']}</span>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

    with col_map:
        st.subheader("🗺️ Zone de Butinage")
        m = folium.Map(location=[lat, lon], zoom_start=13)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        # Rayon 3km (Butinage efficace) et 5km (Limite)
        folium.Circle([lat, lon], radius=3000, color='green', fill=True, opacity=0.1).add_to(m)
        folium.Circle([lat, lon], radius=5000, color='orange', fill=False, dash_array='5,5').add_to(m)
        folium.Marker([lat, lon], icon=folium.Icon(color='green')).add_to(m)
        st_folium(m, width="100%", height=550)

else:
    st.warning("📡 En attente de la localisation précise pour YAMB...")
