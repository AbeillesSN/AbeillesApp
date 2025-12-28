import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import requests
import urllib.parse

# --- CONFIGURATION & DÉCOR THÉMATIQUE ---
st.set_page_config(page_title="YAMB PRO - ÉLITE", layout="wide")

st.markdown("""
    <style>
    /* Fond de page blanc pur */
    .stApp { background-color: #FFFFFF !important; }
    
    /* Textes noirs profonds pour la lisibilité */
    h1, h2, h3, h4, p, span, label, li, div { 
        color: #000000 !important; 
        font-weight: 850 !important; 
    }
    
    /* Boîtes de données stylisées comme des alvéoles */
    .honeycomb-box {
        background-color: #F8F9FA !important;
        border: 4px solid #FFC30B !important; /* Bordure couleur miel */
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 6px 6px 0px rgba(0,0,0,0.1); /* Ombre discrète */
    }
    
    /* Titres de section avec icônes apicoles */
    .section-title {
        display: flex;
        align-items: center;
        gap: 10px;
        color: #000000 !important;
        font-size: 1.8em;
        margin-bottom: 15px;
    }
    .section-title img {
        height: 35px; /* Taille des icônes */
    }

    /* Style pour les boutons */
    .stButton>button {
        background-color: #FFC30B !important; /* Couleur miel */
        color: #000000 !important;
        font-weight: bold !important;
        border: 2px solid #000000 !important;
        border-radius: 8px;
        padding: 10px 20px;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #e6b300 !important; /* Miel plus foncé au survol */
        transform: translateY(-2px);
    }
    
    /* Image de fond discrète (ruche ou alvéoles) */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url("https://www.transparenttextures.com/patterns/honeycomb.png"); /* Texture alvéoles */
        opacity: 0.05; /* Très transparent */
        z-index: -1;
    }

    /* En-tête avec abeille */
    .main-header {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
        margin-bottom: 30px;
    }
    .main-header img {
        height: 80px;
    }
    .main-header h1 {
        font-size: 3em;
        color: #000000 !important;
    }

    </style>
""", unsafe_allow_html=True)

# --- ENTÊTE AVEC ABEILLE ---
st.markdown("""
    <div class="main-header">
        <img src="https://i.imgur.com/uT0mFwX.png" alt="Abeille">
        <h1>YAMB PRO : TABLEAU DE BORD ÉLITE</h1>
    </div>
""", unsafe_allow_html=True)

loc = get_geolocation()

# --- 1. RADAR DE TERRAIN (GPS & SATELLITE) ---
st.markdown('<div class="section-title"><img src="https://i.imgur.com/UfB8sR5.png" alt="GPS"><h2>Radar de Terrain</h2></div>', unsafe_allow_html=True) # Icône GPS
if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    m = folium.Map(location=[lat, lon], zoom_start=13)
    folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', attr='Google Satellite').add_to(m)
    folium.Circle([lat, lon], radius=3000, color='#FFC30B', fill=True, fill_opacity=0.2).add_to(m)
    folium.Marker([lat, lon], tooltip="Votre Rucher", icon=folium.Icon(color='red', icon='home', prefix='fa')).add_to(m)
    st_folium(m, width="100%", height=380)
else:
    st.info("📍 Recherche du signal GPS...")

