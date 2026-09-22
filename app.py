import streamlit as st
import random
from datetime import datetime

# Configuración inicial oculta
st.set_page_config(page_title="V H S _ V A M P I R E", layout="wide", initial_sidebar_state="expanded")

# --- CSS EXTREMO: ESTÉTICA VHS, VAMPIRESCA Y SLASHER 80s ---
css_vhs = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Creepster&family=VT323&display=swap');

/* Ocultar elementos por defecto de Streamlit */
#MainMenu, header, footer, .stDeployButton {visibility: hidden; display: none;}

/* Fondo Global y Tipografía Base (Monitor CRT) */
.stApp {
    background-color: #030000;
    background-image: radial-gradient(circle, #1a0000 0%, #000000 100%);
    color: #ff1a1a;
    font-family: 'VT323', monospace;
    font-size: 22px;
}

/* Efecto Scanlines (Líneas de TV antigua) */
.stApp::before {
    content: " ";
    display: block;
    position: fixed;
    top: 0; left: 0; bottom: 0; right: 0;
    background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.3) 50%), 
                linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
    z-index: 9999;
    background-size: 100% 4px, 3px 100%;
    pointer-events: none;
}

/* Aberración Cromática y Estilo Vampírico/Slasher para Títulos */
h1, h2, h3 {
    font-family: 'Creepster', cursive;
    color: #b30000 !important;
    text-transform: uppercase;
    letter-spacing: 3px;
    text-shadow: 3px 0 0 rgba(255,0,0,0.7), -3px 0 0 rgba(0,255,255,0.4);
    animation: glitch 3s infinite;
}

/* Títulos secundarios estilo VCR (Fecha/Hora) */
.vcr-text {
    font-family: 'VT323', monospace;
    color: #fff;
    text-shadow: 2px 2px 4px #f00;
    font-size: 1.5rem;
}

/* Glitch Animation */
@keyframes glitch {
    0% { text-shadow: 2px 0 0 red, -2px 0 0 cyan; }
    10% { text-shadow: -2px 0 0 red, 2px 0 0 cyan; }
    20% { text-shadow: 2px 0 0 red, -2px 0 0 cyan; }
    30% { text-shadow: 2px 0 0 red, -2px 0 0 cyan; }
    40% { text-shadow: -2px 0 0 red, 2px 0 0 cyan; }
    50% { text-shadow: 2px 0 0 red, -2px 0 0 cyan; }
    60% { text-shadow: 2px 0 0 red, -2px 0 0 cyan; transform: translate(1px, 1px); }
    70% { text-shadow: -2px 0 0 red, 2px 0 0 cyan; transform: translate(-1px, -1px); }
    80% { text-shadow: 2px 0 0 red, -2px 0 0 cyan; }
    100% { text-shadow: 2px 0 0 red, -2px 0 0 cyan; }
}

/* Barra Lateral: Sangrienta y Oscura */
[data-testid="stSidebar"] {
    background-color: #050000 !important;
    border-right: 2px solid #550000;
    box-shadow: 5px 0 15px rgba(255, 0, 0, 0.2);
}

/* Botones (Botones de Videocasetera) */
button {
    border: 1px solid #550000 !important;
    background: rgba(20, 0, 0, 0.8) !important;
    color: #ff3333 !important;
    font-family: 'VT323', monospace !important;
    font-size: 20px !important;
    text-transform: uppercase;
    transition: 0.1s;
}
button:hover {
    background: #ff0000 !important;
    color: #000 !important;
    box-shadow: 0 0 10px #ff0000;
}

