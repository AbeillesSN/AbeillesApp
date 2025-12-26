import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import urllib.parse
from datetime import datetime

# --- CONFIGURATION STYLE URGENCE ---
st.set_page_config(page_title="YAMB SOS Photo", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #FFF5F5; }
    .whatsapp-btn {
        background-color: #25D366;
        color: white !important;
        padding: 20px;
        border-radius: 15px;
        text-decoration: none;
        display: block;
        text-align: center;
        font-weight: bold;
        font-size: 20px;
        box-shadow: 0 4px 15px rgba(37, 211, 102, 0.4);
        margin: 20px 0;
    }
    .camera-box {
        border: 3px dashed #d32f2f;
        border-radius: 20px;
        padding: 10px;
        background: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:#d32f2f;'>🚨 YAMB ALERTE PHOTO</h1>", unsafe_allow_html=True)

loc = get_geolocation()

if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    
    # 1. CAPTURE DE LA PREUVE
    st.markdown("### 📸 1. Preuve visuelle")
    photo = st.camera_input("Prendre une photo du danger")
    
    # 2. TYPE D'URGENCE
    st.markdown("### 🚨 2. Type d'incident")
    danger = st.selectbox("Nature du danger :", ["🔥 FEU / INCENDIE", "🥷 VOL DE RUCHES", "🦟 ATTAQUE PRÉDATEURS", "💀 MORTALITÉ SOUDAINE"])
    
    # 3. GÉNÉRATION DU MESSAGE
    maps_link = f"https://www.google.com/maps?q={lat},{lon}"
    message_text = f"🚨 *URGENCE YAMB - ABEILLES DU SÉNÉGAL*\n\n" \
                   f"⚠️ *DANGER:* {danger}\n" \
                   f"📍 *GPS:* {maps_link}\n" \
                   f"🖼️ *Note:* Photo envoyée ci-jointe."
    
    encoded_message = urllib.parse.quote(message_text)
    whatsapp_url = f"https://wa.me/?text={encoded_message}"

    if photo:
        st.success("✅ Photo capturée ! Maintenant, envoyez l'alerte.")
        st.markdown(f"""
            <a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">
                🟢 ENVOYER SUR WHATSAPP
            </a>
        """, unsafe_allow_html=True)
        st.info("💡 *Astuce :* Une fois sur WhatsApp, joignez la dernière photo de votre galerie au groupe.")

    # 4. CARTE DE SITUATION
    st.divider()
    m = folium.Map(location=[lat, lon], zoom_start=15)
    folium.Circle([lat, lon], radius=500, color='red', fill=True, opacity=0.3).add_to(m)
    st_folium(m, width="100%", height=300)

else:
    st.warning("📡 En attente du signal GPS pour sécuriser le périmètre...")
