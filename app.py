import streamlit as st

st.set_page_config(page_title="BASE DE DATOS_anomala", page_icon="👁️", layout="wide")

# --- CSS: SCP + WEIRDCORE ---
css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Courier+Prime:ital,wght@0,400;0,700;1,400&family=Silkscreen&display=swap');

/* Efecto Monitor CRT y Scanlines */
.stApp {
    background-color: #050505;
    background-image: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
    background-size: 100% 2px, 3px 100%;
    color: #e0e0e0;
    font-family: 'Courier Prime', monospace;
}

/* Ocultar elementos por defecto */
header {visibility: hidden;}
footer {visibility: hidden;}

/* Barra Lateral (Terminal Segura) */
[data-testid="stSidebar"] {
    background-color: #000000 !important;
    border-right: 2px solid #555555;
    box-shadow: inset -5px 0 15px rgba(255,255,255,0.05);
}
[data-testid="stSidebar"] * {
    color: #a0a0a0 !important;
    font-family: 'Courier Prime', monospace;
}

/* Títulos Clínicos SCP pero que glitchean a Weirdcore */
h1, h2, h3 {
    font-family: 'Silkscreen', cursive;
    text-transform: uppercase;
    color: #ffffff !important;
    border-bottom: 2px solid #ffffff;
    padding-bottom: 5px;
    letter-spacing: 2px;
}
h1:hover {
    animation: weirdGlitch 0.3s infinite;
    color: #ff00ff !important; /* Toque weirdcore magenta */
}

@keyframes weirdGlitch {
    0% { transform: translate(0) skew(0deg); text-shadow: 2px 0 blue, -2px 0 red; }
    20% { transform: translate(-2px, 2px) skew(5deg); text-shadow: -2px 0 blue, 2px 0 red; }
    40% { transform: translate(-2px, -2px) skew(-5deg); text-shadow: 2px 0 blue, -2px 0 red; }
    60% { transform: translate(2px, 2px) skew(5deg); text-shadow: -2px 0 blue, 2px 0 red; }
    80% { transform: translate(2px, -2px) skew(-5deg); text-shadow: 2px 0 blue, -2px 0 red; }
    100% { transform: translate(0) skew(0deg); text-shadow: none; }
}

/* Efecto de texto censurado (REDACTED) */
.redacted {
    background-color: #e0e0e0;
    color: #e0e0e0;
    padding: 0 4px;
    cursor: crosshair;
    transition: 0.2s;
}
.redacted:active {
    background-color: transparent;
    color: #ff0000;
}

/* Estilo de Pestañas (Archivos de Sistema Antiguo) */
.stTabs [data-baseweb="tab-list"] {
    background-color: #000000;
    border-bottom: 2px solid #555555;
}
.stTabs [data-baseweb="tab"] {
    color: #888888;
    background-color: #111111;
    border: 1px solid #333333;
    font-family: 'Silkscreen', cursive;
}
.stTabs [aria-selected="true"] {
    background-color: #ffffff !important;
    color: #000000 !important;
}

/* Contenedores de texto (Documentos SCP) */
.stMarkdown {
    background-color: rgba(255, 255, 255, 0.02);
    padding: 15px;
    border-left: 4px solid #ffffff;
}

