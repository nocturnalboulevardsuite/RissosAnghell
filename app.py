import streamlit as st

# 1. CONFIGURACIÓN DE PÁGINA (Debe ser la primera línea)
st.set_page_config(page_title="El Rincón del Rissos", page_icon="👁️", layout="wide")

# 2. CSS PARA ESTÉTICA "HORROR WEB 2005 / USERNAME 666"
css = """
<style>
/* Fondo general sangriento/visceral y fuente clásica de web antigua */
.stApp {
    background-color: #0a0000;
    /* Un patrón CSS oscuro para simular textura si no tienes una imagen de fondo */
    background-image: radial-gradient(#3a0000 1px, transparent 1px), radial-gradient(#3a0000 1px, transparent 1px);
    background-size: 20px 20px;
    background-position: 0 0, 10px 10px;
    color: #cccccc;
    font-family: 'Times New Roman', Times, serif;
}

/* Ocultar el header por defecto de Streamlit para más inmersión */
header {visibility: hidden;}

/* Estilo de la Barra Lateral (Menú de Navegación) */
[data-testid="stSidebar"] {
    background-color: #110000 !important;
    border-right: 4px double #8b0000;
}
[data-testid="stSidebar"] * {
    color: #ffb3b3 !important;
    font-family: 'Courier New', Courier, monospace;
}

/* Títulos estilo web antigua corrompida */
h1, h2, h3 {
    color: #ff0000 !important;
    text-shadow: 2px 2px 4px #000000;
    border-bottom: 1px solid #8b0000;
    padding-bottom: 5px;
    font-family: 'Arial', sans-serif;
    letter-spacing: -1px;
}

/* Estilo de las pestañas (Sub-blogs de historias) */
.stTabs [data-baseweb="tab-list"] {
    background-color: #1a0000;
    border-bottom: 2px solid #550000;
}
.stTabs [data-baseweb="tab"] {
    color: #aa0000;
    border: 1px solid #330000;
    background-color: #050000;
}
.stTabs [aria-selected="true"] {
    background-color: #550000 !important;
    color: #ffffff !important;
}

/* Contenedores de texto / Cajas estilo foro antiguo */
.stMarkdown {
    background-color: rgba(20, 0, 0, 0.7);
    padding: 10px;
    border-left: 3px solid #8b0000;
    margin-bottom: 10px;
}

/* Botones */
div.stButton > button {
    background-color: #330000;
    color: white;
    border: 1px solid #ff0000;
    border-radius: 0px;
}
div.stButton > button:hover {
    background-color: #ff0000;
    color: black;
    border: 1px solid #ffffff;
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# 3. BARRA DE NAVEGACIÓN (SIDEBAR)
st.sidebar.markdown("## 🩸 MENÚ PRINCIPAL")
st.sidebar.markdown("---")
# Usamos un radio button en el sidebar para navegar entre las páginas principales
pagina = st.sidebar.radio(
    "SELECCIONA UN DIRECTORIO:",
    ["[01] ¿Qué es esta página?", "[02] Archivo de Historias", "[03] Frecuencias (Música)", "[04] Sobre mí"]
)
st.sidebar.markdown("---")
st.sidebar.write("Visitante N°: 00666")

# 4. RUTEO DE PÁGINAS

# PÁGINA 1: ¿QUÉ ES ESTO?
if pagina == "[01] ¿Qué es esta página?":
    st.title("👁️ ADVERTENCIA AL USUARIO")
    st.write("""
    **El Rincón del Rissos** no es un blog convencional. 
    
    Estás ingresando a un archivo recuperado. Todo lo que leas, escuches o veas aquí está bajo tu propio riesgo.
    Este espacio fue creado para documentar las anomalías, los textos perdidos y las frecuencias auditivas que he ido recopilando y creando.
    
    Navega usando el panel izquierdo... si la conexión no se corta antes.
    """)
    # Puedes poner una imagen aterradora aquí
    # st.image("tu_imagen_creepy.png")

# PÁGINA 2: HISTORIAS (Sub-blogs)
elif pagina == "[02] Archivo de Historias":
    st.title("📜 REGISTROS Y RELATOS")
    st.write("Selecciona una sub-categoría para explorar los textos:")
    
    # Creamos "Sub-blogs" usando pestañas (Tabs)
    tab1, tab2, tab3 = st.tabs(["📂 Creepypastas", "📂 Experiencias Reales", "📂 Diarios Encontrados"])
    
    with tab1:
        st.subheader("El Reflejo Incorrecto")
        st.write("Publicado: 13/09/2026 | Autor: Rissos")
        st.write("""
        Todo empezó cuando noté que mi reflejo en el espejo del baño parpadeaba un segundo después que yo. 
        Al principio pensé que era el cansancio... *(Aquí va el texto completo de tu historia)*.
        """)
        st.button("Leer más...", key="btn_creepy1")

    with tab2:
        st.subheader("Lo que vi en Puente Alto")
        st.write("Publicado: Archivo Desconocido")
        st.write("Un relato sobre algo que presencié de madrugada. Nadie me cree, pero las marcas en la puerta siguen ahí.")

    with tab3:
        st.subheader("Entrada #44 - La estática")
        st.write("No dejo de escuchar el ruido blanco. Incluso cuando la tele está desenchufada.")

# PÁGINA 3: MÚSICA (Spotify y .wav)
elif pagina == "[03] Frecuencias (Música)":
    st.title("🎵 FRECUENCIAS Y RUIDO")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Mis Composiciones (.wav)")
        st.write("Pistas exportadas directamente desde mi DAW. Se recomienda usar audífonos.")
        
        # Reproductor de audio local (Asegúrate de tener un archivo .wav en la misma carpeta)
        # Descomenta las líneas de abajo cuando tengas tus archivos de audio:
        
        # st.write("▶️ Pista 1: Ansiedad.wav")
        # st.audio("ansiedad.wav", format="audio/wav")
        
        # st.write("▶️ Pista 2: El_Sotano.wav")
        # st.audio("el_sotano.wav", format="audio/wav")
        
        st.info("*(Coloca tus archivos .wav en la misma carpeta del app.py y usa st.audio('nombre.wav') para que suenen aquí)*")

    with col2:
        st.subheader("Playlist de Inspiración (Spotify)")
        st.write("La música que escucho mientras el mundo se cae a pedazos.")
        
        # Para poner tu playlist de Spotify: 
        # Ve a Spotify > Click derecho en tu playlist > Compartir > Insertar playlist (Embed) > Copia el código
        spotify_embed = """
        <iframe style="border-radius:12px" src="https://open.spotify.com/embed/playlist/37i9dQZF1DWZtZ8vUCzche?utm_source=generator&theme=0" width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
        """
        # st.components.v1.html te permite meter cualquier iframe o HTML externo
        import streamlit.components.v1 as components
        components.html(spotify_embed, height=400)

# PÁGINA 4: SOBRE MÍ
elif pagina == "[04] Sobre mí":
    st.title("💀 ACERCA DEL AUTOR")
    st.write("""
    **Alias:** Rissos  
    **Ubicación:** Desconocida (Región Metropolitana)  
    **Estado:** Activo  
    
    Soy un creador de contenido enfocado en el horror core, la producción musical oscura y la escritura visceral.
    Si llegaste hasta aquí, probablemente ya estemos conectados de alguna forma.
    """)
