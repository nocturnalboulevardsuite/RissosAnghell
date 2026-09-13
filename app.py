import streamlit as st

st.set_page_config(page_title="ANGHELL // 血", layout="wide", initial_sidebar_state="expanded")

# --- CSS: RED ROOM JAPONÉS 2000s + CREEPYPASTA ---
css = """
<style>
/* Importar fuente de sistema antigua para el estilo 2000s */
@import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

/* Fondo base: Rojo Vino / Sangre coagulada */
.stApp {
    background-color: #240000;
    background-image: 
        radial-gradient(circle, #3a0000 0%, #120000 100%),
        repeating-linear-gradient(45deg, transparent, transparent 2px, rgba(255,0,0,0.03) 2px, rgba(255,0,0,0.03) 4px);
    color: #ff3333; /* Texto rojo vívido */
    font-family: 'MS Gothic', 'Courier New', monospace; /* Estilo foro japonés 2000 */
    font-size: 16px;
}

/* Efecto de ruido de fondo estilo web antigua */
.stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    background-image: url('https://www.transparenttextures.com/patterns/diagmonds-light.png');
    opacity: 0.1;
    pointer-events: none;
    z-index: 0;
}

/* Títulos: Rojo Sangre Neón con glitch sutil */
h1, h2, h3 {
    font-family: 'Times New Roman', serif;
    color: #ff0000 !important;
    text-transform: uppercase;
    text-shadow: 0px 0px 10px rgba(255, 0, 0, 0.8), 2px 2px 0px #000000;
    border-bottom: 2px double #ff0000;
    padding-bottom: 5px;
    margin-bottom: 20px;
}

/* Estilo del Sidebar - Estilo menú maldito */
[data-testid="stSidebar"] {
    background-color: #140000 !important;
    border-right: 3px double #ff0000;
    box-shadow: 5px 0 20px rgba(255, 0, 0, 0.2);
}
[data-testid="stSidebar"] * {
    font-family: 'MS Gothic', monospace;
    color: #ff4d4d !important;
    font-weight: bold;
}

/* Ocultar UI nativa */
header, footer {visibility: hidden;}

/* Pestañas (Estilo botones 2000s) */
.stTabs [data-baseweb="tab-list"] {
    background-color: #140000;
    border: 1px solid #ff0000;
}
.stTabs [data-baseweb="tab"] {
    color: #cc0000;
    background-color: transparent;
    border-right: 1px solid #ff0000;
}
.stTabs [aria-selected="true"] {
    background-color: #ff0000 !important;
    color: #140000 !important;
    box-shadow: inset 0 0 10px #000;
}

/* Cajas de contenido: Peligrosas y marcadas */
.danger-box {
    background-color: #1a0000;
    border: 1px solid #ff0000;
    border-left: 5px solid #ff0000;
    padding: 20px;
    margin-bottom: 25px;
    box-shadow: inset 0 0 15px rgba(255, 0, 0, 0.1);
    color: #ff6666;
    line-height: 1.6;
}

/* Texto de advertencia / parpadeo */
.blink-text {
    animation: blinker 1.5s linear infinite;
    color: #ff0000;
    font-weight: bold;
    text-shadow: 0 0 5px red;
}
@keyframes blinker {
    50% { opacity: 0; }
}

/* Enlaces estilo web 1.0 */
a {
    color: #ff0000;
    text-decoration: underline dashed;
}
a:hover {
    background-color: #ff0000;
    color: #000;
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# --- NAVEGACIÓN LATERAL ---
st.sidebar.markdown("<h2 style='text-align: center; font-size: 1.8rem;'>【ＡＮＧＨＥＬＬ】</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<div style='text-align: center; color: #ff0000; letter-spacing: 2px;'>C O L L E C T I O N</div>", unsafe_allow_html=True)
st.sidebar.markdown("<br>", unsafe_allow_html=True)

opciones = [
    "➤ [01] 概要 (LA ESENCIA)", 
    "➤ [02] 物語 (RELATOS)", 
    "➤ [03] 音声 (FRECUENCIAS)", 
    "➤ [04] 視覚 (CATÁLOGO)",
    "➤ [05] 深淵 (EL ABISMO)"
]
pagina = st.sidebar.radio("DIRECTORIO", opciones, label_visibility="collapsed")
st.sidebar.markdown("<br><br><br><br>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; font-size: 12px;' class='blink-text'>Do you like the red room?</p>", unsafe_allow_html=True)

# --- RUTEO DE PÁGINAS ---

if pagina == "➤ [01] 概要 (LA ESENCIA)":
    st.markdown("<h1>EL RINCÓN DE RISSOS</h1>", unsafe_allow_html=True)
    st.markdown("<h3>>> ANGHELL_COLLECTION.exe</h3>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="danger-box">
    <b>ADVERTENCIA DE SISTEMA:</b> Este es un blog personal. Un rincón analógico en una red sobresaturada.<br><br>
    
    Lo creé porque hay cosas que de verdad <span style='color: #ff0000; font-weight: bold; font-size: 18px;'>NO SÉ DÓNDE COLOCAR, NI CÓMO CATALOGAR</span>. 
    <br><br>
    Historias viscerales que he escrito en las madrugadas, música y pistas de audio que he producido y que 
    suenan demasiado perturbadoras para un lanzamiento normal. Recomendaciones de películas de culto, series, animes, 
    y recuerdos fragmentados que me niego a perder.<br><br>
    
    Cosas que necesito postear para no perder su esencia. No busques un orden lógico aquí. 
    Solo entra, lee y vete antes de que el servidor colapse.
    </div>
    """, unsafe_allow_html=True)

