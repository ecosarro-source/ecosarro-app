import streamlit as st
import urllib.parse

# Configuración de página
st.set_page_config(page_title="EcoSarro - Diagnóstico", page_icon="💧")

# Estilo visual (Azul y Blanco)
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stButton>button { background-color: #0044CC; color: white; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

st.title("💧 Asistente EcoSarro")
st.subheader("¿Cuántos equipos necesitas?")

# --- ENTRADA DE DATOS ---
zona = st.selectbox("Selecciona tu Provincia/Zona", [
    "Buenos Aires (Costa)", "Buenos Aires (GBA)", "Córdoba", "La Rioja", 
    "Mendoza", "Santa Fe", "Salta", "Neuquén", "Tierra del Fuego"
    # Agregaremos el resto luego
])

origen = st.radio("Origen del agua", ["Red", "Pozo/Napa"])
bomba = st.checkbox("Tengo Bomba Presurizadora")
personas = st.number_input("Cantidad de personas", min_value=1, value=3)
calentador = st.selectbox("Sistema de calentamiento", ["Termotanque", "Calefón"])

# --- LÓGICA DE CÁLCULO ---
if st.button("CALCULAR DIAGNÓSTICO"):
    # Mapeo simple de dureza
    dureza = 10 if "Costa" in zona or "Rioja" in zona else 7
    if origen == "Pozo/Napa": dureza += 2
    
    equipos = 1
    detalles = ["1. Instalación en entrada principal."]
    
    if dureza >= 9 or personas > 5:
        equipos += 1
        detalles.append("2. Refuerzo en bajada de tanque.")
    
    if calentador == "Calefón" and dureza >= 7:
        equipos += 1
        detalles.append(f"{equipos}. Refuerzo en entrada de Calefón.")
    
    # --- RESULTADOS ---
    st.success(f"### Necesitas: {equipos} Equipos EcoSarro")
    for d in detalles:
        st.write(d)
        
    if bomba:
        st.warning("⚠️ Instalar SIEMPRE antes de la bomba presurizadora.")

    # Botón WhatsApp
    msg = urllib.parse.quote(f"Hola! Mi diagnóstico dio {equipos} equipos en {zona}.")
    st.markdown(f"[![WhatsApp](https://img.shields.io/badge/Consultar_por_WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://wa.me/5491100000000?text={msg})")