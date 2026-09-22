import streamlit as st
import random
from datetime import datetime

# Configuración inicial oculta
st.set_page_config(page_title="V H S _ V A M P I R E", layout="wide", initial_sidebar_state="expanded")

# --- CSS EXTREMO: SHADER VHS, GRANULADO Y ANIMACIÓN CIRCULAR ---
css_vhs = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Creepster&family=VT323&display=swap');

/* Ocultar elementos por defecto de Streamlit */
#MainMenu, header, footer, .stDeployButton {visibility: hidden; display: none;}

/* Fondo Global y Tipografía Base (Monitor CRT) */
.stApp {
    background-color: #030000;
    background-image: radial-gradient(circle, #1a0000 0%, #000000 100%);
    color: #ff3333;
    font-family: 'VT323', monospace;
    font-size: 28px;
}

/* VFX SHADER: Ruido VHS / Granulado (Film Grain) + Scanlines */
.stApp::before {
    content: " ";
    display: block;
    position: fixed;
    top: 0; left: 0; bottom: 0; right: 0;
    /* Líneas de escaneo rojas y oscuras */
    background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.5) 50%), 
                linear-gradient(90deg, rgba(255, 0, 0, 0.08), rgba(50, 0, 0, 0.04), rgba(150, 0, 0, 0.05));
    background-size: 100% 4px, 4px 100%;
    z-index: 9998;
    pointer-events: none;
}

.stApp::after {
    content: " ";
    display: block;
    position: fixed;
    top: 0; left: 0; bottom: 0; right: 0;
    /* Generador de ruido fractal en SVG puro codificado */
    background-image: url('data:image/svg+xml,%3Csvg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"%3E%3Cfilter id="noiseFilter"%3E%3CfeTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3" stitchTiles="stitch"/%3E%3C/filter%3E%3Crect width="100%25" height="100%25" filter="url(%23noiseFilter)"/%3E%3C/svg%3E');
    opacity: 0.12;
    z-index: 9999;
    pointer-events: none;
    mix-blend-mode: color-dodge; /* Se mezcla con los rojos y negros dándole un toque vintage */
    animation: noise_flicker 0.2s infinite;
}

@keyframes noise_flicker {
    0% { transform: translate(0, 0); opacity: 0.10; }
    50% { transform: translate(1px, -1px); opacity: 0.14; }
    100% { transform: translate(-1px, 1px); opacity: 0.10; }
}

/* Títulos con efecto Sangriento y tamaños aumentados */
h1 { font-size: 4.5rem !important; margin-bottom: 0.5rem !important; }
h2 { font-size: 3.5rem !important; }
h3 { font-size: 2.5rem !important; }

h1, h2, h3 {
    font-family: 'Creepster', cursive;
    color: #cc0000 !important;
    text-transform: uppercase;
    letter-spacing: 5px;
    /* Animación circular suave en lugar de glitch */
    animation: blood_orbit 4s infinite ease-in-out;
}

/* Títulos secundarios estilo VCR (Fecha/Hora) */
.vcr-text {
    font-family: 'VT323', monospace;
    color: #ffcccc;
    text-shadow: 2px 2px 5px #aa0000;
    font-size: 2rem;
    letter-spacing: 2px;
}

/* Animación Dinámica Profesional: Órbita de Sangre */
@keyframes blood_orbit {
    0% { text-shadow: 0px -4px 6px rgba(255,0,0,0.8), 0px 4px 6px rgba(50,0,0,0.9); transform: scale(1); }
    25% { text-shadow: 4px 0px 6px rgba(255,0,0,0.8), -4px 0px 6px rgba(50,0,0,0.9); }
    50% { text-shadow: 0px 4px 6px rgba(255,0,0,0.8), 0px -4px 6px rgba(50,0,0,0.9); transform: scale(1.02); }
    75% { text-shadow: -4px 0px 6px rgba(255,0,0,0.8), 4px 0px 6px rgba(50,0,0,0.9); }
    100% { text-shadow: 0px -4px 6px rgba(255,0,0,0.8), 0px 4px 6px rgba(50,0,0,0.9); transform: scale(1); }
}

