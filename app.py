import streamlit as st

# Configuración inicial de la página
st.set_page_config(page_title="Rissos | Colección", layout="wide", initial_sidebar_state="expanded")

# --- VARIABLES DE ESTADO ---
if 'muestra_analizada' not in st.session_state:
    st.session_state.muestra_analizada = False

def analizar_muestra():
    st.session_state.muestra_analizada = True

def limpiar_muestra():
    st.session_state.muestra_analizada = False

# --- CSS ELEGANTE (ESTILO AMERICAN PSYCHO / ALTA COSTURA OSCURA) ---
css = """
<style>
/* Importar fuentes elegantes */
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300&display=swap');

/* Fondo base y color de texto (Negro Carbón y Blanco Hueso) */
.stApp {
    background-color: #030101;
    color: #d9d0c7;
    font-family: 'Cormorant Garamond', serif;
    font-size: 20px;
}

/* Ocultar elementos por defecto de Streamlit */
header, footer {visibility: hidden;}

/* Barra lateral elegante */
[data-testid="stSidebar"] {
    background-color: #080202 !important;
    border-right: 1px solid #2a0505;
}
[data-testid="stSidebar"] * {
    font-family: 'Cinzel', serif;
    color: #a3958d !important;
}

/* Títulos y Subtítulos (Rojo Sangre Profundo) */
h1, h2, h3 {
    font-family: 'Cinzel', serif;
    color: #8a0303 !important;
    text-transform: uppercase;
    letter-spacing: 3px;
    font-weight: 400;
    border-bottom: 1px solid #2a0505;
    padding-bottom: 10px;
    margin-bottom: 20px;
}

/* Efecto de pulso muy sutil para el título principal */
.titulo-pulso {
    animation: pulso-sangre 4s infinite alternate ease-in-out;
}
@keyframes pulso-sangre {
    0% { text-shadow: 0 0 5px rgba(138, 3, 3, 0.1); }
    100% { text-shadow: 0 0 20px rgba(138, 3, 3, 0.6); }
}

/* Pestañas (Tabs) Minimalistas */
.stTabs [data-baseweb="tab-list"] {
    background-color: transparent;
    border-bottom: 1px solid #2a0505;
}
.stTabs [data-baseweb="tab"] {
    color: #d9d0c7;
    font-family: 'Cinzel', serif;
    background-color: transparent;
    border: none;
    letter-spacing: 1px;
}
.stTabs [aria-selected="true"] {
    background-color: #0a0202 !important;
    color: #8a0303 !important;
    border-bottom: 2px solid #8a0303 !important;
}

/* Botones con clase */
div.stButton > button {
    background-color: transparent;
    color: #8a0303;
    border: 1px solid #4a0909;
    font-family: 'Cinzel', serif;
    font-size: 16px;
    letter-spacing: 2px;
    padding: 10px 30px;
    transition: all 0.4s ease;
}
div.stButton > button:hover {
    background-color: #8a0303;
    color: #030101;
    border: 1px solid #8a0303;
    box-shadow: 0 0 15px rgba(138, 3, 3, 0.4);
}

/* Separadores elegantes */
hr {
    border: 0;
    height: 1px;
    background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(138, 3, 3, 0.75), rgba(0, 0, 0, 0));
}

/* Efecto CSS Complejo para la sección "Sobre mí" */
.revelacion-sangre {
    background: radial-gradient(circle at center, #1c0202 0%, #030101 100%);
    border-left: 2px solid #8a0303;
    padding: 30px;
    animation: fade-in 2s ease-in;
    color: #d9d0c7;
}
@keyframes fade-in {
    from { opacity: 0; filter: blur(10px); }
    to { opacity: 1; filter: blur(0); }
}

.firma {
    font-family: 'Cinzel', serif;
    color: #4a0909;
    font-style: italic;
    text-align: right;
    margin-top: 20px;
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# --- NAVEGACIÓN LATERAL ---
st.sidebar.markdown("<h2 style='text-align: center; border: none; font-size: 1.5rem;'>RISSOS</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<hr>", unsafe_allow_html=True)

opciones = [
    "I. EL MANIFIESTO", 
    "II. ARCHIVOS CLÍNICOS", 
    "III. AUDIOLOGÍA", 
    "IV. EL AUTOR"
]
pagina = st.sidebar.radio("ÍNDICE", opciones, label_visibility="collapsed")
st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; font-size: 14px;'>SANTIAGO, CHILE.</p>", unsafe_allow_html=True)


# --- CONTENIDO DE LAS PÁGINAS ---

if pagina == "I. EL MANIFIESTO":
    st.markdown("<h1 class='titulo-pulso'>El Manifiesto</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        st.write("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: justify; font-size: 24px; line-height: 1.8;'>
        "Tengo todas las características de un ser humano: carne, sangre, piel y cabello; 
        pero ninguna emoción clara o identificable, excepto la curiosidad y el asco."
        <br><br>
        Lo que estás a punto de presenciar no es un portafolio. Es una disección. 
        Un espacio diseñado para catalogar historias que no deberían ser contadas y frecuencias que 
        alteran el ritmo cardíaco. La estética es meticulosa; el contenido, visceral.
        <br><br>
        Te sugiero que prestes atención a los detalles. La elegancia a menudo esconde las peores intenciones.
        </div>
        """, unsafe_allow_html=True)

