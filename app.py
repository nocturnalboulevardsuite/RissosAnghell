import streamlit as st

st.set_page_config(page_title="ANGHELL COLLECTION", layout="wide", initial_sidebar_state="expanded")

# --- CSS: SHADER DE CINE, FONDO DE LADRILLOS ROJOS Y ESCALERA SILUETA (TIPO EEUU) ---
css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Anton&family=Cormorant+Garamond:ital,wght@0,400;0,700;1,400&display=swap');

/* --- FONDO GLOBAL DE LADRILLOS ROJOS --- */
.stApp {
    /* Color base rojo oscuro puro que brilla a través de la textura transparente */
    background-color: #5a0000;
    /* Gradiente para oscurecer hacia abajo + Textura de ladrillos repetida */
    background-image: 
        linear-gradient(to bottom, rgba(60, 0, 0, 0.5), rgba(5, 0, 0, 0.98)),
        url('https://www.transparenttextures.com/patterns/brick-wall-dark.png');
    background-repeat: repeat;
    background-attachment: fixed;
    color: #ff4d4d; 
    font-family: 'Cormorant Garamond', serif;
    font-size: 22px;
}

/* --- SHADER DE PELÍCULA --- */
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

/* --- TÍTULOS Y TEXTOS --- */
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
    background: rgba(20, 0, 0, 0.5) !important;
    border: 1px solid #330000 !important;
    padding: 15px !important;
    margin-bottom: 5px;
    font-family: 'Anton', sans-serif !important;
    font-size: 20px !important;
}
div[role="radiogroup"] > label p {
    color: #ff3333 !important; 
    font-size: 22px !important;
}
div[role="radiogroup"] > label:hover {
    background: rgba(255, 0, 0, 0.1) !important;
    border-color: #ff1a1a !important;
}
div[role="radiogroup"] > label[data-checked="true"] {
    background: rgba(100, 0, 0, 0.4) !important;
    border-left: 5px solid #ff1a1a !important;
}
div[role="radiogroup"] > label[data-checked="true"] p {
    color: #ffffff !important;
    text-shadow: 0 0 10px #ff1a1a;
}
header, footer { display: none !important; }

/* --- ESCENOGRAFÍA: CALLEJÓN (FONDO INVISIBLE PARA QUE SE VEA EL LADRILLO GLOBAL) --- */
.alley-scene {
    position: relative;
    width: 100%;
    height: 480px;
    /* Totalmente transparente para que la pared roja de fondo asuma el protagonismo */
    background: transparent;
    border: 1px solid rgba(50, 0, 0, 0.3);
    box-shadow: inset 0 0 100px rgba(0,0,0,0.8);
    margin-top: 20px;
    margin-bottom: 40px;
    overflow: hidden;
}

