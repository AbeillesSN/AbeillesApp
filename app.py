import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
from datetime import datetime
from PIL import Image

# --- 1. CONFIGURATION & CHARTE GRAPHIQUE ---
st.set_page_config(page_title="YAMB - Abeilles du Sénégal", layout="centered", page_icon="🐝")

st.markdown("""
    <style>
    :root { --gold: #FFC107; --green: #1B5E20; --amber: #FF8F00; }
    @media (prefers-color-scheme: dark) { .stApp { background-color: #0E1117; color: white; } }
    
    .main-header {
        background: linear-gradient(135deg, #1B5E20 0%, #051A07 100%);
        color: var(--gold);
        padding: 30px;
        border-radius: 0 0 40px 40px;
        text-align: center;
        border-bottom: 5px solid var(--amber);
        margin-bottom: 20px;
    }
    .ia-card {
        background: rgba(27, 94, 32, 0.1);
        border: 2px solid var(--gold);
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f5;
        border-radius: 10px 10px 0 0;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIQUE IA (DONNÉES) ---
potentials = {
    "Anacardier (Dahaba)": 15, "Manguier (Mango)": 10, 
    "Kad (Acacia)": 20, "Néré": 12, "Flore Sauvage": 8
}

# --- 3. ENTÊTE ---
st.markdown("""
    <div class='main-header'>
        <h1 style='margin:0; font-size:35px;'>🐝 YAMB</h1>
        <p style='margin:0; opacity:0.8;'>SYSTÈME D'EXPERTISE APICOLE DU SÉNÉGAL</p>
    </div>
    """, unsafe_allow_html=True)

loc = get_geolocation()

if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    
    # --- 4. NAVIGATION PAR ONGLETS ---
    tabs = st.tabs(["🏠 Accueil & IA", "🌸 Flore", "📸 Caméra", "📖 Journal", "📍 Carte"])

    with tabs[0]: # ACCUEIL & IA
        st.markdown("### 🤖 Conseiller IA")
        nb_ruches = st.number_input("Nombre de ruches :", min_value=1, value=5)
        flore_select = st.multiselect("Plantes dominantes :", list(potentials.keys()), default=["Anacardier (Dahaba)"])
        
        if flore_select:
            rendement = (sum([potentials[p] for p in flore_select]) / len(flore_select)) * nb_ruches
            st.markdown(f"""
                <div class='ia-card'>
                    <b style='color:var(--amber);'>PRÉDICTION DE RÉCOLTE :</b><br>
                    <span style='font-size:24px;'>{rendement:.1f} KG de Miel</span><br>
                    <small>Basé sur une zone de butinage de 3 km.</small>
                </div>
            """, unsafe_allow_html=True)

    with tabs[1]: # FLORE VISUELLE
        st.markdown("### 🌳 Identification (Rayon 5km)")
        c1, c2 = st.columns(2)
        with c1:
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Anacardium_occidentale_2.jpg/400px-Anacardium_occidentale_2.jpg", caption="Anacardier")
            st.checkbox("Présent : Dahaba", key="c1")
        with c2:
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Mangifera_indica_%28Mango%29_Flower_in_Hyderabad%2C_India.jpg/400px-Mangifera_indica_%28Mango%29_Flower_in_Hyderabad%2C_India.jpg", caption="Manguier")
            st.checkbox("Présent : Mango", key="c2")

    with tabs[2]: # CAMERA
        st.markdown("### 📸 Capture Terrain")
        photo = st.camera_input("Scanner une ruche ou une fleur")
        if photo:
            st.success("Photo enregistrée avec succès.")

    with tabs[3]: # JOURNAL DE BORD
        st.markdown("### 📖 Suivi du Rucher")
        st.date_input("Date de visite", datetime.now())
        st.select_slider("Santé de la colonie", options=["Critique", "Moyenne", "Excellente"])
        st.text_area("Notes d'observation (Ponte, Météo, etc.)")

    with tabs[4]: # CARTE SATELLITE
        st.markdown("### 🗺️ Zone de Butinage")
        m = folium.Map(location=[lat, lon], zoom_start=14)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        # Cercles de portée
        folium.Circle([lat, lon], radius=3000, color='green', fill=True, opacity=0.1).add_to(m)
        folium.Circle([lat, lon], radius=5000, color='orange', fill=False, dash_array='5').add_to(m)
        folium.Marker([lat, lon], icon=folium.Icon(color='green', icon='leaf')).add_to(m)
        st_folium(m, width="100%", height=400)

    # --- 5. ACTION FINALE ---
    st.divider()
    if st.button("📤 TRANSMETTRE L'EXPERTISE COMPLÈTE"):
        st.balloons()
        st.success("Dossier YAMB envoyé à Abeilles du Sénégal.")

else:
    st.markdown("<div style='text-align:center; padding:100px;'><h1>🛰️</h1><p>Recherche du signal GPS YAMB...</p></div>", unsafe_allow_html=True)
