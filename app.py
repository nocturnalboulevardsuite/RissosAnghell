import streamlit as st

st.set_page_config(page_title="Anghell Collection | Rissos", layout="wide", initial_sidebar_state="expanded")

# --- CSS: ESTÉTICA VHS, THE LOST BOYS, FEARS TO FATHOM ---
css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&family=Cormorant+Garamond:ital,wght@0,400;0,700;1,400&display=swap');

/* Fondo base hiper-oscuro */
.stApp {
    background-color: #050000;
    color: #bfaea6;
    font-family: 'Special Elite', monospace;
}

/* OVERLAY VHS / GRANULADO (Ruido estático y scanlines CRT) */
.stApp::after {
    content: " ";
    display: block;
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), 
                linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
    z-index: 9999;
    background-size: 100% 2px, 3px 100%;
    pointer-events: none;
}

/* Animación de Parpadeo CRT (Flicker) */
@keyframes flicker {
    0% { opacity: 0.95; }
    5% { opacity: 0.85; }
    10% { opacity: 0.95; }
    15% { opacity: 1; }
    50% { opacity: 0.95; }
    100% { opacity: 1; }
}
.stApp {
    animation: flicker 0.15s infinite;
}

/* Tipografía de Títulos (Rojo Sangre Profundo) */
h1, h2, h3 {
    font-family: 'Cormorant Garamond', serif;
    color: #7a0000 !important;
    text-transform: uppercase;
    letter-spacing: 2px;
    border-bottom: 1px solid #330000;
    padding-bottom: 10px;
    margin-bottom: 20px;
    text-shadow: 2px 2px 5px rgba(10, 0, 0, 0.8);
}

/* Estilo del Sidebar */
[data-testid="stSidebar"] {
    background-color: #020000 !important;
    border-right: 2px solid #220000;
}
[data-testid="stSidebar"] * {
    font-family: 'Special Elite', monospace;
    color: #8c7a70 !important;
}

/* Ocultar UI nativa de Streamlit */
header, footer {visibility: hidden;}

/* Pestañas (Subcategorías) */
.stTabs [data-baseweb="tab-list"] {
    background-color: transparent;
    border-bottom: 1px solid #330000;
}
.stTabs [data-baseweb="tab"] {
    color: #bfaea6;
    font-family: 'Special Elite', monospace;
    background-color: transparent;
    border: none;
    letter-spacing: 1px;
}
.stTabs [aria-selected="true"] {
    background-color: #110000 !important;
    color: #990000 !important;
    border-bottom: 2px solid #990000 !important;
}

/* Efecto de Texto Resaltado / Sangriento */
.blood-text {
    color: #8a0303;
    font-weight: bold;
    text-shadow: 0 0 8px rgba(138, 3, 3, 0.4);
}

