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
# Nouveau nom pour réinitialiser proprement la base de données sans erreurs
DB_FILE = "base_apicole_senegal_finale.csv"

def estimer_business(potentiel, nb_ruches, prix_kg):
    ratios = {"Exceptionnel": 45, "Très Élevé": 35, "Élevé": 25, "Moyen": 15}
    rendement = ratios.get(potentiel, 10)
    total_kg = rendement * nb_ruches
    ca_estime = total_kg * prix_kg
    return rendement, total_kg, ca_estime

def sauvegarder_donnees(zone, lat, lon, potentiel, region, dept, kg, cfa):
    nouveau = {
        "Date": datetime.now().strftime("%d/%m/%Y"),
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
st.title("🐝 Expert Abeilles Sénégal (Officiel)")

tab1, tab2 = st.tabs(["🚀 Diagnostic & Revenus", "🌍 Carte Google Earth"])

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
            
        st.success(f"📍 Zone : {res['zone']}")
        
        with st.container(border=True):
            col_b1, col_b2 = st.columns(2)
            nb_ruches = col_b1.number_input("Nombre de ruches", min_value=1, value=10)
            prix_kg = col_b2.select_slider("Prix du KG (FCFA)", options=[3000, 3500, 4000, 4500, 5000, 6000], value=5000)
            
            rend, kg_tot, ca = estimer_business(res['pot'], nb_ruches, prix_kg)
            
            st.info(f"🌿 **Flore :** {res['flore']} | 💡 **Conseil :** {res['conseil']}")
            m1, m2, m3 = st.columns(3)
            m1.metric("Rendement", f"{rend} kg/ruche")
            m2.metric("Total Miel", f"{kg_tot} kg")
            m3.metric("Revenu CFA", f"{ca:,} FCFA")

        reg = st.selectbox("Région", ["Dakar", "Ziguinchor", "Diourbel", "Saint-Louis", "Tambacounda", "Kaolack", "Thiès", "Louga", "Fatick", "Kolda", "Matam", "Kaffrine", "Kédougou", "Sédhiou"])
        dept = st.text_input("Localité (ex: Bignona, Linguère)")

        if st.button("📥 Enregistrer l'Expertise Pro"):
            sauvegarder_donnees(res['zone'], lat, lon, res['pot'], reg, dept, kg_tot, ca)
            st.balloons()
            st.success("Expertise enregistrée avec succès !")
    else:
        st.warning("🌐 Signal GPS en attente...")

with tab2:
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        st.subheader("🛰️ Vue Satellite de vos Ruchers")
        
        # Vérification de sécurité pour éviter le plantage de la carte
        if not df.empty and 'Lat' in df.columns and 'Revenu_CFA' in df.columns:
            m = folium.Map(location=[14.4974, -14.4524], zoom_start=7)
            folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr='Google', name='Google Satellite').add_to(m)

            for i, row in df.iterrows():
                folium.Marker(
                    [row['Lat'], row['Lon']], 
                    popup=f"<b>{row['Departement']}</b><br>{row['Revenu_CFA']:,} FCFA",
                    icon=folium.Icon(color='green', icon='leaf')
                ).add_to(m)
            st_folium(m, width="100%", height=500)
            
            st.divider()
            fig = px.bar(df, x="Zone_Agro", y="Revenu_CFA", color="Region", title="Revenus par Terroir")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Les données enregistrées sont incomplètes. Faites un nouvel enregistrement.")
    else:
        st.info("Aucune donnée enregistrée. Réalisez votre premier diagnostic dans l'onglet 1.")
