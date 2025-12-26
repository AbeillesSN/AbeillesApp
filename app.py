import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import datetime
from streamlit_js_eval import get_geolocation
from streamlit_folium import st_folium
import folium

# --- CONFIGURATION ---
st.set_page_config(page_title="Expert Abeilles Sénégal", layout="wide", page_icon="🐝")
# Nom de fichier unique pour éviter les erreurs de structure (KeyError)
DB_FILE = "base_expert_senegal_v1.csv"

# --- LOGIQUE DE CALCUL ---
def estimer_business(potentiel, nb_ruches, prix_kg):
    ratios = {"Exceptionnel": 45, "Très Élevé": 35, "Élevé": 25, "Moyen": 15}
    rendement = ratios.get(potentiel, 10)
    total_kg = rendement * nb_ruches
    ca_estime = total_kg * prix_kg
    return rendement, total_kg, ca_estime

# --- SAUVEGARDE DES DONNÉES ---
def sauvegarder_donnees(zone, lat, lon, potentiel, region, dept, kg, cfa):
    nouveau = {
        "Date": datetime.now().strftime("%d/%m/%Y"),
        "Zone_Agro": zone, 
        "Region": region, 
        "Departement": dept,
        "Lat": round(lat, 4), 
        "Lon": round(lon, 4),
        "Potentiel": potentiel, 
        "Production_KG": kg, 
        "Revenu_CFA": cfa
    }
    df = pd.DataFrame([nouveau])
    if not os.path.isfile(DB_FILE):
        df.to_csv(DB_FILE, index=False)
    else:
        df.to_csv(DB_FILE, mode='a', header=False, index=False)

# --- INTERFACE UTILISATEUR ---
st.title("🐝 Expert Abeilles Sénégal (Officiel)")

tab1, tab2 = st.tabs(["🚀 Diagnostic & Revenus", "🌍 Carte Google Earth"])

with tab1:
    loc = get_geolocation()
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        
        # LOGIQUE DE DÉTECTION DES TERROIRS SÉNÉGALAIS
        if 14.7 < lat < 15.8 and lon < -17.0:
            res = {"zone": "Niayes", "pot": "Élevé", "flore": "Eucalyptus, Agrumes", "conseil": "Brise-vent requis."}
        elif lat > 15.3 and lon > -16.0:
            res =
