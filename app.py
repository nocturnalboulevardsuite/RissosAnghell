import streamlit as st

st.set_page_config(page_title="Anghell Collection | Rissos", layout="wide", initial_sidebar_state="expanded")

# --- CSS: VAMPÍRICO DE LOS 80s, DEAD SILENCE & FILM GRAIN ---
css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Special+Elite&display=swap');

/* Fondo base: Negro asfalto profundo, no totalmente opaco para el contraste */
.stApp {
    background-color: #080303;
    color: #e3d5ca; /* Blanco hueso mucho más claro para mejor lectura */
    font-family: 'Special Elite', monospace;
    font-size: 18px;
}

/* OVERLAY GRANULADO DEAD SILENCE (Film Grain & Scanlines Suaves) */
.stApp::after {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-image: 
        repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255, 0, 0, 0.03) 2px, rgba(0, 0, 0, 0.05) 4px),
        url('https://upload.wikimedia.org/wikipedia/commons/7/76/1k_Dissolve_Noise_Texture.png');
    background-size: 100% 4px, 300px;
    opacity: 0.15; /* Bajamos la opacidad para que no oscurezca la web */
    pointer-events: none;
    z-index: 9999;
    animation: grain 0.5s steps(1) infinite;
}

@keyframes grain {
    0%, 100% { background-position: 0 0, 0 0; }
    50% { background-position: 0 2px, 15px 15px; }
}

/* Títulos (Rojo Vivo / The Lost Boys Neon Blood) */
h1, h2, h3 {
    font-family: 'Cinzel', serif;
    color: #ff1a1a !important; /* Rojo sangre brillante */
    text-transform: uppercase;
    letter-spacing: 3px;
    text-shadow: 0px 0px 15px rgba(255, 26, 26, 0.6), 2px 2px 0px #330000;
    border-bottom: 1px solid rgba(255, 26, 26, 0.3);
    padding-bottom: 10px;
    margin-bottom: 25px;
}

/* Estilo del Sidebar */
[data-testid="stSidebar"] {
    background-color: #030000 !important;
    border-right: 1px solid #cc0000; /* Borde rojo vivo */
    box-shadow: 5px 0 20px rgba(204, 0, 0, 0.1);
}
[data-testid="stSidebar"] * {
    font-family: 'Cinzel', serif;
    color: #d4c5bd !important;
    font-weight: bold;
}

/* Ocultar UI nativa */
header, footer {visibility: hidden;}

/* Pestañas (Subcategorías) */
.stTabs [data-baseweb="tab-list"] {
    background-color: transparent;
    border-bottom: 1px solid rgba(255, 26, 26, 0.3);
}
.stTabs [data-baseweb="tab"] {
    color: #e3d5ca;
    font-family: 'Special Elite', monospace;
    background-color: transparent;
    border: none;
    letter-spacing: 1px;
    font-size: 16px;
}
.stTabs [aria-selected="true"] {
    background-color: rgba(255, 26, 26, 0.1) !important;
    color: #ff1a1a !important;
    border-bottom: 2px solid #ff1a1a !important;
    text-shadow: 0 0 8px rgba(255, 26, 26, 0.5);
}

/* Cajas de contenido (Efecto cristal oscuro con bordes sangrientos) */
.content-box {
    background: linear-gradient(135deg, rgba(20, 2, 2, 0.8) 0%, rgba(5, 0, 0, 0.9) 100%);
    border-left: 4px solid #ff1a1a; /* Borde brillante */
    border-top: 1px solid rgba(255, 26, 26, 0.2);
    padding: 25px;
    margin-bottom: 25px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.9), inset 0 0 30px rgba(255, 0, 0, 0.03);
    color: #e3d5ca;
    line-height: 1.7;
}

