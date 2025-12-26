import streamlit as st
import pandas as pd
import os
from streamlit_js_eval import get_geolocation

st.set_page_config(page_title="Expert Abeilles SN")

# --- SOLUTION À L'ERREUR ROUGE ---
# On change le nom du fichier pour forcer l'application à repartir à zéro
DB_FILE = "base_donnees_finale_2026.csv"

st.title("🐝 Expert Abeilles Sénégal")

loc = get_geolocation()
if loc:
    lat, lon = loc['coords']['latitude'], loc['coords']['longitude']
    st.success(f"Position détectée : {lat}, {lon}")
    
    dept = st.text_input("Nom de la localité (ex: Bignona)")
    
    if st.button("Enregistrer l'expertise"):
        nouveau = pd.DataFrame([{"Date": "26/12/2025", "Lieu": dept, "Lat": lat, "Lon": lon}])
        if not os.path.isfile(DB_FILE):
            nouveau.to_csv(DB_FILE, index=False)
        else:
            nouveau.to_csv(DB_FILE, mode='a', header=False, index=False)
        st.balloons()
        st.success("C'est enregistré ! L'erreur a disparu.")
else:
    st.warning("Veuillez activer le GPS sur votre téléphone.")
