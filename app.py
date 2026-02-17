import streamlit as st
import urllib.parse

# Configuración de página
st.set_page_config(page_title="EcoSarro - Diagnóstico", page_icon="💧", layout="centered")

# --- ESTILO VISUAL (DARK MODE FORZADO) ---
st.markdown("""
    <style>
    /* Fondo General Negro/Gris Oscuro */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    
    /* Título Azul EcoSarro */
    h1 {
        color: #0044CC !important;
        text-align: center;
    }
    
    /* Subtítulos y textos */
    h2, h3, p, label {
        color: #FAFAFA !important;
    }

    /* Botón de Calcular (Azul) */
    .stButton>button {
        background-color: #0044CC;
        color: white;
        height: 3em;
        width: 100%;
        font-weight: bold;
        border-radius: 10px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #003399;
        color: white;
    }

    /* Botón WhatsApp (Verde) */
    .whatsapp-button {
        background-color: #25D366;
        color: white;
        padding: 15px 25px;
        text-align: center;
        text-decoration: none;
        display: block;
        border-radius: 10px;
        font-size: 18px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.3);
    }
    .whatsapp-button:hover {
        color: white;
        background-color: #1DA851;
    }

    /* Botón YouTube (Rojo) */
    .youtube-button {
        background-color: #FF0000;
        color: white;
        padding: 12px 20px;
        text-align: center;
        text-decoration: none;
        display: block;
        border-radius: 10px;
        font-size: 16px;
        font-weight: bold;
        margin-top: 5px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.3);
    }
    .youtube-button:hover {
        color: white;
        background-color: #CC0000;
    }
    </style>
    """, unsafe_allow_html=True)

# Encabezado
st.title("Asistente EcoSarro 💧")
st.markdown("<h3 style='text-align: center; color: #aaaaaa;'>Calcula la solución ideal para el sarro en tu hogar</h3>", unsafe_allow_html=True)

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
st.markdown("---")
col1, col2 = st.columns(2)

zona = st.selectbox("Selecciona tu Provincia/Zona", sorted(list(mapa_dureza.keys())))

with col1:
    origen = st.radio("Origen del agua", ["Red", "Pozo/Napa"])
    bomba = st.checkbox("Tengo Bomba Presurizadora")

with col2:
    personas = st.number_input("Personas en la casa", min_value=1, max_value=20, value=3)
    calentador = st.selectbox("Calentamiento de agua", ["Termotanque", "Calefón"])

# --- LÓGICA DE CÁLCULO ---
st.write("") # Espacio
if st.button("CALCULAR MI PLAN ECOSARRO"):
    puntaje = mapa_dureza[zona]
    if origen == "Pozo/Napa":
        puntaje += 2
    
    # Limitar puntaje a 10
    puntaje = min(puntaje, 10)
    
    equipos = 1
    detalles = ["🔹 1 Equipo en la entrada principal (subida al tanque o entrada de calle)."]
    
    # Lógica sensible a personas y dureza
    if puntaje >= 8:
        equipos += 1
        detalles.append("🔹 1 Equipo de Refuerzo en la bajada del tanque (Dureza alta).")
    elif personas > 4 and puntaje >= 6:
        equipos += 1
        detalles.append("🔹 1 Equipo de Refuerzo adicional por alto consumo de agua (+4 personas).")
        
    # Lógica de Calefón
    if calentador == "Calefón" and puntaje >= 7:
        equipos += 1
        detalles.append("🔹 1 Equipo de Refuerzo exclusivo en la entrada de agua fría del Calefón.")

    # --- MOSTRAR RESULTADOS ---
    st.markdown("---")
    st.success(f"### Resultado: Necesitas {equipos} Equipos EcoSarro")
    
    for d in detalles:
        st.info(d)
        
    if bomba:
        st.warning("⚠️ Instalar SIEMPRE 1 equipo antes de la bomba presurizadora.")

    # --- BOTONES DE ACCIÓN ---
    msg = f"Hola EcoSarro! Mi diagnóstico para {zona} con {personas} personas dio {equipos} equipos. ¿Me pasan presupuesto?"
    msg_url = urllib.parse.quote(msg)
    
    st.markdown(f'<a href="https://wa.me/5493515190658?text={msg_url}" class="whatsapp-button" target="_blank">SOLICITAR EQUIPOS POR WHATSAPP</a>', unsafe_allow_html=True)
    st.markdown('<a href="https://www.youtube.com/@EcoSarro" class="youtube-button" target="_blank">🎥 Ver Videos de Instalación</a>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #666;'>Industria Argentina - Protegiendo tu hogar del sarro.</p>", unsafe_allow_html=True)