/* Texto resaltado */
.blood-text {
    color: #ff3333;
    font-family: 'Cinzel', serif;
    font-weight: bold;
    letter-spacing: 1px;
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# --- NAVEGACIÓN LATERAL ---
st.sidebar.markdown("<h2 style='text-align: center; border: none; font-size: 1.5rem; text-shadow: 0 0 20px red;'>ANGHELL COLLECTION</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<div style='text-align: center; color: #ff1a1a; opacity: 0.5;'>━━━━━━━━━━━━━━</div>", unsafe_allow_html=True)

opciones = [
    "I. LA ESENCIA", 
    "II. RELATOS Y TEXTOS", 
    "III. FRECUENCIAS (.WAV)", 
    "IV. CATÁLOGO VISUAL",
    "V. EL ABISMO"
]
pagina = st.sidebar.radio("CINTAS DISPONIBLES", opciones, label_visibility="collapsed")
st.sidebar.markdown("<div style='text-align: center; color: #ff1a1a; opacity: 0.5;'>━━━━━━━━━━━━━━</div>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; font-size: 12px; font-family: monospace; color: #555 !important;'>REC [ O ] 19:87</p>", unsafe_allow_html=True)

# --- RUTEO DE PÁGINAS ---

if pagina == "I. LA ESENCIA":
    st.markdown("<h1>El Rincón de Rissos</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='border: none; color: #cc0000 !important; margin-top: -15px;'>'Anghell Collection'</h3>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="content-box" style="font-size: 19px;">
    Este es un blog personal. Un rincón analógico en una red sobresaturada.
    <br><br>
    Lo creé porque hay cosas que de verdad <span class="blood-text">no sé dónde colocar, ni cómo catalogar</span>. 
    Historias viscerales que he escrito en las madrugadas, música y pistas que he producido pero que no encajan en 
    ningún álbum, recomendaciones de películas de culto, series, animes, y recuerdos fragmentados.
    <br><br>
    Cosas que necesito postear para no perder esa esencia, ese momento exacto en el tiempo. 
    Aquí no hay un orden lógico. Solo lo que considero digno de ser preservado en la oscuridad.
    </div>
    """, unsafe_allow_html=True)

elif pagina == "II. RELATOS Y TEXTOS":
    st.markdown("<h1>Archivo de Relatos</h1>", unsafe_allow_html=True)
    st.write("Historias originales. Sangre seca sobre papel digital.")
    
    tab1, tab2 = st.tabs(["[ HORROR CORE ]", "[ REFLEXIONES ]"])
    
    with tab1:
        st.write("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="content-box">
        <h3 style='font-size: 24px; border:none; margin-bottom: 10px;'>30 Días en Puente Alto</h3>
        La primera noche que las luces de la calle parpadearon y se apagaron al unísono, pensamos que era un simple corte. 
        Pero el frío que entró por las ventanas no era de invierno. Olía a cobre viejo y a tierra removida. 
        <br><br>
        Cuando miré por la persiana, vi siluetas esperando pacientemente en las esquinas. No caminaban. 
        Simplemente nos observaban.
        <br><br>
        <span style="color: #ff1a1a; font-family: 'Cinzel', serif;">[ CONTINUARÁ... ]</span>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.write("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="content-box">
        <h3 style='font-size: 24px; border:none; margin-bottom: 10px;'>Vampirismo Urbano</h3>
        La ciudad es un ente parasitario. A veces, a las 4 AM, cuando no hay autos ni voces, 
        puedes escucharla respirar a través de los ductos de ventilación.
        </div>
        """, unsafe_allow_html=True)

elif pagina == "III. FRECUENCIAS (.WAV)":
    st.markdown("<h1>Frecuencias Acústicas</h1>", unsafe_allow_html=True)
    st.write("Composiciones de mi autoría y curaduría externa.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="content-box">
        <h3 style='font-size: 20px; border:none;'>ARCHIVOS LOCALES (.WAV)</h3>
        Música que he creado. Pistas huérfanas y experimentos sonoros.
        <br><br>
        <span style="color:#777; font-family: monospace;">> Esperando integración de archivos...</span>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="content-box" style="padding: 10px;">
        <h3 style='font-size: 20px; border:none; padding-left: 10px;'>CURADURÍA SPOTIFY</h3>
        <iframe style="border-radius:0; border: 1px solid #330000;" 
        src="https://open.spotify.com/embed/playlist/37i9dQZF1DWZtZ8vUCzche?utm_source=generator&theme=0" 
        width="100%" height="300" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
        </div>
        """, unsafe_allow_html=True)

elif pagina == "IV. CATÁLOGO VISUAL":
    st.markdown("<h1>Recomendaciones</h1>", unsafe_allow_html=True)
    st.write("Películas de culto, series y animes que comparten esta misma estética.")
    
    st.markdown("""
    <div class="content-box">
    <h3 style='border: none;'>Cine: The Lost Boys (1987)</h3>
    Vampiros motociclistas en una ciudad costera. La mezcla perfecta entre neón, sangre y rock oscuro. 
    Una influencia directa en la manera en que visualizo la noche.
    <br><br>
    <hr style='border: 0; height: 1px; background: linear-gradient(to right, transparent, rgba(255, 26, 26, 0.5), transparent);'>
    <br>
    <h3 style='border: none;'>Cine: Dead Silence (2007)</h3>
    Esa paleta de colores desaturada, azulada y carmesí. La textura granulada del celuloide viejo y 
    la sensación constante de que algo de plástico o madera te está observando.
    <br><br>
    <hr style='border: 0; height: 1px; background: linear-gradient(to right, transparent, rgba(255, 26, 26, 0.5), transparent);'>
    <br>
    <h3 style='border: none;'>Cine: 30 Días de Oscuridad (2007)</h3>
    Depredadores implacables y nieve manchada de sangre. El vampirismo alejado del romance y 
    devuelto a su estado más animal y visceral.
    </div>
    """, unsafe_allow_html=True)

elif pagina == "V. EL ABISMO":
    st.markdown("<h1>El Abismo</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="content-box" style="text-align: center; border-left: none; border-top: 4px solid #ff1a1a;">
    <br><br>
    <h2 style='border: none; color: #ff1a1a !important; letter-spacing: 5px;'>MEMORIAS NO CATALOGADAS</h2>
    <br>
    <p style="font-size: 20px;">
    Hay cosas que no encajan en ninguna otra pestaña.<br>
    Ideas sueltas, sueños febriles, y estática visual.<br>
    Aquí es donde entierro lo que no quiero perder, pero tampoco sé explicar.
    </p>
    <br><br><br>
    </div>
    """, unsafe_allow_html=True)