/* Sobreescribir las barras de progreso azules de Streamlit a Rojo Sangre */
[data-testid="stProgressBar"] > div > div {
    background-color: #8b0000 !important;
    background-image: linear-gradient(90deg, #4a0000, #ff0000, #4a0000) !important;
    background-size: 200% 100%;
    box-shadow: 0 0 15px rgba(255,0,0,0.6);
    animation: blood_flow 3s infinite linear;
}

@keyframes blood_flow {
    0% { background-position: 100% 0; }
    100% { background-position: -100% 0; }
}

/* Barra Lateral: Sangrienta y Oscura */
[data-testid="stSidebar"] {
    background-color: #050000 !important;
    border-right: 3px solid #660000;
    box-shadow: 8px 0 20px rgba(150, 0, 0, 0.15);
}

/* Botones (Botones de Videocasetera) */
button {
    border: 2px solid #770000 !important;
    background: rgba(30, 0, 0, 0.9) !important;
    color: #ff4444 !important;
    font-family: 'VT323', monospace !important;
    font-size: 26px !important;
    text-transform: uppercase;
    padding: 10px 20px !important;
    transition: 0.2s ease-in-out;
}
button:hover {
    background: #550000 !important;
    color: #ffffff !important;
    box-shadow: 0 0 20px rgba(255,0,0,0.8);
    border-color: #ff0000 !important;
    transform: scale(1.05);
}

/* Opciones de Menú (Radio Buttons) */
div[role="radiogroup"] > label {
    background: rgba(15, 0, 0, 0.9) !important;
    border-left: 5px solid #440000 !important;
    padding: 15px !important;
    margin-bottom: 8px;
    font-family: 'VT323', monospace !important;
    transition: all 0.3s ease;
}
div[role="radiogroup"] > label p { color: #dd0000 !important; font-size: 26px !important; }
div[role="radiogroup"] > label:hover { border-left: 5px solid #ff4444 !important; background: rgba(30, 0, 0, 0.9) !important; }
div[role="radiogroup"] > label[data-checked="true"] { border-left: 5px solid #ff0000 !important; background: rgba(60, 0, 0, 0.9) !important; }
div[role="radiogroup"] > label[data-checked="true"] p { color: #ffffff !important; text-shadow: 0 0 8px #ff0000; font-size: 28px !important; }

/* Contenedores Malditos (Cajas de VHS) */
.vhs-box {
    border: 3px solid #550000;
    background: rgba(15, 0, 0, 0.85);
    padding: 30px;
    margin: 15px 0;
    box-shadow: inset 0 0 30px #000;
    position: relative;
    overflow: hidden;
}
p { font-size: 1.4rem; line-height: 1.6; }
</style>
"""
st.markdown(css_vhs, unsafe_allow_html=True)

# --- INTERFAZ LATERAL (MENÚ VCR) ---
st.sidebar.markdown("<h1 style='font-size: 4rem; text-align: center; margin-bottom: 0;'>TAPE 01</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<p class='vcr-text' style='text-align: center; font-size: 2.2rem;'>PLAY ► SP</p>", unsafe_allow_html=True)
st.sidebar.markdown("<hr style='border: 1px solid #770000;'>", unsafe_allow_html=True)

menu = ["[ TRACK 1 ] Biblioteca Sangrienta", "[ TRACK 2 ] Archivos Encontrados", "[ TRACK 3 ] Psicofonías", "[ TRACK 4 ] Videoclub de Culto", "[ TRACK 5 ] Pacto de Sangre"]
eleccion = st.sidebar.radio("CANALES", menu, label_visibility="collapsed")
st.sidebar.markdown("<br><br><p style='color: #ff0000; font-family: VT323; font-size: 32px; text-align: center; text-shadow: 0 0 10px red;'>REC 🔴</p>", unsafe_allow_html=True)

# --- 1. SECCIÓN HISTORIA ---
if eleccion == "[ TRACK 1 ] Biblioteca Sangrienta":
    st.markdown("<h1>ARCHIVO DE MANUSCRITOS</h1>", unsafe_allow_html=True)
    st.markdown("<p class='vcr-text'>SELECCIONA UNA CINTA PARA DESATAR LA HISTORIA...</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🕷️ LA VIUDA NEGRA"):
            st.session_state.libro_actual = "arana"
            
    with col2:
        if st.button("🩸 JARDÍN DE ESPINAS"):
            st.session_state.libro_actual = "rosa"

    if "libro_actual" in st.session_state:
        if st.session_state.libro_actual == "arana":
            st.markdown("""
            <style>
            .spider-web { 
                border: 3px dashed #660000; padding: 40px; 
                background: url('https://www.transparenttextures.com/patterns/cobweb.png'), rgba(10,0,0,0.9); 
                box-shadow: inset 0 0 60px #000, 0 0 20px rgba(255,0,0,0.1); 
            }
            </style>
            <div class="spider-web vhs-box">
                <h2 style="color: #990000;">LA VIUDA NEGRA</h2>
                <p style="font-family: monospace; font-size: 24px; color: #cc4444;">[ TEXTO CORRUPTO ] Las patas crujen en la oscuridad. El hilo de seda baja desde el techo, manchado de óxido...</p>
            </div>
            """, unsafe_allow_html=True)
            
        elif st.session_state.libro_actual == "rosa":
            st.markdown("""
            <style>
            .rose-garden { 
                border: 3px solid #990000; padding: 40px; 
                background: url('https://www.transparenttextures.com/patterns/dark-matter.png'), rgba(25,0,0,0.9); 
                box-shadow: inset 0 0 50px #330000; 
            }
            </style>
            <div class="rose-garden vhs-box">
                <h2 style="color: #cc0000; text-shadow: 3px 3px 6px #000;">EL JARDÍN DE ESPINAS</h2>
                <p style="font-style: italic; font-size: 26px; color: #ff6666;">"El aroma era dulce, pero el tallo exigía sangre para florecer..."</p>
            </div>
            """, unsafe_allow_html=True)

# --- 2. SECCIÓN MULTIMEDIA ---
elif eleccion == "[ TRACK 2 ] Archivos Encontrados":
    st.markdown("<h1>METRAJE RECUPERADO</h1>", unsafe_allow_html=True)
    st.markdown("<p class='vcr-text'>EVIDENCIA VISUAL SUBIDA DESDE FUENTES DESCONOCIDAS.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='vhs-box' style='height: 300px; display: flex; align-items: center; justify-content: center; border-color:#660000;'><h3 style='color:#aa0000;'>NO SIGNAL // FOTO 1</h3></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='vhs-box' style='height: 300px; display: flex; align-items: center; justify-content: center; border-color:#660000;'><h3 style='color:#aa0000;'>STATIC.MP4</h3></div>", unsafe_allow_html=True)

# --- 3. SECCIÓN AUDIOLOGÍA ---
elif eleccion == "[ TRACK 3 ] Psicofonías":
    st.markdown("<h1>FRECUENCIAS MUERTAS</h1>", unsafe_allow_html=True)
    st.markdown("<p class='vcr-text'>CINTAS DE CASSETTE ENCONTRADAS EN EL SÓTANO.</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='vhs-box'><h3>CINTA A: Lluvia y Neón</h3><p style='color:#cc4444;'>TRACKING...</p></div>", unsafe_allow_html=True)
    # La barra ahora será roja con un flujo animado
    st.progress(15) 
    
    st.markdown("<br><div class='vhs-box'><h3>CINTA B: Tema Principal (Distorsionado)</h3><p style='color:#cc4444;'>TRACKING...</p></div>", unsafe_allow_html=True)
    st.progress(45)

# --- 4. SECCIÓN PELÍCULAS Y SERIES ---
elif eleccion == "[ TRACK 4 ] Videoclub de Culto":
    st.markdown("<h1>VIDEOCLUB MALDITO</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""<div class='vhs-box' style='text-align:center;'>
        <h3>SILENT HILL</h3>
        <div style='height:220px; background:#1a0000; margin:15px 0; border: 2px solid #550000; display:flex; align-items:center; justify-content:center;'><p style='color:#ff0000; font-size:24px;'>[VHS COVER]</p></div>
        </div>""", unsafe_allow_html=True)
        with st.expander("DECODIFICAR INFO"):
            st.write("Niebla, ceniza, y traumas que toman forma física.")

    with col2:
        st.markdown("""<div class='vhs-box' style='text-align:center;'>
        <h3>EVANGELION</h3>
        <div style='height:220px; background:#1a0000; margin:15px 0; border: 2px solid #550000; display:flex; align-items:center; justify-content:center;'><p style='color:#ff0000; font-size:24px;'>[VHS COVER]</p></div>
        </div>""", unsafe_allow_html=True)
        with st.expander("DECODIFICAR INFO"):
            st.write("Mechas gigantes, crisis existenciales y ángeles apocalípticos.")

    with col3:
        st.markdown("""<div class='vhs-box' style='text-align:center;'>
        <h3>MR. ROBOT</h3>
        <div style='height:220px; background:#1a0000; margin:15px 0; border: 2px solid #550000; display:flex; align-items:center; justify-content:center;'><p style='color:#ff0000; font-size:24px;'>[VHS COVER]</p></div>
        </div>""", unsafe_allow_html=True)
        with st.expander("DECODIFICAR INFO"):
            st.write("Hacking realista, ansiedad y caída del sistema.")

# --- 5. SECCIÓN ESTRELLAS (ORÁCULO) ---
elif eleccion == "[ TRACK 5 ] Pacto de Sangre":
    st.markdown("<h1 style='text-align: center;'>PACTO CON LA ESTRELLA NEGRA</h1>", unsafe_allow_html=True)
    st.markdown("<p class='vcr-text' style='text-align:center;'>INGRESA TUS DATOS PARA LEER TU CONDENA.</p>", unsafe_allow_html=True)
    
    with st.form("form_estrella"):
        st.markdown("""
        <style>
        /* Estilizar inputs del form para que coincidan con la escala */
        div[data-baseweb="input"] > div { background-color: #0a0000 !important; border: 2px solid #880000 !important; font-family: 'VT323'; }
        input { color: #ff3333 !important; font-size: 26px !important; }
        </style>
        """, unsafe_allow_html=True)
        
        nombre = st.text_input("SUJETO:")
        fecha_nacimiento = st.date_input("ORIGEN TEMPORAL:", min_value=datetime(1920, 1, 1), max_value=datetime.today())
        
        revelar = st.form_submit_button("S E L L A R   P A C T O")
        
    if revelar and nombre:
        respuestas = [
            f"El universo se oscurece a tu favor, {nombre}. Una oportunidad nacerá de las sombras.",
            f"Cuidado al dormir, {nombre}. Alguien de tu pasado acecha desde la estática de tu televisor.",
            f"Tu origen en {fecha_nacimiento.year} dejó una grieta. Algo cruzará esa grieta hacia ti hoy.",
            f"{nombre}... el fallo en la matriz es inminente. Prepárate para el caos absoluto.",
            f"La sangre llama a la sangre, {nombre}. Esa idea oscura que tienes en mente... ejecútala."
        ]
        
        prediccion = random.choice(respuestas)
        
        st.markdown(f"""
        <div class="vhs-box" style="border-color: #ff0000; text-align: center; margin-top: 30px;">
            <h2 style="color: #ff0000; animation: none; text-shadow: 2px 2px 15px #aa0000; font-size: 4rem;">[ PREDICCIÓN ACEPTADA ]</h2>
            <p style="font-size: 38px; font-family: 'Creepster', cursive; color: #ffcccc; margin-top: 20px; line-height: 1.2;">{prediccion}</p>
        </div>
        """, unsafe_allow_html=True)
    elif revelar and not nombre:
        st.error("EL SISTEMA REQUIERE UN NOMBRE PARA EL SACRIFICIO.")
