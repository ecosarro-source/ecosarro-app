import streamlit as st
import urllib.parse

# Configuración de página
st.set_page_config(page_title="EcoSarro - Diagnóstico", page_icon="💧", layout="centered")

# --- ESTILO VISUAL (DARK MODE + BOTONES PERSONALIZADOS) ---
st.markdown("""
    <style>
    /* 1. FONDO NEGRO */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    
    /* 2. TÍTULO AZUL GRANDE */
    .title-ecosarro {
        color: #0044CC !important;
        text-align: center;
        font-size: 3.5rem !important; /* Más grande */
        font-weight: 800 !important;
        margin-bottom: 0px;
    }
    
    /* 3. SUBTÍTULO BLANCO CHICO */
    .subtitle-ecosarro {
        color: #FFFFFF !important;
        text-align: center;
        font-size: 1.2rem !important;
        font-weight: 300;
        margin-top: -10px;
        margin-bottom: 30px;
        opacity: 0.9;
    }

    /* ESTILOS DE BOTONES */
    a { text-decoration: none !important; }

    /* Botón WhatsApp (Verde con Icono) */
    .whatsapp-btn {
        background-color: #25D366;
        color: white !important;
        padding: 12px 20px;
        border-radius: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        font-weight: bold;
        font-size: 18px;
        box-shadow: 0 4px 10px rgba(37, 211, 102, 0.3);
        transition: transform 0.2s;
        margin-top: 20px;
    }
    .whatsapp-btn:hover {
        transform: scale(1.02);
        background-color: #1DA851;
    }

    /* Botón YouTube (Vertical: Icono arriba, texto abajo) */
    .youtube-btn {
        background-color: transparent;
        border: 2px solid #FF0000;
        color: white !important;
        padding: 10px 20px;
        border-radius: 15px;
        display: flex;
        flex-direction: column; /* Icono arriba, texto abajo */
        align-items: center;
        justify-content: center;
        gap: 5px;
        font-size: 16px;
        font-weight: 600;
        margin-top: 15px;
        transition: background-color 0.3s;
    }
    .youtube-btn:hover {
        background-color: rgba(255, 0, 0, 0.1);
    }
    
    /* Ajuste del botón nativo de Streamlit (Calcular) */
    .stButton>button {
        background-color: #0044CC;
        color: white;
        border-radius: 8px;
        border: none;
        height: 3em;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #0033A0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown('<h1 class="title-ecosarro">EcoSarro</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-ecosarro">Asistente de cálculo de equipos para el hogar</p>', unsafe_allow_html=True)

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
zona = st.selectbox("Selecciona tu Provincia/Zona", sorted(list(mapa_dureza.keys())))

col1, col2 = st.columns(2)
with col1:
    origen = st.radio("Origen del agua", ["Red", "Pozo/Napa"])
    bomba = st.checkbox("Tengo Bomba Presurizadora")

with col2:
    personas = st.number_input("Personas en la casa", min_value=1, max_value=50, value=4)
    calentador = st.selectbox("Calentamiento de agua", ["Termotanque", "Calefón"])

# --- LÓGICA DE CÁLCULO CORREGIDA ---
st.write("") # Espacio
if st.button("CALCULAR MI PLAN"):
    puntaje = mapa_dureza[zona]
    if origen == "Pozo/Napa":
        puntaje += 2
    
    puntaje = min(puntaje, 10) # Tope máximo 10
    
    equipos = 1 # Base siempre 1
    detalles = ["🔹 1 Equipo en la entrada principal (subida al tanque o entrada de calle)."]
    
    # 1. REFUERZO POR DUREZA (Agua muy dura)
    if puntaje >= 8:
        equipos += 1
        detalles.append("🔹 1 Equipo de Refuerzo en la bajada del tanque (Requerido por Dureza Alta).")
        
    # 2. REFUERZO POR CONSUMO (Mucha gente) - ¡AHORA SUMA SIEMPRE!
    # Antes se bloqueaba si la dureza era alta. Ahora es un 'if' independiente.
    if personas >= 6:
        equipos += 1
        detalles.append(f"🔹 1 Equipo Extra por alto caudal de consumo (+{personas} personas).")

    # 3. REFUERZO CALEFÓN (Específico para serpentina)
    if calentador == "Calefón" and puntaje >= 7:
        equipos += 1
        detalles.append("🔹 1 Equipo de Refuerzo exclusivo en la entrada de agua fría del Calefón.")

    # --- MOSTRAR RESULTADOS ---
    st.markdown("---")
    st.success(f"### Resultado: Necesitas {equipos} Equipos")
    
    for d in detalles:
        st.info(d)
        
    if bomba:
        st.warning("⚠️ Instalar SIEMPRE 1 equipo ANTES de la bomba presurizadora.")

    # --- BOTONES DE ACCIÓN ---
    
    # Mensaje de WhatsApp
    msg = f"Hola EcoSarro! Mi diagnóstico para {zona} ({personas} personas) dio {equipos} equipos. ¿Me podrían asesorar?"
    msg_url = urllib.parse.quote(msg)
    
    # 1. BOTÓN WHATSAPP (Verde con Icono)
    st.markdown(f"""
        <a href="https://wa.me/5493515190658?text={msg_url}" class="whatsapp-btn" target="_blank">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="white" xmlns="http://www.w3.org/2000/svg">
                <path d="M17.472 14.382C17.117 14.382 16.761 14.382 16.406 14.382C16.273 14.382 16.14 14.442 16.05 14.549C15.823 14.821 15.594 15.092 15.367 15.364C15.289 15.457 15.158 15.485 15.047 15.43C14.467 15.138 13.916 14.793 13.403 14.398C12.788 13.923 12.235 13.376 11.751 12.77C11.365 12.285 11.026 11.766 10.741 11.218C10.686 11.112 10.712 10.985 10.801 10.906C11.08 10.662 11.359 10.419 11.637 10.176C11.74 10.086 11.796 9.957 11.796 9.82C11.796 9.467 11.796 9.115 11.796 8.762C11.796 8.528 11.796 8.293 11.796 8.059C11.796 7.922 11.739 7.794 11.637 7.704C11.378 7.476 11.12 7.247 10.861 7.019C10.623 6.809 10.384 6.599 10.146 6.389C10.057 6.31 9.93 6.335 9.873 6.442C9.571 7.014 9.227 7.562 8.842 8.077C8.619 8.375 8.397 8.674 8.175 8.972C8.079 9.101 8.071 9.278 8.154 9.417C9.043 10.908 10.36 12.096 11.942 12.872C12.091 12.945 12.274 12.928 12.396 12.822C12.636 12.613 12.875 12.404 13.114 12.195C13.204 12.116 13.33 12.141 13.387 12.247C13.689 12.819 14.033 13.367 14.418 13.882C14.641 14.18 14.863 14.479 15.085 14.777C15.181 14.906 15.189 15.083 15.106 15.222C14.938 15.503 14.77 15.785 14.602 16.066C14.512 16.216 14.596 16.408 14.764 16.446C15.253 16.556 15.748 16.634 16.246 16.68C17.683 16.812 19.052 16.438 20.254 15.656C20.378 15.575 20.395 15.4 20.293 15.298C19.352 14.358 18.412 13.418 17.472 12.478C17.37 12.376 17.194 12.393 17.113 12.517C16.853 12.915 16.55 13.284 16.211 13.618C16.121 13.707 16.146 13.856 16.264 13.914C16.654 14.106 17.062 14.262 17.472 14.382Z"/>
            </svg>
            Consultanos a través de Whatsapp
        </a>
    """, unsafe_allow_html=True)

    # 2. BOTÓN YOUTUBE (Icono arriba, texto abajo)
    st.markdown("""
        <a href="https://www.youtube.com/@EcoSarro" class="youtube-btn" target="_blank">
            <svg width="30" height="30" viewBox="0 0 24 24" fill="red" xmlns="http://www.w3.org/2000/svg">
                <path d="M23.498 6.186C23.221 5.145 22.404 4.328 21.363 4.051C19.479 3.549 12 3.549 12 3.549C12 3.549 4.521 3.549 2.637 4.051C1.596 4.328 0.779 5.145 0.502 6.186C0 8.07 0 12 0 12C0 12 0 15.93 0.502 17.814C0.779 18.855 1.596 19.672 2.637 19.949C4.521 20.451 12 20.451 12 20.451C12 20.451 19.479 20.451 21.363 19.949C22.404 19.672 23.221 18.855 23.498 17.814C24 15.93 24 12 24 12C24 12 24 8.07 23.498 6.186ZM9.545 15.568V8.432L15.818 12L9.545 15.568Z"/>
            </svg>
            Videos de instalación
        </a>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #555; font-size: 0.8rem;'>Industria Argentina - Protegiendo tu hogar del sarro</p>", unsafe_allow_html=True)