/* Opciones de Menú (Radio Buttons) */
div[role="radiogroup"] > label {
    background: rgba(10, 0, 0, 0.9) !important;
    border-left: 4px solid #330000 !important;
    padding: 10px !important;
    margin-bottom: 5px;
    font-family: 'VT323', monospace !important;
}
div[role="radiogroup"] > label p { color: #cc0000 !important; font-size: 22px !important; }
div[role="radiogroup"] > label[data-checked="true"] { border-left: 4px solid #ff0000 !important; background: rgba(50, 0, 0, 0.9) !important; }
div[role="radiogroup"] > label[data-checked="true"] p { color: #fff !important; text-shadow: 0 0 5px #ff0000; }

/* Contenedores Malditos (Cajas de VHS) */
.vhs-box {
    border: 2px solid #330000;
    background: rgba(10, 0, 0, 0.7);
    padding: 20px;
    margin: 10px 0;
    box-shadow: inset 0 0 20px #000;
}
</style>
"""
st.markdown(css_vhs, unsafe_allow_html=True)

# --- INTERFAZ LATERAL (MENÚ VCR) ---
st.sidebar.markdown("<h1 style='font-size: 3rem; text-align: center; margin-bottom: 0;'>TAPE 01</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<p class='vcr-text' style='text-align: center;'>PLAY ► SP</p>", unsafe_allow_html=True)
st.sidebar.markdown("<hr style='border: 1px solid #550000;'>", unsafe_allow_html=True)

menu = ["[ TRACK 1 ] Biblioteca Sangrienta", "[ TRACK 2 ] Archivos Encontrados", "[ TRACK 3 ] Psicofonías", "[ TRACK 4 ] Videoclub de Culto", "[ TRACK 5 ] Pacto de Sangre"]
eleccion = st.sidebar.radio("CANALES", menu, label_visibility="collapsed")
st.sidebar.markdown("<br><br><p style='color: #ff0000; font-family: VT323; font-size: 24px; text-align: center; animation: glitch 2s infinite;'>REC 🔴</p>", unsafe_allow_html=True)

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
            .stApp { background-color: #050505; color: #888; }
            .spider-web { 
                border: 2px dashed #444; padding: 30px; 
                background: url('https://www.transparenttextures.com/patterns/cobweb.png'), rgba(0,0,0,0.8); 
                box-shadow: inset 0 0 50px #000, 0 0 15px rgba(255,0,0,0.2); 
            }
            </style>
            <div class="spider-web vhs-box">
                <h2 style="color: #660000;">LA VIUDA NEGRA</h2>
                <p style="font-family: monospace; font-size: 18px;">[ TEXTO CORRUPTO ] Las patas crujen en la oscuridad. El hilo de seda baja desde el techo, manchado de óxido...</p>
                <p><i>(Sección reservada para el despliegue del terror arácnido)</i></p>
            </div>
            """, unsafe_allow_html=True)
            
        elif st.session_state.libro_actual == "rosa":
            st.markdown("""
            <style>
            .stApp { background-color: #1a0505; color: #ff9999; }
            .rose-garden { 
                border: 2px solid #800000; padding: 30px; 
                background: url('https://www.transparenttextures.com/patterns/dark-matter.png'), rgba(20,0,0,0.9); 
                box-shadow: inset 0 0 40px #330000; 
            }
            </style>
            <div class="rose-garden vhs-box">
                <h2 style="color: #990000; text-shadow: 2px 2px 5px #000;">EL JARDÍN DE ESPINAS</h2>
                <p style="font-style: italic; font-size: 22px;">"El aroma era dulce, pero el tallo exigía sangre para florecer..."</p>
                <p><i>(Romance gótico, pétalos negros cayendo en el CSS a futuro)</i></p>
            </div>
            """, unsafe_allow_html=True)

# --- 2. SECCIÓN MULTIMEDIA ---
elif eleccion == "[ TRACK 2 ] Archivos Encontrados":
    st.markdown("<h1>METRAJE RECUPERADO</h1>", unsafe_allow_html=True)
    st.markdown("<p class='vcr-text'>EVIDENCIA VISUAL SUBIDA DESDE FUENTES DESCONOCIDAS.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='vhs-box' style='height: 250px; display: flex; align-items: center; justify-content: center; border-color:#444;'><h3 style='color:#555;'>NO SIGNAL // FOTO 1</h3></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='vhs-box' style='height: 250px; display: flex; align-items: center; justify-content: center; border-color:#444;'><h3 style='color:#555;'>STATIC.MP4</h3></div>", unsafe_allow_html=True)

# --- 3. SECCIÓN AUDIOLOGÍA ---
elif eleccion == "[ TRACK 3 ] Psicofonías":
    st.markdown("<h1>FRECUENCIAS MUERTAS</h1>", unsafe_allow_html=True)
    st.markdown("<p class='vcr-text'>CINTAS DE CASSETTE ENCONTRADAS EN EL SÓTANO.</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='vhs-box'><h3>CINTA A: Lluvia y Neón</h3><p style='color:#aaa;'>TRACKING...</p></div>", unsafe_allow_html=True)
    st.progress(15) 
    
    st.markdown("<br><div class='vhs-box'><h3>CINTA B: Tema Principal (Distorsionado)</h3><p style='color:#aaa;'>TRACKING...</p></div>", unsafe_allow_html=True)
    st.progress(45)

# --- 4. SECCIÓN PELÍCULAS Y SERIES ---
elif eleccion == "[ TRACK 4 ] Videoclub de Culto":
    st.markdown("<h1>VIDEOCLUB MALDITO</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""<div class='vhs-box' style='text-align:center;'>
        <h3 style='font-size:1.5rem;'>SILENT HILL</h3>
        <div style='height:180px; background:#111; margin:10px 0; border: 1px solid #444; display:flex; align-items:center; justify-content:center;'><p style='color:#f00;'>[VHS COVER]</p></div>
        </div>""", unsafe_allow_html=True)
        with st.expander("DECODIFICAR INFO"):
            st.write("Niebla, ceniza, y traumas que toman forma física.")

    with col2:
        st.markdown("""<div class='vhs-box' style='text-align:center;'>
        <h3 style='font-size:1.5rem;'>EVANGELION</h3>
        <div style='height:180px; background:#111; margin:10px 0; border: 1px solid #444; display:flex; align-items:center; justify-content:center;'><p style='color:#f00;'>[VHS COVER]</p></div>
        </div>""", unsafe_allow_html=True)
        with st.expander("DECODIFICAR INFO"):
            st.write("Mechas gigantes, crisis existenciales y ángeles apocalípticos.")

    with col3:
        st.markdown("""<div class='vhs-box' style='text-align:center;'>
        <h3 style='font-size:1.5rem;'>MR. ROBOT</h3>
        <div style='height:180px; background:#111; margin:10px 0; border: 1px solid #444; display:flex; align-items:center; justify-content:center;'><p style='color:#f00;'>[VHS COVER]</p></div>
        </div>""", unsafe_allow_html=True)
        with st.expander("DECODIFICAR INFO"):
            st.write("Hacking realista, ansiedad y caída del sistema.")

# --- 5. SECCIÓN ESTRELLAS (ORÁCULO) ---
elif eleccion == "[ TRACK 5 ] Pacto de Sangre":
    st.markdown("<h1 style='text-align: center; color: #ff0000;'>PACTO CON LA ESTRELLA NEGRA</h1>", unsafe_allow_html=True)
    st.markdown("<p class='vcr-text' style='text-align:center;'>INGRESA TUS DATOS PARA LEER TU CONDENA.</p>", unsafe_allow_html=True)
    
    with st.form("form_estrella"):
        st.markdown("""
        <style>
        /* Estilizar inputs del form */
        div[data-baseweb="input"] > div { background-color: #000 !important; border: 1px solid #ff0000 !important; color: #f00 !important; font-family: 'VT323'; }
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
        <div class="vhs-box" style="border-color: #ff0000; text-align: center; margin-top: 20px;">
            <h2 style="color: #ff0000; animation: none; text-shadow: none;">[ PREDICCIÓN ACEPTADA ]</h2>
            <p style="font-size: 28px; font-family: 'Creepster'; color: #fff;">{prediccion}</p>
        </div>
        """, unsafe_allow_html=True)
    elif revelar and not nombre:
        st.error("EL SISTEMA REQUIERE UN NOMBRE PARA EL SACRIFICIO.")
