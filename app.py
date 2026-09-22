import streamlit as st
import random
from datetime import datetime

# Configuración inicial oculta
st.set_page_config(page_title="V H S _ V A M P I R E", layout="wide", initial_sidebar_state="expanded")

# --- INYECCIÓN DE SONIDOS (RE OUTBREAK + OBSCURE) ---
re_sound_js = """
<script>
const parentDoc = window.parent.document;
if (!parentDoc.getElementById('sfx_initialized')) {
    let flag = parentDoc.createElement('div');
    flag.id = 'sfx_initialized';
    flag.style.display = 'none';
    parentDoc.body.appendChild(flag);

    // SFX Botones (RE Outbreak)
    const btnSoundUrl = 'https://assets.mixkit.co/active_storage/sfx/2570/2570-preview.mp3';
    // SFX Tracks Menú Lateral (Obscure - Eco metálico y oscuro)
    const trackSoundUrl = 'https://assets.mixkit.co/active_storage/sfx/2864/2864-preview.mp3'; 
    
    parentDoc.addEventListener('mousedown', function(e) {
        let target = e.target;
        
        // Si clickea en los TRACKS del menú lateral
        if (target.closest('[data-testid="stSidebar"] label')) {
            let audio = new Audio(trackSoundUrl);
            audio.volume = 0.6;
            audio.play().catch(err => console.log('Audio error:', err));
        } 
        // Si clickea en botones normales de la página
        else if (target.closest('button')) {
            let audio = new Audio(btnSoundUrl);
            audio.volume = 0.4;
            audio.play().catch(err => console.log('Audio error:', err));
        }
    });
}
</script>
"""
st.components.v1.html(re_sound_js, height=0, width=0)

# --- CSS EXTREMO: SHADER VHS ROJO, F.E.A.R. 3 TEXT Y MENÚ PS2 ---
css_vhs = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Creepster&family=VT323&family=Share+Tech+Mono&display=swap');

#MainMenu, header, footer, .stDeployButton {visibility: hidden; display: none;}

/* Fondo base CRT */
.stApp {
    background-color: #040000;
    font-size: 28px;
}

/* EFECTO F.E.A.R. 3: Viñeta oscura de fondo */
.stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    background: radial-gradient(circle at center, transparent 30%, rgba(40, 0, 0, 0.4) 70%, rgba(0, 0, 0, 0.95) 100%);
    pointer-events: none;
    z-index: 9996;
}

/* SHADER VHS GRANULADO ROJO (Película Antigua) */
.stApp::after {
    content: " ";
    display: block;
    position: fixed;
    top: 0; left: 0; bottom: 0; right: 0;
    /* Genera ruido y líneas horizontales intercaladas con un tinte rojo */
    background: 
        url('data:image/svg+xml,%3Csvg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"%3E%3Cfilter id="noiseFilter"%3E%3CfeTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" stitchTiles="stitch"/%3E%3C/filter%3E%3Crect width="100%25" height="100%25" filter="url(%23noiseFilter)"/%3E%3C/svg%3E'),
        linear-gradient(rgba(18, 0, 0, 0) 50%, rgba(20, 0, 0, 0.3) 50%),
        rgba(30, 0, 0, 0.15);
    background-size: auto, 100% 4px, auto;
    opacity: 0.35;
    z-index: 9998;
    pointer-events: none;
    mix-blend-mode: color-dodge;
    animation: vhs_red_grain 0.15s infinite;
}

@keyframes vhs_red_grain {
    0% { transform: translate(0, 0); opacity: 0.30; }
    50% { transform: translate(1px, -1px); opacity: 0.40; }
    100% { transform: translate(-1px, 1px); opacity: 0.35; }
}

/* LETRAS BLANCAS EFECTO F.E.A.R. 3 (Aberración Cromática + Glitch) */
p, .vcr-text, div[data-baseweb="input"] input, div[data-baseweb="select"] {
    font-family: 'Share Tech Mono', monospace !important;
    color: #ffffff !important;
    letter-spacing: 1.5px;
    /* Sombra dividida en rojo y cian para simular el fallo de cámara/HUD */
    text-shadow: 
        2.5px 0px 0px rgba(255, 0, 0, 0.85), 
        -2.5px 0px 0px rgba(0, 255, 255, 0.6),
        0px 0px 8px rgba(255, 255, 255, 0.3);
    animation: fear3_glitch 4s infinite linear alternate-reverse;
}

@keyframes fear3_glitch {
    0%, 100% { text-shadow: 2px 0px 0px rgba(255, 0, 0, 0.8), -2px 0px 0px rgba(0, 255, 255, 0.6); transform: skew(0deg); }
    10% { text-shadow: 3px 0px 0px rgba(255, 0, 0, 0.9), -3px 0px 0px rgba(0, 255, 255, 0.7); }
    11% { text-shadow: -2px 0px 0px rgba(255, 0, 0, 0.9), 3px 0px 0px rgba(0, 255, 255, 0.7); transform: skew(-3deg); }
    12% { transform: skew(0deg); }
    50% { text-shadow: 1px 0px 0px rgba(255, 0, 0, 0.7), -1px 0px 0px rgba(0, 255, 255, 0.5); }
    52% { text-shadow: 5px 1px 0px rgba(255, 0, 0, 1), -5px -1px 0px rgba(0, 255, 255, 0.8); transform: scale(1.02); }
    53% { transform: scale(1); }
}