/* Elemento Weirdcore Flotante (Un ojo que te sigue lentamente) */
.floating-eye {
    position: fixed;
    font-size: 60px;
    opacity: 0.3;
    z-index: 9999;
    pointer-events: none;
    animation: drift 20s infinite alternate linear;
}
@keyframes drift {
    0% { top: 10%; left: 5%; transform: scale(1); filter: hue-rotate(0deg); }
    50% { top: 80%; left: 80%; transform: scale(1.5); filter: hue-rotate(90deg); }
    100% { top: 40%; left: 90%; transform: scale(0.8); filter: hue-rotate(180deg); }
}
</style>
<div class="floating-eye">👁️</div>
"""
st.markdown(css, unsafe_allow_html=True)

# --- SISTEMA DE NAVEGACIÓN (TERMINAL) ---
st.sidebar.markdown("## SISTEMA O.S. SECURE")
st.sidebar.markdown("---")
st.sidebar.write("**USUARIO:** <span class='redacted'>███████</span>", unsafe_allow_html=True)
st.sidebar.write("**NIVEL DE ACCESO:** 4 (CLASIFICADO)")
st.sidebar.markdown("---")

pagina = st.sidebar.radio(
    "ACCEDER A DIRECTORIO:",
    ["[1] PROTOCOLO_INICIAL.exe", "[2] REGISTROS_ANOMALOS", "[3] ARCHIVOS_MEMETICOS.wav", "[4] ENTIDAD_AUTORA"]
)

st.sidebar.markdown("---")
st.sidebar.write("¿estás seguro de que estás solo en tu habitación?")

# --- RUTEO DE PÁGINAS ---

if pagina == "[1] PROTOCOLO_INICIAL.exe":
    st.title("ÍTEM #: R-666 (EL RINCÓN)")
    st.write("**CLASE DE OBJETO:** EUCLID / ESPACIO LIMINAL")
    
    st.write("""
    **Procedimientos Especiales de Contención:**
    El acceso a esta base de datos debe ser monitoreado. Los sujetos expuestos a los textos o frecuencias de *El Rincón del Rissos* suelen reportar sensación de paranoia, distorsión temporal y la visión de <span class="redacted">ojos en las paredes</span>.
    
    **Descripción:**
    Estás interactuando con una anomalía digital. Este no es un blog normal. Es un espacio que se reescribe a sí mismo. Haz clic sobre los textos en bloque blanco para revelar información clasificada. (MANTÉN PRESIONADO EL CLICK).
    
    *Nostalgia... es solo un error en tu cerebro.*
    """)
    
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/ec/SMPTE_Color_Bars.svg", caption="SEÑAL PERDIDA", width=400)

elif pagina == "[2] REGISTROS_ANOMALOS":
    st.title("REGISTROS DE INCIDENTES")
    st.write("ADVERTENCIA: RIESGO DE CORRUPCIÓN COGNITIVA.")
    
    tab1, tab2, tab3 = st.tabs(["LOG_01", "LOG_02", "LOG_03 (CORRUPTO)"])
    
    with tab1:
        st.subheader("INCIDENTE: El Reflejo")
        st.write("FECHA: 13/09/2026 | UBICACIÓN: <span class='redacted'>Puente Alto</span>", unsafe_allow_html=True)
        st.write("""
        Todo empezó cuando noté que mi reflejo en el espejo del baño parpadeaba un segundo después que yo. 
        Al principio pensé que era el cansancio... pero luego el reflejo me sonrió, aunque yo estaba serio.
        *(Inserta aquí tu historia...)*
        """)
        
    with tab2:
        st.subheader("INCIDENTE: La Escalera Infinita")
        st.write("El sujeto reportó bajar las escaleras de su edificio durante 4 horas. Nunca llegó al primer piso. Afirma que el olor a ozono se hacía más fuerte en cada nivel.")

    with tab3:
        st.subheader("e r r o r r r r r r r")
        st.markdown("<h2 style='color:#ff00ff; text-transform:lowercase;'>¿te acuerdas de este lugar? tú estuviste aquí antes.</h2>", unsafe_allow_html=True)
        st.write("no despiertes no despiertes no despiertes no despiertes")

elif pagina == "[3] ARCHIVOS_MEMETICOS.wav":
    st.title("PELIGROS AUDITIVOS")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("EXTRACCIONES LOCALES")
        st.write("Archivos recuperados de los discos duros de la Entidad Rissos.")
        st.write("⚠️ *Advertencia: Riesgo de parálisis del sueño.*")
        
        # st.audio("frecuencia_anomala.wav", format="audio/wav")
        # st.audio("ruido_blanco_voces.wav", format="audio/wav")
        st.info("Directorio vacío. Sube los archivos .wav al servidor y descomenta el código.")

    with col2:
        st.subheader("TRANSMISIÓN EXTERNA (SPOTIFY)")
        st.write("Señales interceptadas de la red de streaming.")
        
        spotify_embed = """
        <iframe style="border-radius:0px; border: 2px solid white;" src="https://open.spotify.com/embed/playlist/37i9dQZF1DWZtZ8vUCzche?utm_source=generator&theme=0" width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
        """
        import streamlit.components.v1 as components
        components.html(spotify_embed, height=400)

elif pagina == "[4] ENTIDAD_AUTORA":
    st.title("ENTIDAD: R I S S O S")
    
    st.write("""
    **ALIAS:** Rissos  
    **CLASIFICACIÓN:** Creador / Vector de Anomalías  
    **ESTADO:** <span class="redacted">MONITOREADO</span>
    
    **Notas del Investigador:**
    El sujeto se dedica a crear contenido "Horror Core" y música electrónica/oscura. Su nivel de influencia sobre la red está creciendo. Ha creado esta interfaz para recopilar sus creaciones bajo la apariencia de un simple portafolio web.
    
    *No le mires directamente a los ojos si llegas a encontrarlo en Puente Alto.*
    """, unsafe_allow_html=True)
