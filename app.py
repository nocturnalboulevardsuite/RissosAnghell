import streamlit as st

st.set_page_config(page_title="ANGHELL COLLECTION", layout="wide", initial_sidebar_state="expanded")

# --- CSS: VHS + DEAD SILENCE + ARMY OF TWO UI ---
css = """
<style>
/* Importar fuentes: 
   Bebas Neue (Menú Táctico Army of Two)
   Cinzel (Elegancia macabra estilo Dead Silence)
   Share Tech Mono (Textos técnicos/VHS)
*/
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Cinzel:wght@600;700&family=Share+Tech+Mono&display=swap');

/* Fondo base oscuro abisal */
.stApp {
    background-color: #030000;
    color: #c4b5b5;
    font-family: 'Share Tech Mono', monospace;
    font-size: 18px;
}

/* OVERLAY VHS & FILM GRAIN (Fears to Fathom / VHS 80s) */
.stApp::after {
    content: "";
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    background-image: 
        repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255, 0, 0, 0.04) 2px, rgba(0, 0, 0, 0.05) 4px),
        url('https://upload.wikimedia.org/wikipedia/commons/7/76/1k_Dissolve_Noise_Texture.png');
    background-size: 100% 4px, 250px;
    opacity: 0.25;
    pointer-events: none;
    z-index: 9999;
    animation: vhs-flicker 0.15s infinite;
}

@keyframes vhs-flicker {
    0% { opacity: 0.25; }
    50% { opacity: 0.28; }
    100% { opacity: 0.25; }
}

/* Títulos principales (Dead Silence - Rojo Vivo) */
h1, h2, h3 {
    font-family: 'Cinzel', serif;
    color: #ff0a0a !important; /* Rojo sangre hiper-vívido */
    text-transform: uppercase;
    text-shadow: 0px 0px 12px rgba(255, 10, 10, 0.6), 3px 3px 0px #220000;
    border-bottom: 1px solid rgba(255, 10, 10, 0.4);
    padding-bottom: 10px;
    margin-bottom: 25px;
    letter-spacing: 2px;
}

/* --- MENÚ LATERAL ESTILO ARMY OF TWO --- */
[data-testid="stSidebar"] {
    background-color: #050101 !important;
    border-right: 2px solid #330000;
    box-shadow: 10px 0 30px rgba(255, 0, 0, 0.05);
}

/* Estilizar el Radio Button de Streamlit para que parezca un menú de juego */
div[role="radiogroup"] {
    gap: 5px;
}
div[role="radiogroup"] > label {
    background: linear-gradient(90deg, #110000 0%, transparent 100%);
    border-left: 4px solid #330000;
    padding: 15px 20px !important;
    margin-bottom: 5px;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 26px !important;
    color: #665555 !important;
    text-transform: uppercase;
    letter-spacing: 2px;
    transition: all 0.2s ease-in-out;
    cursor: pointer;
}
div[role="radiogroup"] > label:hover {
    border-left: 4px solid #8a0303;
    color: #ff0a0a !important;
    background: linear-gradient(90deg, rgba(255, 10, 10, 0.05) 0%, transparent 100%);
}
div[role="radiogroup"] > label[data-checked="true"] {
    border-left: 8px solid #ff0a0a !important; /* Marca táctica gruesa */
    color: #ffffff !important; /* Blanco para alto contraste Army of Two */
    background: linear-gradient(90deg, rgba(255, 10, 10, 0.2) 0%, transparent 100%);
    text-shadow: 0 0 10px rgba(255, 10, 10, 0.8);
    transform: translateX(5px); /* Efecto de selección hacia adelante */
}

/* Ocultar los círculos nativos del radio button */
div[role="radiogroup"] circle {
    display: none;
}
div[role="radiogroup"] label div:first-child {
    display: none;
}

/* Ocultar UI nativa de Streamlit */
header, footer {visibility: hidden;}

/* Cajas de contenido (Efecto Táctico/VHS) */
.tactical-box {
    background: rgba(10, 2, 2, 0.85);
    border: 1px solid #330000;
    border-left: 3px solid #ff0a0a;
    padding: 25px;
    margin-bottom: 25px;
    box-shadow: inset 0 0 20px rgba(0,0,0,1);
    position: relative;
}
.tactical-box::before {
    content: "[ REC ]";
    position: absolute;
    top: 5px; right: 10px;
    font-size: 12px;
    color: #ff0a0a;
    animation: blinker 2s linear infinite;
}

@keyframes blinker {
    50% { opacity: 0; }
}

.blood-text {
    color: #ff0a0a;
    font-weight: bold;
    text-shadow: 0 0 8px rgba(255, 10, 10, 0.5);
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# --- NAVEGACIÓN LATERAL (UI TÁCTICA) ---
st.sidebar.markdown("<h2 style='font-family: \"Bebas Neue\", sans-serif; text-align: center; font-size: 2.5rem; text-shadow: 0 0 15px red; border:none;'>ANGHELL<br>COLLECTION</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<div style='text-align: center; color: #ff0a0a; font-family: monospace;'>// SYS.OVERRIDE_ACTIVATED</div><br>", unsafe_allow_html=True)

opciones = [
    "01. LA ESENCIA", 
    "02. ARCHIVO_RELATOS", 
    "03. FRECUENCIAS_AUDIO", 
    "04. CATÁLOGO_VISUAL",
    "05. EL_ABISMO"
]
pagina = st.sidebar.radio("MAIN MENU", opciones, label_visibility="collapsed")

st.sidebar.markdown("<br><br><br><div style='text-align: center; color: #444; font-family: \"Bebas Neue\"; font-size: 20px;'>STATUS: DISCONNECTED</div>", unsafe_allow_html=True)

# --- RUTEO DE PÁGINAS ---

if pagina == "01. LA ESENCIA":
    st.markdown("<h1>El Rincón de Rissos</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='border: none; color: #aa0000 !important; font-family: \"Share Tech Mono\"; margin-top: -15px;'>[ ARCHIVO CLASIFICADO: 'ANGHELL COLLECTION' ]</h3>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="tactical-box" style="font-size: 19px; line-height: 1.8;">
    Este es un blog personal. Un rincón analógico en una red sobresaturada.
    <br><br>
    Lo creé porque hay cosas que de verdad <span class="blood-text">no sé dónde colocar, ni cómo catalogar</span>. 
    Historias viscerales que he escrito en las madrugadas, música y pistas que he producido pero que no encajan en 
    ningún álbum estructurado, recomendaciones de películas de terror, series, animes, y recuerdos fragmentados.
    <br><br>
    Son fragmentos que necesito postear para no perder esa esencia, ese recuerdo, ese momento exacto en el tiempo. 
    Aquí no hay un orden lógico. Solo lo que sobrevive a la estática.
    </div>
    """, unsafe_allow_html=True)

