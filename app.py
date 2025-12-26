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

# CSS pour corriger la lisibilité (Contraste élevé)
st.markdown("""
    <style>
    .stApp { background-color: #fcfaf0; }
    /* Titres en Marron foncé pour être très lisibles */
    h1, h2, h3 { color: #5d4037 !important; text-align: center; font-weight: bold; }
    /* Texte d'info en noir */
    .stMarkdown, p { color: #212121 !important; }
    /* Boutons avec texte noir bien visible */
    .stButton>button { background-color: #f1c40f; color: #000000 !important; border-radius: 10px; font-weight: bold; border: 2px solid #d35400; }
    .stDownloadButton>button { background-color: #2e7d32; color: #ffffff !important; border-radius: 10px; }
    /* Boîtes de mesures avec texte foncé */
    [data-testid="stMetricValue"] { color: #d35400 !important; font-weight: bold; }
    [data-testid="stMetricLabel"] { color: #5d4037 !important; }
    </style>
    """, unsafe_allow_html=True)

DB_FILE = "base_apicole_senegal_finale.csv"

# --- EN-TÊTE ET LOGO ---
col_logo_1, col_logo_2, col_logo_3 = st.columns([1, 3, 1])
with col_logo_2:
    if os.path.exists("logo.png.png"):
        st.image("logo.png.png", use_container_width=True)
    # Titre en contraste élevé
    st.markdown("<h1>ABEILLES DU SÉNÉGAL</h1>", unsafe_allow_html=True)
    st.markdown("<h3>Plateforme d'Expertise Apicole</h3>", unsafe_allow_html=True)

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
tab1, tab2 = st.tabs(["🚀 Nouveau Diagnostic", "📊 Rapports & Carte Satellite"])

with tab1:
    loc = get_geolocation()
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        
        # LOGIQUE DÉTECTION ZONES
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
            
        st.success(f"📍 **Zone détectée : {res['zone']}**")
        
        with st.container(border=True):
            st.markdown("<p style='text-align:center; font-weight:bold;'>Simulateur de Production</p>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            ruches = c1.number_input("Nombre de ruches", min_value=1, value=10)
            prix = c2.select_slider("Prix du KG (CFA)", options=[3000, 4000, 5000, 6000], value=5000)
            
            rend, kg_tot, ca = estimer_business(res['pot'], ruches, prix)
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Rendement", f"{rend} kg/u")
            m2.metric("Total Miel", f"{kg_tot} kg")
            m3.metric("Revenu CFA", f"{ca:,} FCFA")

        st.divider()
        reg = st.selectbox("Sélectionnez la Région", ["Dakar", "Ziguinchor", "Diourbel", "Saint-Louis", "Tambacounda", "Kaolack", "Thiès", "Louga", "Fatick", "Kolda", "Matam", "Kaffrine", "Kédougou", "Sédhiou"])
        dept = st.text_input("Localité précise (ex: Bignona)")

        if st.button("✅ ENREGISTRER L'EXPERTISE"):
            sauvegarder_donnees(res['zone'], lat, lon, res['pot'], reg, dept, kg_tot, ca)
            st.success("Expertise archivée avec succès !")
            st.balloons()
    else:
        st.warning("🌐 Signal GPS en attente... Vérifiez vos autorisations.")

with tab2:
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        
        st.download_button(
            label="📥 TÉLÉCHARGER LE RAPPORT COMPLET (CSV)",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name=f"Rapport_Abeilles_du_Senegal_{datetime.now().strftime('%d_%m_%Y')}.csv",
            mime='text/csv',
        )

        st.divider()
        st.subheader("🛰️ Carte Satellite des Ruchers")
        m = folium.Map(location=[14.4974, -14.4524], zoom_start=7)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr='Google', name='Google Satellite').add_to(m)

        for i, row in df.iterrows():
            folium.Marker(
                [row['Lat'], row['Lon']], 
                popup=f"<b>{row['Departement']}</b><br>{row['Revenu_CFA']:,} CFA",
                icon=folium.Icon(color='orange')
            ).add_to(m)
        st_folium(m, width="100%", height=400)
        
        st.write("### 📄 Historique des Diagnostics")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aucun historique disponible.")
