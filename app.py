import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import datetime
from streamlit_js_eval import get_geolocation
from streamlit_folium import st_folium
import folium

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Expert Abeilles Sénégal", layout="wide", page_icon="🐝")
DB_FILE = "historique_expertises.csv"

# --- LOGIQUE FINANCIÈRE ET RENDEMENT ---
def estimer_business(potentiel, nb_ruches, prix_kg):
    ratios = {
        "Exceptionnel": 45,
        "Très Élevé": 35,
        "Élevé": 25,
        "Moyen": 15
    }
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

# --- INTERFACE PRINCIPALE ---
st.title("🐝 Expert Abeilles Sénégal")
st.markdown("### Système National d'Aide à la Décision Apicole")

tab1, tab2 = st.tabs(["🚀 Diagnostic & Business", "🌍 Carte Satellite & Analyse"])

with tab1:
    loc = get_geolocation()
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        
        # --- MOTEUR DE DÉTERMINATION DES ZONES AGROÉCOLOGIQUES ---
        if 14.7 < lat < 15.8 and lon < -17.0:
            res = {"zone": "Niayes", "pot": "Élevé", "flore": "Eucalyptus, Filao, Agrumes", "conseil": "Installer des brise-vent."}
        elif lat > 15.3 and lon > -16.0:
            res = {"zone": "Ferlo (Zone Sylvopastorale)", "pot": "Moyen", "flore": "Gommier, Siddem, Soump", "conseil": "Abreuvoirs solaires indispensables."}
        elif lat < 13.5 and lon < -15.0:
            res = {"zone": "Casamance", "pot": "Très Élevé", "flore": "Anacardier, Manguier, Fromager", "conseil": "Lutter contre l'humidité."}
        elif lon > -13.5:
            res = {"zone": "Sénégal Oriental", "pot": "Exceptionnel", "flore": "Madd, Karité, Bambou", "conseil": "Vigilance feux de brousse."}
        else:
            res = {"zone": "Bassin Arachidier", "pot": "Moyen", "flore": "Baobab, Kad, Tamarinier", "conseil": "Enrichir la flore (reboisement)."}
            
        st.success(f"📍 **Terroir détecté : {res['zone']}**")
        
        # --- CALCULATEUR ÉCONOMIQUE ---
        with st.container(border=True):
            st.subheader("💰 Simulateur de Rentabilité")
            c1, c2 = st.columns(2)
            with c1:
                nb_ruches = st.number_input("Nombre de ruches", min_value=1, value=10)
            with c2:
                prix_kg = st.select_slider("Prix du KG (FCFA)", options=[3000, 3500, 4000, 4500, 5000, 6000], value=4500)
            
            rend_u, tot_kg, ca = estimer_business(res['pot'], nb_ruches, prix_kg)
            
            st.info(f"🌿 **Flore locale :** {res['flore']} | 💡 **Conseil :** {res['conseil']}")
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Rendement/Ruche", f"{rend_u} kg")
            m2.metric("Total Miel", f"{tot_kg} kg")
            m3.metric("Revenu Estimé", f"{ca:,} FCFA")

        # --- INFORMATIONS ADMINISTRATIVES ---
        st.divider()
        col_reg, col_dept = st.columns(2)
        with col_reg:
            reg = st.selectbox("Région", ["Dakar", "Ziguinchor", "Diourbel", "Saint-Louis", "Tambacounda", "Kaolack", "Thiès", "Louga", "Fatick", "Kolda", "Matam", "Kaffrine", "Kédougou", "Sédhiou"])
        with col_dept:
            dept = st.text_input("Département / Commune", placeholder="Ex: Bignona, Linguère...")

        if st.button("📥 Enregistrer l'Expertise"):
            sauvegarder_donnees(res['zone'], lat, lon, res['pot'], reg, dept, tot_kg, ca)
            st.success(f"Expertise enregistrée pour {dept} !")
            st.balloons()
    else:
        st.warning("🌐 Recherche du signal GPS... Veuillez autoriser la localisation.")

with tab2:
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        
        # --- CARTE SATELLITE ---
        st.subheader("🛰️ Vue Google Earth des sites")
        m = folium.Map(location=[14.4974, -14.4524], zoom_start=7)
        
        folium.TileLayer(
            tiles = 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
            attr = 'Google Satellite',
            name = 'Google Earth',
            overlay = False,
            control = True
        ).add_to(m)

        for i, row in df.iterrows():
            folium.Marker(
                [row['Lat'], row['Lon']],
                popup=f"<b>{row['Departement']}</b><br>{row['Revenu_CFA']:,} FCFA",
                icon=folium.Icon(color='orange', icon='record')
            ).add_to(m)
        
        st_folium(m, width="100%", height=500)
        
        # --- ANALYSE GRAPHIQUE ---
        st.divider()
        st.subheader("📊 Performance par Zone")
        fig = px.bar(df, x="Zone_Agro", y="Revenu_CFA", color="Region", barmode="group", title="Chiffre d'Affaires potentiel par zone")
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("### 📄 Historique des expertises")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aucune donnée disponible. Réalisez votre premier diagnostic !")