elif pagina == "02. ARCHIVO_RELATOS":
    st.markdown("<h1>Archivos de Texto</h1>", unsafe_allow_html=True)
    st.write("> ACCEDIENDO A SECTOR DE FICCIÓN/REALIDAD...")
    
    st.markdown("""
    <div class="tactical-box">
    <h3 style='font-size: 24px; border:none; margin-bottom: 10px;'>[ CASO: EL PERRO SIN ROSTRO ]</h3>
    Puente Alto, 3:15 AM. La niebla era tan espesa que las luces del alumbrado parecían estática. 
    Pensé que era un perro callejero buscando comida en la basura. Hice el típico sonido para llamarlo. 
    <br><br>
    Cuando se dio la vuelta, el área donde debía estar su rostro era plana, como piel tensada sobre un cráneo liso. 
    No tenía ojos, pero supe que me estaba mirando.
    <br><br>
    <span style="color: #ff0a0a; font-family: 'Bebas Neue', sans-serif; font-size: 20px;">[ FIN DE TRANSMISIÓN ]</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="tactical-box">
    <h3 style='font-size: 24px; border:none; margin-bottom: 10px;'>[ CASO: ESTÁTICA EN LA PARED ]</h3>
    A veces, el silencio de la madrugada pesa tanto que zumba en los oídos. Pero otras veces, 
    el zumbido no está en tu cabeza, viene de detrás de la pintura de tu habitación.
    </div>
    """, unsafe_allow_html=True)

