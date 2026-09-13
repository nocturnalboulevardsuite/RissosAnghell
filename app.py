import streamlit as st

st.set_page_config(page_title="ANGHELL COLLECTION", layout="wide", initial_sidebar_state="expanded")

# --- CSS: SHADER DE CINE, CALLEJÓN ROJO Y ESCALERA GRINGA ---
css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Anton&family=Cormorant+Garamond:ital,wght@0,400;0,700;1,400&display=swap');

/* --- FONDO GLOBAL OSCURO --- */
.stApp {
    background-color: #080000;
    color: #ff4d4d; /* Texto rojo claro y visible */
    font-family: 'Cormorant Garamond', serif;
    font-size: 22px;
}

/* --- SHADER DE PELÍCULA (FILM GRAIN GLOBAL) --- */
.stApp::after {
    content: "";
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    background-image: url('https://upload.wikimedia.org/wikipedia/commons/7/76/1k_Dissolve_Noise_Texture.png');
    opacity: 0.25;
    pointer-events: none;
    z-index: 9999;
    mix-blend-mode: overlay;
    animation: film-shader 0.15s steps(2) infinite;
}

@keyframes film-shader {
    0% { background-position: 0 0; }
    50% { background-position: 10% 10%; }
    100% { background-position: -10% -5%; }
}

/* --- TÍTULOS --- */
h1, h2, h3 {
    font-family: 'Anton', sans-serif;
    color: #ff1a1a !important;
    text-transform: uppercase;
    letter-spacing: 4px;
    text-shadow: 2px 2px 5px rgba(0,0,0,0.9), 0px 0px 20px rgba(255, 26, 26, 0.6);
}

p, div { text-shadow: 1px 1px 3px rgba(0,0,0,0.8); }

/* --- BARRA LATERAL --- */
[data-testid="stSidebar"] {
    background-color: rgba(5, 0, 0, 0.95) !important;
    border-right: 2px solid #550000;
}
div[role="radiogroup"] > label {
    background: transparent !important;
    border: none !important;
    padding: 10px 15px !important;
    margin-bottom: 5px;
    font-family: 'Anton', sans-serif !important;
}
div[role="radiogroup"] > label p {
    color: #881111 !important; 
    font-size: 20px !important;
    transition: 0.3s;
}
div[role="radiogroup"] > label:hover p {
    color: #ff1a1a !important;
}
div[role="radiogroup"] > label[data-checked="true"] p {
    color: #ffffff !important;
    text-shadow: 0 0 10px #ff1a1a;
}
div[role="radiogroup"] > label[data-checked="true"] {
    border-left: 3px solid #ff1a1a !important;
}
header, footer { display: none !important; }

/* --- ESCENOGRAFÍA: CALLEJÓN ROJO Y ESCALERA GRINGA (FIRE ESCAPE) --- */
.alley-scene {
    position: relative;
    width: 100%;
    height: 450px;
    /* Fondo de ladrillos teñido fuertemente de rojo */
    background: 
        linear-gradient(to bottom, rgba(120, 0, 0, 0.4), rgba(10, 0, 0, 0.95)),
        url('https://www.transparenttextures.com/patterns/brick-wall-dark.png');
    background-color: #3a0000;
    border: 1px solid #220000;
    box-shadow: inset 0 0 80px #000;
    margin-top: 20px;
    margin-bottom: 40px;
    overflow: hidden;
}

