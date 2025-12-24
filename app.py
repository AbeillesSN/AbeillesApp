import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
from fpdf import FPDF
import datetime
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Expert Abeilles Sénégal", layout="wide")

# --- FONCTION GÉNÉRATION PDF AVEC PHOTO ---
def generate_pdf(data, lat, lon, photo_path=None):
    pdf = FPDF()
    pdf.add_page()
    
    # Logo
    if os.path.exists("logo.png"):
        pdf.image("logo.png", 10, 8, 30)
    
    # En-tête professionnel
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "ABEILLES DU SENEGAL", ln=True, align='R')
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "DIAGNOSTIC D'EXPERTISE TECHNIQUE", ln=True, align='R')
    pdf.ln(15)
    
    # Infos Techniques
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, f"Date : {datetime.date.today()}", ln=True)
    pdf.cell(0, 8, f"Position GPS : Lat {lat:.4f} / Lon {lon:.4f}", ln=True)
    pdf.ln(5)
    
    # Terroir et Potentiel
    pdf.set_fill_color(255, 243, 224) 
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f" TERROIR : {data['zone'].upper()}", ln=True, fill=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 8, f"Potentiel : {data['potentiel']} | Recoltes : {data['recoltes']}/an", ln=True)
    pdf.cell(0, 8, f"Flore : {', '.join(data['flore'])}", ln=True)
    pdf.cell(0, 8, f"Floraison : {data['calendrier']}", ln=True)
    pdf.ln(5)

    # Recommandations
    pdf.set_font("Arial", 'B', 11)
    pdf.set_text_color(200, 0, 0)
    pdf.cell(0, 8, "CONSEILS DE L'EXPERT :", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 8, data['conseil'])
    pdf.ln(5)

    # --- INSERTION DE LA PHOTO CAPTUREE ---
    if photo_path and os.path.exists(photo_path):
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(0, 10, "DOCUMENTATION VISUELLE DU TERRAIN :", ln=True)
        pdf.image(photo_path, x=10, w=100)
        pdf.ln(5)
    
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 10, "Cachet et Signature de l'Expert Conseil", ln=True, align='R')
    
    return pdf.output(dest='S').encode('latin-1')

# --- INTERFACE ---
st.title("🐝 Abeilles du Sénégal : Diagnostic Inclusif")

loc = get_geolocation()

if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    
    def identifier_zone(lat):
        if lat < 13.8:
            return {"zone": "Casamance", "flore": ["Anacardier", "Fromager"], "potentiel": "Exceptionnel", "recoltes": 4, "couleur": "green", "calendrier": "Mars a Juillet", "conseil": "Zone humide. Surveillez les predateurs."}
        elif 14.7 < lat < 15.8:
            return {"zone": "Niayes", "flore": ["Eucalyptus", "Maraichage", "Neem"], "potentiel": "Eleve", "recoltes": 3, "couleur": "blue", "calendrier": "Septembre a Janvier", "conseil": "Zone stable. Protegez les ruches des vents forts."}
        else:
            return {"zone": "Bassin Arachidier / Nord", "flore": ["Baobab", "Acacia", "Siddem"], "potentiel": "Moyen", "recoltes": 2, "couleur": "orange", "calendrier": "Novembre a Mars", "conseil": "Zone seche. Installation d'un abreuvoir obligatoire a moins de 500m."}

    res = identifier_zone(lat)

    # SECTION TERRAIN & INCLUSION
    st.divider()
    st.header("📸 Terrain et inclusion")
    tab1, tab2 = st.tabs(["📷 Captureur/Joint", "🗣️ Aide Vocale"])
    
    photo_file = None
    with tab1:
        img_file = st.camera_input("Prendre une photo de la ruche")
        if img_file:
            photo_file = "temp_capture.png"
            with open(photo_file, "wb") as f:
                f.write(img_file.getbuffer())
            st.success("Photo prete pour le rapport PDF.")

    with tab2:
        langue = st.selectbox("Langue", ["Wolof", "Peulh", "Diola", "Serer", "Français"])
        if st.button(f"🔊 Ecouter en {langue}"):
            st.info(f"Lecture du conseil en {langue}...")

    # TELECHARGEMENT
    st.divider()
    pdf_bytes = generate_pdf(res, lat, lon, photo_path=photo_file)
    st.download_button(label="📥 Télécharger Rapport avec Photo (PDF)", 
                       data=pdf_bytes, 
                       file_name=f"Expertise_{res['zone']}.pdf", 
                       mime="application/pdf")

else:
    st.info("🌐 En attente du signal GPS...")