elif pagina == "03. FRECUENCIAS_AUDIO":
    st.markdown("<h1>Frecuencias de Audio</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="tactical-box">
        <h3 style='font-size: 20px; border:none; color:#ff0a0a !important;'>[ PISTAS MAESTRAS .WAV ]</h3>
        Audios corrompidos, bases rítmicas oscuras y frecuencias que he compuesto a lo largo de los años.
        <br><br>
        <span style="color:#555; font-family: monospace;">>> CONECTANDO CON SERVIDOR LOCAL... FAIL.</span>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="tactical-box" style="padding: 10px;">
        <h3 style='font-size: 20px; border:none; padding-left: 10px; color:#ff0a0a !important;'>[ SPOTIFY OVERRIDE ]</h3>
        <iframe style="border-radius:0; border: 1px solid #ff0a0a; filter: grayscale(50%) contrast(150%);" 
        src="https://open.spotify.com/embed/playlist/37i9dQZF1DWZtZ8vUCzche?utm_source=generator&theme=0" 
        width="100%" height="280" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
        </div>
        """, unsafe_allow_html=True)

elif pagina == "04. CATÁLOGO_VISUAL":
    st.markdown("<h1>Catálogo Visual</h1>", unsafe_allow_html=True)
    st.write("> RECOPILANDO RECOMENDACIONES CLASIFICADAS...")
    
    st.markdown("""
    <div class="tactical-box">
    <h3 style='border: none; font-family: "Bebas Neue"; font-size: 28px;'>TARGET 01: THE LOST BOYS (1987)</h3>
    La cumbre de la estética vampírica. Cuero, sangre, noches interminables y una banda sonora perfecta. 
    Es el molde exacto del estilo de vida que respira esta colección.
    <br><br>
    <hr style='border: 1px solid #330000;'>
    <br>
    <h3 style='border: none; font-family: "Bebas Neue"; font-size: 28px;'>TARGET 02: DEAD SILENCE (2007)</h3>
    Esa paleta de colores desaturada donde solo resalta la sangre. La sensación macabra de los objetos antiguos, 
    la madera y el terror silencioso. Pura inspiración.
    <br><br>
    <hr style='border: 1px solid #330000;'>
    <br>
    <h3 style='border: none; font-family: "Bebas Neue"; font-size: 28px;'>TARGET 03: FEARS TO FATHOM</h3>
    El terror de la rutina. La estética granulada y el miedo irracional a mirar por la ventana en medio de la noche 
    y ver que alguien te devuelve la mirada.
    </div>
    """, unsafe_allow_html=True)

elif pagina == "05. EL_ABISMO":
    st.markdown("<h1>El Abismo</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="tactical-box" style="text-align: center; border: 2px dashed #ff0a0a; background: #050000;">
    <br><br>
    <h2 style='border: none; font-family: "Bebas Neue"; font-size: 50px; color: #ff0a0a !important; letter-spacing: 5px; text-shadow: 0 0 20px red;'>DATA FRAGMENTADA</h2>
    <br>
    <p style="font-size: 20px; font-family: 'Share Tech Mono';">
    Cosas que no son historias, ni música, ni películas.<br>
    Pensamientos intrusivos, ruido blanco y estática pura.<br>
    Todo lo que no sé dónde poner, cae aquí.
    </p>
    <br><br><br>
    </div>
    """, unsafe_allow_html=True)