/* La Ventana con Fuego */
.fire-window {
    position: absolute;
    top: 60px;
    right: 120px;
    width: 140px;
    height: 180px;
    border: 6px solid #0a0a0a;
    background: #000;
    box-shadow: 0 0 60px #ff3300, inset 0 0 25px #ff3300;
    z-index: 1;
}
.fire-window::before {
    content: "";
    position: absolute;
    bottom: -20px; left: -20px; right: -20px; height: 130%;
    background: radial-gradient(circle at bottom, #ffea00 0%, #ff3300 50%, transparent 80%);
    opacity: 0.85;
    animation: flicker 0.12s infinite alternate;
}
.fire-window::after {
    /* Barrotes estilo guillotina / Nueva York */
    content: "";
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    background: 
        linear-gradient(to right, transparent 48%, #0a0a0a 48%, #0a0a0a 52%, transparent 52%),
        linear-gradient(to bottom, transparent 48%, #0a0a0a 48%, #0a0a0a 52%, transparent 52%);
    z-index: 2;
}
@keyframes flicker {
    0% { opacity: 0.7; transform: translateY(0); }
    100% { opacity: 1; transform: translateY(-3px); }
}

/* --- FIRE ESCAPE (ESTILO DESTINO FINAL / NY) --- */
.fire-escape-platform {
    position: absolute;
    top: 240px;
    right: 80px;
    width: 220px;
    height: 15px;
    background: #111;
    border-bottom: 5px solid #000;
    box-shadow: 0 15px 30px rgba(0,0,0,0.9);
    z-index: 3;
}
.fire-escape-railing {
    position: absolute;
    bottom: 15px; /* Sube desde la plataforma */
    left: 0;
    width: 100%;
    height: 70px;
    /* Rejas verticales */
    background: repeating-linear-gradient(to right, transparent, transparent 15px, #1a1a1a 15px, #1a1a1a 22px);
    border-top: 6px solid #1a1a1a;
    border-left: 6px solid #1a1a1a;
    border-right: 6px solid #1a1a1a;
    z-index: 4;
}
.fire-escape-ladder {
    position: absolute;
    top: 255px;
    right: 240px; /* Colgando de un lado de la plataforma */
    width: 45px;
    height: 250px;
    /* Escalones horizontales */
    background: repeating-linear-gradient(to bottom, transparent, transparent 25px, #111 25px, #111 32px);
    border-left: 5px solid #111;
    border-right: 5px solid #111;
    z-index: 2;
    box-shadow: 15px 15px 20px rgba(0,0,0,0.8);
    /* Inclinación rota/desprendida */
    transform-origin: top;
    transform: rotate(4deg) skewX(-2deg);
}

/* Efecto de rotura al final de la escalera */
.fire-escape-ladder::after {
    content: "";
    position: absolute;
    bottom: -10px; left: -10px; width: 65px; height: 60px;
    background: rgba(20, 0, 0, 0.95); /* Oculta la parte inferior fundiéndola con la sombra */
    filter: blur(5px);
}

/* Contenedor de contenido */
.content-box {
    background: rgba(15, 0, 0, 0.6);
    border-left: 2px solid #ff1a1a;
    padding: 30px;
    margin-bottom: 30px;
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# --- NAVEGACIÓN LATERAL ---
st.sidebar.markdown("<h1 style='text-align: center; font-size: 3.5rem; margin-bottom: 0;'>ANGHELL</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<h3 style='text-align: center; color: #ff3333 !important; font-size: 1rem; margin-top: -10px; letter-spacing: 5px;'>COLLECTION</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<br><br>", unsafe_allow_html=True)

opciones = [
    "EL CALLEJÓN (INICIO)", 
    "CINTAS ENCONTRADAS", 
    "FRECUENCIAS (AUDIO)", 
    "REFERENCIAS VISUALES"
]
pagina = st.sidebar.radio("NAVEGACIÓN", opciones, label_visibility="collapsed")
st.sidebar.markdown("<br><br><br><br><br><div style='text-align: center; font-family: Anton; color: #ff1a1a; font-size: 1.5rem;'>REC 🔴</div>", unsafe_allow_html=True)

# --- PÁGINAS ---

if pagina == "EL CALLEJÓN (INICIO)":
    st.markdown("<h1 style='font-size: 4rem;'>EL RINCÓN DE RISSOS</h1>", unsafe_allow_html=True)
    
    # Escena del callejón rojo + escalera gringa
    st.markdown("""
    <div class="alley-scene">
        <div class="fire-window"></div>
        <div class="fire-escape-platform">
            <div class="fire-escape-railing"></div>
        </div>
        <div class="fire-escape-ladder"></div>
        
        <div style="position: absolute; bottom: 30px; left: 40px; width: 55%; z-index: 5;">
            <h2 style="font-size: 2.2rem; background: rgba(5,0,0,0.85); display: inline-block; padding: 5px 15px; margin-bottom: 0;">ZONA CERO</h2>
            <p style="background: rgba(5,0,0,0.85); padding: 15px; font-weight: bold; border-left: 2px solid #ff1a1a; font-size: 20px; color: #ff6666;">
            Este es mi rincón. Fuera del sistema.<br>
            La escalera de emergencia está colapsando y el edificio de al lado está en llamas, pero el servidor sigue encendido.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="content-box">
    <p style='font-size: 24px; line-height: 1.6;'>
    Lo creé porque hay cosas que de verdad <strong>NO SÉ DÓNDE COLOCAR, NI CÓMO CATALOGAR.</strong> 
    <br><br>
    Historias viscerales que he escrito en las madrugadas. Frecuencias de audio que suenan a estática y sirenas a lo lejos. 
    Recomendaciones de películas de culto, metraje encontrado y recuerdos que la ciudad devoró.
    <br><br>
    No hay interfaz limpia ni diseño corporativo aquí. Es ladrillo, fuego y cinta magnética.
    </p>
    </div>
    """, unsafe_allow_html=True)

elif pagina == "CINTAS ENCONTRADAS":
    st.markdown("<h1>[ ARCHIVOS DE TEXTO ]</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="content-box">
    <h3>TAPE_01: EL PERRO SIN ROSTRO</h3>
    <p style='font-size: 22px;'>
    Puente Alto. 3:15 AM.<br><br>
    La niebla es tan espesa que las luces de los postes parecen linternas muriendo. 
    Una silueta canina busca en la basura. Haces un sonido para llamarlo.<br><br>
    El animal se gira. El área donde debería estar su rostro es plana. Como piel tensada sobre un cráneo liso. 
    No tiene ojos, pero la atmósfera pesa tanto que sabes que te está mirando directamente al centro del pecho.
    </p>
    </div>
    
    <div class="content-box">
    <h3>TAPE_02: VAMPIRISMO DE ASFALTO</h3>
    <p style='font-size: 22px;'>
    La ciudad drena. No usa colmillos, usa horarios, boletos de micro y concreto armado. <br>
    A las 4 AM, los paraderos están vacíos, pero si te quedas mirando fijo a las esquinas, 
    las sombras tienen una densidad distinta. Huelen a ozono y a sangre vieja.
    </p>
    </div>
    """, unsafe_allow_html=True)

elif pagina == "FRECUENCIAS (AUDIO)":
    st.markdown("<h1>[ BANDA SONORA DEL CALLEJÓN ]</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="content-box">
        <h3>PISTAS .WAV</h3>
        <p>Sonido crudo. Mezclas que nunca pasaron por un estudio. 
        Ruido blanco, bajos distorsionados y el zumbido de los cables de alta tensión.</p>
        <div style="margin-top: 20px; padding: 15px; border: 1px solid #ff1a1a; text-align: center; font-family: Anton; font-size: 24px; cursor: pointer;">
        ▶ REPRODUCIR CINTA
        </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="content-box">
        <h3>RADIO EXTERNA</h3>
        <iframe style="border-radius:0; border: none; filter: grayscale(30%) contrast(150%) sepia(80%) hue-rotate(330deg);" 
        src="https://open.spotify.com/embed/playlist/37i9dQZF1DWZtZ8vUCzche?utm_source=generator&theme=0" 
        width="100%" height="250" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
        </div>
        """, unsafe_allow_html=True)

elif pagina == "REFERENCIAS VISUALES":
    st.markdown("<h1>[ INFLUENCIAS DIRECTAS ]</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="content-box">
    <h3 style="font-size: 2rem;">[ REC ] (2007)</h3>
    <p style='font-size: 22px;'>
    El terror de estar encerrado en tu propio edificio. La cámara al hombro, la oscuridad en las escaleras, 
    el caos realista. La sensación de que no hay salida y todo está siendo grabado.
    </p>
    </div>
    
    <div class="content-box">
    <h3 style="font-size: 2rem;">DEAD SILENCE (2007)</h3>
    <p style='font-size: 22px;'>
    Paletas de colores desaturadas donde el único color que resalta es el rojo carmesí. 
    Teatros abandonados, silencio absoluto y la sensación de que algo de madera y porcelana te observa.
    </p>
    </div>
    
    <div class="content-box">
    <h3 style="font-size: 2rem;">FINAL DESTINATION / SCARFACE</h3>
    <p style='font-size: 22px;'>
    De Destino Final: Las callejuelas traseras, las escaleras de emergencia oxidadas, lo macabro en lo urbano. <br>
    De Scarface: Los contrastes neón, la agresividad de la tipografía y esa atmósfera densa, sangrienta y nocturna.
    </p>
    </div>
    """, unsafe_allow_html=True)
