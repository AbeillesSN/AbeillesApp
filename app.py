import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import datetime
from streamlit_js_eval import get_geolocation
from fpdf import FPDF

# --- CONFIGURATION ---
st.set_page_config(page_title="Expert Abeilles Sénégal", layout="wide")
DB_FILE = "historique_expertises.csv"

# --- FONCTION GÉNÉRATION PDF ---
def generate_pdf(data, lat, lon, photo_path=None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "ABEILLES DU SENEGAL - RAPPORT D'EXPERTISE", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 8, f"Date : {datetime.now().strftime('%d/%m/%Y')}", ln=True)
    pdf.cell(0, 8, f"Localisation GPS : {lat:.4f}, {lon:.4f}", ln=True)
    pdf.cell(0, 8, f"Terroir : {data['zone']}", ln=True)
    pdf.cell(0, 8, f"Potentiel Mellifere : {data['potentiel']}", ln=True)
    pdf.cell(0, 8, f"Conseil : {data['conseil']}", ln=True)
    
    if photo_path and os.path.exists(photo_path):
        pdf.ln(10)
        pdf.cell(0, 10, "Photo du site :", ln=True)
        pdf.image(photo_path, x=10, w=100)
    
    return pdf.output(dest='S').encode('latin-1')

# --- LOGIQUE DE SAUVEGARDE ---
def sauvegarder_diagnostic(zone, lat, lon, potentiel):
    nouveau = {
        "Date": datetime.now().strftime("%d/%m/%Y"),
        "Zone": zone,
        "Latitude": round(lat, 4),
        "Longitude": round(lon, 4),
        "Potentiel": potentiel
    }
    df = pd.DataFrame([nouveau])
    if not os.path.isfile(DB_FILE):
        df.to_csv(DB_FILE, index=False)
    else:
        df.to_csv(DB_FILE, mode='a', header=False, index=False)

# --- INTERFACE ---
st.title("🐝 Abeilles du Sénégal")

st.markdown("""
### 🇸🇳 Bienvenue sur votre Assistant Apicole / Akksil ak Jàmm
---
**FR :** Cet outil vous permet de réaliser un diagnostic précis de votre terroir, de calculer le potentiel de récolte et d'archiver vos visites.

**WO :** Jumtukaay bi day tax nga mën a xam ni sa gàncax gi mel, limu nuyub bëj mën a jur, ak denc sa yëngu-yëngu.
""")

tab1, tab2 = st.tabs(["🆕 Nouveau Diagnostic", "📊 Analyses & Historique"])

with tab1:
    loc = get_geolocation()
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        
        # Logique Terroir
        if 14.7 < lat < 15.8:
            res = {"zone": "Niayes", "potentiel": "Eleve", "conseil": "Protegez les ruches des vents forts."}
        else:
            res = {"zone": "Bassin Arachidier / Autre", "potentiel": "Moyen", "conseil": "Prevoir un abreuvoir pour les abeilles."}
            
        st.subheader(f"📍 Terroir identifié : {res['zone']}")
        st.write(f"**Potentiel :** {res['potentiel']}")
        st.info(f"💡 **Conseil de l'Expert :** {res['conseil']}")
        
        # Photo
        img_file = st.camera_input("Prendre une photo du rucher")
        photo_path = None
        if img_file:
            photo_path = "temp_img.png"
            with open(photo_path, "wb") as f:
                f.write(img_file.getbuffer())
        
        # Actions
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📥 Enregistrer l'expertise"):
                sauvegarder_diagnostic(res['zone'], lat, lon, res['potentiel'])
                st.success("C'est enregistré !")
                st.balloons()
        
        with c2:
            pdf_data = generate_pdf(res, lat, lon, photo_path)
            st.download_button("📄 Télécharger le Rapport PDF", pdf_data, "Rapport_Abeilles.pdf")

        # Partage
        st.markdown("---")
        st.write("### 📲 Partager avec l'équipe")
        msg = f"Diagnostic Apicole - Terroir: {res['zone']} - Potentiel: {res['potentiel']}"
        col_w, col_e = st.columns(2)
        with col_w:
            st.link_button("🟢 WhatsApp", f"https://wa.me/?text={msg}")
        with col_e:
            st.link_button("📧 Email", f"mailto:?subject=Expertise Abeilles&body={msg}")
    else:
        st.warning("🌐 Recherche du signal GPS en cours...")

with tab2:
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        st.subheader("📈 Statistiques des Expertises")
        
        fig = px.pie(df, names='Zone', title="Répartition des Terroirs visités", hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("### 📚 Historique complet")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aucun historique pour le moment.")
