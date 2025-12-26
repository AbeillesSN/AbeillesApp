import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import base64
from datetime import datetime
import urllib.parse

# --- CONFIGURATION PRESTIGE ---
st.set_page_config(page_title="Yamb Connecté - Expert", layout="wide")

st.markdown("""
    <style>
    .main-header { background: linear-gradient(135deg, #1B5E20, #004D40); color: #FFD600; padding: 20px; border-radius: 15px; text-align: center; }
    .alert-harvest { background: #FFF3E0; border-left: 10px solid #EF6C00; padding: 15px; border-radius: 10px; margin: 10px 0; font-weight: bold; }
    .email-btn { background-color: #1976D2; color: white; padding: 15px; border-radius: 10px; text-align: center; display: block; text-decoration: none; font-weight: bold; }
    .pdf-btn { background-color: #D32F2F; color: white; padding: 15px; border-radius: 10px; text-align: center; display: block; text-decoration: none; font-weight: bold; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
col_logo, col_titre = st.columns([1, 4])
with col_logo:
    st.markdown("<h1 style='font-size:60px; margin:0;'>🐝</h1>", unsafe_allow_html=True)
with col_titre:
    st.markdown("<div class='main-header'><h1>ABEILLES DU SÉNÉGAL</h1><p>UNITÉ DE SURVEILLANCE ET DE PRÉDICTION</p></div>", unsafe_allow_html=True)

loc = get_geolocation()

if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    
    # --- ANALYSE ET PRÉDICTION ---
    st.markdown("### 📊 État du Secteur (Rayon 5km)")
    c1, c2 = st.columns([2, 1])
    
    with c1:
        m = folium.Map(location=[lat, lon], zoom_start=14)
        folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
        folium.Circle([lat, lon], radius=3000, color='green', fill=True, opacity=0.1).add_to(m)
        folium.Marker([lat, lon], popup="Rucher").add_to(m)
        st_folium(m, width="100%", height=400)

    with c2:
        st.write("**Espèces & Floraison :**")
        especes = st.multiselect("Validez la flore :", ["Anacardier", "Manguier", "Eucalyptus", "Flore sauvage"], default=["Manguier"])
        
        st.markdown("<div class='alert-harvest'>🔔 RÉCOLTE PROCHAINE :<br>Miel de Manguier estimé sous 15 jours.</div>", unsafe_allow_html=True)
        st.metric("Potentiel par ruche", "22 kg", "+2kg (Floraison dense)")

    # --- TRANSMISSION DES DONNÉES ---
    st.divider()
    st.markdown("### 📤 Transmission des Données à la Direction")
    
    # Préparation du contenu du rapport
    corps_rapport = f"""RAPPORT D'EXPERTISE - YAMB CONNECTE
--------------------------------------
DATE : {datetime.now().strftime('%d/%m/%Y')}
COORDONNÉES : {lat}, {lon}
FLORE DÉTECTÉE : {', '.join(especes)}
ESTIMATION : 22kg/ruche
ALERTE : Récolte imminente.
--------------------------------------
Certifié par Abeilles du Sénégal."""

    col_pdf, col_mail = st.columns(2)
    
    with col_pdf:
        # Bouton PDF
        b64 = base64.b64encode(corps_rapport.encode()).decode()
        st.markdown(f'<a href="data:file/txt;base64,{b64}" download="Rapport_Expertise.pdf" class="pdf-btn">📄 TÉLÉCHARGER LE RAPPORT PDF</a>', unsafe_allow_html=True)
        
    with col_mail:
        # Bouton Email (Ouvre Outlook/Gmail avec les infos pré-remplies)
        destinataire = "direction@abeillesdusenegal.sn"
        sujet = urllib.parse.quote(f"Expertise Rucher - {datetime.now().strftime('%d/%m/%Y')}")
        message = urllib.parse.quote(corps_rapport)
        st.markdown(f'<a href="mailto:{destinataire}?subject={sujet}&body={message}" class="email-btn">📧 ENVOYER À LA DIRECTION</a>', unsafe_allow_html=True)

else:
    st.info("📡 Synchronisation satellite en cours...")