elif pagina == "II. ARCHIVOS CLÍNICOS":
    st.markdown("<h1>Archivos Clínicos</h1>", unsafe_allow_html=True)
    st.write("Seleccione un expediente para su revisión.")
    
    tab1, tab2, tab3 = st.tabs(["[ EXPEDIENTE 01 ]", "[ EXPEDIENTE 02 ]", "[ CASO CERRADO ]"])
    
    with tab1:
        st.write("<br>", unsafe_allow_html=True)
        st.markdown("<h3>El Reflejo Incorrecto</h3>", unsafe_allow_html=True)
        st.markdown("""
        **Sujeto:** Masculino, 24 años.  
        **Diagnóstico Preliminar:** Delirio de Capgras aplicado al propio reflejo.
        
        *Transcripción:*  
        "La primera vez que ocurrió, me estaba lavando las manos. Levanté la vista hacia el espejo y, 
        por una fracción de segundo, mi reflejo siguió mirando hacia abajo. Parpadeé y todo volvió a la normalidad. 
        Pero anoche... anoche yo estaba llorando, y mi reflejo me devolvió una sonrisa impecable."
        """)
        
    with tab2:
        st.write("<br>", unsafe_allow_html=True)
        st.markdown("<h3>La Habitación 402</h3>", unsafe_allow_html=True)
        st.markdown("""
        No hay registros de construcción para la habitación 402 en el plano original del edificio. 
        Sin embargo, los inquilinos del cuarto piso se quejan de un olor a cobre antiguo y del sonido 
        metódico de algo goteando sobre madera fina.
        """)

    with tab3:
        st.write("<br>", unsafe_allow_html=True)
        st.markdown("<h3>[ CENSURADO ]</h3>", unsafe_allow_html=True)
        st.write("Este documento ha sido sellado por bioseguridad. La exposición prolongada a sus descripciones induce paranoia severa.")

elif pagina == "III. AUDIOLOGÍA":
    st.markdown("<h1>Audiología</h1>", unsafe_allow_html=True)
    st.write("Frecuencias curadas y compuestas para la inducción de estados alterados.")
    
    col1, col_space, col2 = st.columns([4, 1, 4])
    
    with col1:
        st.markdown("<h3>Producción Original (.wav)</h3>", unsafe_allow_html=True)
        st.write("Sonido crudo. Mezclado en aislamiento.")
        # st.audio("tu_cancion.wav")
        st.markdown("<p style='color: #4a0909; font-style: italic;'>[ Esperando inyección de archivos locales... ]</p>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<h3>Curaduría Externa (Spotify)</h3>", unsafe_allow_html=True)
        spotify_embed = """
        <div style="border: 1px solid #2a0505; padding: 5px; background: #050101;">
            <iframe src="https://open.spotify.com/embed/playlist/37i9dQZF1DWZtZ8vUCzche?utm_source=generator&theme=0" width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
        </div>
        """
        import streamlit.components.v1 as components
        components.html(spotify_embed, height=400)

elif pagina == "IV. EL AUTOR":
    st.markdown("<h1>El Autor</h1>", unsafe_allow_html=True)
    
    if not st.session_state.muestra_analizada:
        st.write("La información personal requiere un análisis de identidad.")
        st.write("<br><br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("PROCEDER CON LA EXTRACCIÓN", use_container_width=True):
                analizar_muestra()
                st.rerun()
    else:
        st.markdown("""
        <div class="revelacion-sangre">
            <h2 style="border: none; margin-bottom: 0;">RISSOS</h2>
            <p style="font-family: 'Cinzel', serif; color: #8a0303; letter-spacing: 1px;">DISEÑADOR / ESCRITOR / PRODUCTOR</p>
            <hr>
            <p style="font-size: 22px; line-height: 1.6; text-align: justify;">
                Resido en Puente Alto, aunque mi mente habita en arquitecturas mucho más sombrías. 
                Me especializo en la intersección entre el terror psicológico profundo y la elegancia minimalista. 
                No busco asustar mediante el caos, sino incomodar mediante la perfección estéril y clínica.
                <br><br>
                Cada texto, cada línea de código y cada nota musical en este espacio ha sido medida con la misma 
                precisión con la que un sastre toma medidas para un traje fúnebre.
            </p>
            <div class="firma">- Rissos.</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("<br>", unsafe_allow_html=True)
        if st.button("LIMPIAR MUESTRA (CERRAR)", use_container_width=False):
            limpiar_muestra()
            st.rerun()
