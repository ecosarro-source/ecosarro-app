import streamlit as st
import urllib.parse

# Configuración de página
st.set_page_config(page_title="EcoSarro - Diagnóstico", page_icon="💧")

# Estilo visual personalizado (Fondo blanco y Título Azul)
st.markdown("""
    <style>
    .stApp {
        background-color: #FFFFFF;
    }
    h1 {
        color: #0044CC !important;
    }
    .stButton>button {
        background-color: #0044CC;
        color: white;
        height: 3em;
        font-weight: bold;
        border-radius: 10px;
    }
    .whatsapp-button {
        background-color: #25D366;
        color: white;
        padding: 15px 25px;
        text-align: center;
        text-decoration: none;
        display: block;
        border-radius: 10px;
        font-size: 20px;
        font-weight: bold;
        margin-top: 20px;
    }
    .youtube-button {
        background-color: #FF0000;
        color: white;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: block;
        border-radius: 10px;
        font-size: 16px;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Asistente EcoSarro")
st.write("Calcula la solución ideal para el sarro en tu hogar.")

# Base de datos de provincias (Dureza 1 a 10)
mapa_dureza = {
    "Buenos Aires (Costa Atlántica)": 10, "Buenos Aires (Bahía Blanca/Sur)": 10, "Buenos Aires (GBA)": 8,
    "Buenos Aires (Interior)": 8, "CABA": 6, "Catamarca": 9, "Chaco": 7, "Chubut": 3, "Córdoba": 9,
    "Corrientes": 6, "Entre Ríos": 8, "Formosa": 6, "Jujuy": 7, "La Pampa": 10, "La Rioja": 9,
    "Mendoza": 9, "Misiones": 6, "Neuquén": 3, "Río Negro": 3, "Salta": 7, "San Juan": 9,
    "San Luis": 9, "Santa Cruz": 3, "Santa Fe (Rosario/Sur)": 9, "Santa Fe (Capital/Norte)": 8,
    "Santiago del Estero": 8, "Tierra del Fuego": 3, "Tucumán": 7
}

# --- ENTRADA DE DATOS ---
with st.container():
    zona = st.selectbox("Selecciona tu Provincia/Zona", sorted(list(mapa_dureza.keys())))
    origen = st.radio("Origen del agua", ["Red", "Pozo/Napa"])
    bomba = st.checkbox("Tengo Bomba Presurizadora")
    personas = st.number_input("Cantidad de personas que viven en la casa", min_value=1, max_value=20, value=3)
    calentador = st.selectbox("Sistema de calentamiento de agua", ["Termotanque", "Calefón"])

# --- LÓGICA DE CÁLCULO ---
if st.button("CALCULAR MI PLAN ECOSARRO"):
    puntaje = mapa_dureza[zona]
    if origen == "Pozo/Napa":
        puntaje += 2
    
    # Limitar puntaje a 10
    puntaje = min(puntaje, 10)
    
    equipos = 1
    detalles = ["🔹 1 Equipo en la entrada principal (subida al tanque o entrada de calle)."]
    
    # Lógica sensible a personas y dureza
    # Si hay muchas personas (ej. > 4) el consumo es mayor y el agua requiere más contacto magnético
    if puntaje >= 8:
        equipos += 1
        detalles.append("🔹 1 Equipo de Refuerzo en la bajada del tanque (Dureza alta).")
    elif personas > 4 and puntaje >= 6:
        equipos += 1
        detalles.append("🔹 1 Equipo de Refuerzo adicional por alto consumo de agua (más de 4 personas).")
        
    # Lógica de Calefón (muy sensible al sarro)
    if calentador == "Calefón" and puntaje >= 7:
        equipos += 1
        detalles.append("🔹 1 Equipo de Refuerzo exclusivo en la entrada de agua fría del Calefón.")

    # --- MOSTRAR RESULTADOS ---
    st.markdown("---")
    st.subheader(f"Resultado: Necesitas {equipos} Equipos EcoSarro")
    
    for d in detalles:
        st.write(d)
        
    if bomba:
        st.warning("⚠️ Instalar SIEMPRE 1 equipo antes de la bomba presurizadora.")

    # --- BOTONES DE ACCIÓN ---
    # WhatsApp (Número corregido y mensaje dinámico)
    msg = f"Hola EcoSarro! Mi diagnóstico para {zona} con {personas} personas dio {equipos} equipos. ¿Me pasan presupuesto?"
    msg_url = urllib.parse.quote(msg)
    st.markdown(f'<a href="https://wa.me/5493515190658?text={msg_url}" class="whatsapp-button">SOLICITAR EQUIPOS POR WHATSAPP</a>', unsafe_allow_html=True)

    # Botón YouTube
    st.markdown('<a href="https://www.youtube.com/@EcoSarro" class="youtube-button">🎥 Ver Videos de Instalación</a>', unsafe_allow_html=True)

st.markdown("---")
st.caption("Industria Argentina - Protegiendo tu hogar del sarro.")
