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
    "Mendoza": 9, "Misiones": 6, "Neuqu
