import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import datetime
from streamlit_js_eval import get_geolocation
from fpdf import FPDF

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Expert Abeilles Sénégal", layout="wide")

DB_FILE = "historique_expertises.csv"

# --- FONCTION GÉNÉRATION PDF ---
def generate_pdf(data, lat, lon, photo_path=None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "ABEILLES DU SENEGAL", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 8, f"Date : {datetime.now().strftime('%d/%m/%Y')}", ln=True)
    pdf.cell(0, 8, f"Coordonnees GPS : {lat:.4f}, {lon:.4f}", ln=True)
    pdf.cell(0, 8, f"Terroir : {data['zone']}", ln=True)
    pdf.cell(0, 8, f"Potentiel : {data['potentiel']}", ln=True)
    
    if photo_path and os.path.exists(photo_path):
        pdf.ln(5)
        pdf.cell(0, 10, "Photo du Rucher :", ln=True)
        pdf.image(photo_path, x=10, w=100)
    
    return pdf.output(dest='S').encode('latin-1')

# --- LOGIQUE DE SAUVEGARDE ---
def sauvegarder_diagnostic(zone, lat, lon, potentiel):
    nouveau_rapport = {
        "Date": datetime.now().strftime("%d/%m/%Y"),
        "Zone": zone,
        "Latitude": round(lat, 4),
        "Longitude": round(lon, 4),
        "Potentiel": potentiel
    }
    df = pd.DataFrame([nouveau_rapport])
    if not os.path.isfile(DB_FILE):
        df.to_csv(DB_FILE, index=False)
    else:
        df.to_csv(DB_FILE, mode='a', header=False, index=False)

# --- INTERFACE PRINCIPALE ---
st.title("🐝 Abeilles du Sénégal : Diagnostic Inclusif")

# Message de bienvenue bilingue
st.markdown("""
### 🇸🇳 Bienvenue sur votre Assistant Apicole / Akksil ak Jàmm
---
**FR :** Cet outil vous permet de réaliser un diagnostic précis de votre terroir, de calculer le potentiel de récolte et d'archiver vos visites pour un meilleur suivi de vos ruches.

**WO :** Jumtukaay bi day tax nga mën a xam ni sa gàncax gi mel, limu nuyub bëj mën a jur, ak denc sa yëngu-yëngu ngir gën a toppato say mbege.
""")

tab1, tab2 = st.tabs(["🆕 Nouveau Diagnostic", "📊 Analyses & Historique"])

with tab1:
    loc = get_geolocation()
    if loc:
        lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
        
        # Intelligence Terroir (Logique simplifiée basée sur la latitude)
        if 14.7 < lat < 15.8:
            res = {"zone": "Niayes", "potentiel": "Eleve", "conseil": "Protegez les ruches des vents forts."}
        else:
            res = {"zone": "Bassin Arachidier / Nord", "potentiel": "Moyen", "conseil": "Installation d'un abreuvoir obligatoire."}
            
        st.subheader(f"📍 Terroir identifié : {res['zone']}")
        st.info(f"💡 Conseil : {res['conseil']}")
        
        # Capture Photo
        img_file = st.camera_input("Prendre une photo de la ruche")
        photo_temp = None
        if img_file:
            photo_temp = "temp_capture.png"
            with open(photo_temp, "wb") as f:
                f.write(img_file.getbuffer())
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("📥 Enregistrer dans l'Historique"):
                sauvegarder_diagnostic(res['zone'], lat, lon, res['potentiel'])
                st.success("Données archivées !")
                st.balloons()
        
        with col_btn2:
            pdf_bytes = generate_pdf(res, lat, lon, photo_temp)
            st.download_button("📄 Telecharger le Rapport PDF", pdf_bytes, file_name="Expertise_Abeille.pdf")
    else:
        st.warning("🌐 En attente du signal GPS pour débuter l'expertise...")

with tab2:
    if os.path.exists(DB_FILE):
        df_hist = pd.read_csv(DB_FILE)
        
        st.subheader("📈 Statistiques de vos Rachers")
        col_fig1, col_fig2 = st.columns(2)
        
        with col_fig1:
            fig_pie = px.pie(df_hist, names='Zone', title="Répartition par Terroir", hole=0.3)
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with col_fig2:
            fig_bar = px.bar(df_hist, x='Date', y='Zone', color='Potentiel', title="Historique des visites")
            st.plotly_chart(fig_bar, use_container_width=True)

        st.divider()
        st.write("### Liste des expertises passées")
        st.dataframe(df_hist, use_container_width=True)
    else:
        st.info("Aucune archive disponible. Réalisez votre premier diagnostic !")
