import streamlit as st
import random
from datetime import datetime

# Configuración inicial oculta
st.set_page_config(page_title="V H S _ V A M P I R E", layout="wide", initial_sidebar_state="expanded")

# --- INYECCIÓN DE SONIDOS Y ATMÓSFERA AMBIENTAL (RUIDO BLANCO + EVENTOS RANDOMS) ---
re_sound_js = """
<script>
const parentDoc = window.parent.document;
if (!parentDoc.getElementById('sfx_initialized')) {
    let flag = parentDoc.createElement('div');
    flag.id = 'sfx_initialized';
    flag.style.display = 'none';
    parentDoc.body.appendChild(flag);

    // SFX Botones y Menú
    const btnSoundUrl = 'https://assets.mixkit.co/active_storage/sfx/2570/2570-preview.mp3';
    const trackSoundUrl = 'https://assets.mixkit.co/active_storage/sfx/2864/2864-preview.mp3'; 
    
    // SFX Randoms para la atmósfera (Crujidos, Disparos lejanos, Fuego, Ecos)
    const ambientEvents = [
        'https://pixabay.com/sound-effects/film-special-effects-distant-war-377958/', // TIROS LEJANOS
        'https://assets.mixkit.co/active_storage/sfx/214/214-preview.mp3',   // Disparo lejano
        'https://assets.mixkit.co/active_storage/sfx/2463/2463-preview.mp3', // Fuego crepitante
        'https://assets.mixkit.co/active_storage/sfx/2572/2572-preview.mp3'  // Eco metálico / Zombie
    ];

    let audioCtx = null;
    let ambientStarted = false;

    // Generador Web Audio API de Ruido Blanco Analógico
    function startAmbientAudio() {
        if (ambientStarted) return;
        ambientStarted = true;
        try {
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            const bufferSize = audioCtx.sampleRate * 2;
            const noiseBuffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
            const output = noiseBuffer.getChannelData(0);
            for (let i = 0; i < bufferSize; i++) {
                output[i] = Math.random() * 2 - 1;
            }
            const whiteNoise = audioCtx.createBufferSource();
            whiteNoise.buffer = noiseBuffer;
            whiteNoise.loop = true;

            // Filtro de frecuencia oscura tipo TV vieja
            const filter = audioCtx.createBiquadFilter();
            filter.type = 'bandpass';
            filter.frequency.value = 350;
            filter.Q.value = 0.6;

            const gainNode = audioCtx.createGain();
            gainNode.gain.value = 0.025; // Volumen de fondo muy sutil

            whiteNoise.connect(filter);
            filter.connect(gainNode);
            gainNode.connect(audioCtx.destination);
            whiteNoise.start(0);

            // Disparador aleatorio de eventos ambientales cada 30 segundos
            setInterval(() => {
                let randomSfx = ambientEvents[Math.floor(Math.random() * ambientEvents.length)];
                let eventAudio = new Audio(randomSfx);
                // Si es el disparo, bajarle un poco más el volumen para que suene a lo lejos
                eventAudio.volume = randomSfx.includes('214') ? 0.25 : 0.45;
                eventAudio.play().catch(e => console.log('Event audio error:', e));
            }, 30000);
            
        } catch(e) { 
            console.log('Audio Context error:', e); 
        }
    }

    parentDoc.addEventListener('mousedown', function(e) {
        startAmbientAudio();
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

# --- CSS EXTREMO: SHADER TV CRT ROJO Y GLITCH ROJO/NEGRO ---
css_vhs = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Creepster&family=VT323&family=Share+Tech+Mono&display=swap');

/* Se removió 'header' para que el botón de colapsar la barra lateral siga visible */
#MainMenu, footer, .stDeployButton {visibility: hidden; display: none;}

/* Estilizar el header superior y el botón de la barra lateral para que no rompa la estética */
header { background-color: transparent !important; }
[data-testid="collapsedControl"] svg { color: #ff0000 !important; }
[data-testid="collapsedControl"]:hover { background-color: rgba(255, 0, 0, 0.1) !important; }

/* Fondo base CRT */
.stApp {
    background-color: #030000;
    font-size: 28px;
}

/* EFECTO TV ANTIGUA 1: Viñeta cóncava CRT + Parpadeo sutil de tubocatódico */
.stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    background: radial-gradient(circle at center, rgba(30, 0, 0, 0.1) 30%, rgba(15, 0, 0, 0.75) 75%, rgba(0, 0, 0, 0.98) 100%);
    pointer-events: none;
    z-index: 9996;
    animation: tv_flicker 0.15s infinite;
}

@keyframes tv_flicker {
    0% { opacity: 0.92; }
    50% { opacity: 1; }
    100% { opacity: 0.95; }
}

/* EFECTO TV ANTIGUA 2: Barrido de líneas CRT + Granulado de interferencia rojo/negro */
.stApp::after {
    content: " ";
    display: block;
    position: fixed;
    top: 0; left: 0; bottom: 0; right: 0;
    background: 
        url('data:image/svg+xml,%3Csvg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"%3E%3Cfilter id="noiseFilter"%3E%3CfeTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3" stitchTiles="stitch"/%3E%3C/filter%3E%3Crect width="100%25" height="100%25" filter="url(%23noiseFilter)"/%3E%3C/svg%3E'),
        repeating-linear-gradient(
            0deg,
            rgba(0, 0, 0, 0.65),
            rgba(0, 0, 0, 0.65) 1px,
            transparent 1px,
            transparent 3px
        ),
        linear-gradient(180deg, rgba(80, 0, 0, 0.2) 0%, rgba(10, 0, 0, 0.5) 100%);
    background-size: auto, 100% 3px, auto;
    opacity: 0.42;
    z-index: 9998;
    pointer-events: none;
    mix-blend-mode: overlay;
    animation: tv_scanlines_scroll 12s linear infinite, red_noise_jump 0.12s infinite;
}

@keyframes tv_scanlines_scroll {
    0% { background-position: 0 0, 0 0, 0 0; }
    100% { background-position: 0 0, 0 100%, 0 0; }
}

@keyframes red_noise_jump {
    0% { transform: translate(0, 0); }
    25% { transform: translate(-1px, 1px); }
    50% { transform: translate(1px, -1px); }
    75% { transform: translate(-1px, -1px); }
    100% { transform: translate(1px, 1px); }
}

/* LETRAS BLANCAS EFECTO GLITCH ROJO Y NEGRO (EXCLUSIVO ROJO/NEGRO) */
p, .vcr-text, div[data-baseweb="input"] input, div[data-baseweb="select"] {
    font-family: 'Share Tech Mono', monospace !important;
    color: #ffffff !important;
    letter-spacing: 1.5px;
    text-shadow: 
        3px 0px 0px rgba(255, 0, 0, 0.9), 
        -3px 0px 0px rgba(40, 0, 0, 0.95),
        0px 0px 6px rgba(200, 0, 0, 0.4);
    animation: red_black_glitch 3.5s infinite linear alternate-reverse;
}

@keyframes red_black_glitch {
    0%, 100% { 
        text-shadow: 2.5px 0px 0px #ff0000, -2.5px 0px 0px #330000, 0 0 5px #ff0000; 
        transform: skew(0deg); 
    }
    10% { text-shadow: 3.5px 0px 0px #cc0000, -3.5px 0px 0px #1a0000, 0 0 8px #990000; }
    11% { text-shadow: -3px 0px 0px #ff0000, 3px 0px 0px #000000, 0 0 10px #ff2222; transform: skew(-2.5deg); }
    12% { transform: skew(0deg); }
    50% { text-shadow: 1.5px 0px 0px #880000, -1.5px 0px 0px #111111; }
    52% { text-shadow: 5px 0px 0px #ff0000, -4px 0px 0px #220000, 0 0 12px #ff0000; transform: scale(1.015); }
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
    color: #888888 !important; 
    font-size: 22px !important; 
    line-height: 1.2 !important;
    white-space: nowrap !important;
    text-shadow: 1.5px 0px 0px rgba(120, 0, 0, 0.6), -1.5px 0px 0px rgba(0, 0, 0, 0.9) !important;
    animation: none !important;
}

div[role="radiogroup"] > label:hover p { 
    color: #ffffff !important; 
    text-shadow: 2.5px 0px 0px #ff0000, -2.5px 0px 0px #330000 !important;
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

/* Contenedores y Cassettes */
.vhs-box {
    border: 2px solid #440000;
    background: rgba(10, 0, 0, 0.7);
    padding: 25px;
    margin: 15px 0;
    box-shadow: inset 0 0 20px #000;
}

.cassette-card {
    border: 2px solid #550000;
    background: radial-gradient(circle at center, #180202 0%, #050000 100%);
    padding: 20px;
    margin: 15px 0;
    box-shadow: inset 0 0 15px #000, 0 0 10px rgba(255,0,0,0.2);
    border-radius: 4px;
}

.cassette-body {
    border: 2px solid #880000;
    background: #0a0000;
    border-radius: 8px;
    padding: 15px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
}

.cassette-label-box {
    background: linear-gradient(90deg, #300, #600, #300);
    border: 1px solid #ff2222;
    width: 100%;
    text-align: center;
    padding: 8px;
}

.cassette-reels-window {
    width: 220px;
    height: 70px;
    background: #000;
    border: 2px solid #440000;
    border-radius: 35px;
    display: flex;
    justify-content: space-around;
    align-items: center;
    position: relative;
    padding: 0 10px;
}

.cassette-reel {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    border: 3px dashed #ff3333;
    background: radial-gradient(circle, #220000 35%, #880000 100%);
    box-shadow: 0 0 6px #ff0000;
}

.cassette-reels-window.spinning .cassette-reel {
    animation: reel_spin 1.8s linear infinite;
}

@keyframes reel_spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

audio {
    width: 100%;
    filter: invert(100%) hue-rotate(180deg) drop-shadow(0 0 4px #ff0000);
    outline: none;
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
    st.markdown("<h1>EL RINCÓN DE RISSOS</h1>", unsafe_allow_html=True)
    st.markdown("<p class='vcr-text'>'ANGHELL' COLLECTION...</p>", unsafe_allow_html=True)
    
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

# --- 3. SECCIÓN AUDIOLOGÍA (CASSETTES CON SPINNERS E INTERFAZ NUEVA) ---
elif eleccion == "[ TRACK 3 ] Psicofonías":
    st.markdown("<h1>FRECUENCIAS MUERTAS</h1>", unsafe_allow_html=True)
    st.markdown("<p class='vcr-text'>CINTAS DE CASSETTE ENCONTRADAS EN EL SÓTANO.</p>", unsafe_allow_html=True)
    
    html_cintas = """
    <div class="cassette-card">
        <h3 style="color: #ff3333; font-size: 24px; margin-bottom: 10px;">[ CINTA A: Lluvia y Neón ]</h3>
        <div class="cassette-body">
            <div class="cassette-label-box">
                <span style="font-family: 'Share Tech Mono'; color: #fff; letter-spacing: 2px;">TDK D60 - VOICES.WAV</span>
            </div>
            
            <div id="reels-A" class="cassette-reels-window">
                <div class="cassette-reel"></div>
                <div class="cassette-reel"></div>
            </div>

            <audio id="audio-A" controls onplay="document.getElementById('reels-A').classList.add('spinning')" onpause="document.getElementById('reels-A').classList.remove('spinning')">
                <source src="https://assets.mixkit.co/active_storage/sfx/2859/2859-preview.mp3" type="audio/mpeg">
                Navegador incompatible.
            </audio>
        </div>
    </div>

    <div class="cassette-card">
        <h3 style="color: #ff3333; font-size: 24px; margin-bottom: 10px;">[ CINTA B: Tema Principal (Distorsionado) ]</h3>
        <div class="cassette-body">
            <div class="cassette-label-box">
                <span style="font-family: 'Share Tech Mono'; color: #fff; letter-spacing: 2px;">MAXELL UR90 - MAIN_THEME.WAV</span>
            </div>
            
            <div id="reels-B" class="cassette-reels-window">
                <div class="cassette-reel"></div>
                <div class="cassette-reel"></div>
            </div>

            <audio id="audio-B" controls onplay="document.getElementById('reels-B').classList.add('spinning')" onpause="document.getElementById('reels-B').classList.remove('spinning')">
                <source src="https://assets.mixkit.co/active_storage/sfx/2864/2864-preview.mp3" type="audio/mpeg">
                Navegador incompatible.
            </audio>
        </div>
    </div>
    """
    st.components.v1.html(html_cintas, height=650)

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
