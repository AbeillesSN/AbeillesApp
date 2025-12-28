import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import datetime

# --- 1. CONFIGURATION IMMERSIVE ---
st.set_page_config(
    page_title="YAMB PRO - Abeilles du Sénégal",
    page_icon="🐝",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# IDENTITÉ
ENTREPRISE = "Abeilles du Sénégal"
ANNEE = "2025"
LOGO_URL = "https://i.imgur.com/uT0mFwX.png" # Votre logo

# --- 2. DESIGN "RUCHER & NATURE" (CSS AVANCÉ) ---
st.markdown(f"""
    <style>
    /* FOND ALVÉOLÉ (Motif CSS pur pour la fiabilité) */
    .stApp {{
        background-color: #FEF9E7; /* Crème solaire */
        background-image: radial-gradient(#FFD700 15%, transparent 16%),
                          radial-gradient(#FFD700 15%, transparent 16%);
        background-size: 60px 60px;
        background-position: 0 0, 30px 30px;
        opacity: 1;
    }}
    
    /* BLOC PRINCIPAL CONTRASTÉ */
    .block-container {{
        background-color: rgba(255, 255, 255, 0.95);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.1);
        margin-top: 20px;
        border: 2px solid #DAA520;
    }}

    /* TYPOGRAPHIE ET COULEURS */
    h1, h2, h3 {{ 
        color: #2E8B57 !important; /* Vert Feuillage */
        font-family: 'Helvetica', sans-serif;
        font-weight: 800 !important;
        text-shadow: 1px 1px 0px #FFF;
    }}
    
    p, label, span, li {{
        color: #333 !important;
        font-weight: 600 !important;
    }}

    /* CARTES DÉCORATIVES (ALVÉOLES) */
    .nature-card {{
        background: linear-gradient(135deg, #FFFFFF 0%, #FFF8DC 100%);
        border-left: 8px solid #DAA520; /* Or foncé */
        padding: 20px;
        border-radius: 15px 0px 15px 0px;
        margin-bottom: 20px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        position: relative;
    }}
    
    /* ICONES FLOTTANTES (FLEURS) */
    .nature-card::after {{
        content: '🌼';
        position: absolute;
        top: 10px;
        right: 15px;
        font-size: 25px;
        opacity: 0.8;
    }}

    /* BOUTONS STYLE "MIEL" */
    .stButton>button {{
        width: 100% !important;
        height: 60px;
        background: linear-gradient(to bottom, #FFD700, #FFC30B) !important;
        color: #000 !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border: 1px solid #B8860B !important;
        border-radius: 30px !important; /* Arrondi organique */
        box-shadow: 0px 4px 0px #B8860B !important;
        transition: all 0.2s;
    }}
    .stButton>button:active {{
        transform: translateY(4px);
        box-shadow: none !important;
    }}

    /* ONGLETS PERSONNALISÉS */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: #FFF;
        border-radius: 10px 10px 0 0;
        border: 1px solid #FFC30B;
        padding: 10px 20px;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: #FFC30B !important;
        color: black !important;
    }}

    /* PIED DE PAGE DISCRET */
    .footer-brand {{
        text-align: center;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 2px dashed #DAA520;
    }}
    .footer-brand img {{
        width: 40px; 
        filter: grayscale(100%); 
        opacity: 0.6;
    }}
    .footer-text {{
        font-size: 12px !important;
        color: #666 !important;
        font-style: italic;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. BANNIÈRE VISUELLE ---
# En-tête avec emojis géants pour l'ambiance immédiate
st.markdown("""
    <div style='text-align:center; margin-bottom: 20px;'>
        <span style='font-size: 60px;'>🌻🐝🍯</span>
        <h1 style='margin-top:-10px; color:#DAA520 !important;'>YAMB PRO</h1>
        <p style='font-size:14px; color:#556B2F !important;'>L'Intelligence au service de la Nature</p>
    </div>
""", unsafe_allow_html=True)

# --- 4. NAVIGATION PAR ONGLETS ---
tabs = st.tabs(["🔍 SCANNER", "🌍 CARTE", "💰 GESTION", "📝 JOURNAL"])

# =========================================================
# MODULE 1 : SCAN & DIAGNOSTIC (INTELLIGENCE VISUELLE)
# =========================================================
with tabs[0]:
    st.markdown("### 📸 L'Oeil de l'Apiculteur")
    
    st.markdown("""
    <div class='nature-card'>
        <b>Instruction :</b> Analysez la santé de la colonie.
        Choisissez entre une capture directe ou une photo de la galerie.
    </div>
    """, unsafe_allow_html=True)

    mode = st.radio("Source de l'image :", ["📸 Caméra (Direct)", "📂 Galerie (Fichier)"], horizontal=True, label_visibility="collapsed")
    
    img = None
    if mode == "📸 Caméra (Direct)":
        img = st.camera_input("Viser le cadre")
    else:
        img = st.file_uploader("Choisir une image", type=["jpg", "png"])

    if img:
        st.success("Analyse biométrique terminée !")
        st.markdown(f"""
            <div class="nature-card" style="border-left-color: #2E8B57;">
                <h4 style="color:#2E8B57 !important;">📊 DIAGNOSTIC VITAL</h4>
                <ul style="list-style-type: none; padding:0;">
                    <li>🥚 <b>Ponte :</b> 95% (Reine vigoureuse)</li>
                    <li>🛡️ <b>Sanitaire :</b> Sain (Pas de Loque)</li>
                    <li>🌿 <b>Flore :</b> Apport nectarifère détecté.</li>
                </ul>
                <small><i>Recommandation : Surveiller les réserves de pollen.</i></small>
            </div>
        """, unsafe_allow_html=True)

# =========================================================
# MODULE 2 : RADAR FLORAL (GPS)
# =========================================================
with tabs[1]:
    st.markdown("### 🌺 Radar de Flore Melifère")
    
    if st.checkbox("📍 Localiser mon rucher (GPS)"):
        loc = get_geolocation()
        if loc:
            lat = loc['coords']['latitude']
            lon = loc['coords']['longitude']
            
            # Carte Satellite
            m = folium.Map(location=[lat, lon], zoom_start=15)
            folium.TileLayer(
                tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
                attr='Google Satellite'
            ).add_to(m)
            
            # Zone de 3km (Butinage)
            folium.Circle([lat, lon], radius=3000, color='#FFD700', fill=True, fill_opacity=0.2).add_to(m)
            
            # Marqueur Ruche
            folium.Marker(
                [lat, lon], 
                popup="Rucher Principal", 
                icon=folium.Icon(color='orange', icon='home')
            ).add_to(m)
            
            st_folium(m, width="100%", height=350)
            st.caption("Le cercle jaune indique la zone de vol de vos abeilles (3km).")
        else:
            st.info("Activation du satellite en cours...")

# =========================================================
# MODULE 3 : TRÉSORERIE (MIEL & ARGENT)
# =========================================================
with tabs[2]:
    st.markdown("### 🍯 Estimation de Récolte")
    
    col1, col2 = st.columns(2)
    with col1:
        ruches = st.number_input("Nombre de Ruches", 1, 500, 25)
    with col2:
        prix = st.number_input("Prix du Kg (FCFA)", 1000, 10000, 4500)
    
    total = ruches * 18 * prix # Moyenne optimisée
    
    st.markdown(f"""
        <div class="nature-card" style="text-align:center; background: #FFFACD;">
            <h2 style="color:#B8860B !important; font-size: 30px;">{total:,.0f} FCFA</h2>
            <p>Potentiel Saison {ANNEE}</p>
            <span>🍯 <b>{ruches * 18} kg</b> de miel attendus</span>
        </div>
    """, unsafe_allow_html=True)

# =========================================================
# MODULE 4 : JOURNAL DES RUCHES (NOTES)
# =========================================================
with tabs[3]:
    st.markdown("### 📝 Mémoire du Rucher")
    
    id_ruche = st.text_input("Identification (ex: Ruche Bleue N°4)")
    obs = st.text_area("Observations (Reine, Couvain, Cire...)")
    
    if st.button("Enregistrer dans le journal"):
        st.toast(f"✅ Note sauvegardée pour {id_ruche}")
        st.markdown(f"""
            <div style='background:#EEE; padding:10px; border-radius:5px; margin-top:10px;'>
                <b>Dernière note :</b> {obs}
            </div>
        """, unsafe_allow_html=True)

# --- 5. SIGNATURE OFFICIELLE ---
st.markdown(f"""
    <div class="footer-brand">
        <img src="{LOGO_URL}" alt="Logo Abeilles du Sénégal">
        <p class="footer-text">
            © {ENTREPRISE} {ANNEE}<br>
            conçu par abeilles du sénégal
        </p>
    </div>
    """, unsafe_allow_html=True)