# --- 2. INTELLIGENCE ENVIRONNEMENTALE ---
st.markdown('<div class="section-title"><img src="https://i.imgur.com/8fG2G0P.png" alt="Fleur"><h2>Intelligence Environnementale</h2></div>', unsafe_allow_html=True) # Icône Fleur
st.markdown("<div class='honeycomb-box'>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.write("### 🌿 Flore Active")
    st.write("• **Kadd :** Floraison dense (Miel clair)")
    st.write("• **Anacarde :** Début de miellée (Miel fruité)")
with col2:
    st.write("### ☁️ Météo Tactique")
    st.write("• **Température :** 29°C")
    st.write("• **Vent :** 12 km/h (Est) - Faible Harmattan")
st.markdown("</div>", unsafe_allow_html=True)

# --- 3. BIOLOGIE ET LUNE ---
st.markdown('<div class="section-title"><img src="https://i.imgur.com/p2g6O8p.png" alt="Lune"><h2>Biologie & Cycle Lunaire</h2></div>', unsafe_allow_html=True) # Icône Lune
st.markdown("<div class='honeycomb-box'>", unsafe_allow_html=True)
st.write("### 🌙 Phase Lunaire : Premier Croissant")
st.write("• **Impact :** Forte activité de la reine. Colonies en expansion.")
st.write("• **Conseil :** Idéal pour la pose des hausses. Surveiller l'espace dans le nid.")
st.markdown("</div>", unsafe_allow_html=True)

# --- 4. CLINIQUE APICOLE (SANTÉ & NEEM) ---
st.markdown('<div class="section-title"><img src="https://i.imgur.com/A6jMv50.png" alt="Santé"><h2>Clinique Apicole</h2></div>', unsafe_allow_html=True) # Icône Abeille Santé
st.markdown("<div class='honeycomb-box'>", unsafe_allow_html=True)
maladie = st.selectbox("Scanner une anomalie :", ["Fausse Teigne", "Fourmis Magnan", "Varroa"], key="maladie_select")
if maladie == "Fausse Teigne":
    st.write("### 🦋 Fausse Teigne (Galleria mellonella)")
    st.write("• **Diagnostic :** Toiles de cire, galeries, larves.")
    st.write("• **Traitement :** Utilisation de **feuilles de NEEM** broyées sur les cadres. Renforcer la colonie. Nettoyer les déchets de cire.")
elif maladie == "Fourmis Magnan":
    st.write("### 🐜 Attaque de Fourmis Magnan")
    st.write("• **Diagnostic :** Colonnes de fourmis sur les supports de ruche.")
    st.write("• **Traitement :** Barrière physique (graisse + cendre) sur les pieds. Éloigner les sources de nourriture.")
st.markdown("</div>", unsafe_allow_html=True)

# --- 5. PUISSANCE FINANCIÈRE & LOGISTIQUE ---
st.markdown('<div class="section-title"><img src="https://i.imgur.com/E0l81yQ.png" alt="Argent"><h2>Puissance Économique & Logistique</h2></div>', unsafe_allow_html=True) # Icône Argent
st.markdown("<div class='honeycomb-box'>", unsafe_allow_html=True)
col_eco1, col_eco2 = st.columns(2)
with col_eco1:
    nb_ruches = st.number_input("Nombre de ruches :", 1, 1000, 25, key="nb_ruches_input")
    pot_kg = nb_ruches * 15 # Est. 15kg/ruche
    st.write(f"### 🍯 Récolte Estimée : {pot_kg} KG")
    st.markdown(f"<h3 style='color:#FFC30B !important;'>{pot_kg * 4500:,.0f} FCFA</h3>", unsafe_allow_html=True) # Prix au kg
with col_eco2:
    st.write("### 🍞 Planification Soudure")
    sucre_necessaire = nb_ruches * 5 # 5kg sucre par ruche pour soudure
    st.write(f"• **Sucre nécessaire :** {sucre_necessaire} kg")
    st.write(f"• **Eau nécessaire :** {sucre_necessaire / 2} litres (Ratio 2:1)")
st.markdown("</div>", unsafe_allow_html=True)

# --- 6. URGENCE SOS ---
st.markdown('<div class="section-title"><img src="https://i.imgur.com/mO3hV2n.png" alt="SOS"><h2>Ligne d\'Urgence</h2></div>', unsafe_allow_html=True) # Icône Sirène
st.markdown("<div class='honeycomb-box' style='border-color:red !important;'>", unsafe_allow_html=True)
st.error("🔥 **ALERTE FEU :** Risque très élevé en saison sèche. Mettre en place des pare-feux de 5m.")
if st.button("📲 ENVOYER ALERTE GPS PAR WHATSAPP"):
    if loc:
        msg = urllib.parse.quote(f"ALERTE YAMB PRO\nIncident grave au rucher.\nLocalisation GPS: {lat},{lon}")
        st.markdown(f'<a href="https://wa.me/221XXXXXXX?text={msg}" target="_blank" style="background-color:#FF0000; color:white; padding:15px; border-radius:10px; text-decoration:none; display:block; text-align:center;">CONFIRMER L\'ENVOI AU PC ÉLITE</a>', unsafe_allow_html=True)
    else:
        st.warning("Activez le GPS pour envoyer votre position.")
st.markdown("</div>", unsafe_allow_html=True)
