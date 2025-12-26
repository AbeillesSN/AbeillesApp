import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import datetime
from streamlit_js_eval import get_geolocation
from streamlit_folium import st_folium
import folium

# --- CONFIGURATION DU THÈME ---
st.set_page_config(page_title="Abeilles du Sénégal", layout="wide", page_icon="🐝")

# CSS pour la lisibilité maximale (Texte marron foncé sur fond crème)
st.markdown("""
    <style>
    .stApp { background-color: #fcfaf0; }
    h1 { color: #5d4037 !important; text-align: center; font-weight: bold; margin-bottom: 0px; }
    h3 { color: #8d6e63 !important; text-align: center; margin-top: 0px; font-weight: bold; }
    .stMarkdown, p { color: #1a1a1a !important; font-size: 1.1rem; }
    .stButton>button { background-color: #f1c40f; color: #000000 !important; border-radius: 12px; font-weight: bold; border: 2px solid #5d4037; height: 3em; }
    .stDownloadButton>button { background-color: #2e7d32; color: #ffffff !important; border-radius: 12px; }
    [data-testid="stMetricValue"] { color: #d35400 !important; font-weight: bold; }
    [data-testid="stMetricLabel"] { color: #5d4037 !important; font-size: 1rem; }
    .stSuccess { background-color: #e8f5e9; border: 1px solid #2e7d32; color: #1b5e20; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

DB_FILE = "base_apicole_senegal_finale.csv"

# --- EN-TÊTE ET LOGO ---
col_logo_1, col_logo_2, col_logo_3 = st.columns([1, 2, 1])
with col_logo_2:
    if os.path.exists("logo.png.png"):
        st.image("logo.png.png", use_container_width=True)
    st.markdown("<h1>ABEILLES DU SÉNÉGAL</h1>", unsafe_allow_html=True)
    st.markdown("<h3>Plateforme d'Expertise Apicole</h3>", unsafe_allow_html=True)

# --- LOGIQUE MÉTIER ---
def estimer_business(potentiel, nb_ruches, prix_kg):
    ratios = {"Exceptionnel": 45, "Très Élevé": 35, "Élevé": 25, "Moyen": 15}
    rendement = ratios.get(potentiel, 10)
    total_kg = rendement * nb_ruches
    ca_estime = total_kg * prix_kg
    return rendement, total_kg, ca_estime

def sauvegarder_donnees(zone, lat, lon, potentiel, region, dept, kg, cfa):
    nouveau = {
        "Date": datetime.now().strftime("%d/%m/%Y"),
        "Entreprise": "Abeilles du Sénégal",
        "Zone_Agro": zone, "Region": region, "Departement": dept,
        "Lat": round(lat, 6), "Lon": round(lon, 6),
        "Potentiel": potentiel, "Production_KG": kg, "Revenu_CFA": cfa
    }
    df = pd.DataFrame([nouveau])
    if not os.path.isfile(DB_FILE):
        df.to_csv(DB_FILE, index=False)
    else:
        df.to_csv(DB_FILE, mode='a', header=False, index=False)

# --- NAVIGATION ---
tab1, tab2 = st.tabs(["🚀 Nouveau Diagnostic", "📊 Rapports & Carte Satellite"])

with tab1:
    loc = get_geolocation()
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        
        # LOGIQUE DÉTECTION SÉNÉGAL (Version Affinée Niayes)
        if 14.3 < lat < 16.2 and lon < -16.8:
            res = {"zone": "Niayes", "pot": "Élevé", "flore": "Eucalyptus, Agrumes, Maraîchage", "conseil": "Protéger contre les vents salins."}
        elif lat > 15.3 and lon > -16.0:
            res = {"zone": "Ferlo", "pot": "Moyen", "flore": "Acacia (Gommier), Siddem", "conseil": "Abreuvoirs solaires indispensables."}
        elif lat < 13.5 and lon < -15.0:
            res = {"zone": "Casamance", "pot": "Très Élevé", "flore": "Anacardier, Manguier, Fromager", "conseil": "Surveiller l'humidité des ruches."}
        elif lon > -13.5:
            res = {"zone": "Sénégal Oriental", "pot": "Exceptionnel", "flore": "Madd, Karité, Bambou", "conseil": "Vigilance maximale feux de brousse."}
        else:
            res = {"zone": "Bassin Arachidier", "pot": "Moyen", "flore": "Baobab, Kad, Néré", "conseil": "Favoriser le reboisement mellifère."}
            
        st.success(f"📍 Zone Identifiée : {res['zone']}")
        st.caption(f"Précision GPS : Lat {round(lat,4)}, Lon {round(lon,4)}")
        
        with st.container(border=True):
            st.markdown("<p style='text-align:center; font-weight:bold; color:#5d4037;'>SIMULATEUR DE RENDEMENT</p>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            ruches = c1.number_input("Nombre de ruches", min_value=1, value=10)
            prix = c2.select_slider("Prix de vente du KG (FCFA)", options=[3000, 4000, 5000, 6000], value=5000)
            
            rend, kg_tot, ca = estimer_business(res['pot'], ruches, prix)
            
            st.info(f"🌿 **Flore :** {res['flore']} | 💡 **Conseil :** {res['conseil']}")
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Rendement", f"{rend} kg/ruche")
            m2.metric("Total Miel", f"{kg_tot} kg")
            m3.metric("Revenu Estimé", f"{ca:,} FCFA")

        st.divider()
        reg = st.selectbox("Sélectionnez la Région", ["Dakar", "Ziguinchor", "Diourbel", "Saint-Louis", "Tambacounda", "Kaolack", "Thiès", "Louga", "Fatick", "Kolda", "Matam", "Kaffrine", "Kédougou", "Sédhiou"])
        dept = st.text_input("Localité précise (Ex: Bignona, Kayar, Sangalkam)")

        if st.button("✅ ENREGISTRER L'EXPERTISE ABEILLES DU SÉNÉGAL"):
            sauvegarder_donnees(res['zone'], lat, lon, res['pot'], reg, dept, kg_tot, ca)
            st.balloons()
            st.success(f"Diagnostic enregistré pour {dept} !")
    else:
        st.warning("🌐 Signal GPS en attente... Merci d'autoriser la localisation sur votre téléphone.")

with tab2:
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        
        st.subheader("📋 Rapport d'Expertise Professionnel")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📤 TÉLÉCHARGER LE RAPPORT ABEILLES DU SÉNÉGAL (CSV)",
            data=csv,
            file_name=f"Expertise_Abeilles_SN_{datetime.now().strftime('%d_%m_%Y')}.csv",
            mime='text/csv',
        )

        st.divider()
        st.subheader("🛰️ Cartographie Satellite Google Earth")
        m = folium.Map(location=[14.4974, -14.4524], zoom_start=7)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr='Google', name='Google Satellite').add_to(m)

        for i, row in df.iterrows():
            folium.Marker(
                [row['Lat'], row['Lon']], 
                popup=f"<b>{row['Departement']}</b><br>{row['Revenu_CFA']:,} FCFA",
                icon=folium.Icon(color='orange', icon='leaf', prefix='fa')
            ).add_to(m)
        st_folium(m, width="100%", height=500)
        
        st.divider()
        st.subheader("📊 Analyse des Revenus par Zone")
        fig = px.pie(df, values='Revenu_CFA', names='Zone_Agro', hole=.3, color_discrete_sequence=px.colors.sequential.YlOrBr)
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("### 📄 Registre Historique")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aucun historique disponible. Réalisez votre premier diagnostic pour voir les données.")
