import streamlit as st
import random
from datetime import datetime

st.set_page_config(page_title="Mi Ecosistema Web", layout="wide", initial_sidebar_state="expanded")

# --- NAVEGACIÓN PRINCIPAL ---
menu = ["Historia (Mis Libros)", "Multimedia", "Audiología", "Películas y Series", "El Oráculo Estelar"]
eleccion = st.sidebar.radio("Navegación", menu)

# --- 1. SECCIÓN HISTORIA ---
if eleccion == "Historia (Mis Libros)":
    st.markdown("<h1 style='text-align: center;'>BIBLIOTECA PERSONAL</h1>", unsafe_allow_html=True)
    st.write("Selecciona una obra para entrar en su mundo.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🕷️ La Viuda Negra (Terror)"):
            st.session_state.libro_actual = "arana"
            
    with col2:
        if st.button("🌹 El Jardín de Espinas (Romance)"):
            st.session_state.libro_actual = "rosa"

    # Lógica dinámica para cambiar el tema según el libro
    if "libro_actual" in st.session_state:
        if st.session_state.libro_actual == "arana":
            st.markdown("""
            <style>
            .stApp { background-color: #0a0a0a; color: #a3a3a3; font-family: monospace; }
            .spider-web { border: 2px solid #333; padding: 20px; background: url('https://www.transparenttextures.com/patterns/cobweb.png'); box-shadow: 0 0 20px #000; }
            </style>
            <div class="spider-web">
                <h2 style="color: #ff3333;">La Viuda Negra</h2>
                <p>Las patas crujen en la oscuridad. El hilo de seda baja desde el techo...</p>
                <p><i>(Aquí va el contenido de tu libro de terror, con animaciones CSS de arañas bajando que agregaremos luego)</i></p>
            </div>
            """, unsafe_allow_html=True)
            
        elif st.session_state.libro_actual == "rosa":
            st.markdown("""
            <style>
            .stApp { background-color: #ffe6e6; color: #5c0016; font-family: serif; }
            .rose-garden { border: 2px solid #ff99aa; padding: 20px; background: url('https://www.transparenttextures.com/patterns/floral-texture.png'); box-shadow: 0 0 20px #ffb3c6; }
            </style>
            <div class="rose-garden">
                <h2 style="color: #cc0033;">El Jardín de Espinas</h2>
                <p>El aroma era dulce, pero el tallo exigía sangre para florecer...</p>
                <p><i>(Aquí va tu libro de romance oscuro, rodeado de estética floral)</i></p>
            </div>
            """, unsafe_allow_html=True)

# --- 2. SECCIÓN MULTIMEDIA ---
elif eleccion == "Multimedia":
    st.markdown("<h1>GALERÍA VISUAL</h1>", unsafe_allow_html=True)
    st.write("Imágenes y videos subidos a mi antojo.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("Espacio para Imagen 1")
        # st.image("ruta_a_tu_imagen.jpg")
    with col2:
        st.info("Espacio para Video 1")
        # st.video("ruta_a_tu_video.mp4")

# --- 3. SECCIÓN AUDIOLOGÍA ---
elif eleccion == "Audiología":
    st.markdown("<h1>FRECUENCIAS Y SONIDOS</h1>", unsafe_allow_html=True)
    st.write("Composiciones propias, backgrounds y experimentación sonora.")
    
    st.markdown("### Pista 1: Ambiente de Lluvia y Neón")
    # st.audio("ruta_a_tu_audio1.wav")
    st.progress(0) # Simulador de reproductor
    
    st.markdown("### Pista 2: Tema Principal")
    # st.audio("ruta_a_tu_audio2.mp3")
    st.progress(0)

# --- 4. SECCIÓN PELÍCULAS Y SERIES ---
elif eleccion == "Películas y Series":
    st.markdown("<h1>MIS RECOMENDACIONES</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""<div style='background:#111; padding:10px; text-align:center; border-radius:10px;'>
        <h3>🎬 SILENT HILL</h3><div style='height:150px; background:#333; margin-bottom:10px;'>[CARÁTULA]</div></div>""", unsafe_allow_html=True)
        with st.expander("Ver mi recomendación"):
            st.write("**De qué trata:** Un pueblo envuelto en niebla y ceniza donde los traumas toman forma física.")
            st.write("**Por qué la recomiendo:** La atmósfera y el diseño de sonido son legendarios.")

    with col2:
        st.markdown("""<div style='background:#111; padding:10px; text-align:center; border-radius:10px;'>
        <h3>👾 EVANGELION</h3><div style='height:150px; background:#333; margin-bottom:10px;'>[CARÁTULA]</div></div>""", unsafe_allow_html=True)
        with st.expander("Ver mi recomendación"):
            st.write("**De qué trata:** Mechas gigantes, crisis existenciales y ángeles apocalípticos.")
            st.write("**Por qué la recomiendo:** Cambió mi forma de ver la animación y la psicología de personajes.")

    with col3:
        st.markdown("""<div style='background:#111; padding:10px; text-align:center; border-radius:10px;'>
        <h3>📺 MR. ROBOT</h3><div style='height:150px; background:#333; margin-bottom:10px;'>[CARÁTULA]</div></div>""", unsafe_allow_html=True)
        with st.expander("Ver mi recomendación"):
            st.write("**De qué trata:** Un hacker con ansiedad social intenta destruir la corporación más grande del mundo.")
            st.write("**Por qué la recomiendo:** Representación realista del hacking y una cinematografía impecable.")

# --- 5. SECCIÓN ESTRELLAS (ORÁCULO) ---
elif eleccion == "El Oráculo Estelar":
    st.markdown("<h1 style='text-align: center; color: #ffd700;'>✨ LA ESTRELLA DEL DESTINO ✨</h1>", unsafe_allow_html=True)
    st.write("Toca un brillo de la estrella e ingresa tus datos para revelar qué te depara el futuro.")
    
    # Formulario para capturar los datos
    with st.form("form_estrella"):
        nombre = st.text_input("Tu Nombre")
        fecha_nacimiento = st.date_input("Fecha de Nacimiento", min_value=datetime(1920, 1, 1), max_value=datetime.today())
        
        # Botón para revelar
        revelar = st.form_submit_button("Tocar la Estrella 🌟")
        
    if revelar and nombre:
        # Respuestas mezcladas (buenas y malas)
        respuestas = [
            f"El universo conspira a tu favor, {nombre}. Una oportunidad creativa tocará tu puerta pronto.",
            f"Cuidado, {nombre}. Alguien de tu pasado reciente intentará drenar tu energía esta semana.",
            f"La alineación de tu nacimiento en {fecha_nacimiento.year} indica que encontrarás algo perdido que dabas por olvidado.",
            f"{nombre}... prepárate. Un fallo en tu sistema (o en tu rutina) te forzará a improvisar de manera caótica.",
            f"Las estrellas dicen que hoy es un buen día para escribir, {nombre}. No ignores esa idea que tienes en la cabeza."
        ]
        
        prediccion = random.choice(respuestas)
        
        st.markdown(f"""
        <div style="background: rgba(255, 215, 0, 0.1); border: 2px solid #ffd700; padding: 30px; border-radius: 10px; text-align: center; margin-top: 20px;">
            <h2 style="color: #ffd700;">Tu Destino:</h2>
            <p style="font-size: 24px;">{prediccion}</p>
        </div>
        """, unsafe_allow_html=True)
    elif revelar and not nombre:
        st.error("La estrella necesita tu nombre para leer tu destino.")
