import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation

# Configuration haute visibilité
st.set_page_config(page_title="YAMB PRO - Dashboard", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    h1, h2, h3, p, li { color: #000000 !important; font-weight: 800 !important; }
    .box { border: 4px solid #000000; padding: 20px; border-radius: 10px; margin-bottom: 20px; background-color: #F8F9FA; }
    </style>
""", unsafe_allow_html=True)

st.title("🐝 YAMB PRO : TABLEAU DE BORD TACTIQUE")

# Simulation de données
loc = get_geolocation()
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📍 Radar Satellite & Rayon de 3 km")
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        m = folium.Map(location=[lat, lon], zoom_start=13)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        folium.Circle([lat, lon], radius=3000, color='#FFC30B', fill=True, fill_opacity=0.2).add_to(m)
        folium.Marker([lat, lon], icon=folium.Icon(color='red')).add_to(m)
        st_folium(m, width="100%", height=450)

with col2:
    st.markdown("<div class='box'><h3>💰 Potentiel Économique</h3>", unsafe_allow_html=True)
    ruches = st.number_input("Nombre de ruches", 1, 500, 25)
    recolte = ruches * 15
    st.write(f"Estimation : **{recolte} kg**")
    st.write(f"Valeur : **{recolte * 4500:,.0F} FCFA**")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='box'><h3>🔬 Santé & Neem</h3>", unsafe_allow_html=True)
    st.write("• **Symptôme** : Fausse Teigne")
    st.write("• **Remède** : Feuilles de Neem sur les cadres.")
    st.markdown("</div>", unsafe_allow_html=True)

st.error("🚨 ALERTE FEU : Zone sèche. Vérifiez vos pare-feux autour du rucher.")
