import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import datetime
from streamlit_js_eval import get_geolocation

# --- CONFIGURATION ---
st.set_page_config(page_title="Expert Abeilles Sénégal", layout="wide")
DB_FILE = "historique_expertises.csv"

# --- LOGIQUE DE SAUVEGARDE ---
def sauvegarder_diagnostic(zone, lat, lon, potentiel):
    nouveau_rapport = {
        "Date": datetime.now().strftime("%d/%m/%Y"),
        "Zone": zone,
        "Latitude": round(lat, 4),
        "Longitude": round(lon, 4),
        "Potentiel": potentiel
    }
    df = pd.DataFrame([nouveau_rapport])
    if not os.path.isfile(DB_FILE):
        df.to_csv(DB_FILE, index=False)
    else:
        df.to_csv(DB_FILE, mode='a', header=False, index=False)

# --- INTERFACE ---
st.title("🐝 Abeilles du Sénégal : Pilotage & Statistiques")

tab1, tab2 = st.tabs(["🆕 Nouveau Diagnostic", "📊 Analyses & Historique"])

with tab1:
    loc = get_geolocation()
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        
        # Intelligence Terroir (Exemple Niayes vs Bassin Arachidier)
        if 14.7 < lat < 15.8:
            res = {"zone": "Niayes", "potentiel": "Eleve"}
        else:
            res = {"zone": "Bassin Arachidier", "potentiel": "Moyen"}
            
        st.subheader(f"📍 Diagnostic actuel : {res['zone']}")
        st.write(f"Potentiel détecté : **{res['potentiel']}**")
        
        if st.button("📥 Enregistrer et Archiver"):
            sauvegarder_diagnostic(res['zone'], lat, lon, res['potentiel'])
            st.success("Données ajoutées aux statistiques !")
            st.balloons()
    else:
        st.info("🌐 Recherche du signal GPS...")

with tab2:
    if os.path.exists(DB_FILE):
        df_hist = pd.read_csv(DB_FILE)
        
        # --- SECTION GRAPHIQUES ---
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### Répartition par Zone")
            fig_pie = px.pie(df_hist, names='Zone', hole=0.3, color_discrete_sequence=px.colors.sequential.YlOrBr)
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with col2:
            st.write("### Analyse du Potentiel")
            fig_bar = px.bar(df_hist, x='Potentiel', color='Potentiel', 
                             color_discrete_map={'Eleve': 'green', 'Moyen': 'orange', 'Faible': 'red'})
            st.plotly_chart(fig_bar, use_container_width=True)

        st.divider()
        st.write("### Table des données brutes")
        st.dataframe(df_hist, use_container_width=True)
    else:
        st.warning("Aucune donnée disponible pour l'analyse.")