/* La Ventana con Fuego (Resplandor fuerte) */
.fire-window {
    position: absolute;
    top: 60px;
    right: 120px;
    width: 150px;
    height: 180px;
    border: 8px solid #0a0a0a;
    background: #000;
    box-shadow: 0 0 80px #ff4500, inset 0 0 40px #ff2200;
    z-index: 1;
}
.fire-window::before {
    /* Fuego ardiente interior */
    content: "";
    position: absolute;
    bottom: -10px; left: -10px; right: -10px; height: 130%;
    background: radial-gradient(circle at bottom, #ffaa00 0%, #ff2200 50%, transparent 80%);
    opacity: 0.9;
    animation: flicker 0.12s infinite alternate;
}
.fire-window::after {
    /* Marco en cruz de la ventana (Silueta) */
    content: "";
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    background: 
        linear-gradient(to right, transparent 46%, #0a0a0a 46%, #0a0a0a 54%, transparent 54%),
        linear-gradient(to bottom, transparent 46%, #0a0a0a 46%, #0a0a0a 54%, transparent 54%);
    z-index: 2;
}

@keyframes flicker {
    0% { opacity: 0.8; transform: translateY(0); }
    100% { opacity: 1; transform: translateY(-2px); }
}

/* --- FIRE ESCAPE (SILUETA ESTILO EEUU CONTRA EL FUEGO) --- */
.fire-escape-platform {
    position: absolute;
    top: 240px;
    right: 80px;
    width: 230px;
    height: 12px;
    background: #0f0f0f;
    box-shadow: 0 20px 40px rgba(0,0,0,0.95);
    z-index: 3;
}
.fire-escape-railing {
    position: absolute;
    bottom: 12px; 
    left: 0;
    width: 100%;
    height: 80px;
    /* Barrotes verticales muy marcados */
    background: repeating-linear-gradient(to right, transparent, transparent 18px, #0f0f0f 18px, #0f0f0f 28px);
    border-top: 8px solid #0f0f0f;
    border-left: 8px solid #0f0f0f;
    border-right: 8px solid #0f0f0f;
    z-index: 4;
}
.fire-escape-ladder {
    position: absolute;
    top: 252px;
    right: 170px; /* Colgando cerca del centro */
    width: 50px;
    height: 250px;
    /* Escalones horizontales densos */
    background: repeating-linear-gradient(to bottom, transparent, transparent 28px, #0f0f0f 28px, #0f0f0f 36px);
    border-left: 8px solid #0f0f0f;
    border-right: 8px solid #0f0f0f;
    z-index: 5;
    /* Ligera inclinación como si colgara torcida */
    transform-origin: top;
    transform: rotate(4deg);
}

.fire-escape-ladder::after {
    content: "";
    position: absolute;
    bottom: -20px; left: -20px; width: 90px; height: 80px;
    background: rgba(10, 0, 0, 0.98); 
    filter: blur(10px); /* Funde la base de la escalera en la oscuridad */
}

/* Contenedor de contenido */
.content-box {
    background: rgba(10, 0, 0, 0.85);
    border-left: 3px solid #ff1a1a;
    padding: 30px;
    margin-bottom: 30px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.95);
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# --- NAVEGACIÓN LATERAL ---
st.sidebar.markdown("<h1 style='text-align: center; font-size: 3.5rem; margin-bottom: 0;'>ANGHELL</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<h3 style='text-align: center; color: #ff3333 !important; font-size: 1.2rem; margin-top: -10px; letter-spacing: 5px;'>COLLECTION</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<br>", unsafe_allow_html=True)

opciones = [
    "EL CALLEJÓN (INICIO)", 
    "CINTAS ENCONTRADAS", 
    "FRECUENCIAS (AUDIO)", 
    "REFERENCIAS VISUALES"
]
pagina = st.sidebar.radio("NAVEGACIÓN", opciones, label_visibility="collapsed")
st.sidebar.markdown("<br><br><br><div style='text-align: center; font-family: Anton; color: #ff1a1a; font-size: 1.5rem;'>REC 🔴</div>", unsafe_allow_html=True)

# --- PÁGINAS ---
if pagina == "EL CALLEJÓN (INICIO)":
    st.markdown("<h1 style='font-size: 4rem;'>EL RINCÓN DE RISSOS</h1>", unsafe_allow_html=True)
    
    st.markdown("""
<div class="alley-scene">
    <div class="fire-window"></div>
    <div class="fire-escape-platform">
        <div class="fire-escape-railing"></div>
    </div>
    <div class="fire-escape-ladder"></div>
    
    <div style="position: absolute; bottom: 30px; left: 40px; width: 55%; z-index: 10;">
        <h2 style="font-size: 2.2rem; background: rgba(5,0,0,0.9); display: inline-block; padding: 5px 15px; margin-bottom: 0;">ZONA CERO</h2>
        <p style="background: rgba(5,0,0,0.9); padding: 15px; font-weight: bold; border-left: 2px solid #ff1a1a; font-size: 20px; color: #ff6666;">
        Este es mi rincón. Fuera del sistema.<br>
        La escalera está rota y el edificio de al lado está en llamas, pero el servidor sigue encendido.
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
<iframe style="border-radius:0; border: none; filter: grayscale(50%) contrast(200%) sepia(50%) hue-rotate(320deg);" 
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
<h3 style="font-size: 2rem;">CLOVERFIELD / SCARFACE</h3>
<p style='font-size: 22px;'>
De Cloverfield: La escala del monstruo y la destrucción urbana vista a nivel del suelo, a través de una lente sucia. <br>
De Scarface: Los contrastes neón, la agresividad de la tipografía y esa atmósfera densa de los ochenta.
</p>
</div>
""", unsafe_allow_html=True)
