import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import datetime
from streamlit_js_eval import get_geolocation
from streamlit_folium import st_folium
import folium

# --- CONFIGURATION DU THÈME ---
st.set_page_config(page_title="Abeilles du Sénégal - Expert", layout="wide", page_icon="🐝")

# CSS pour le style Or et Nature (Identité Abeilles du Sénégal)
st.markdown("""
    <style>
    .stApp { background-color: #fcfaf0; }
    .stButton>button { background-color: #f1c40f; color: black; border-radius: 10px; border: none; font-weight: bold; width: 100%; }
    .stDownloadButton>button { background-color: #27ae60; color: white; border-radius: 10px; width: 100%; }
    h1 { color: #d35400; text-align: center; margin-bottom: 0px; }
    h3 { color: #2e7d32; text-align: center; margin-top: 0px; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

DB_FILE = "base_apicole_senegal_finale.csv"

# --- EN-TÊTE ET LOGO ---
col_logo_1, col_logo_2, col_logo_3 = st.columns([1, 2, 1])
with col_logo_2:
    if os.path.exists("logo.png.png"):
        st.image("logo.png.png", use_container_width=True)
    st.title("Abeilles du Sénégal")
    st.write("### Plateforme d'Expertise Apicole")

# --- LOGIQUE ---
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
        "Lat": round(lat, 4), "Lon": round(lon, 4),
        "Potentiel": potentiel, "Production_KG": kg, "Revenu_CFA": cfa
    }
    df = pd.DataFrame([nouveau])
    if not os.path.isfile(DB_FILE):
        df.to_csv(DB_FILE, index=False)
    else:
        df.to_csv(DB_FILE, mode='a', header=False, index=False)

# --- INTERFACE ---
tab1, tab2 = st.tabs(["🚀 Nouveau Diagnostic", "📊 Rapports & Cartographie"])

with tab1:
    loc = get_geolocation()
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        
        # LOGIQUE DÉTECTION SÉNÉGAL
        if 14.7 < lat < 15.8 and lon < -17.0:
            res = {"zone": "Niayes", "pot": "Élevé", "flore": "Eucalyptus, Agrumes", "conseil": "Brise-vent requis."}
        elif lat > 15.3 and lon > -16.0:
            res = {"zone": "Ferlo", "pot": "Moyen", "flore": "Gommier, Siddem", "conseil": "Abreuvoirs solaires."}
        elif lat < 13.5 and lon < -15.0:
            res = {"zone": "Casamance", "pot": "Très Élevé", "flore": "Anacardier, Manguier", "conseil": "Gérer l'humidité."}
        elif lon > -13.5:
            res = {"zone": "Sénégal Oriental", "pot": "Exceptionnel", "flore": "Madd, Karité", "conseil": "Vigilance feux."}
        else:
            res = {"zone": "Bassin Arachidier", "pot": "Moyen", "flore": "Baobab, Kad", "conseil": "Reboisement."}
            
        st.info(f"📍 **Zone identifiée par Abeilles du Sénégal : {res['zone']}**")
        
        with st.expander("💰 Simulation de Production", expanded=True):
            c1, c2 = st.columns(2)
            ruches = c1.number_input("Nombre de ruches", min_value=1, value=10)
            prix = c2.select_slider("Prix de vente KG (CFA)", options=[3000, 4000, 5000, 6000], value=5000)
            
            rend, kg_tot, ca = estimer_business(res['pot'], ruches, prix)
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Rendement Est.", f"{rend} kg/u")
            m2.metric("Total Miel", f"{kg_tot} kg")
            m3.metric("Revenu CFA", f"{ca:,} FCFA")

        st.markdown("---")
        reg = st.selectbox("Région de l'expertise", ["Dakar", "Ziguinchor", "Diourbel", "Saint-Louis", "Tambacounda", "Kaolack", "Thiès", "Louga", "Fatick", "Kolda", "Matam", "Kaffrine", "Kédougou", "Sédhiou"])
        dept = st.text_input("Préciser la Localité")

        if st.button("✅ VALIDER L'EXPERTISE ABEILLES DU SÉNÉGAL"):
            sauvegarder_donnees(res['zone'], lat, lon, res['pot'], reg, dept, kg_tot, ca)
            st.success("Expertise enregistrée avec succès sous le label Abeilles du Sénégal !")
            st.balloons()
    else:
        st.warning("⚠️ Accès GPS requis pour le diagnostic territorial...")

with tab2:
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        
        st.download_button(
            label="📤 TÉLÉCHARGER LE RAPPORT ABEILLES DU SÉNÉGAL",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name=f"rapport_Abeilles_du_Senegal_{datetime.now().strftime('%d_%m_%Y')}.csv",
            mime='text/csv',
        )

        st.markdown("---")
        st.subheader("🛰️ Cartographie Satellite des Zones Exploitées")
        m = folium.Map(location=[14.4974, -14.4524], zoom_start=7)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr='Google', name='Google Satellite').add_to(m)

        for i, row in df.iterrows():
            folium.Marker(
                [row['Lat'], row['Lon']], 
                popup=f"<b>Abeilles du Sénégal - {row['Departement']}</b><br>{row['Revenu_CFA']:,} CFA",
                icon=folium.Icon(color='orange')
            ).add_to(m)
        st_folium(m, width="100%", height=400)
        
        st.write("### 📄 Registre des expertises")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aucun historique pour Abeilles du Sénégal. Commencez par enregistrer une expertise.")