elif pagina == "➤ [02] 物語 (RELATOS)":
    st.markdown("<h1>ARCHIVO DE TEXTOS // 血</h1>", unsafe_allow_html=True)
    st.write(">> No creas todo lo que está escrito aquí. O hazlo. Da igual.")
    
    tab1, tab2 = st.tabs(["[ ARCHIVO_01 ]", "[ ARCHIVO_02 ]"])
    
    with tab1:
        st.write("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="danger-box">
        <h3 style='font-size: 20px; border:none;'>La Chica del Fotolog (2006)</h3>
        Recuerdo cuando la internet chilena estaba dominada por fondos negros y letras fucsias. 
        Había una cuenta, <i>@Anghell_Tears</i>, que subía fotos diarias. Siempre en el mismo ángulo, 
        siempre en la misma habitación oscura.<br><br>
        El problema fue cuando la habitación en sus fotos empezó a parecerse demasiado a la mía. 
        Y el ángulo... era desde adentro de mi propio armario.<br><br>
        <span class="blink-text">[ LEYENDO DATOS... ]</span>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.write("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="danger-box">
        <h3 style='font-size: 20px; border:none;'>Asfalto y Sangre</h3>
        Vampirismo urbano en Puente Alto. No hay castillos, solo paraderos de micro vacíos a las 4 AM y 
        ojos que brillan al fondo de los pasajes oscuros.
        </div>
        """, unsafe_allow_html=True)

elif pagina == "➤ [03] 音声 (FRECUENCIAS)":
    st.markdown("<h1>FRECUENCIAS ACÚSTICAS</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="danger-box">
        <h3 style='font-size: 18px; border:none;'>/LOCAL_AUDIO/</h3>
        Pistas creadas por mí. Frecuencias diseñadas para alterar tu ritmo cardíaco.
        <br><br>
        <p style='color: #ff0000;'>[ ERROR DE REPRODUCCIÓN: ARCHIVOS NO ENCONTRADOS EN EL DISCO ]</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="danger-box" style="padding: 5px;">
        <h3 style='font-size: 18px; border:none; padding-left: 15px;'>/SPOTIFY_EMBED/</h3>
        <iframe style="border-radius:0; border: 1px solid #ff0000; filter: contrast(120%) saturate(150%);" 
        src="https://open.spotify.com/embed/playlist/37i9dQZF1DWZtZ8vUCzche?utm_source=generator&theme=0" 
        width="100%" height="280" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
        </div>
        """, unsafe_allow_html=True)

elif pagina == "➤ [04] 視覚 (CATÁLOGO)":
    st.markdown("<h1>CATÁLOGO VISUAL</h1>", unsafe_allow_html=True)
    st.write(">> Medios audiovisuales para consumir en la oscuridad.")
    
    st.markdown("""
    <div class="danger-box">
    <h3 style='border: none; font-size: 18px;'>[ PELÍCULA ] The Lost Boys (1987)</h3>
    Estética vampírica pura. Cuero, sangre, noches eternas de los 80. Define exactamente el color 
    rojo vivo y la oscuridad que busco transmitir en este espacio.
    <br><br><hr style='border: 1px dashed #ff0000;'>
    <h3 style='border: none; font-size: 18px;'>[ ANIME ] Serial Experiments Lain (1998)</h3>
    La desconexión total. El ruido estático de los cables de tensión japoneses. Si este blog tuviera 
    un estado mental, sería la red de Lain.
    <br><br><hr style='border: 1px dashed #ff0000;'>
    <h3 style='border: none; font-size: 18px;'>[ JUEGO ] Fears to Fathom</h3>
    El terror de estar solo en casa narrado a través de gráficos de PS1 y filtros VHS. 
    La tensión de saber que alguien te está mirando.
    </div>
    """, unsafe_allow_html=True)

elif pagina == "➤ [05] 深淵 (EL ABISMO)":
    st.markdown("<h1>EL ABISMO // 死</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="danger-box" style="text-align: center; background-color: #000000;">
    <br><br>
    <h2 class="blink-text" style='border: none;'>MEMORIAS CORROMPIDAS</h2>
    <br>
    <p style="font-size: 18px; color: #cc0000;">
    Hay cosas que no encajan en ninguna otra parte.<br>
    Imágenes residuales de las madrugadas.<br>
    Aquí es donde caen cuando nadie más quiere verlas.
    </p>
    <br>
    <div style="font-family: 'Times New Roman'; font-size: 40px; color: #ff0000; letter-spacing: 10px;">
    見えないで
    </div>
    <br><br>
    </div>
    """, unsafe_allow_html=True)