/* Títulos Sangrientos (Creepster) */
h1 { font-size: 4.5rem !important; margin-bottom: 0.5rem !important; }
h2 { font-size: 3.5rem !important; }
h3 { font-size: 2.5rem !important; }

h1, h2, h3 {
    font-family: 'Creepster', cursive;
    color: #cc0000 !important;
    text-transform: uppercase;
    letter-spacing: 5px;
    animation: blood_orbit 4s infinite ease-in-out;
    text-shadow: 2px 2px 10px #000;
}

@keyframes blood_orbit {
    0% { text-shadow: 0px -2px 4px rgba(255,0,0,0.8), 0px 2px 4px rgba(50,0,0,0.9); }
    50% { text-shadow: 0px 2px 4px rgba(255,0,0,0.8), 0px -2px 4px rgba(50,0,0,0.9); }
    100% { text-shadow: 0px -2px 4px rgba(255,0,0,0.8), 0px 2px 4px rgba(50,0,0,0.9); }
}

/* Barra Lateral Oscura */
[data-testid="stSidebar"] {
    background-color: #030000 !important;
    border-right: 2px solid #4a0000;
}

/* ========================================= */
/* MENÚ LATERAL ESTILO JUEGO PS2             */
/* ========================================= */
div[role="radiogroup"] {
    gap: 0px !important;
}

div[role="radiogroup"] > label {
    background: transparent !important;
    border: none !important;
    padding: 6px 10px !important;
    margin: 0 !important;
    transition: all 0.1s;
}

div[role="radiogroup"] > label p { 
    color: #888888 !important; /* Texto inactivo apagado */
    font-size: 22px !important; 
    line-height: 1.2 !important;
    white-space: nowrap !important;
    /* Reducir efecto FEAR en botones inactivos para mejor lectura */
    text-shadow: 1px 0px 0px rgba(100, 0, 0, 0.5), -1px 0px 0px rgba(0, 100, 100, 0.3) !important;
    animation: none !important;
}

div[role="radiogroup"] > label:hover p { 
    color: #ffffff !important; 
    text-shadow: 2px 0px 0px rgba(255,0,0,0.8), -2px 0px 0px rgba(0,255,255,0.6) !important;
}

/* Opción Seleccionada */
div[role="radiogroup"] > label[data-checked="true"] p { 
    color: #ff2222 !important; 
    text-shadow: 0 0 10px #ff0000, 2px 2px 4px #000 !important; 
    font-size: 22px !important; 
}

div[role="radiogroup"] > label[data-checked="true"] span[data-baseweb="radio"] div {
    background-color: #ff0000 !important;
}

/* Botones de acción */
button {
    border: 1px solid #550000 !important;
    background: rgba(20, 0, 0, 0.9) !important;
    color: #ffffff !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 22px !important;
    text-transform: uppercase;
    padding: 10px 20px !important;
}
button:hover {
    background: #440000 !important;
    box-shadow: 0 0 15px rgba(255,0,0,0.6);
    border-color: #ff0000 !important;
}

/* Contenedores */
.vhs-box {
    border: 2px solid #440000;
    background: rgba(10, 0, 0, 0.7);
    padding: 25px;
    margin: 15px 0;
    box-shadow: inset 0 0 20px #000;
}
</style>
"""
st.markdown(css_vhs, unsafe_allow_html=True)

# --- INTERFAZ LATERAL (MENÚ VCR) ---
st.sidebar.markdown("<h1 style='font-size: 4rem; text-align: center; margin-bottom: 0;'>TAPE 01</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; font-size: 2.2rem; color: #ffcccc;'>PLAY ► SP</p>", unsafe_allow_html=True)
st.sidebar.markdown("<hr style='border: 1px solid #440000; margin-top:0;'>", unsafe_allow_html=True)

menu = ["[ TRACK 1 ] Biblioteca Sangrienta", "[ TRACK 2 ] Archivos Encontrados", "[ TRACK 3 ] Psicofonías", "[ TRACK 4 ] Videoclub de Culto", "[ TRACK 5 ] Pacto de Sangre"]
eleccion = st.sidebar.radio("CANALES", menu, label_visibility="collapsed")
st.sidebar.markdown("<br><p style='color: #ff0000; font-family: VT323; font-size: 32px; text-align: center; text-shadow: 0 0 10px red; animation: none;'>REC 🔴</p>", unsafe_allow_html=True)

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
            <style>.spider-web { border: 2px dashed #660000; padding: 40px; background: rgba(10,0,0,0.9); }</style>
            <div class="spider-web vhs-box">
                <h2 style="color: #990000;">LA VIUDA NEGRA</h2>
                <p>[ TEXTO CORRUPTO ] Las patas crujen en la oscuridad. El hilo de seda baja desde el techo, manchado de óxido...</p>
            </div>
            """, unsafe_allow_html=True)
            
        elif st.session_state.libro_actual == "rosa":
            st.markdown("""
            <style>.rose-garden { border: 2px solid #990000; padding: 40px; background: rgba(25,0,0,0.9); }</style>
            <div class="rose-garden vhs-box">
                <h2 style="color: #cc0000;">EL JARDÍN DE ESPINAS</h2>
                <p>"El aroma era dulce, pero el tallo exigía sangre para florecer..."</p>
            </div>
            """, unsafe_allow_html=True)

