import streamlit as st
import time

# Configuración inicial de la página
st.set_page_config(page_title="SYS.ERR // DIRECTORIO_ROJO", page_icon="🩸", layout="wide")

# --- INICIALIZACIÓN DE VARIABLES SECRETAS (DINÁMICAS) ---
if 'corazon_explotado' not in st.session_state:
    st.session_state.corazon_explotado = False
if 'zona_secreta' not in st.session_state:
    st.session_state.zona_secreta = False
if 'glitch_activo' not in st.session_state:
    st.session_state.glitch_activo = False

# Función para desbloquear zona secreta
def desbloquear_secreto():
    st.session_state.zona_secreta = True

# Función para hacer explotar el corazón
def explotar_corazon():
    st.session_state.corazon_explotado = True

# --- CSS: RED SCP + WEIRDCORE + WINDOWS ANTIGUO ---
css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=VT323&family=Courier+Prime:ital,wght@0,400;0,700;1,400&display=swap');

/* Fondo General: Oscuro, sangriento, scanlines */
.stApp {
    background-color: #080000;
    background-image: 
        repeating-linear-gradient(0deg, rgba(255, 0, 0, 0.03) 0px, rgba(255, 0, 0, 0.03) 1px, transparent 1px, transparent 2px),
        radial-gradient(circle at center, #1a0000 0%, #000000 100%);
    color: #ff3333;
    font-family: 'Courier Prime', monospace;
}

/* Ocultar elementos de Streamlit */
header, footer {visibility: hidden;}

/* Estilo Windows 95 / SCP Terminal */
.win95-box {
    background-color: #0a0000;
    border: 3px solid;
    border-color: #ff6666 #330000 #330000 #ff6666;
    padding: 15px;
    margin-bottom: 15px;
    box-shadow: 4px 4px 0px #220000;
}

/* Títulos con efecto Creepypasta */
h1, h2, h3 {
    font-family: 'VT323', monospace;
    color: #ff0000 !important;
    text-transform: uppercase;
    text-shadow: 2px 2px 0px #330000, -1px -1px 0px #ffaaaa;
    border-bottom: 2px dashed #660000;
}

/* Animación del Corazón Latiendo */
@keyframes latido {
    0% { transform: scale(1); }
    15% { transform: scale(1.3); text-shadow: 0 0 20px red; }
    30% { transform: scale(1); }
    45% { transform: scale(1.3); text-shadow: 0 0 20px red; }
    60% { transform: scale(1); }
}
.corazon {
    font-size: 100px;
    text-align: center;
    animation: latido 1.2s infinite;
    cursor: pointer;
}

/* Efecto de explosión de sangre */
.sangre-explosion {
    background-image: url('https://media.giphy.com/media/3o7aD2e1EoW6yXqV9K/giphy.gif'); /* GIF de estática/sangre roja */
    background-size: cover;
    background-position: center;
    background-blend-mode: multiply;
    background-color: #550000;
    color: white !important;
    padding: 30px;
    border: 5px solid red;
    box-shadow: inset 0 0 50px black;
    animation: shake 0.5s;
}

@keyframes shake {
    0% { transform: translate(1px, 1px) rotate(0deg); }
    10% { transform: translate(-1px, -2px) rotate(-1deg); }
    20% { transform: translate(-3px, 0px) rotate(1deg); }
    30% { transform: translate(3px, 2px) rotate(0deg); }
    100% { transform: translate(0px, 0px) rotate(0deg); }
}

/* Pestañas (Sub-blogs) estilo carpetas corrompidas */
.stTabs [data-baseweb="tab-list"] {
    background-color: #110000;
    border-bottom: 2px solid #ff0000;
}
.stTabs [data-baseweb="tab"] {
    color: #aa0000;
    font-family: 'VT323', monospace;
    font-size: 20px;
    background-color: #050000;
    border: 1px solid #330000;
}
.stTabs [aria-selected="true"] {
    background-color: #aa0000 !important;
    color: #000000 !important;
    box-shadow: inset 2px 2px 0px #ffcccc;
}

/* Botones genéricos de la terminal */
div.stButton > button {
    background-color: #1a0000;
    color: #ff3333;
    border: 2px solid #ff0000;
    font-family: 'VT323', monospace;
    font-size: 20px;
    border-radius: 0;
    transition: 0.1s;
}
div.stButton > button:hover {
    background-color: #ff0000;
    color: #000000;
    border: 2px solid #ffffff;
}

/* Botón Ojo (Invisible/Weirdcore) */
.ojo-secreto {
    position: fixed;
    bottom: 10px;
    right: 10px;
    opacity: 0.1;
    transition: 0.3s;
}
.ojo-secreto:hover {
    opacity: 1;
    filter: drop-shadow(0 0 10px red);
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# --- BARRA LATERAL (DIRECTORIO WINDOWS 95) ---
st.sidebar.markdown("<div class='win95-box'>", unsafe_allow_html=True)
st.sidebar.markdown("## C:\\RISSOS_SYS>")
st.sidebar.markdown("---")

opciones_menu = ["[01] INICIO.exe", "[02] ARCHIVOS_SCP", "[03] FRECUENCIAS.wav", "[04] SOBRE_MI.dll"]
if st.session_state.zona_secreta:
    opciones_menu.append("[??] EL_ABISMO.sys")

pagina = st.sidebar.radio("SELECCIONAR RUTA:", opciones_menu)
st.sidebar.markdown("---")
st.sidebar.write("ESTADO: AISLADO")

# El ojo secreto camuflado en la barra lateral
col_vacia, col_ojo = st.sidebar.columns([4, 1])
with col_ojo:
    if st.button("👁️", key="btn_ojo", help="No lo mires"):
        desbloquear_secreto()
        st.rerun()

st.sidebar.markdown("</div>", unsafe_allow_html=True)

# --- RUTEO DE PÁGINAS ---

if pagina == "[01] INICIO.exe":
    st.markdown("<div class='win95-box'>", unsafe_allow_html=True)
    st.title("BIENVENIDO AL RINCÓN")
    st.write("Has accedido a un servidor no indexado. La estética que ves no es una elección de diseño, es la degradación del código por la exposición a [DATOS BORRADOS].")
    
    st.markdown("### REGLAS DE NAVEGACIÓN:")
    st.write("- No confíes en los enlaces rotos.")
    st.write("- Si escuchas estática, baja el volumen inmediatamente.")
    st.write("- Hay puertas aquí que no deberían abrirse. *(Pista: Algunas miradas devuelven la mirada)*.")
    
    st.image("https://upload.wikimedia.org/wikipedia/commons/3/30/Red_solid_screen.jpg", caption="████████", width=200)
    st.markdown("</div>", unsafe_allow_html=True)

elif pagina == "[02] ARCHIVOS_SCP":
    st.title("BASE DE DATOS ANÓMALA")
    st.write("Directorio de entidades, objetos liminales y registros recuperados.")
    
    tab1, tab2, tab3 = st.tabs(["[ ÍTEM: R-01 ]", "[ ÍTEM: R-02 ]", "[ EXPEDIENTES PERDIDOS ]"])
    
    with tab1:
        st.markdown("<div class='win95-box'>", unsafe_allow_html=True)
        st.subheader("ÍTEM R-01: El Reflejo Incorrecto")
        st.write("**Clase:** Euclid")
        st.write("**Descripción:** Una entidad memética que se adhiere a los espejos de la comuna de Puente Alto. Se manifiesta parpadeando a destiempo del observador original.")
        st.write("*(Aquí va tu historia principal o creepypasta)*")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<div class='win95-box'>", unsafe_allow_html=True)
        st.subheader("ÍTEM R-02: La Estación Vacía")
        st.write("**Clase:** Safe / Dreamcore")
        st.write("**Descripción:** Un espacio que se asemeja a una estación de metro chilena a las 3:00 AM. Los letreros están escritos en un idioma incomprensible. El olor a ozono es persistente.")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        st.error("ERROR 404: ARCHIVO CORROMPIDO. DEMASIADA SANGRE EN EL DISCO DURO.")

elif pagina == "[03] FRECUENCIAS.wav":
    st.title("AISLAMIENTO ACÚSTICO")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='win95-box'>", unsafe_allow_html=True)
        st.subheader("ARCHIVOS LOCALES (.WAV)")
        st.write("Pistas creadas por la entidad Rissos.")
        # st.audio("tu_cancion.wav")
        st.write("*(Esperando carga de archivos desde el directorio raíz...)*")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='win95-box'>", unsafe_allow_html=True)
        st.subheader("TRANSMISIÓN SPOTIFY")
        spotify_embed = """
        <iframe style="border-radius:0px; border: 1px solid #ff0000; filter: contrast(150%) sepia(100%) hue-rotate(300deg);" src="https://open.spotify.com/embed/playlist/37i9dQZF1DWZtZ8vUCzche?utm_source=generator&theme=0" width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
        """
        import streamlit.components.v1 as components
        components.html(spotify_embed, height=400)
        st.markdown("</div>", unsafe_allow_html=True)

elif pagina == "[04] SOBRE_MI.dll":
    st.title("INFORMACIÓN DEL SISTEMA / AUTOR")
    
    if not st.session_state.corazon_explotado:
        st.write("EXTRAYENDO DATOS ORGÁNICOS...")
        st.markdown("<div class='corazon'>🫀</div>", unsafe_allow_html=True)
        st.write("---")
        
        # Botón gigante debajo del corazón animado
        if st.button("PUNZAR EL TEJIDO (HAZ CLIC AQUÍ)", use_container_width=True):
            explotar_corazon()
            st.rerun()
    else:
        # Estado cuando el corazón ha explotado
        st.markdown("<div class='sangre-explosion'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color: white; text-shadow: 2px 2px black;'>████ DESANGRE COMPLETADO ████</h2>", unsafe_allow_html=True)
        st.write("""
        **ALIAS:** RISSOS  
        **UBICACIÓN:** PUENTE ALTO, RM.  
        **ESTADO:** ASIMILADO POR LA RED.
        
        Soy un productor musical, escritor y recopilador de anomalías web. 
        Este espacio fue diseñado para almacenar el "Horror Core" que brota de mi cabeza.
        Música, textos, y código moribundo. 
        
        *Gracias por donar tu sangre al sistema.*
        """)
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("RECONSTRUIR TEJIDO (VOLVER)", use_container_width=True):
            st.session_state.corazon_explotado = False
            st.rerun()

elif pagina == "[??] EL_ABISMO.sys" and st.session_state.zona_secreta:
    st.markdown("<div style='background-color: red; padding: 50px; text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color: black !important; font-size: 80px; text-shadow: none;'>LO ENCONTRASTE</h1>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.write("""
    Nadie debería estar aquí.  
    Este es el cuarto trasero (Backroom) del Rincón del Rissos.  
    Aquí se archivan los borradores que me dieron tanto miedo que decidí no publicar.
    """)
    st.write("... *Próximamente contenido exclusivo* ...")
    
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Eyes_icon.svg/512px-Eyes_icon.svg.png", width=150)
