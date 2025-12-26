import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
import urllib.parse

# --- FONCTION AUDIO (Text-to-Speech) ---
def parler(texte):
    composant_audio = f"""
        <script>
        var msg = new SpeechSynthesisUtterance("{texte}");
        msg.lang = 'fr-FR';
        window.speechSynthesis.speak(msg);
        </script>
    """
    st.components.v1.html(composant_audio, height=0)

# --- CONFIGURATION ---
st.set_page_config(page_title="YAMB - Audio", layout="centered")

st.markdown("<h1 style='text-align:center; color:#1B5E20;'>🐝 YAMB AUDIO</h1>", unsafe_allow_html=True)

tabs = st.tabs(["📊 IA", "📸 Photo", "🚨 SOS"])

with tabs[0]:
    if st.button("🔊 ÉCOUTER LES CONSIGNES (IA)"):
        parler("Bienvenue sur Yambe. Indiquez le nombre de ruches pour calculer votre récolte de miel.")
    
    st.subheader("Estimation de Récolte")
    nb = st.number_input("Nombre de ruches :", min_value=1, value=10)
    st.success(f"Récolte : {nb * 12} kg")

with tabs[1]:
    if st.button("🔊 ÉCOUTER LES CONSIGNES (PHOTO)"):
        parler("Appuyez sur le bouton de l'appareil photo pour prendre une image de votre ruche ou d'une plante.")
    
    st.subheader("Prendre une Photo")
    st.camera_input("Capture terrain")

with tabs[2]:
    if st.button("🔊 ÉCOUTER LES CONSIGNES (URGENCE)"):
        parler("En cas de danger, incendie ou vol, choisissez le type d'alerte et appuyez sur le gros bouton vert pour prévenir le groupe WhatsApp.")
    
    st.subheader("Alerte SOS")
    danger = st.selectbox("Danger :", ["Incendie 🔥", "Vol 🥷", "Maladie 🐝"])
    
    msg = f"ALERTE SOS YAMB : {danger} détecté."
    whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(msg)}"
    st.markdown(f'<a href="{whatsapp_url}" target="_blank" style="background-color:#25D366; color:white; padding:15px; border-radius:10px; text-decoration:none; display:block; text-align:center; font-weight:bold;">🟢 SIGNALER SUR WHATSAPP</a>', unsafe_allow_html=True)
