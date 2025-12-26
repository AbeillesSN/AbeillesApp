import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import pandas as pd
from datetime import datetime
import requests

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="YAMB - Abeilles du Sénégal", page_icon="🐝", layout="centered")

# --- 2. STYLE ALVÉOLE & BOIS ---
st.markdown("""
    <style>
    .stApp { background-color: #FDF5E6; }
    .main-header {
        background: linear-gradient(135deg, #8B4513 0%, #5D2E0A 100%);
        color: #FFC30B; padding: 25px; border-radius: 0 0 40px 40px;
        text-align: center; border-bottom: 6px solid #FFC30B;
    }
    .flore-card {
        background-color: #FFF9E3; border-radius: 15px; padding: 15px;
        border: 2px solid #FFC30B; margin-bottom: 10px; color: #5D2E0A;
    }
    .status-ok { color: #28a745; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DONNÉES FLORE MELLIFÈRE SÉNÉGALAISE ---
data_flore = [
    {"Espèce": "Kadd (Faidherbia)", "Type": "🌳 Arbre", "Mois": [11, 12, 1, 2, 3], "Zone": "Sénégal Septentrional / Centre"},
    {"Espèce": "Anacardier (Cajou)", "Type": "🌳 Culture", "Mois": [12, 1, 2, 3], "Zone": "Casamance / Niayes / Centre"},
    {"Espèce": "Manguier", "Type": "🌳 Culture", "Mois": [1, 2, 3], "Zone": "National"},
    {"Espèce": "Eucalyptus", "Type": "🌳 Arbre", "Mois": [3, 4, 5, 6], "Zone": "Littoral / Niayes"},
    {"Espèce": "Néré (Parkia)", "Type": "🌳 Arbre", "Mois": [1, 2, 3, 4], "Zone": "Sud / Est"},
    {"Espèce": "Acacia Sénégal", "Type": "🌳 Arbre", "Mois": [8, 9, 10], "Zone": "Nord / Centre"},
    {"Espèce": "Baobab", "Type": "🌳 Arbre", "Mois": [5, 6, 7], "Zone": "Centre / Sud"},
    {"Espèce": "Kinkeliba", "Type": "🌿 Arbuste", "Mois": [7, 8, 9], "Zone": "National"}
]
df_flore = pd.DataFrame(data_flore)

# --- 4. LOGIQUE DE DÉTECTION ---
mois_actuel = datetime.now().month
nom_mois = datetime.now().strftime('%B')

# --- 5. ENTÊTE ---
st.markdown("""
    <div class='main-header'>
        <div style='font-size:12px; font-weight:bold; color:#FFC30B; letter-spacing:4px;'>ABEILLES DU SÉNÉGAL</div>
        <h1 style='margin:0; color:white;'>🐝 YAMB PRO</h1>
    </div>
    """, unsafe_allow_html=True)

# --- 6. NAVIGATION ---
tabs = st.tabs(["🌸 FLORE & MÉTÉO", "🍯 PRODUCTION", "🚨 SOS"])

loc = get_geolocation()

with tabs[0]:
    st.header(f"Analyse du Rayon (3 km) - {nom_mois}")
    
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        
        # --- BLOC MÉTÉO ---
        try:
            w_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            res = requests.get(w_url).json()['current_weather']
            col1, col2 = st.columns(2)
            col1.metric("Température", f"{res['temperature']}°C")
            col2.metric("Vent", f"{res['windspeed']} km/h")
        except: st.write("Météo en attente...")

        st.divider()

        # --- BLOC FLORE MELLIFÈRE ---
        st.subheader("🌿 Ressources disponibles actuellement")
        
        # Filtrage de la flore selon le mois actuel
        flore_active = df_flore[df_flore['Mois'].apply(lambda x: mois_actuel in x)]
        
        if not flore_active.empty:
            for _, row in flore_active.iterrows():
                with st.expander(f"{row['Type']} : {row['Espèce']}"):
                    st.write(f"📍 **Zone principale :** {row['Zone']}")
                    st.write(f"📅 **Période :** Fleurit jusqu'au mois {max(row['Mois'])}")
                    st.progress(100 if mois_actuel in row['Mois'] else 0)
        else:
            st.info("Période de repos floral. Surveillez les réserves de la ruche.")

        # --- CARTE SATELLITE 3KM ---
        st.subheader("🛰️ Surveillance Satellite")
        m = folium.Map(location=[lat, lon], zoom_start=14)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        # Cercle de 3km pour la flore
        folium.Circle([lat, lon], radius=3000, color='#FFC30B', fill=True, fill_opacity=0.1, popup="Zone de butinage").add_to(m)
        st_folium(m, width="100%", height=300)
    else:
        st.warning("📍 Activez la localisation pour voir la flore autour de vous.")

with tabs[1]:
    st.subheader("Estimation Production")
    nb = st.number_input("Nombre de ruches", 1, 500, 10)
    st.metric("Récolte Abeilles du Sénégal", f"{nb * 12} kg", "Miel de cru")

with tabs[2]:
    st.subheader("Urgence Sécurité")
    st.markdown('<a href="https://wa.me/" class="whatsapp-btn" style="display:block; background:#25D366; color:white; padding:20px; text-align:center; border-radius:15px; text-decoration:none; font-weight:bold;">🟢 CONTACTER LE SIÈGE (SOS)</a>', unsafe_allow_html=True)

st.markdown("<p style='text-align:center; padding:30px; font-weight:bold;'>© 2025 Abeilles du Sénégal</p>", unsafe_allow_html=True)