/* Cajas de contenido */
.content-box {
    background-color: rgba(10, 0, 0, 0.6);
    border-left: 3px solid #550000;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: inset 0 0 20px rgba(0,0,0,0.8);
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# --- NAVEGACIÓN LATERAL ---
st.sidebar.markdown("<h2 style='text-align: center; border: none; font-size: 1.2rem;'>ANGHELL COLLECTION</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<div style='text-align: center; color: #550000;'>-------------------</div>", unsafe_allow_html=True)

opciones = [
    "[ REC. 1 ] LA ESENCIA", 
    "[ REC. 2 ] RELATOS", 
    "[ REC. 3 ] FRECUENCIAS", 
    "[ REC. 4 ] RECOMENDACIONES",
    "[ REC. 5 ] EL ABISMO"
]
pagina = st.sidebar.radio("CINTAS DISPONIBLES", opciones, label_visibility="collapsed")
st.sidebar.markdown("<div style='text-align: center; color: #550000;'>-------------------</div>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; font-size: 12px; opacity: 0.5;'>VGA_IN / 1999</p>", unsafe_allow_html=True)

# --- RUTEO DE PÁGINAS ---

if pagina == "[ REC. 1 ] LA ESENCIA":
    st.markdown("<h1>El Rincón de Rissos</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='border: none; color: #550000 !important; font-style: italic;'>'Anghell Collection'</h3>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="content-box" style="font-size: 18px; line-height: 1.8;">
    Este es un blog personal. Un espacio analógico en una red muerta.
    <br><br>
    Lo creé porque hay cosas que simplemente <span class="blood-text">no sé dónde colocar ni cómo catalogar</span>. 
    Historias viscerales que he escrito en la madrugada, pistas de audio corrompidas que he compuesto, 
    recomendaciones de películas, series y animes que me han marcado, y recuerdos fragmentados que no quiero 
    perder en el fondo de un disco duro.
    <br><br>
    No hay un orden lógico aquí, solo esencia pura. Navega por las cintas si quieres ver lo que hay dentro de mi cabeza.
    </div>
    """, unsafe_allow_html=True)

elif pagina == "[ REC. 2 ] RELATOS":
    st.markdown("<h1>Archivo de Textos</h1>", unsafe_allow_html=True)
    st.write("Cosas que he escrito. Ficciones o realidades, tú decides.")
    
    tab1, tab2 = st.tabs(["CINTA A: Horror Core", "CINTA B: Reflexiones"])
    
    with tab1:
        st.write("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="content-box">
        <h3 style='font-size: 20px; border:none;'>El Perro de la Estación</h3>
        Eran las 3:15 AM en Puente Alto. La niebla era tan espesa que las luces de la calle parecían manchas de acuarela sucia. 
        Vi un perro al otro lado de la calle. Al menos, la silueta era de un perro. Pero cuando se dio la vuelta, 
        su rostro era completamente plano. Sin ojos, sin hocico. Solo piel tensa. 
        <br><br>
        <i>[Continuará...]</i>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.write("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="content-box">
        <h3 style='font-size: 20px; border:none;'>Vampiros de Asfalto</h3>
        A veces siento que la ciudad entera te drena. No con colmillos, sino con horarios de oficina, 
        ruido de motores y luces de neón parpadeantes.
        </div>
        """, unsafe_allow_html=True)

elif pagina == "[ REC. 3 ] FRECUENCIAS":
    st.markdown("<h1>Frecuencias de Audio</h1>", unsafe_allow_html=True)
    st.write("Música que he creado. Escucha bajo tu propio riesgo.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="content-box">
        <h3 style='font-size: 18px; border:none;'>Pistas Maestras (.WAV)</h3>
        Exportaciones crudas desde el estudio. 
        <br><br>
        <span style="color:#550000;">[ Insertar archivos de audio aquí ]</span>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="content-box" style="padding: 0;">
        <iframe style="border-radius:0; border: none; filter: sepia(0.8) hue-rotate(320deg) brightness(0.7) contrast(1.5);" 
        src="https://open.spotify.com/embed/playlist/37i9dQZF1DWZtZ8vUCzche?utm_source=generator&theme=0" 
        width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
        </div>
        """, unsafe_allow_html=True)

elif pagina == "[ REC. 4 ] RECOMENDACIONES":
    st.markdown("<h1>Catálogo Visual</h1>", unsafe_allow_html=True)
    st.write("Cine de culto, series perturbadoras y animación que merece no ser olvidada.")
    
    st.markdown("""
    <div class="content-box">
    <h3 style='border: none; color: #8a0303;'>Cine: The Lost Boys (1987)</h3>
    La estética definitiva. Vampiros en motocicleta, cuero, sangre y una banda sonora impecable. 
    Define exactamente la vibra que busco transmitir en las noches de verano.
    <br><br><hr style='border-color: #330000;'>
    <h3 style='border: none; color: #8a0303;'>Juegos: Fears to Fathom</h3>
    El terror psicológico episódico llevado al estilo VHS de los 90. Jugarlo es sentirte 
    inseguro en tu propia casa. Exactamente el tono de este blog.
    <br><br><hr style='border-color: #330000;'>
    <h3 style='border: none; color: #8a0303;'>Anime: Serial Experiments Lain</h3>
    La red lo sabe todo. La disociación hecha animación de 1998.
    </div>
    """, unsafe_allow_html=True)

elif pagina == "[ REC. 5 ] EL ABISMO":
    st.markdown("<h1>El Abismo</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="content-box" style="border-left: 3px solid #000000; text-align: center;">
    <br><br>
    <h2 style='border: none; text-shadow: none; color: #330000 !important;'>MEMORIAS NO CATALOGADAS</h2>
    <br>
    Hay pedazos de memoria que no son historias, ni recomendaciones, ni música. 
    Son solo sensaciones. Un olor a lluvia en concreto seco. El ruido blanco de una TV antigua.
    <br><br>
    Aquí irán a parar cuando sienta que el tiempo intenta borrarlas.
    <br><br><br>
    </div>
    """, unsafe_allow_html=True)
