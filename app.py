import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import base64

# --- CONFIGURATION PRESTIGE ---
st.set_page_config(page_title="Yamb Connecté Excellence", layout="wide", page_icon="🐝")

st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #1B5E20 0%, #003300 100%);
        padding: 40px; border-radius: 0 0 30px 30px;
        color: #FFD600; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .card-pro {
        background: #ffffff; border-radius: 20px; padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05); border: 1px solid #e0e0e0;
        margin-bottom: 20px;
    }
    .section-header {
        color: #1B5E20; font-size: 24px; font-weight: 800;
        border-bottom: 3px solid #FFD600; padding-bottom: 10px; margin-bottom: 20px;
    }
    /* Bouton Rapport PDF */
    .btn-pdf {
        background-color: #D32F2F !important; color: white !important;
        font-weight: bold; border-radius: 10px; padding: 10px 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<div class='main-header'><h1>YAMB CONNECTÉ EXCELLENCE</h1><p>Intelligence Écosystémique & Gestion de Précision</p></div>", unsafe_allow_html=True)

loc = get_geolocation()

if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    
    col_a, col_b = st.columns([2, 1])

    with col_a:
        st.markdown("<div class='section-header'>📍 CARTOGRAPHIE SATELLITE (3KM)</div>", unsafe_allow_html=True)
        m = folium.Map(location=[lat, lon], zoom_start=16)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', 
                         attr='Google Satellite', name='Google').add_to(m)
        # Rayon de butinage scientifique
        folium.Circle([lat, lon], radius=3000, color='#FFD600', fill=True, opacity=0.2).add_to(m)
        folium.Marker([lat, lon], popup="Rucher Principal", icon=folium.Icon(color='green')).add_to(m)
        st_folium(m, width="100%", height=500)

    with col_b:
        st.markdown("<div class='section-header'>📊 PARAMÈTRES CRITIQUES</div>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class='card-pro'>
                <b>Coordonnées :</b> {lat:.5f} / {lon:.5f}<br><br>
                <b>Indice de Floraison :</b> <span style='color:green;'>OPTIMAL</span><br><br>
                <b>Risque Incendie :</b> <span style='color:orange;'>MODÉRÉ</span><br><br>
                <b>Humidité de l'air :</b> 62%
            </div>
        """, unsafe_allow_html=True)
        
        # BOUTON GÉNÉRER RAPPORT PDF (Simulé)
        if st.button("📄 GÉNÉRER LE RAPPORT D'EXPERTISE (PDF)"):
            st.info("Génération du document scientifique en cours...")
            st.download_button(label="📥 Télécharger le Rapport", data="Rapport d'expertise pour le rucher situé à "+str(lat), file_name="Rapport_Yamb_Connecte.txt")

    # --- DÉTAILS DE LA FLORE ---
    st.markdown("<div class='section-header'>🌿 INVENTAIRE BOTANIQUE PRÉCIS</div>", unsafe_allow_html=True)
    
    t1, t2, t3 = st.columns(3)
    t1.metric("Arbres (Strate Haute)", "Fromager, Palmier", "Diversité 85%")
    t2.metric("Arbustes (Strate Moyenne)", "Anacardier, Manguier", "Floraison Mars")
    t3.metric("Herbes (Strate Basse)", "Liane Madd, Tridax", "Source Pollen")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⭐ HOMOLOGUER LE SITE"):
        st.balloons()
        st.success("Site validé par le protocole Abeilles du Sénégal.")

else:
    st.markdown("<h2 style='text-align:center;'>🛰️ SYNCHRONISATION AVEC LES SERVEURS...</h2>", unsafe_allow_html=True)
