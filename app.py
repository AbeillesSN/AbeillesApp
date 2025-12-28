import streamlit as st

# --- STYLE TACTIQUE NOIR SUR BLANC ---
st.markdown("""
    <style>
    .health-card {
        border: 4px solid #000000;
        background-color: #FFFFFF;
        padding: 15px;
        margin-bottom: 15px;
        border-radius: 10px;
    }
    .remede { color: #006400 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.header("🔬 MODULE DE SANTÉ : L'ARMURE BIOLOGIQUE")

maladie = st.selectbox("Identifier une anomalie :", 
                      ["Fausse Teigne", "Varroa", "Petit Coléoptère", "Fourmis Magnan"])

if maladie == "Fausse Teigne":
    st.markdown("""
        <div class='health-card'>
            <h3>🦋 Fausse Teigne (Larves de cire)</h3>
            <p><b>Diagnostic :</b> Toiles d'araignées noires sur les cadres, cire détruite.</p>
            <p class='remede'>⚔️ ACTION : Renforcer la colonie (nourrissement). Nettoyer les planchers. 
            Placer des feuilles de NEEM fraîches sous le toit.</p>
        </div>
    """, unsafe_allow_html=True)

elif maladie == "Fourmis Magnan":
    st.markdown("""
        <div class='health-card'>
            <h3>🐜 Attaque de Fourmis</h3>
            <p><b>Diagnostic :</b> Colonnes de fourmis montant aux pieds de la ruche.</p>
            <p class='remede'>⚔️ ACTION : Enduire les supports de la ruche de graisse mécanique mélangée à de la cendre 
            ou placer les pieds dans des boîtes remplies d'eau.</p>
        </div>
    """, unsafe_allow_html=True)

# --- BASE DE CONNAISSANCES : LES PLANTES MÉDICINALES ---
st.subheader("🌿 Pharmacopée de l'Apiculteur")
with st.expander("Voir les plantes utiles au Sénégal"):
    st.write("- **Neem :** Antiparasitaire puissant.")
    st.write("- **Citronnelle :** Calme les abeilles et désinfecte.")
    st.write("- **Eucalyptus :** Stimule les défenses naturelles.")
