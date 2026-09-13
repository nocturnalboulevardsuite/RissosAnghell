import streamlit as st

# Configuración de página rompiendo el estándar
st.set_page_config(page_title="ANGHELL COLLECTION", layout="wide", initial_sidebar_state="expanded")

# --- CSS: CINEMÁTICO 80s, SCARFACE, THE LOST BOYS, FILM GRAIN PROFESIONAL ---
css = """
<style>
/* Fuentes: Anton (Títulos agresivos estilo Scarface) / Cormorant (Textos estilo Lost Boys) */
@import url('https://fonts.googleapis.com/css2?family=Anton&family=Cormorant+Garamond:ital,wght@0,400;0,700;1,400&display=swap');

/* FONDO ROJO OSCURO PROFUNDO Y TEXTO ROJO CLARO */
.stApp {
    background-color: #120000; /* Rojo casi negro */
    background-image: radial-gradient(circle at center, #240000 0%, #0a0000 100%);
    color: #ff6666; /* Rojo claro / Salmón sangriento para lectura */
    font-family: 'Cormorant Garamond', serif;
    font-size: 20px;
}

/* EFECTO DE CINE PROFESIONAL: Viñeta (Bordes oscuros) + Film Grain Animado */
.stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    box-shadow: inset 0 0 150px rgba(0,0,0,0.95);
    pointer-events: none;
    z-index: 9998;
}

.stApp::after {
    content: "";
    position: fixed;
    top: -50%; left: -50%; width: 200%; height: 200%;
    background-image: url('https://upload.wikimedia.org/wikipedia/commons/7/76/1k_Dissolve_Noise_Texture.png');
    opacity: 0.12; /* Granulado sutil pero presente */
    pointer-events: none;
    z-index: 9999;
    animation: film-grain 1.5s steps(4) infinite;
}

@keyframes film-grain {
    0% { transform: translate(0, 0); }
    10% { transform: translate(-1%, -1%); }
    20% { transform: translate(1%, 1%); }
    30% { transform: translate(-2%, 2%); }
    40% { transform: translate(2%, -2%); }
    50% { transform: translate(-1%, 1%); }
    60% { transform: translate(1%, -1%); }
    70% { transform: translate(2%, 2%); }
    80% { transform: translate(-2%, -2%); }
    90% { transform: translate(1%, 1%); }
    100% { transform: translate(0, 0); }
}

/* TÍTULOS CINEMÁTICOS */
h1, h2, h3 {
    font-family: 'Anton', sans-serif;
    color: #ff1a1a !important; /* Rojo puro e intenso */
    text-transform: uppercase;
    letter-spacing: 4px;
    margin-bottom: 20px;
    text-shadow: 2px 2px 0px #330000, -1px -1px 15px rgba(255, 26, 26, 0.4);
}

/* ESCONDER LA INTERFAZ ABURRIDA DE STREAMLIT */
header, footer { display: none !important; }
div[data-testid="stDecoration"] { display: none !important; }

/* BARRA LATERAL (ESTILO CINTA DE CINE) */
[data-testid="stSidebar"] {
    background-color: #080000 !important;
    border-right: 2px dashed #ff1a1a;
}

/* BOTONES DE NAVEGACIÓN ESTILO GLITCH/PELÍCULA */
div[role="radiogroup"] > label {
    background: transparent !important;
    border: none !important;
    border-bottom: 1px solid #330000 !important;
    padding: 15px 10px !important;
    font-family: 'Anton', sans-serif !important;
    font-size: 22px !important;
    color: #883333 !important;
    letter-spacing: 3px;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    cursor: crosshair;
}
div[role="radiogroup"] > label:hover {
    color: #ff1a1a !important;
    transform: skewX(-10deg) scale(1.05);
    text-shadow: 2px 0px 5px rgba(255, 0, 0, 0.8);
    background: rgba(255, 0, 0, 0.05) !important;
}
div[role="radiogroup"] > label[data-checked="true"] {
    color: #ffffff !important;
    border-bottom: 2px solid #ff1a1a !important;
    text-shadow: 0 0 10px #ff1a1a, 0 0 20px #ff1a1a;
    transform: translateX(10px);
}
div[role="radiogroup"] circle, div[role="radiogroup"] label div:first-child {
    display: none;
}

/* CONTENEDOR FUERA DEL SISTEMA (CORTES DE PELÍCULA) */
.film-cut {
    position: relative;
    padding: 40px;
    background: rgba(15, 0, 0, 0.7);
    border-top: 1px solid #ff1a1a;
    border-bottom: 1px solid #ff1a1a;
    margin: 30px 0;
    box-shadow: 0 15px 30px rgba(0,0,0,0.8);
    transition: transform 0.5s ease;
}
.film-cut:hover {
    transform: scale(1.01);
}
.film-cut::before, .film-cut::after {
    content: "■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■";
    position: absolute;
    left: 0;
    width: 100%;
    color: #330000;
    font-size: 10px;
    letter-spacing: 8px;
    text-align: center;
}
.film-cut::before { top: -15px; }
.film-cut::after { bottom: -15px; }

/* TEXTO CONFIDENCIAL / CENSURADO */
.censored {
    background-color: #ff1a1a;
    color: #ff1a1a;
    transition: 0.2s;
    cursor: help;
}
.censored:hover {
    background-color: transparent;
    color: #ff6666;
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# --- NAVEGACIÓN LATERAL CINEMÁTICA ---
st.sidebar.markdown("<h1 style='text-align: center; font-size: 3rem; margin-bottom: 0;'>ANGHELL</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<h3 style='text-align: center; color: #ff6666 !important; font-family: \"Cormorant Garamond\"; letter-spacing: 5px; font-size: 1.2rem; margin-top: -10px;'>COLLECTION</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<br>", unsafe_allow_html=True)

opciones = [
    "REEL 01: EL MANIFIESTO", 
    "REEL 02: HISTORIAS", 
    "REEL 03: AUDIO", 
    "REEL 04: CATÁLOGO VISUAL",
    "REEL 05: ESTÁTICA"
]
pagina = st.sidebar.radio("NAVEGACIÓN", opciones, label_visibility="collapsed")
st.sidebar.markdown("<br><br><br><div style='text-align: center; font-family: Anton; color: #330000; font-size: 1.5rem;'>REC 🔴</div>", unsafe_allow_html=True)


# --- RUTAS DE CINTA (PÁGINAS) ---

if pagina == "REEL 01: EL MANIFIESTO":
    st.markdown("<div style='text-align: center;'><h1 style='font-size: 5rem;'>EL RINCÓN DE RISSOS</h1></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="film-cut">
    <h2 style='font-size: 2rem;'>SINOPSIS: ANGHELL_COLLECTION</h2>
    <p style='font-size: 24px; line-height: 1.6; color: #ff8080;'>
    Este es un blog personal. Un carrete de película olvidado en una red sobresaturada.
    <br><br>
    Lo creé porque hay cosas que de verdad <span style="font-family: Anton; font-size: 26px; color: #ff1a1a; letter-spacing: 1px;">NO SÉ DÓNDE COLOCAR, NI CÓMO CATALOGAR.</span> 
    <br><br>
    Historias viscerales que he escrito en las madrugadas. Frecuencias y pistas de audio que he producido pero que se sienten 
    demasiado hostiles para un álbum normal. Recomendaciones de películas de culto, series, animes, y recuerdos 
    fragmentados de la ciudad.
    <br><br>
    Cosas que necesito proyectar para no perder esa esencia, ese momento exacto en el tiempo. <br>
    No hay un orden lógico. <span class="censored">Solo lo que sobrevive al corte final.</span>
    </p>
    </div>
    """, unsafe_allow_html=True)