# --- 2. SECCIÓN MULTIMEDIA ---
elif eleccion == "[ TRACK 2 ] Archivos Encontrados":
    st.markdown("<h1>METRAJE RECUPERADO</h1>", unsafe_allow_html=True)
    st.markdown("<p class='vcr-text'>EVIDENCIA VISUAL SUBIDA DESDE FUENTES DESCONOCIDAS.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='vhs-box' style='height: 300px; display: flex; align-items: center; justify-content: center;'><h3 style='color:#aa0000;'>NO SIGNAL // FOTO 1</h3></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='vhs-box' style='height: 300px; display: flex; align-items: center; justify-content: center;'><h3 style='color:#aa0000;'>STATIC.MP4</h3></div>", unsafe_allow_html=True)

# --- 3. SECCIÓN AUDIOLOGÍA ---
elif eleccion == "[ TRACK 3 ] Psicofonías":
    st.markdown("<h1>FRECUENCIAS MUERTAS</h1>", unsafe_allow_html=True)
    st.markdown("<p class='vcr-text'>CINTAS DE CASSETTE ENCONTRADAS EN EL SÓTANO.</p>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='vhs-box'>
        <h3>CINTA A: Lluvia y Neón</h3>
        <p style='color:#ff5555 !important; animation: none; text-shadow: none;'>TRACKING...</p>
        <div style="width:100%; background:#1a0000; border:1px solid #550000; height:15px;">
            <div style="width:15%; height:100%; background: linear-gradient(90deg, #880000, #ff0000);"></div>
        </div>
    </div>
    <br>
    <div class='vhs-box'>
        <h3>CINTA B: Tema Principal (Distorsionado)</h3>
        <p style='color:#ff5555 !important; animation: none; text-shadow: none;'>TRACKING...</p>
        <div style="width:100%; background:#1a0000; border:1px solid #550000; height:15px;">
            <div style="width:45%; height:100%; background: linear-gradient(90deg, #880000, #ff0000);"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 4. SECCIÓN PELÍCULAS Y SERIES ---
elif eleccion == "[ TRACK 4 ] Videoclub de Culto":
    st.markdown("<h1>VIDEOCLUB MALDITO</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""<div class='vhs-box' style='text-align:center;'>
        <h3>SILENT HILL</h3>
        <div style='height:220px; background:#1a0000; margin:15px 0; border: 1px solid #550000; display:flex; align-items:center; justify-content:center;'><p style='color:#ff0000 !important; animation: none; text-shadow: none;'>[COVER]</p></div>
        </div>""", unsafe_allow_html=True)
        with st.expander("DECODIFICAR INFO"):
            st.write("Niebla, ceniza, y traumas que toman forma física.")

    with col2:
        st.markdown("""<div class='vhs-box' style='text-align:center;'>
        <h3>EVANGELION</h3>
        <div style='height:220px; background:#1a0000; margin:15px 0; border: 1px solid #550000; display:flex; align-items:center; justify-content:center;'><p style='color:#ff0000 !important; animation: none; text-shadow: none;'>[COVER]</p></div>
        </div>""", unsafe_allow_html=True)
        with st.expander("DECODIFICAR INFO"):
            st.write("Mechas gigantes, crisis existenciales y ángeles apocalípticos.")

    with col3:
        st.markdown("""<div class='vhs-box' style='text-align:center;'>
        <h3>MR. ROBOT</h3>
        <div style='height:220px; background:#1a0000; margin:15px 0; border: 1px solid #550000; display:flex; align-items:center; justify-content:center;'><p style='color:#ff0000 !important; animation: none; text-shadow: none;'>[COVER]</p></div>
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
        div[data-baseweb="input"] > div { background-color: #050000 !important; border: 1px solid #880000 !important; }
        input { color: #ffffff !important; font-size: 24px !important; }
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
            f"{nombre}... el fallo en la matriz es inminente. Prepárate para el caos absoluto."
        ]
        
        st.markdown(f"""
        <div class="vhs-box" style="border-color: #ff0000; text-align: center; margin-top: 30px;">
            <h2 style="color: #ff0000; text-shadow: 2px 2px 10px #aa0000; font-size: 3rem;">[ PREDICCIÓN ACEPTADA ]</h2>
            <p style="font-size: 28px; margin-top: 20px;">{random.choice(respuestas)}</p>
        </div>
        """, unsafe_allow_html=True)
