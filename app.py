import streamlit as st

# Configuración inicial de la página
st.set_page_config(page_title="El Rincón del Rissos", page_icon="🩸", layout="centered")

# --- CSS BASE: ESTÉTICA VHS, MATRIX SANGRIENTO Y ARAÑAS ---
css_global = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Creepster&family=VT323&display=swap');

/* Fondo base estilo Error de Sistema / VHS */
.stApp {
    background-color: #030000;
    color: #ff0000;
    font-family: 'VT323', monospace;
    font-size: 24px;
    background-image: 
        repeating-linear-gradient(
            0deg,
            rgba(255, 0, 0, 0.05),
            rgba(255, 0, 0, 0.05) 1px,
            transparent 1px,
            transparent 2px
        );
}

/* Efecto Glitch y Aberración para Títulos */
h1, h2, h3 {
    font-family: 'Creepster', cursive;
    text-shadow: 2px 0 0 rgba(255,0,0,0.8), -2px 0 0 rgba(100,0,0,0.8);
    color: #aa0000;
    text-align: center;
    animation: glitch 1.5s infinite;
}

@keyframes glitch {
    0% { text-shadow: 2px 0 0 red, -2px 0 0 darkred; }
    50% { text-shadow: -2px 0 0 red, 2px 0 0 darkred; }
    100% { text-shadow: 2px 0 0 red, -2px 0 0 darkred; }
}

/* Botones Sangrientos Neón */
div.stButton > button:first-child {
    background-color: #110000;
    color: #ff0000;
    border: 2px solid #8a0000;
    font-family: 'VT323', monospace;
    font-size: 26px;
    width: 100%;
    box-shadow: 0 0 15px #ff0000;
    transition: 0.3s;
}
div.stButton > button:first-child:hover {
    background-color: #4a0000;
    color: #ffffff;
    box-shadow: 0 0 30px #ff0000;
    border: 2px solid #ff0000;
}

/* Animación de la araña caminando por la pantalla */
@keyframes crawl {
    0% { top: -50px; left: 10%; transform: rotate(180deg); }
    100% { top: 110vh; left: 30%; transform: rotate(190deg); }
}
.spider {
    position: fixed;
    font-size: 50px;
    animation: crawl 10s linear infinite;
    z-index: 9999;
    pointer-events: none;
    opacity: 0.8;
}
</style>
<div class="spider">🕷️</div>
"""

# --- CSS ESPECÍFICOS PARA CADA HISTORIA ---

# Historia 1: Dinosaurios (Verde pantano, reptiliano)
css_dino = """
<style>
.stApp { background-color: #001100; color: #77ff77; }
h1, h2 { color: #22aa22; text-shadow: 2px 2px #000000; animation: none; }
div.stButton > button:first-child { border: 2px solid #22aa22; box-shadow: 0 0 15px #22aa22; color: #22aa22; }
div.stButton > button:first-child:hover { background-color: #004400; color: white; box-shadow: 0 0 30px #22aa22; border-color: #77ff77;}
</style>
"""

# Historia 2: Misterio (Azul oscuro, paranormal)
css_mystery = """
<style>
.stApp { background-color: #050515; color: #aaddff; }
h1, h2 { color: #5599cc; text-shadow: 2px 2px #ffffff; font-family: 'VT323', monospace; animation: none;}
div.stButton > button:first-child { border: 2px solid #5599cc; box-shadow: 0 0 15px #5599cc; color: #5599cc; }
div.stButton > button:first-child:hover { background-color: #001144; color: white; box-shadow: 0 0 30px #5599cc; border-color: #aaddff;}
</style>
"""

# --- SISTEMA DE NAVEGACIÓN (PÁGINAS) ---
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = 'inicio'

def cambiar_pagina(nueva_pagina):
    st.session_state.pagina_actual = nueva_pagina

# --- RENDERIZADO DE LAS INTERFAZ ---

if st.session_state.pagina_actual == 'inicio':
    # Inyectar CSS global (Rojo, negro, arañas)
    st.markdown(css_global, unsafe_allow_html=True)
    
    st.markdown("<h1>EL RINCÓN DEL RISSOS</h1>", unsafe_allow_html=True)
    st.markdown("<h3>🩸 'Anghell Collection' 🩸</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.write("> **SYSTEM ERROR: CINTAS RECUPERADAS DESDE EL VACÍO.**")
    st.write("Selecciona una de las historias restauradas. No nos hacemos responsables de lo que leas a continuación...")
    
    st.write("<br>", unsafe_allow_html=True)
    
    # Grid de historias
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📼 Play: Terror Jurásico"):
            cambiar_pagina('historia_dino')
            st.rerun()
            
    with col2:
        if st.button("📼 Play: El Misterio del Sótano"):
            cambiar_pagina('historia_misterio')
            st.rerun()

elif st.session_state.pagina_actual == 'historia_dino':
    # Inyectar CSS global + CSS específico de dinosaurios
    st.markdown(css_global + css_dino, unsafe_allow_html=True)
    
    st.markdown("<h1>Terror Jurásico</h1>", unsafe_allow_html=True)
    
    st.write("""
    *(Estética de jungla tóxica cargada...)*
    
    El sonido de las hojas rompiéndose en la oscuridad me heló la sangre. 
    No era un animal normal. El olor a humedad y reptil inundó la cabaña...
    
    *(Aquí puedes pegar todo el texto de tu historia sobre dinosaurios o monstruos)*.
    """)
    
    st.markdown("---")
    if st.button("🔙 Eject: Volver al Archivo Principal"):
        cambiar_pagina('inicio')
        st.rerun()

elif st.session_state.pagina_actual == 'historia_misterio':
    # Inyectar CSS global + CSS específico de misterio
    st.markdown(css_global + css_mystery, unsafe_allow_html=True)
    
    st.markdown("<h1>El Misterio del Sótano</h1>", unsafe_allow_html=True)
    
    st.write("""
    *(Estética paranormal oscura cargada...)*
    
    La puerta siempre estuvo cerrada con llave. Mi abuelo me advirtió que nunca bajara. 
    Pero anoche, escuché susurros provenientes desde las escaleras...
    
    *(Aquí puedes pegar todo el texto de tu historia de misterio y suspenso)*.
    """)
    
    st.markdown("---")
    if st.button("🔙 Eject: Volver al Archivo Principal"):
        cambiar_pagina('inicio')
        st.rerun()