elif pagina == "REEL 02: HISTORIAS":
    st.markdown("<h1>[ ARCHIVOS DE GUION ]</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="film-cut">
    <h3>TOMA 1: EL PERRO SIN ROSTRO</h3>
    <p style='font-size: 22px;'>
    <strong>EXT. PUENTE ALTO - NOCHE (3:15 AM)</strong><br><br>
    La niebla es espesa. Las luces de la calle parpadean. <br>
    Una silueta canina busca en la basura. Haces un sonido para llamarlo.<br><br>
    El animal se gira. El área donde debería estar su rostro es plana. Como piel tensada sobre un cráneo liso. 
    No tiene ojos, pero la atmósfera pesa. Sabes que te está mirando.
    </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="film-cut">
    <h3>TOMA 2: VAMPIRISMO DE ASFALTO</h3>
    <p style='font-size: 22px;'>
    La ciudad drena. No usa colmillos, usa horarios y concreto. <br>
    A las 4 AM, los paraderos de micro están vacíos, pero si te quedas mirando fijo a las esquinas, 
    las sombras tienen una densidad distinta. Pesada. Viva.
    </p>
    </div>
    """, unsafe_allow_html=True)

elif pagina == "REEL 03: AUDIO":
    st.markdown("<h1>[ BANDA SONORA ORIGINAL ]</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="film-cut" style="padding: 20px;">
        <h3>PISTAS .WAV</h3>
        <p>Sonido crudo. Mezclas que nunca pasaron por un proceso de masterización limpio. 
        Puro ruido y bajo.</p>
        <div style="width: 100%; height: 50px; border: 1px solid #ff1a1a; display: flex; align-items: center; justify-content: center; font-family: Anton; color: #ff1a1a;">
        PLAY ▶
        </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="film-cut" style="padding: 20px;">
        <h3>PLAYLIST EXTERNA</h3>
        <iframe style="border-radius:0; border: none; filter: sepia(100%) hue-rotate(320deg) saturate(200%) contrast(150%);" 
        src="https://open.spotify.com/embed/playlist/37i9dQZF1DWZtZ8vUCzche?utm_source=generator&theme=0" 
        width="100%" height="250" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
        </div>
        """, unsafe_allow_html=True)

elif pagina == "REEL 04: CATÁLOGO VISUAL":
    st.markdown("<h1>[ REFERENCIAS VISUALES ]</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="film-cut">
    <h3 style="font-size: 2rem;">THE LOST BOYS (1987)</h3>
    <p style='font-size: 22px;'>
    Vampiros en motocicleta, chaquetas de cuero y playas californianas en la noche. 
    La mezcla perfecta entre terror y rebeldía. Esta es la paleta de colores de mi mente.
    </p>
    </div>
    
    <div class="film-cut">
    <h3 style="font-size: 2rem;">SCARFACE (1983)</h3>
    <p style='font-size: 22px;'>
    El neón rojo, los excesos y la tragedia operística. La agresividad visual de los títulos 
    y la música de sintetizador que te mantiene tenso.
    </p>
    </div>
    """, unsafe_allow_html=True)

elif pagina == "REEL 05: ESTÁTICA":
    st.markdown("<h1 style='text-align: center; font-size: 6rem; opacity: 0.3;'>ESTÁTICA</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-top: 100px;">
    <p style="font-size: 30px; color: #ff1a1a; font-family: Anton;">
    IMÁGENES RESIDUALES. <br>
    PENSAMIENTOS INTRUSIVOS.<br>
    ESCENAS ELIMINADAS.
    </p>
    <p style="font-size: 20px; color: #ff6666;">
    Vuelve más tarde. El carrete se está revelando.
    </p>
    </div>
    """, unsafe_allow_html=True)
