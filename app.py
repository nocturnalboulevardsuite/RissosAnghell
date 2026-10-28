"""
EL RINCÓN DE RISSOS — Blog personal estilo lost media / VHS / años 80.

Estructura:
  - Inicio: escena animada (callejón de ladrillos + terraza en llamas) y últimas entradas.
  - Historias: relatos propios con lector tipo expediente. Cada historia puede tener
    su propio escenario animado: liminal (backrooms), naturaleza abandonada,
    castillo maldito o arañas (que además caminan por toda la página).
  - Canciones: reproductor de cassette con carretes que giran.
  - Metraje: videos e imágenes en marco VHS.
  - Videoclub: recomendaciones de películas/series.
  - Creaciones: mis apps web, apps y código. Cada creación tiene su pantalla (captura),
    una ficha de detalle con enlace "Ir a la App Web" y un tutorial con fotos paso a paso.
  - Oráculo: el pacto con la estrella negra.
  - Sala de edición: panel privado para publicar, editar y borrar.

Los datos se guardan en ./archivo/entradas.json y los archivos en ./archivo/media/.
Contraseña del panel: define ADMIN_PASSWORD en .streamlit/secrets.toml
(o como variable de entorno). Si no existe, se usa "medianoche".
"""

import base64
import html
import json
import mimetypes
import os
import random
import re
import uuid
from datetime import date
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="El Rincón de Rissos",
    page_icon="📼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# ALMACENAMIENTO
# =============================================================================
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "archivo"
MEDIA_DIR = DATA_DIR / "media"
DB_PATH = DATA_DIR / "entradas.json"
CLAVE_POR_DEFECTO = "medianoche"
LIMITE_EMBEBIDO_MB = 25  # audios más grandes usan el reproductor nativo

EXT_IMAGEN = ["png", "jpg", "jpeg", "gif", "webp"]
EXT_AUDIO = ["mp3", "wav", "ogg", "m4a"]
EXT_VIDEO = ["mp4", "webm", "mov"]

TIPOS = {
    "historia": {
        "nombre": "Historia",
        "contenido": "Texto completo (admite Markdown)",
        "extra": "Colección (ej. Anghell)",
        "ext": None,
        "portada": True,
    },
    "cancion": {
        "nombre": "Canción",
        "contenido": "Letra (opcional)",
        "extra": "Etiqueta de la cinta (ej. TDK D60)",
        "ext": EXT_AUDIO,
        "portada": False,
    },
    "video": {
        "nombre": "Video",
        "contenido": "Descripción",
        "extra": None,
        "ext": EXT_VIDEO,
        "portada": False,
    },
    "imagen": {
        "nombre": "Imagen",
        "contenido": "Descripción",
        "extra": None,
        "ext": EXT_IMAGEN,
        "portada": False,
    },
    "recomendacion": {
        "nombre": "Videoclub",
        "contenido": "Reseña",
        "extra": "Formato (Película, Serie, Anime…)",
        "ext": None,
        "portada": True,
    },
    "proyecto": {
        "nombre": "Creación",
        "contenido": "Descripción completa (admite Markdown)",
        "extra": "Tipo y tecnología (ej. App web · Streamlit · Python)",
        "ext": None,
        "portada": True,
        "enlace": True,
    },
}

SECCIONES = ["Inicio", "Historias", "Canciones", "Metraje", "Videoclub", "Creaciones", "Oráculo", "Sala de edición"]
SECCION_POR_TIPO = {
    "historia": "Historias",
    "cancion": "Canciones",
    "video": "Metraje",
    "imagen": "Metraje",
    "recomendacion": "Videoclub",
    "proyecto": "Creaciones",
}
CON_DETALLE = ("historia", "proyecto")  # tipos que se abren en su propia ficha
MESES = ["ENE.", "FEB.", "MAR.", "ABR.", "MAY.", "JUN.", "JUL.", "AGO.", "SEP.", "OCT.", "NOV.", "DIC."]


HISTORIAS_DEMO = [
    {
        "id": "demo-nivel0",
        "tipo": "historia",
        "titulo": "Nivel 0",
        "fecha": "2026-10-20",
        "extra": "Archivo liminal",
        "escena": "liminal",
        "resumen": "Me apoyé en una pared del supermercado y la pared no estaba.",
        "contenido": (
            "Me apoyé en una pared del supermercado y la pared no estaba.\n\n"
            "Caí sobre una alfombra húmeda. Olía a cartón mojado y a algo dulce, como fruta olvidada en una bolsa. "
            "Arriba, los tubos fluorescentes zumbaban todos en la misma nota, una nota que se te mete detrás de los dientes.\n\n"
            "El papel mural era amarillo. No amarillo limón: amarillo de diente viejo, de foto expuesta al sol. "
            "Un pasillo terminaba en una sala, la sala en tres pasillos, y los tres pasillos en la misma sala de antes, "
            "solo que la mancha del techo había cambiado de forma.\n\n"
            "Conté las luces para no perder la cabeza. En la luz 400 encontré la cámara.\n\n"
            "Era una videograbadora de hombro, de esas de los ochenta, apoyada contra un zócalo. La cinta seguía dentro. "
            "En el visor, la fecha decía OCT. 31 1987 y el contador avanzaba solo. Le di play. Era este pasillo. "
            "Era yo, de espaldas, contando luces en voz baja.\n\n"
            "Nadie sostenía la cámara.\n\n"
            "Al fondo de la imagen, donde el amarillo se vuelve niebla, había algo alto y delgado que no se movía. "
            "Cuando levanté la vista del visor, seguía ahí. Un poco más cerca.\n\n"
            "Ahora escribo esto en la pared con la uña, por si alguien más cae. Reglas que aprendí: no corras, porque el "
            "zumbido te sigue. No duermas bajo una luz que parpadea. Y si encuentras una cámara grabando, no mires lo que "
            "hay detrás de ti en la pantalla.\n\n"
            "Voy en la luz 612. Lo escucho caminar sobre la alfombra mojada."
        ),
        "etiquetas": ["backrooms", "liminal", "found footage"],
        "archivo": "", "url": "", "portada": "",
    },
    {
        "id": "demo-ceniza",
        "tipo": "historia",
        "titulo": "Lo que crece en Puerto Ceniza",
        "fecha": "2026-10-18",
        "extra": "Zona de cuarentena",
        "escena": "naturaleza",
        "resumen": "Veinte años después de la evacuación, el bosque terminó lo que el virus empezó.",
        "contenido": (
            "Veinte años después de la evacuación, volví a Puerto Ceniza con una mochila, una linterna y la radio de mi papá.\n\n"
            "El bosque había terminado lo que el virus empezó. Las enredaderas bajaban por los edificios como cortinas "
            "mojadas. Un árbol había crecido a través de un bus escolar y lo levantaba del suelo, con las ventanas llenas "
            "de helechos. En la avenida principal, los autos seguían en fila, esperando un semáforo que se apagó en 2006. "
            "El musgo los cubría hasta las manillas.\n\n"
            "Todo estaba en silencio, salvo los cuervos y el letrero del hotel, que todavía chispeaba: H_TEL, H_TEL, "
            "como un corazón que no se rinde.\n\n"
            "La radio captó una transmisión en la frecuencia de emergencia. Una voz de mujer leía nombres. "
            "Reconocí el de mi papá. Reconocí el mío.\n\n"
            "En la plaza, el pasto me llegaba a la cintura. Ahí vi la primera figura: alguien parado entre los arbustos, "
            "de espaldas, cubierto de hojas. Pensé que era una estatua hasta que dio un paso. Arrastraba un pie. "
            "El musgo le crecía por el cuello, por las orejas, por dentro de la boca abierta.\n\n"
            "No era uno. Eran cientos, quietos entre los árboles, enraizados a medias, girando la cabeza despacio hacia "
            "mi linterna como girasoles hacia el sol.\n\n"
            "Apagué la luz. Corrí.\n\n"
            "Desde entonces siento algo en la planta de los pies, una picazón suave, como raíces buscando tierra. "
            "La radio sigue leyendo nombres cada noche. Ya no lee el mío.\n\n"
            "Creo que es porque ya llegué."
        ),
        "etiquetas": ["survival horror", "naturaleza", "ciudad abandonada"],
        "archivo": "", "url": "", "portada": "",
    },
    {
        "id": "demo-velmora",
        "tipo": "historia",
        "titulo": "El castillo de Velmora",
        "fecha": "2026-10-15",
        "extra": "Noche de brujas",
        "escena": "castillo",
        "resumen": "La invitación decía: ven disfrazado de lo que más temes. Yo no llevé disfraz.",
        "contenido": (
            "La invitación llegó en un sobre morado, sellado con cera verde: *Ven disfrazado de lo que más temes. "
            "Velmora, 31 de octubre, medianoche.*\n\n"
            "El castillo estaba en la colina que todos en el pueblo fingen no ver. Subí por un camino de calabazas "
            "talladas. Ninguna tenía vela: las caras ardían con un fuego verde que no daba calor, y todas giraban los "
            "ojos para seguirme.\n\n"
            "Los árboles de la colina estaban muertos desde antes de que yo naciera. Aun así, sus ramas se cerraban "
            "detrás de mí, como una puerta.\n\n"
            "Adentro había música de órgano y cientos de invitados con máscaras. Bailaban sin hacer ruido con los pies. "
            "Un mayordomo muy alto me preguntó de qué venía disfrazado. Le dije que no llevaba disfraz.\n\n"
            "—Perfecto —dijo—. Entonces usted es lo que el castillo más teme.\n\n"
            "No entendí hasta que vi los espejos. Los invitados no se reflejaban. Las máscaras sí: flotaban solas, vacías, "
            "sobre vestidos que nadie llenaba. El único reflejo de carne y hueso en todo el salón era el mío.\n\n"
            "Las ventanas se encendieron de verde, una por una, como si el castillo contara a sus huéspedes. "
            "Cuando llegó a mí, la luz se puso morada.\n\n"
            "Las puertas se cerraron. Los invitados se giraron, todos a la vez, y por primera vez escuché sus pasos.\n\n"
            "No sé cuántos años llevo aquí. Cada 31 de octubre, el castillo manda invitaciones nuevas. "
            "Yo ayudo a tallar las calabazas.\n\n"
            "La tuya ya tiene cara."
        ),
        "etiquetas": ["halloween", "castillo", "gótico"],
        "archivo": "", "url": "", "portada": "",
    },
    {
        "id": "demo-viuda",
        "tipo": "historia",
        "titulo": "La viuda negra",
        "fecha": "2026-10-13",
        "extra": "Anghell",
        "escena": "aranas",
        "resumen": "Heredé el departamento de mi abuela con todo adentro. También con las arañas.",
        "contenido": (
            "Las patas crujen en la oscuridad.\n\n"
            "Heredé el departamento de mi abuela con todo adentro: los muebles con plástico, el reloj detenido a las 3:17 "
            "y las arañas. Ella nunca las mataba. Decía que las arañas cuidan las casas donde alguien murió solo.\n\n"
            "La primera noche conté siete. Una tarántula del tamaño de mi mano dormía dentro de la zapatera. "
            "Una araña saltarina me miraba desde el espejo con sus dos ojos negros enormes, siguiendo cada movimiento "
            "de mi cepillo de dientes. Las de patas largas temblaban en las esquinas del techo como si alguien soplara.\n\n"
            "Y en el centro de la sala, entre la lámpara y la ventana, había una tela perfecta. En el medio, una viuda "
            "negra con el reloj de arena rojo brillando como una brasa.\n\n"
            "Cada noche baja un poco más. El hilo de seda es café, manchado de óxido, y huele a hierro. Cada mañana hay "
            "más arañas: en las tazas, en los bolsillos de los abrigos, dentro del reloj detenido.\n\n"
            "Anoche no pude dormir. Las escuché caminar por el techo, cientos de patas pequeñas, como lluvia que cae "
            "hacia arriba. Encendí la luz y estaban todas quietas, mirando la tela.\n\n"
            "La viuda había tejido algo nuevo. No era un círculo. Eran letras.\n\n"
            "Era mi nombre.\n\n"
            "Ahora entiendo lo que decía la abuela. Las arañas no cuidan la casa. Cuidan que nadie se vaya.\n\n"
            "Si estás leyendo esto, mira tu pantalla con atención. No todas están en el dibujo."
        ),
        "etiquetas": ["anghell", "arañas"],
        "archivo": "", "url": "", "portada": "",
    },
]

CREACIONES_DEMO = [
    {
        "id": "demo-musicnow",
        "tipo": "proyecto",
        "titulo": "MusicNow",
        "fecha": "2026-10-28",
        "extra": "App web · Streamlit · Python",
        "escena": "",
        "mock": "vinilo",  # pantalla de vinilo mientras no subas una captura real
        "resumen": "Busca, reproduce y organiza tu música desde YouTube Music, con playlists que se comparten por QR.",
        "contenido": (
            "**MusicNow** es una plataforma web interactiva diseñada para buscar, reproducir y organizar tu música "
            "favorita de forma rápida, sencilla y sin interrupciones. Conectada a la vasta biblioteca de YouTube Music, "
            "la aplicación te permite explorar catálogos completos y construir listas de reproducción dinámicas en "
            "tiempo real mediante una interfaz moderna e intuitiva.\n\n"
            "🎧 Pensada tanto para el uso diario como para animar reuniones sociales, la plataforma integra funciones "
            "colaborativas como la generación automática de códigos QR para compartir tu playlist activa al instante. "
            "Su diseño combina la estética clásica del disco de vinilo con una experiencia fluida, directa y accesible "
            "para mantener la música sonando siempre."
        ),
        "etiquetas": ["streamlit", "python", "youtube music", "códigos QR"],
        "archivo": "",
        "url": "https://musicnowcl.streamlit.app/",
        "portada": "",
        "pasos": [
            {"texto": "Ingresa el nombre de la canción en el buscador.", "imagen": ""},
            {"texto": "Selecciona la canción que quieres de la lista de resultados.", "imagen": ""},
            {"texto": "La canción se reproduce y queda sonando en la playlist.", "imagen": ""},
            {"texto": "Tienes un tiempo de espera de 2 minutos para poner otra canción. ¡Disfruta!!", "imagen": ""},
        ],
    },
]

DB_INICIAL = {
    "ajustes": {
        "titulo": "El Rincón de Rissos",
        "subtitulo": "Historias, canciones y metraje encontrado",
        "autor": "Rissos",
        "bio": (
            "Escribo historias, grabo canciones y guardo cintas que nadie debería ver. "
            "Todo lo que hay aquí lo hice yo, de noche, con la tele encendida sin señal."
        ),
    },
    "demos_v2": True,
    "creaciones_v1": True,
    "entradas": [
        *HISTORIAS_DEMO,
        *CREACIONES_DEMO,
        {
            "id": "demo-jardin",
            "tipo": "historia",
            "titulo": "El jardín de espinas",
            "fecha": "2026-09-02",
            "extra": "Anghell",
            "resumen": "El aroma era dulce, pero el tallo exigía sangre para florecer.",
            "contenido": (
                "El aroma era dulce, pero el tallo exigía sangre para florecer.\n\n"
                "La abuela decía que las rosas del patio trasero nunca se regaban con agua.\n\n"
                "*Texto de ejemplo: edítalo o bórralo desde la Sala de edición.*"
            ),
            "etiquetas": ["anghell", "rosas"],
            "escena": "",
            "archivo": "",
            "url": "",
            "portada": "",
        },
        {
            "id": "demo-lluvia",
            "tipo": "cancion",
            "titulo": "Lluvia y neón",
            "fecha": "2026-08-20",
            "extra": "TDK D60",
            "resumen": "Grabada en el sótano, con la ventana abierta.",
            "contenido": "",
            "etiquetas": ["demo"],
            "archivo": "",
            "url": "https://assets.mixkit.co/active_storage/sfx/2859/2859-preview.mp3",
            "portada": "",
        },
        {
            "id": "demo-tema",
            "tipo": "cancion",
            "titulo": "Tema principal (distorsionado)",
            "fecha": "2026-07-04",
            "extra": "Maxell UR90",
            "resumen": "La cinta se comió la mitad. Así quedó.",
            "contenido": "",
            "etiquetas": ["demo"],
            "archivo": "",
            "url": "https://assets.mixkit.co/active_storage/sfx/2864/2864-preview.mp3",
            "portada": "",
        },
        {
            "id": "demo-sh",
            "tipo": "recomendacion",
            "titulo": "Silent Hill",
            "fecha": "2026-06-01",
            "extra": "Videojuego / Película",
            "resumen": "Niebla, ceniza y traumas que toman forma física.",
            "contenido": "Niebla, ceniza y traumas que toman forma física.",
            "etiquetas": [],
            "archivo": "",
            "url": "",
            "portada": "",
        },
        {
            "id": "demo-eva",
            "tipo": "recomendacion",
            "titulo": "Evangelion",
            "fecha": "2026-05-15",
            "extra": "Anime",
            "resumen": "Mechas gigantes, crisis existenciales y ángeles apocalípticos.",
            "contenido": "Mechas gigantes, crisis existenciales y ángeles apocalípticos.",
            "etiquetas": [],
            "archivo": "",
            "url": "",
            "portada": "",
        },
        {
            "id": "demo-mr",
            "tipo": "recomendacion",
            "titulo": "Mr. Robot",
            "fecha": "2026-04-10",
            "extra": "Serie",
            "resumen": "Hacking realista, ansiedad y la caída del sistema.",
            "contenido": "Hacking realista, ansiedad y la caída del sistema.",
            "etiquetas": [],
            "archivo": "",
            "url": "",
            "portada": "",
        },
    ],
}


def guardar_db(db):
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    tmp = DB_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(DB_PATH)


def cargar_db():
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    if not DB_PATH.exists():
        guardar_db(DB_INICIAL)
    try:
        db = json.loads(DB_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        st.error("No se pudo leer archivo/entradas.json. Se muestra el contenido de ejemplo.")
        db = json.loads(json.dumps(DB_INICIAL))
    db.setdefault("ajustes", {})
    for k, v in DB_INICIAL["ajustes"].items():
        db["ajustes"].setdefault(k, v)
    db.setdefault("entradas", [])
    cambio_historias = migrar_demos(db)
    cambio_creaciones = migrar_creaciones(db)
    if cambio_historias or cambio_creaciones:
        guardar_db(db)
    return db


def migrar_demos(db):
    """Agrega las historias con escenario a un archivo creado con la versión anterior (una sola vez)."""
    if db.get("demos_v2"):
        return False
    ids = {e["id"] for e in db["entradas"]}
    for demo in HISTORIAS_DEMO:
        if demo["id"] == "demo-viuda" and demo["id"] in ids:
            vieja = next(e for e in db["entradas"] if e["id"] == "demo-viuda")
            if "Texto de ejemplo" in vieja.get("contenido", ""):  # solo si no la editaste
                vieja.update(json.loads(json.dumps(demo)))
        elif demo["id"] not in ids:
            db["entradas"].append(json.loads(json.dumps(demo)))
    db["demos_v2"] = True
    return True


def migrar_creaciones(db):
    """Agrega MusicNow a un archivo creado antes de que existiera la sección Creaciones (una sola vez)."""
    if db.get("creaciones_v1"):
        return False
    ids = {e["id"] for e in db["entradas"]}
    for demo in CREACIONES_DEMO:
        if demo["id"] not in ids:
            db["entradas"].append(json.loads(json.dumps(demo)))
    db["creaciones_v1"] = True
    return True


def guardar_archivo(subida):
    if subida is None:
        return ""
    limpio = re.sub(r"[^A-Za-z0-9._-]+", "_", subida.name)[-60:]
    nombre = f"{uuid.uuid4().hex[:8]}_{limpio}"
    (MEDIA_DIR / nombre).write_bytes(subida.getbuffer())
    return nombre


def ruta_media(nombre):
    if not nombre:
        return None
    ruta = MEDIA_DIR / nombre
    return ruta if ruta.exists() else None


def borrar_media(entrada):
    nombres = [entrada.get("archivo", ""), entrada.get("portada", "")]
    nombres += [paso.get("imagen", "") for paso in entrada.get("pasos") or []]
    for nombre in nombres:
        ruta = ruta_media(nombre)
        if ruta:
            ruta.unlink(missing_ok=True)


def orden_natural(nombre):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", nombre)]


def armar_pasos(texto, fotos, anteriores=None):
    """Une las líneas del tutorial con sus fotos. Si no se suben fotos nuevas, conserva las anteriores."""
    lineas = [l.strip() for l in (texto or "").splitlines() if l.strip()]
    fotos = sorted(fotos or [], key=lambda f: orden_natural(f.name))
    anteriores = anteriores or []
    pasos = []
    for i in range(max(len(lineas), len(fotos))):
        if fotos:
            imagen = guardar_archivo(fotos[i]) if i < len(fotos) else ""
        else:
            imagen = anteriores[i].get("imagen", "") if i < len(anteriores) else ""
        pasos.append({"texto": lineas[i] if i < len(lineas) else "", "imagen": imagen})
    return pasos


def data_uri(ruta):
    mime = mimetypes.guess_type(ruta.name)[0] or "application/octet-stream"
    return f"data:{mime};base64,{base64.b64encode(ruta.read_bytes()).decode()}"


def clave_admin():
    try:
        return st.secrets["ADMIN_PASSWORD"]
    except Exception:
        return os.environ.get("ADMIN_PASSWORD", CLAVE_POR_DEFECTO)


# =============================================================================
# UTILIDADES DE PRESENTACIÓN
# =============================================================================
def esc(texto):
    return html.escape(str(texto or ""), quote=True)


def fecha_vhs(iso):
    try:
        d = date.fromisoformat(iso)
        return f"{MESES[d.month - 1]} {d.day:02d} {d.year}"
    except (TypeError, ValueError):
        return "SIN FECHA"


def ordenar(entradas):
    return sorted(entradas, key=lambda e: e.get("fecha", ""), reverse=True)


def por_tipo(db, *tipos):
    return ordenar([e for e in db["entradas"] if e["tipo"] in tipos])


def minutos_lectura(texto):
    return max(1, round(len((texto or "").split()) / 200))


def html_etiquetas(etiquetas):
    return "".join(f"<span class='tag'>{esc(t)}</span>" for t in etiquetas or [])


def encabezado(titulo, bajada=""):
    t = esc(titulo)
    st.markdown(
        f"<div class='sec-head'><h1 class='glitch' data-text='{t}'>{t}</h1>"
        f"<p class='sec-sub'>{esc(bajada)}</p></div>",
        unsafe_allow_html=True,
    )


def ir_a(seccion, leyendo=None):
    st.session_state.nav = seccion
    st.session_state.leyendo = leyendo


# =============================================================================
# ESTILOS GLOBALES
# =============================================================================
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Creepster&family=Special+Elite&family=UnifrakturMaguntia&family=VT323&display=swap');

:root{
  --negro:#050203; --panel:#0d0607; --sangre:#b3060f; --sangre-viva:#e3141f;
  --brasa:#ff6a2a; --hueso:#e9dfd3; --ceniza:#8c807a; --linea:#3a1414;
}

#MainMenu, footer, .stDeployButton, [data-testid="stAppDeployButton"]{display:none !important;}
header[data-testid="stHeader"]{background:transparent !important;}

.stApp{
  background:radial-gradient(ellipse at 50% -10%, #1c0507 0%, var(--negro) 55%) fixed;
  color:var(--hueso);
}
.stApp p, .stApp li, .stApp label, .stApp input, .stApp textarea, .stApp td, .stApp th{
  font-family:'Special Elite','Courier New',monospace;
}
.stApp p, .stApp li{color:var(--hueso); line-height:1.7;}
.block-container{padding-top:2.2rem; max-width:1180px;}

/* Atmósfera CRT: viñeta + scanlines + grano */
.stApp::before{
  content:""; position:fixed; inset:0; pointer-events:none; z-index:9990;
  background:radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,.78) 100%);
  animation:parpadeo .18s steps(2) infinite;
}
.stApp::after{
  content:""; position:fixed; inset:0; pointer-events:none; z-index:9991; opacity:.22;
  background:
    url('data:image/svg+xml,%3Csvg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"%3E%3Cfilter id="n"%3E%3CfeTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3" stitchTiles="stitch"/%3E%3C/filter%3E%3Crect width="100%25" height="100%25" filter="url(%23n)"/%3E%3C/svg%3E'),
    repeating-linear-gradient(0deg, rgba(0,0,0,.6) 0 1px, transparent 1px 3px);
  mix-blend-mode:overlay;
  animation:grano .12s steps(3) infinite;
}
@keyframes parpadeo{0%{opacity:.93}100%{opacity:1}}
@keyframes grano{0%{transform:translate(0,0)}33%{transform:translate(-1px,1px)}66%{transform:translate(1px,-1px)}}

/* Tipografía */
.stApp h2, .stApp h3, .stApp h4{
  font-family:'VT323',monospace !important; color:var(--hueso) !important;
  letter-spacing:.04em; font-weight:400 !important;
}
.stApp h2{font-size:2.2rem !important;}
.stApp h3{font-size:1.7rem !important;}

.sec-head{margin:0 0 1.6rem; border-bottom:1px solid var(--linea); padding-bottom:.9rem;}
.sec-head h1{
  font-family:'Creepster',cursive !important; font-weight:400 !important;
  font-size:clamp(2.4rem, 6vw, 4rem) !important; line-height:1 !important;
  color:var(--sangre-viva) !important; letter-spacing:.06em; margin:0 !important; padding:0 !important;
  text-shadow:0 0 18px rgba(227,20,31,.35);
  position:relative; display:inline-block;
}
.sec-sub{font-family:'VT323',monospace !important; font-size:1.35rem; color:var(--ceniza) !important; margin:.4rem 0 0 !important;}

/* Glitch de título: idle largo, tirón corto */
.glitch::before, .glitch::after{
  content:attr(data-text); position:absolute; left:0; top:0; width:100%; overflow:hidden;
  opacity:0;
}
.glitch::before{color:#ff2a2a; animation:tiron 7s infinite steps(1);}
.glitch::after{color:#3a0000; animation:tiron 7s .07s infinite steps(1);}
@keyframes tiron{
  0%,91%,100%{opacity:0; transform:none; clip-path:none;}
  92%{opacity:.85; transform:translate(-4px,1px); clip-path:inset(10% 0 55% 0);}
  94%{opacity:.85; transform:translate(4px,-1px); clip-path:inset(60% 0 8% 0);}
  96%{opacity:.6; transform:translate(-2px,0); clip-path:inset(35% 0 40% 0);}
}

/* Texto OSD y etiquetas */
.osd{font-family:'VT323',monospace; color:var(--ceniza); font-size:1.15rem; letter-spacing:.06em;}
.osd b{color:var(--sangre-viva); font-weight:400;}
.tag-escena{color:var(--sangre-viva) !important; border-color:var(--sangre) !important;}
.tag{font-family:'VT323',monospace; font-size:1rem; color:var(--ceniza); border:1px solid var(--linea);
     padding:0 .45rem; margin-right:.35rem; display:inline-block;}

/* Barra lateral */
[data-testid="stSidebar"]{background:#030102 !important; border-right:1px solid var(--linea);}
.logo{text-align:center; padding:.4rem 0 1rem; border-bottom:1px solid var(--linea); margin-bottom:.8rem;}
.logo .cinta{font-family:'Creepster',cursive; font-size:2.6rem; color:var(--sangre-viva); line-height:1;}
.logo .modo{font-family:'VT323',monospace; font-size:1.4rem; color:var(--hueso); letter-spacing:.2em;}
.pie{font-family:'VT323',monospace; color:var(--ceniza); font-size:1.05rem; text-align:center; margin-top:1.6rem;}
.pie .rec{color:var(--sangre-viva); animation:rec 1.4s steps(1) infinite;}
@keyframes rec{50%{opacity:0}}

[data-testid="stSidebar"] div[role="radiogroup"]{gap:0 !important;}
[data-testid="stSidebar"] div[role="radiogroup"] > label{
  padding:.35rem .6rem !important; margin:0 !important; border-left:2px solid transparent; width:100%;
}
[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child{display:none !important;}
[data-testid="stSidebar"] div[role="radiogroup"] > label p{
  font-family:'VT323',monospace !important; font-size:1.45rem !important; color:#857a75 !important;
  line-height:1.2 !important; white-space:nowrap;
}
[data-testid="stSidebar"] div[role="radiogroup"] > label:hover p{color:var(--hueso) !important;}
[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked){
  border-left-color:var(--sangre-viva); background:rgba(179,6,15,.12);
}
[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) p{
  color:var(--sangre-viva) !important; text-shadow:0 0 8px rgba(227,20,31,.6);
}

/* Botones */
.stButton > button, [data-testid="stFormSubmitButton"] > button, [data-testid="stDownloadButton"] > button{
  font-family:'VT323',monospace !important; font-size:1.25rem !important; letter-spacing:.05em;
  background:transparent !important; color:var(--hueso) !important;
  border:1px solid var(--sangre) !important; border-radius:0 !important; padding:.2rem 1rem !important;
  transition:background .12s, color .12s;
}
.stButton > button p, [data-testid="stFormSubmitButton"] > button p, [data-testid="stDownloadButton"] > button p{
  font-family:'VT323',monospace !important; font-size:1.25rem !important;
}
.stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover, [data-testid="stDownloadButton"] > button:hover{
  background:var(--sangre) !important; color:#fff !important;
}
button:focus-visible{outline:2px solid var(--brasa) !important; outline-offset:2px;}

/* Formularios */
[data-baseweb="input"], [data-baseweb="textarea"], [data-baseweb="select"] > div, [data-testid="stDateInput"] [data-baseweb="input"]{
  background:#0a0405 !important; border:1px solid var(--linea) !important; border-radius:0 !important;
}
[data-baseweb="input"] input, [data-baseweb="textarea"] textarea{color:var(--hueso) !important; background:transparent !important;}
[data-testid="stFileUploaderDropzone"]{background:#0a0405 !important; border:1px dashed var(--sangre) !important; border-radius:0 !important;}
[data-testid="stForm"]{border:1px solid var(--linea) !important; border-radius:0 !important; background:rgba(13,6,7,.6);}
[data-testid="stExpander"] details{border:1px solid var(--linea) !important; border-radius:0 !important; background:rgba(13,6,7,.6);}
[data-testid="stExpander"] summary p{font-family:'VT323',monospace !important; font-size:1.25rem !important;}
[data-baseweb="tab"] p{font-family:'VT323',monospace !important; font-size:1.35rem !important;}
[data-baseweb="tab-highlight"]{background:var(--sangre-viva) !important;}

/* Inicio: índice de cintas */
[class*="st-key-fila_"]{border-bottom:1px dashed var(--linea); padding:.55rem 0 .7rem;}
.fila-titulo{font-family:'Special Elite',monospace; font-size:1.2rem; color:var(--hueso); margin:0;}
.fila-resumen{color:var(--ceniza) !important; font-size:.95rem; margin:.1rem 0 0 !important;}
.bio{border-left:3px solid var(--sangre); padding:.2rem 0 .2rem 1.1rem; margin-bottom:1.4rem;}
.bio .firma{font-family:'VT323',monospace; color:var(--sangre-viva); font-size:1.3rem;}

/* Historias: expedientes */
[class*="st-key-caso_"]{
  background:linear-gradient(90deg, rgba(179,6,15,.10), rgba(13,6,7,.7) 30%);
  border-left:3px solid var(--sangre); padding:1.1rem 1.3rem .9rem; margin-bottom:.9rem;
}
.caso-titulo{font-family:'Special Elite',monospace; font-size:1.6rem; color:var(--hueso); margin:.2rem 0 .3rem;}

/* Lector */
[class*="st-key-lector_"]{
  max-width:46rem; margin:0 auto; background:#0b0506; border:1px solid var(--linea);
  padding:2.4rem clamp(1.2rem, 4vw, 3rem) 2rem; box-shadow:0 0 60px rgba(0,0,0,.8) inset;
}
[class*="st-key-lector_"] p, [class*="st-key-lector_"] li{font-size:1.12rem; line-height:1.9; color:#e3d8cb;}
.lector-titulo{font-family:'Creepster',cursive; color:var(--sangre-viva); font-size:clamp(2.2rem,5vw,3.4rem); line-height:1.05; margin:.2rem 0 .6rem;}
.fin{font-family:'VT323',monospace; text-align:center; color:var(--sangre-viva); font-size:1.4rem; letter-spacing:.3em; margin-top:2rem;}

/* Metraje */
[class*="st-key-tape_"]{background:#000; border:1px solid #241010; padding:.7rem .7rem .9rem; margin-bottom:1rem;}
[class*="st-key-tape_"] img, [class*="st-key-tape_"] video{filter:contrast(1.12) saturate(.8) sepia(.18);}
.tape-osd{display:flex; justify-content:space-between; font-family:'VT323',monospace; font-size:1.15rem; color:var(--hueso); margin-bottom:.4rem;}
.tape-osd .play{color:var(--sangre-viva);}

/* Videoclub: carátulas */
.caratula{
  aspect-ratio:2/3; background:repeating-linear-gradient(180deg,#140607 0 34px,#0d0405 34px 68px);
  border:1px solid #2a0c0c; position:relative; overflow:hidden; display:flex; flex-direction:column; justify-content:flex-end;
  padding:1rem; box-shadow:inset 0 0 40px #000;
}
.caratula .banda{position:absolute; top:0; left:0; right:0; background:var(--sangre); color:#fff;
  font-family:'VT323',monospace; font-size:1.2rem; padding:.15rem .6rem; letter-spacing:.15em;}
.caratula .nombre{font-family:'Creepster',cursive; color:var(--hueso); font-size:clamp(1.6rem,3vw,2.4rem); line-height:1;}
.caratula .formato{font-family:'VT323',monospace; color:var(--ceniza); font-size:1.15rem;}
.caratula .sticker{position:absolute; top:2.6rem; right:-.4rem; background:#f2d53c; color:#111; transform:rotate(6deg);
  font-family:'VT323',monospace; font-size:.95rem; padding:.1rem .5rem; line-height:1.1; max-width:8rem; text-align:center;}

/* Creaciones: pantallas clicables */
[class*="st-key-app_"]{
  position:relative; background:#0b0506; border:1px solid var(--linea); padding:.8rem .8rem 1rem; margin-bottom:1rem;
  transition:border-color .15s, box-shadow .15s, transform .15s;
}
[class*="st-key-app_"]:hover{border-color:var(--sangre-viva); box-shadow:0 0 26px rgba(227,20,31,.28); transform:translateY(-3px);}
[class*="st-key-app_"]:hover .app-ver span:first-child{color:var(--sangre-viva);}
[class*="st-key-verapp_"]{position:absolute !important; inset:0; z-index:6; margin:0 !important;}
[class*="st-key-verapp_"] .stButton, [class*="st-key-verapp_"] .stButton > button{width:100% !important; height:100% !important;}
[class*="st-key-verapp_"] .stButton > button, [class*="st-key-verapp_"] .stButton > button:hover{
  background:transparent !important; border:none !important; color:transparent !important; cursor:pointer;
}
[class*="st-key-verapp_"] .stButton > button p{color:transparent !important;}
.monitor{position:relative; aspect-ratio:16/10; background:#000; border:1px solid #241010; overflow:hidden;
  box-shadow:inset 0 0 40px #000;}
.monitor > img{width:100%; height:100%; object-fit:cover; object-position:top; display:block; filter:contrast(1.06) saturate(.92);}
.monitor::after{content:""; position:absolute; inset:0; pointer-events:none; z-index:3;
  background:repeating-linear-gradient(0deg, rgba(0,0,0,.28) 0 1px, transparent 1px 3px),
             radial-gradient(ellipse at center, transparent 60%, rgba(0,0,0,.55) 100%);}
.monitor .ch{position:absolute; top:.35rem; right:.6rem; z-index:4; font-family:'VT323',monospace; font-size:1.2rem;
  color:#fff; text-shadow:0 0 6px rgba(0,0,0,.9), 0 0 2px #000;}
.mock{position:absolute; inset:0; display:flex; flex-direction:column;
  background:radial-gradient(circle at 75% 60%, #2a0a12 0%, #08030a 70%);}
.mock .barra{display:flex; align-items:center; gap:.3rem; padding:.35rem .55rem; background:#140809;
  border-bottom:1px solid var(--linea); font-family:'VT323',monospace; font-size:1rem; color:var(--ceniza);}
.mock .barra i{width:.55rem; height:.55rem; border-radius:50%; background:#3a1414; display:inline-block;}
.mock .barra .url{margin-left:.4rem; margin-right:3rem; flex:1; background:#0a0405; padding:0 .5rem;
  white-space:nowrap; overflow:hidden; text-overflow:ellipsis;}
.mock .cuerpo{flex:1; position:relative; display:flex; align-items:center; padding:0 7%; overflow:hidden;}
.mock .texto{position:relative; z-index:2; max-width:62%;}
.mock .nombre-app{font-family:'Creepster',cursive; color:var(--hueso); font-size:clamp(1.6rem,3.4vw,2.8rem); line-height:1;
  text-shadow:0 0 16px rgba(227,20,31,.45);}
.mock .buscador{margin-top:.7rem; font-family:'VT323',monospace; font-size:1.05rem; color:var(--ceniza);
  border:1px solid var(--linea); background:rgba(0,0,0,.55); padding:.1rem .6rem;}
.vinilo{position:absolute; right:-10%; top:50%; width:60%; aspect-ratio:1; border-radius:50%;
  background:
    radial-gradient(circle, #050203 0 2.5%, var(--sangre-viva) 3% 15%, #111 15.5% 17%, transparent 17.5%),
    conic-gradient(from 30deg, rgba(255,255,255,.10), transparent 12%, transparent 50%, rgba(255,255,255,.07) 62%, transparent 75%),
    repeating-radial-gradient(circle, #0c0c0c 0 2px, #1a1a1a 2px 4px);
  box-shadow:0 0 34px rgba(0,0,0,.9); animation:girar 5s linear infinite;}
@keyframes girar{from{transform:translateY(-50%) rotate(0deg)} to{transform:translateY(-50%) rotate(360deg)}}
.app-nombre{font-family:'Creepster',cursive; color:var(--sangre-viva); font-size:clamp(1.8rem,3vw,2.4rem); line-height:1; margin:.8rem 0 .2rem;}
.app-resumen{color:var(--ceniza) !important; font-size:.98rem; margin:.3rem 0 .4rem !important;}
.app-ver{display:flex; justify-content:space-between; border-top:1px dashed var(--linea); padding-top:.45rem;
  font-family:'VT323',monospace; font-size:1.2rem; color:var(--hueso); letter-spacing:.05em;}
.app-ver span:last-child{color:var(--ceniza);}
.btn-app{display:inline-block; margin:.6rem 0 .3rem; font-family:'VT323',monospace; font-size:1.55rem; letter-spacing:.06em;
  background:var(--sangre); color:#fff !important; text-decoration:none !important; padding:.3rem 1.4rem;
  border:1px solid var(--sangre-viva); box-shadow:0 0 18px rgba(227,20,31,.35); transition:background .12s, box-shadow .12s;}
.btn-app:hover{background:var(--sangre-viva); box-shadow:0 0 28px rgba(227,20,31,.6);}
.btn-app:focus-visible{outline:2px solid var(--brasa); outline-offset:2px;}
.paso{background:#0b0506; border:1px solid var(--linea); padding:.6rem .6rem .8rem; height:100%;}
.paso-num{font-family:'VT323',monospace; font-size:1.3rem; color:var(--sangre-viva); letter-spacing:.15em; margin-bottom:.35rem;}
.paso-foto{aspect-ratio:4/3; background:#000; border:1px solid #241010; display:flex; align-items:center; justify-content:center; overflow:hidden;}
.paso-foto img{width:100%; height:100%; object-fit:contain; display:block;}
.paso-vacio{font-size:2.6rem; opacity:.85; filter:grayscale(.2);}
.paso-texto{font-size:1rem !important; margin:.55rem 0 0 !important;}

/* Oráculo */
.condena{border:1px solid var(--sangre); background:rgba(179,6,15,.08); padding:1.6rem; text-align:center; margin-top:1.2rem;}
.condena .osd{font-size:1.4rem; color:var(--sangre-viva);}
.condena p{font-size:1.3rem;}

/* Vacío */
.vacio{border:1px dashed var(--linea); padding:2rem; text-align:center;}
.vacio .osd{font-size:1.6rem; color:var(--sangre-viva);}

@media (prefers-reduced-motion: reduce){
  .stApp::before, .stApp::after, .glitch::before, .glitch::after, .pie .rec, .vinilo{animation:none !important;}
  [class*="st-key-app_"]:hover{transform:none;}
}
</style>
"""

# Sonidos de interfaz: clic en el menú y en botones (se crean en la página padre).
SFX_JS = """
<script>
const P = window.parent;
const doc = P.document;
if (!doc.getElementById('sfx_listo')) {
  const flag = doc.createElement('div'); flag.id = 'sfx_listo'; flag.style.display = 'none';
  doc.body.appendChild(flag);
  const menu = 'https://assets.mixkit.co/active_storage/sfx/2864/2864-preview.mp3';
  const boton = 'https://assets.mixkit.co/active_storage/sfx/2570/2570-preview.mp3';
  doc.addEventListener('mousedown', (e) => {
    let src = null, vol = .4;
    if (e.target.closest('[data-testid="stSidebar"] label')) { src = menu; vol = .5; }
    else if (e.target.closest('button')) { src = boton; }
    if (src) { const a = new P.Audio(src); a.volume = vol; a.play().catch(() => {}); }
  });
}
</script>
"""

# =============================================================================
# ESCENA DE PORTADA: callejón de ladrillos + terraza con fuego
# =============================================================================
ESCENA_HTML = r"""
<!doctype html>
<html><head><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Creepster&family=VT323&display=swap');
html,body{margin:0;height:100%;background:#000;overflow:hidden;}
#wrap{position:relative;height:100vh;overflow:hidden;background:#000;}
canvas{display:block;width:100%;height:100%;object-fit:cover;filter:contrast(1.12) saturate(1.12) blur(.35px);}
#wrap.tear canvas{filter:contrast(1.3) saturate(1.5) hue-rotate(-8deg) blur(.35px);}
.osd{position:absolute;font-family:'VT323',monospace;color:#f1ece6;font-size:clamp(18px,3.2vw,30px);
     text-shadow:2px 0 0 rgba(255,0,0,.55),-2px 0 0 rgba(0,120,255,.35);letter-spacing:.06em;z-index:5;}
.tl{top:18px;left:22px;} .tr{top:18px;right:22px;} .br{bottom:18px;right:22px;text-align:right;}
.titulo{position:absolute;left:22px;bottom:18px;z-index:5;max-width:60%;}
.titulo h1{font-family:'Creepster',cursive;font-weight:400;margin:0;color:#e3141f;line-height:.95;
  font-size:clamp(34px,6.4vw,76px);letter-spacing:.04em;text-shadow:0 0 22px rgba(255,90,20,.45),3px 0 0 rgba(60,0,0,.9);}
.titulo p{font-family:'VT323',monospace;color:#d9cfc4;margin:.3rem 0 0;font-size:clamp(16px,2.4vw,24px);}
#snd{position:absolute;top:58px;left:22px;z-index:6;background:rgba(0,0,0,.45);color:#d9cfc4;border:1px solid #6b1212;
  font-family:'VT323',monospace;font-size:18px;padding:2px 10px;cursor:pointer;}
#snd:hover{background:#b3060f;color:#fff;} #snd:focus-visible{outline:2px solid #ff6a2a;}
.fx{position:absolute;inset:0;pointer-events:none;z-index:4;}
.scan{background:repeating-linear-gradient(0deg,rgba(0,0,0,.35) 0 1px,transparent 1px 3px);}
.noise{opacity:.10;animation:jit .12s steps(3) infinite;
  background:url('data:image/svg+xml,%3Csvg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"%3E%3Cfilter id="n"%3E%3CfeTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" stitchTiles="stitch"/%3E%3C/filter%3E%3Crect width="100%25" height="100%25" filter="url(%23n)"/%3E%3C/svg%3E');}
.track{top:-10%;bottom:auto;height:22px;background:linear-gradient(180deg,transparent,rgba(255,255,255,.10),rgba(255,255,255,.03),transparent);
  animation:track 8s linear infinite;}
.vig{background:radial-gradient(ellipse at center,transparent 50%,rgba(0,0,0,.85) 100%);}
.rec{color:#e3141f;animation:blink 1.2s steps(1) infinite;}
@keyframes blink{50%{opacity:0}}
@keyframes jit{0%{transform:translate(0,0)}33%{transform:translate(-2px,1px)}66%{transform:translate(1px,-2px)}}
@keyframes track{0%{top:-10%}100%{top:110%}}
@media (max-width:600px){.titulo{max-width:85%;bottom:64px}.br{font-size:16px}}
@media (prefers-reduced-motion: reduce){.noise,.track,.rec{animation:none}.track{display:none}}
</style></head>
<body>
<div id="wrap">
  <canvas id="scene" width="1000" height="600" role="img"
    aria-label="Callejón de ladrillos de noche bajo la lluvia. Al fondo, un edificio de departamentos con una terraza cuya habitación arde."></canvas>
  <div class="fx scan"></div><div class="fx noise"></div><div class="fx track"></div><div class="fx vig"></div>
  <div class="osd tl">PLAY ►</div>
  <button id="snd" type="button">♪ Activar sonido</button>
  <div class="osd tr"><span class="rec">●</span> <span id="counter">0:00:00</span></div>
  <div class="titulo"><h1>__TITULO__</h1><p>__SUBTITULO__</p></div>
  <div class="osd br"><span id="clock">11:47:03 PM</span><br><span id="fecha">OCT. 31 1987</span></div>
</div>
<script>
(function(){
const cv=document.getElementById('scene'), ctx=cv.getContext('2d'), wrap=document.getElementById('wrap');
const W=1000,H=600,VX=500,VY=330,WX=500,Z=3.6,TOP=-560,BOT=270;
const reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
let seed=1987; function sr(){seed=(seed*16807)%2147483647;return (seed-1)/2147483646;}
function rnd(a,b){return a+Math.random()*(b-a);}
function P(s,z,y){return [VX+s*WX/z, VY+y/z];}
function poly(c,p){c.beginPath();c.moveTo(p[0][0],p[0][1]);for(let i=1;i<p.length;i++)c.lineTo(p[i][0],p[i][1]);c.closePath();c.fill();}
function capa(){const k=document.createElement('canvas');k.width=W;k.height=H;return k;}
const back=capa(), mid=capa(), front=capa();
const b=back.getContext('2d'), m=mid.getContext('2d'), f=front.getContext('2d');
const DOOR={x0:458,x1:542,y0:160,y1:232};
const TV={x:563,y:250,w:44,h:54}, W4={x:393,y:80,w:44,h:54};

/* ---------- CAPA TRASERA: cielo, ciudad, edificio ---------- */
let g=b.createLinearGradient(0,0,0,420);
g.addColorStop(0,'#020103'); g.addColorStop(.55,'#0d0408'); g.addColorStop(1,'#2b0b07');
b.fillStyle=g; b.fillRect(0,0,W,H);
for(let i=0;i<22;i++){
  const x=i*48-20, h=60+sr()*170;
  b.fillStyle=i%2?'#07030a':'#0a0509'; b.fillRect(x,300-h,44,h+200);
  for(let k=0;k<4;k++) if(sr()<.35){b.fillStyle='rgba(170,70,30,.35)';b.fillRect(x+6+sr()*30,300-h+10+sr()*h*.6,3,4);}
}
const BX0=290,BX1=710,BY0=40,BY1=405;
b.fillStyle='#160806'; b.fillRect(BX0,BY0,BX1-BX0,BY1-BY0);
for(let y=BY0+12,r=0;y<BY1;y+=7,r++){
  for(let x=BX0-(r%2)*8;x<BX1;x+=16){
    const v=sr()*26; b.fillStyle=`rgb(${44+v|0},${20+v*.45|0},${15+v*.3|0})`;
    const x0=Math.max(x,BX0); b.fillRect(x0,y,Math.min(x+14,BX1)-x0,5);
  }
}
b.fillStyle='#2e2522'; b.fillRect(BX0-8,BY0,BX1-BX0+16,12);
b.fillStyle='#1c1513'; for(let x=BX0;x<BX1;x+=10) b.fillRect(x,BY0+12,5,4);
[320,235,150].forEach(y=>{b.fillStyle='#2a211e';b.fillRect(BX0,y,BX1-BX0,4);});
function ventana(x,y,w,h,fill){
  b.fillStyle='#2a211e'; b.fillRect(x-4,y-5,w+8,5); b.fillRect(x-3,y+h,w+6,5);
  b.fillStyle=fill||'#040203'; b.fillRect(x,y,w,h);
  b.fillStyle='#1b1412'; b.fillRect(x+w/2-1,y,2,h); b.fillRect(x,y+h/2-1,w,2);
}
const cols=[330,415,500,585,670];
cols.forEach(cx=>ventana(cx-22,80,44,54,cx===415?'#2a110a':null));
cols.forEach(cx=>{if(cx!==500)ventana(cx-22,165,44,54);});
cols.forEach(cx=>ventana(cx-22,250,44,54,cx===585?'#05070d':null));
b.fillStyle='#2a211e'; b.fillRect(476,340,48,65); b.fillStyle='#0d0b0b'; b.fillRect(480,345,40,60);
b.fillStyle='#1d1817'; b.fillRect(512,375,4,3); b.fillStyle='#3a302a'; b.fillRect(494,330,12,6);
b.fillStyle='#1f1d1c'; b.fillRect(401,222,28,12); b.fillStyle='#121010'; for(let i=0;i<5;i++) b.fillRect(404+i*5,224,2,8);
b.fillStyle='rgba(0,0,0,.35)'; b.fillRect(BX0,BY0,BX1-BX0,BY1-BY0);

/* ---------- CAPA MEDIA: siluetas interiores, marco, terraza ---------- */
m.fillStyle='#000';
m.beginPath(); m.moveTo(458,160); m.lineTo(473,160); m.lineTo(468,185); m.lineTo(474,205); m.lineTo(466,232); m.lineTo(458,232); m.fill();
m.beginPath(); m.moveTo(476,232); m.lineTo(476,214); m.quadraticCurveTo(478,208,486,209); m.lineTo(512,209);
m.quadraticCurveTo(520,208,521,214); m.lineTo(521,232); m.fill();
m.fillRect(531,186,2,46); m.beginPath(); m.moveTo(525,186); m.lineTo(539,186); m.lineTo(535,176); m.lineTo(529,176); m.fill();
m.fillStyle='#1e1715'; m.fillRect(454,156,92,4); m.fillRect(454,156,4,78); m.fillRect(542,156,4,78); m.fillRect(498,160,4,72);
m.strokeStyle='rgba(255,220,200,.28)'; m.lineWidth=1; m.beginPath();
m.moveTo(503,164); m.lineTo(515,178); m.lineTo(510,190); m.moveTo(515,178); m.lineTo(531,171); m.stroke();
m.fillStyle='#231a17'; m.fillRect(430,232,140,7); m.fillStyle='#0f0a09'; m.fillRect(432,239,136,3);
m.fillStyle='#080505'; m.fillRect(440,222,10,10); m.beginPath(); m.arc(445,217,7,0,Math.PI*2); m.fill();
m.fillStyle='#0c0807'; m.fillRect(430,207,140,3); for(let x=432;x<=568;x+=7) m.fillRect(x,210,2,22);

/* ---------- CAPA DELANTERA: suelo, muros de ladrillo, basurero, farol ---------- */
let gg=f.createLinearGradient(0,405,0,600); gg.addColorStop(0,'#0c0707'); gg.addColorStop(1,'#030202');
f.fillStyle=gg; poly(f,[P(-1,1,BOT),P(1,1,BOT),P(1,Z,BOT),P(-1,Z,BOT)]);
f.strokeStyle='rgba(90,70,70,.16)';
for(let i=0;i<70;i++){const z=1+sr()*(Z-1), xw=(sr()*2-1)*WX*.9, x=VX+xw/z, y=VY+BOT/z;
  f.beginPath(); f.moveTo(x,y); f.lineTo(x+(sr()-.5)*36/z,y+sr()*4/z); f.stroke();}
f.fillStyle='#0a0808'; f.beginPath(); f.ellipse(500,VY+BOT/1.5,38,8,0,0,Math.PI*2); f.fill();
f.strokeStyle='#1c1616'; f.stroke();

function muro(s){
  const a=P(s,1,TOP), c2=P(s,Z,TOP), c=P(s,Z,BOT), d=P(s,1,BOT);
  f.fillStyle='#0b0504'; poly(f,[a,c2,c,d]);
  const bh=22, bl=0.11; let row=0;
  for(let yw=TOP; yw<BOT; yw+=bh, row++){
    const off=(row%2)*bl/2;
    for(let q=-off; q<Z-1; q+=bl){
      const z0=1+Math.max(0,q)+.004, z1=Math.min(Z,1+q+bl)-.004;
      if(z1<=z0) continue;
      const y0=yw+2, y1=yw+bh-1, v=sr();
      const dark=sr()<.06?.55:1;
      f.fillStyle=`rgb(${(48+v*34)*dark|0},${(19+v*12)*dark|0},${(16+v*9)*dark|0})`;
      poly(f,[P(s,z0,y0),P(s,z1,y0),P(s,z1,y1),P(s,z0,y1)]);
    }
  }
  const gr=f.createLinearGradient(d[0],0,c[0],0);
  gr.addColorStop(0,'rgba(0,0,0,.84)'); gr.addColorStop(1,'rgba(0,0,0,.38)');
  f.fillStyle=gr; poly(f,[a,c2,c,d]);
  const gv=f.createLinearGradient(0,VY,0,600);
  gv.addColorStop(0,'rgba(0,0,0,0)'); gv.addColorStop(1,'rgba(0,0,0,.5)');
  f.fillStyle=gv; poly(f,[P(s,1,0),P(s,Z,0),c,d]);
}
muro(-1); muro(1);
// bajada de agua en el muro izquierdo
f.strokeStyle='#120d0c'; f.lineWidth=4; f.beginPath();
let p1=P(-1,2.3,TOP), p2=P(-1,2.3,BOT); f.moveTo(p1[0]+3,p1[1]); f.lineTo(p2[0]+3,p2[1]); f.stroke(); f.lineWidth=1;
// basurero
const zA=1.3,zB=1.9,IN=WX-115,TD=BOT-115;
function Qx(z,y){return [VX+IN/z, VY+y/z];}
f.fillStyle='#060c08'; poly(f,[Qx(zA,TD),Qx(zB,TD),P(1,zB,TD),P(1,zA,TD)]);
f.fillStyle='#0a130d'; poly(f,[Qx(zA,TD),Qx(zB,TD),Qx(zB,BOT),Qx(zA,BOT)]);
f.fillStyle='#0e1911'; poly(f,[Qx(zA,TD),P(1,zA,TD),P(1,zA,BOT),Qx(zA,BOT)]);
f.fillStyle='rgba(0,0,0,.45)'; poly(f,[Qx(zA,TD),P(1,zA,TD),P(1,zA,BOT),Qx(zA,BOT)]);
// bolsas de basura
f.fillStyle='#060505';
[[90,575,52,22],[150,588,40,16],[60,556,34,18]].forEach(e=>{f.beginPath();f.ellipse(e[0],e[1],e[2],e[3],0,0,Math.PI*2);f.fill();});
// farol
f.fillStyle='#1a1614'; f.fillRect(206,246,26,3); poly(f,[[224,249],[244,249],[240,256],[228,256]]);

/* ---------- ANIMACIÓN ---------- */
const fire=[], flames=[], smoke=[], steam=[], rain=[];
for(let i=0;i<(reduce?0:240);i++) rain.push({x:rnd(-60,W),y:rnd(-H,H),l:rnd(10,26),v:rnd(10,16)});
let t=0, flick=1, tvA=.2, lampDark=0, figT=0, figNext=700, glitch=0, glitchNext=360;

function particulas(list){
  for(let i=list.length-1;i>=0;i--){
    const p=list[i]; p.age++;
    if(p.age>p.life){list.splice(i,1);continue;}
    p.x+=p.vx+Math.sin((p.age+p.y)*.15)*.25; p.y+=p.vy;
    const k=p.age/p.life;
    const c=k<.2?'255,235,170':k<.5?'255,140,35':k<.8?'200,50,12':'80,14,6';
    ctx.fillStyle=`rgba(${c},${(1-k)*.32})`;
    ctx.beginPath(); ctx.arc(p.x,p.y,p.s*(1-k*.55),0,6.283); ctx.fill();
  }
}
function figura(){
  ctx.fillStyle='#000';
  ctx.beginPath(); ctx.arc(W4.x+22,W4.y+20,6,0,6.283); ctx.fill();
  ctx.beginPath(); ctx.moveTo(W4.x+9,W4.y+54); ctx.quadraticCurveTo(W4.x+10,W4.y+30,W4.x+22,W4.y+28);
  ctx.quadraticCurveTo(W4.x+34,W4.y+30,W4.x+35,W4.y+54); ctx.fill();
  ctx.fillStyle='#1b1412'; ctx.fillRect(W4.x+21,W4.y,2,W4.h); ctx.fillRect(W4.x,W4.y+26,W4.w,2);
}

function frame(){
  t++;
  flick=.78+.14*Math.sin(t*.11)+.08*Math.sin(t*.37+2)+rnd(-.06,.06);
  ctx.globalCompositeOperation='source-over';
  ctx.drawImage(back,0,0);

  // TV azul en un departamento vecino
  if(t%5===0) tvA=.10+Math.random()*.32;
  ctx.globalCompositeOperation='lighter';
  ctx.fillStyle=`rgba(60,100,190,${tvA})`; ctx.fillRect(TV.x,TV.y,TV.w,TV.h);
  // ampolleta sobre la puerta trasera
  const bul=Math.random()<.03?.15:1;
  let bg2=ctx.createRadialGradient(500,338,1,500,338,46);
  bg2.addColorStop(0,`rgba(255,200,120,${.35*bul})`); bg2.addColorStop(1,'rgba(0,0,0,0)');
  ctx.fillStyle=bg2; ctx.fillRect(450,290,100,100);
  ctx.globalCompositeOperation='source-over';

  // alguien en la ventana del cuarto piso
  figT++;
  if(figT>figNext){ figura(); if(figT>figNext+80){figT=0; figNext=900+Math.random()*1300;} }

  // fuego dentro de la habitación
  ctx.save(); ctx.beginPath(); ctx.rect(DOOR.x0,DOOR.y0,DOOR.x1-DOOR.x0,DOOR.y1-DOOR.y0); ctx.clip();
  ctx.fillStyle=`rgb(${80+flick*60|0},${16+flick*18|0},4)`; ctx.fillRect(DOOR.x0,DOOR.y0,DOOR.x1-DOOR.x0,DOOR.y1-DOOR.y0);
  for(let i=0;i<7;i++) fire.push({x:rnd(DOOR.x0,DOOR.x1),y:DOOR.y1+4,vx:rnd(-.3,.3),vy:rnd(-1.8,-.8),s:rnd(8,18),age:0,life:rnd(30,60)});
  ctx.globalCompositeOperation='lighter'; particulas(fire);
  ctx.restore();

  ctx.globalCompositeOperation='source-over'; ctx.drawImage(mid,0,0);

  // llamas que escapan por el vidrio roto
  for(let i=0;i<2;i++) flames.push({x:rnd(470,530),y:DOOR.y0+6,vx:rnd(-.2,.3),vy:rnd(-2.2,-1.2),s:rnd(5,11),age:0,life:rnd(18,34)});
  ctx.globalCompositeOperation='lighter'; particulas(flames);

  // humo
  if(t%2===0) smoke.push({x:rnd(470,530),y:DOOR.y0,vx:rnd(.1,.45),vy:rnd(-.9,-.5),s:rnd(8,14),age:0,life:rnd(220,320)});
  ctx.globalCompositeOperation='source-over';
  for(let i=smoke.length-1;i>=0;i--){
    const p=smoke[i]; p.age++; if(p.age>p.life){smoke.splice(i,1);continue;}
    p.x+=p.vx; p.y+=p.vy; p.s+=.22; const k=p.age/p.life, a=Math.sin(Math.PI*k)*.32, w=Math.max(0,1-k*4);
    ctx.fillStyle=`rgba(${18+w*90|0},${14+w*25|0},14,${a})`;
    ctx.beginPath(); ctx.arc(p.x,p.y,p.s,0,6.283); ctx.fill();
  }

  ctx.drawImage(front,0,0);

  // luz del incendio sobre todo el callejón
  ctx.globalCompositeOperation='lighter';
  let gl=ctx.createRadialGradient(500,205,5,500,240,480);
  gl.addColorStop(0,`rgba(255,130,50,${.30*flick})`); gl.addColorStop(.22,`rgba(220,70,20,${.12*flick})`);
  gl.addColorStop(.55,`rgba(120,25,8,${.035*flick})`); gl.addColorStop(1,'rgba(0,0,0,0)');
  ctx.fillStyle=gl; ctx.fillRect(0,0,W,H);
  // reflejo en el asfalto mojado
  for(let y=420;y<592;y+=3){
    const k=(y-420)/172, w=(46+k*80)*(.8+.2*Math.sin(y*.21+t*.15)), x=500+Math.sin(y*.13+t*.09)*6;
    ctx.fillStyle=`rgba(255,110,40,${(1-k)*.11*flick})`; ctx.fillRect(x-w/2,y,w,2);
  }
  // farol que falla
  let lamp=1;
  if(lampDark>0){lampDark--; lamp=Math.random()<.35?.4:0;} else if(Math.random()<.006) lampDark=(Math.random()*16+4)|0;
  if(lamp>0){
    const lg=ctx.createLinearGradient(0,257,0,489);
    lg.addColorStop(0,`rgba(210,200,160,${.17*lamp})`); lg.addColorStop(1,'rgba(210,200,160,0)');
    ctx.fillStyle=lg; poly(ctx,[[227,257],[241,257],[330,489],[140,489]]);
    ctx.fillStyle=`rgba(255,240,200,${.8*lamp})`; ctx.fillRect(229,255,10,2);
    ctx.save(); ctx.translate(235,489); ctx.scale(1,.25);
    let pg=ctx.createRadialGradient(0,0,2,0,0,120); pg.addColorStop(0,`rgba(200,190,150,${.12*lamp})`); pg.addColorStop(1,'rgba(0,0,0,0)');
    ctx.fillStyle=pg; ctx.fillRect(-120,-120,240,240); ctx.restore();
  }
  // vapor de la alcantarilla
  ctx.globalCompositeOperation='source-over';
  if(t%4===0) steam.push({x:500+rnd(-20,20),y:508,vx:rnd(-.15,.25),vy:rnd(-.6,-.35),s:6,age:0,life:170});
  for(let i=steam.length-1;i>=0;i--){
    const p=steam[i]; p.age++; if(p.age>p.life){steam.splice(i,1);continue;}
    p.x+=p.vx; p.y+=p.vy; p.s+=.3; const a=Math.sin(Math.PI*p.age/p.life)*.022;
    ctx.fillStyle=`rgba(120,105,100,${a})`; ctx.beginPath(); ctx.arc(p.x,p.y,p.s,0,6.283); ctx.fill();
  }
  // lluvia
  if(rain.length){
    ctx.strokeStyle='rgba(200,190,190,.22)'; ctx.lineWidth=1; ctx.beginPath();
    for(const r of rain){ r.y+=r.v; r.x+=1.6; if(r.y>H){r.y=-20; r.x=rnd(-60,W);} ctx.moveTo(r.x,r.y); ctx.lineTo(r.x+r.l*.12,r.y+r.l); }
    ctx.stroke();
  }
  // desgarro de cinta
  if(!reduce){
    if(--glitchNext<=0){glitch=8; glitchNext=300+Math.random()*500;}
    if(glitch>0){
      glitch--;
      for(let i=0;i<4;i++){const y=Math.random()*H|0, h=(Math.random()*40+6)|0, dx=(Math.random()*40-20)|0; ctx.drawImage(cv,0,y,W,h,dx,y,W,h);}
      wrap.classList.add('tear');
    } else wrap.classList.remove('tear');
  }
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);

/* ---------- RELOJ DE LA CINTA ---------- */
const MES=['ENE.','FEB.','MAR.','ABR.','MAY.','JUN.','JUL.','AGO.','SEP.','OCT.','NOV.','DIC.'];
const inicio=new Date(1987,9,31,23,47,3).getTime(); let seg=0;
function dd(n){return String(n).padStart(2,'0');}
setInterval(()=>{
  seg++; const d=new Date(inicio+seg*1000); let h=d.getHours(); const ap=h>=12?'PM':'AM'; h=h%12||12;
  document.getElementById('clock').textContent=`${h}:${dd(d.getMinutes())}:${dd(d.getSeconds())} ${ap}`;
  document.getElementById('fecha').textContent=`${MES[d.getMonth()]} ${dd(d.getDate())} ${d.getFullYear()}`;
  document.getElementById('counter').textContent=`${Math.floor(seg/3600)}:${dd(Math.floor(seg/60)%60)}:${dd(seg%60)}`;
},1000);

/* ---------- SONIDO AMBIENTE SINTETIZADO (lluvia, fuego, zumbido) ---------- */
let ac=null, master=null, on=false;
const btn=document.getElementById('snd');
function iniciar(){
  ac=new (window.AudioContext||window.webkitAudioContext)();
  master=ac.createGain(); master.gain.value=.7; master.connect(ac.destination);
  const len=ac.sampleRate*3, buf=ac.createBuffer(1,len,ac.sampleRate), d=buf.getChannelData(0);
  for(let i=0;i<len;i++) d[i]=Math.random()*2-1;
  function ruido(tipo,freq,vol){
    const s=ac.createBufferSource(); s.buffer=buf; s.loop=true;
    const fl=ac.createBiquadFilter(); fl.type=tipo; fl.frequency.value=freq;
    const gn=ac.createGain(); gn.gain.value=vol; s.connect(fl).connect(gn).connect(master); s.start();
  }
  ruido('lowpass',1700,.07);   // lluvia
  ruido('lowpass',260,.16);    // rugido del fuego
  const o=ac.createOscillator(); o.type='sawtooth'; o.frequency.value=60;
  const of=ac.createBiquadFilter(); of.type='lowpass'; of.frequency.value=180;
  const og=ac.createGain(); og.gain.value=.012; o.connect(of).connect(og).connect(master); o.start();
  setInterval(()=>{ // chasquidos del fuego
    if(!on||Math.random()>.35) return;
    const s=ac.createBufferSource(); s.buffer=buf;
    const hp=ac.createBiquadFilter(); hp.type='highpass'; hp.frequency.value=900+Math.random()*2500;
    const gn=ac.createGain(); const n=ac.currentTime, dur=.01+Math.random()*.03;
    gn.gain.setValueAtTime(.0001,n); gn.gain.exponentialRampToValueAtTime(.25+Math.random()*.3,n+.002);
    gn.gain.exponentialRampToValueAtTime(.0001,n+dur);
    s.connect(hp).connect(gn).connect(master); s.start(n,Math.random()*2,dur+.02);
  },70);
}
btn.addEventListener('click',()=>{
  if(!ac){iniciar(); on=true;}
  else if(on){ac.suspend(); on=false;}
  else {ac.resume(); on=true;}
  btn.textContent=on?'♪ Silenciar':'♪ Activar sonido';
});
})();
</script>
</body></html>
"""

# =============================================================================
# REPRODUCTOR DE CASSETTE
# =============================================================================
CASSETTE_HTML = r"""
<!doctype html><html><head><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=VT323&family=Special+Elite&display=swap');
html,body{margin:0;background:transparent;font-family:'VT323',monospace;color:#e9dfd3;}
.tape{max-width:560px;margin:0 auto;padding:4px;}
.shell{position:relative;background:linear-gradient(180deg,#1c1617,#0c0909);border:2px solid #2d2324;
  border-radius:14px 14px 10px 10px;padding:14px 16px 40px;box-shadow:inset 0 0 0 6px #141010,0 10px 26px rgba(0,0,0,.65);}
.label{position:relative;background:linear-gradient(180deg,#e9dfd3 0 26%,#b3060f 26% 33%,#e9dfd3 33%);color:#1a0c0c;
  border-radius:4px;padding:6px 12px 74px;}
.brand{font-size:16px;letter-spacing:.12em;opacity:.85;}
.side{position:absolute;right:12px;top:3px;font-size:24px;}
.name{display:block;font-family:'Special Elite',monospace;font-size:20px;margin-top:12px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.window{position:absolute;left:50%;transform:translateX(-50%);bottom:50px;width:64%;height:62px;background:#060404;
  border:2px solid #3a2a2a;border-radius:31px;display:flex;align-items:center;justify-content:space-between;padding:0 10px;box-sizing:border-box;overflow:hidden;}
.reel{position:relative;width:58px;height:58px;display:grid;place-items:center;}
.pack{position:absolute;width:var(--s,40px);height:var(--s,40px);border-radius:50%;background:radial-gradient(circle,#3a2418 40%,#22140d 100%);transition:width .3s,height .3s;}
.hub{position:relative;width:24px;height:24px;border-radius:50%;
  background:radial-gradient(circle,#060404 0 4px,transparent 5px),repeating-conic-gradient(#e9dfd3 0 22deg,#1a1212 22deg 60deg);}
.band{flex:1;height:4px;background:#22140d;margin:0 4px;}
.on .hub{animation:spin 1.6s linear infinite;}
@keyframes spin{to{transform:rotate(360deg)}}
.foot{position:absolute;left:18%;right:18%;bottom:0;height:30px;background:#141011;border:2px solid #2d2324;border-bottom:none;
  clip-path:polygon(8% 0,92% 0,100% 100%,0 100%);}
.screw{position:absolute;width:8px;height:8px;border-radius:50%;background:#3a3030;}
.deck{display:flex;align-items:center;gap:10px;margin-top:12px;}
button{background:transparent;color:#e9dfd3;border:1px solid #b3060f;font-family:'VT323',monospace;font-size:20px;padding:2px 12px;cursor:pointer;}
button:hover{background:#b3060f;color:#fff;} button:focus-visible{outline:2px solid #ff6a2a;outline-offset:2px;}
.bar{flex:1;height:8px;background:#1a0b0c;border:1px solid #3a1414;cursor:pointer;position:relative;}
#prog{height:100%;width:0;background:#e3141f;box-shadow:0 0 8px #e3141f;}
#time{min-width:96px;text-align:right;font-size:19px;color:#8c807a;}
@media (prefers-reduced-motion: reduce){.on .hub{animation:none}}
</style></head><body>
<div class="tape" id="tape">
  <div class="shell">
    <div class="screw" style="left:8px;top:8px"></div><div class="screw" style="right:8px;top:8px"></div>
    <div class="screw" style="left:8px;bottom:8px"></div><div class="screw" style="right:8px;bottom:8px"></div>
    <div class="label"><span class="brand">__CINTA__</span><span class="side">A</span><span class="name">__TITULO__</span></div>
    <div class="window"><div class="reel"><div class="pack" id="p1"></div><div class="hub"></div></div><div class="band"></div>
      <div class="reel"><div class="pack" id="p2"></div><div class="hub"></div></div></div>
    <div class="foot"></div>
  </div>
  <div class="deck">
    <button id="play" type="button" aria-label="Reproducir o pausar">► PLAY</button>
    <button id="stop" type="button" aria-label="Detener">■ STOP</button>
    <div class="bar" id="bar" aria-label="Posición"><div id="prog"></div></div>
    <span id="time">0:00 / 0:00</span>
  </div>
  <audio id="a" preload="metadata" src="__SRC__"></audio>
</div>
<script>
const a=document.getElementById('a'), tape=document.getElementById('tape'), play=document.getElementById('play'),
      prog=document.getElementById('prog'), time=document.getElementById('time'), bar=document.getElementById('bar'),
      p1=document.getElementById('p1'), p2=document.getElementById('p2');
function fmt(s){if(!isFinite(s))return '0:00';return Math.floor(s/60)+':'+String(Math.floor(s%60)).padStart(2,'0');}
function upd(){const p=a.duration?a.currentTime/a.duration:0; prog.style.width=(p*100)+'%';
  time.textContent=fmt(a.currentTime)+' / '+fmt(a.duration);
  p1.style.setProperty('--s',(22+34*(1-p))+'px'); p2.style.setProperty('--s',(22+34*p)+'px');}
play.onclick=()=>{a.paused?a.play().catch(()=>{time.textContent='SIN SEÑAL';}):a.pause();};
document.getElementById('stop').onclick=()=>{a.pause();a.currentTime=0;upd();};
a.onplay=()=>{tape.classList.add('on');play.textContent='❚❚ PAUSA';};
a.onpause=()=>{tape.classList.remove('on');play.textContent='► PLAY';};
a.ontimeupdate=upd; a.onloadedmetadata=upd; a.onerror=()=>{time.textContent='SIN SEÑAL';};
bar.onclick=e=>{const r=bar.getBoundingClientRect(); if(a.duration) a.currentTime=(e.clientX-r.left)/r.width*a.duration;};
upd();
</script></body></html>
"""


def incrustar(doc, alto):
    """Incrusta HTML con JavaScript (st.iframe en Streamlit nuevo, components.html en versiones previas)."""
    if hasattr(st, "iframe"):
        st.iframe(doc, height=max(alto, 1))
    else:
        components.html(doc, height=alto)


# =============================================================================
# ESCENARIOS DE HISTORIAS (cada historia puede tener su propia página animada)
# =============================================================================
ESCENAS = {
    "": "Clásico (sin escenario)",
    "liminal": "Liminal (backrooms)",
    "naturaleza": "Naturaleza abandonada",
    "castillo": "Castillo maldito",
    "aranas": "Arañas",
}

ESCENA_BASE = r"""
<!doctype html>
<html><head><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Creepster&family=Special+Elite&family=UnifrakturMaguntia&family=VT323&display=swap');
html,body{margin:0;height:100%;background:#000;overflow:hidden;}
#wrap{position:relative;height:100vh;overflow:hidden;background:#000;}
canvas{display:block;width:100%;height:100%;object-fit:cover;filter:contrast(1.08) saturate(1.08) blur(.3px);}
.fx{position:absolute;inset:0;pointer-events:none;z-index:4;}
.scan{background:repeating-linear-gradient(0deg,rgba(0,0,0,.28) 0 1px,transparent 1px 3px);}
.noise{opacity:.09;animation:jit .12s steps(3) infinite;
  background:url('data:image/svg+xml,%3Csvg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"%3E%3Cfilter id="n"%3E%3CfeTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" stitchTiles="stitch"/%3E%3C/filter%3E%3Crect width="100%25" height="100%25" filter="url(%23n)"/%3E%3C/svg%3E');}
.vig{background:radial-gradient(ellipse at center,transparent 50%,rgba(0,0,0,.8) 100%);}
.osd{position:absolute;font-family:'VT323',monospace;color:#f1ece6;font-size:clamp(16px,2.8vw,26px);letter-spacing:.06em;z-index:5;
  text-shadow:2px 0 0 rgba(255,0,0,.5),-2px 0 0 rgba(0,120,255,.3);}
.tl{top:16px;left:20px;} .tr{top:16px;right:20px;}
.titulo{position:absolute;left:20px;bottom:16px;z-index:5;max-width:80%;}
.titulo .meta{font-family:'VT323',monospace;font-size:clamp(15px,2.2vw,22px);letter-spacing:.08em;color:#e9dfd3;}
.titulo h1{margin:.1em 0 0;font-weight:400;line-height:.95;font-size:clamp(32px,6vw,72px);}
.ctl{position:absolute;left:20px;z-index:6;background:rgba(0,0,0,.45);color:#e9dfd3;border:1px solid rgba(255,255,255,.35);
  font-family:'VT323',monospace;font-size:18px;padding:2px 10px;cursor:pointer;}
.ctl:hover{background:rgba(255,255,255,.15);} .ctl:focus-visible{outline:2px solid #ff6a2a;}
#snd{top:54px;} #ctl2{top:86px;}
.rec{color:#e3141f;animation:blink 1.2s steps(1) infinite;}
@keyframes blink{50%{opacity:0}}
@keyframes jit{0%{transform:translate(0,0)}33%{transform:translate(-2px,1px)}66%{transform:translate(1px,-2px)}}
@media (max-width:600px){.titulo{max-width:92%}}
@media (prefers-reduced-motion: reduce){.noise,.rec{animation:none}}
__TEMA_CSS__
</style></head>
<body>
<div id="wrap">
  <canvas id="cv" width="1000" height="600" role="img" aria-label="__ALT__"></canvas>
  <div class="fx scan"></div><div class="fx noise"></div><div class="fx vig"></div>
  <div class="osd tl">__OSD__</div>
  <button id="snd" class="ctl" type="button">♪ Activar sonido</button>
  <div class="osd tr"><span class="rec">●</span> <span id="clk">0:00:00</span></div>
  <div class="titulo"><div class="meta">__META__</div><h1>__TITULO__</h1></div>
</div>
<script>
(function(){
const cv=document.getElementById('cv'), ctx=cv.getContext('2d'), wrap=document.getElementById('wrap');
const W=1000, H=600, reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
let seed=__SEED__; function sr(){seed=(seed*16807)%2147483647;return (seed-1)/2147483646;}
function rnd(a,b){return a+Math.random()*(b-a);}
function capa(w,h){const k=document.createElement('canvas');k.width=w||W;k.height=h||H;return k;}
function poly(c,p){c.beginPath();c.moveTo(p[0][0],p[0][1]);for(let i=1;i<p.length;i++)c.lineTo(p[i][0],p[i][1]);c.closePath();c.fill();}
function dd(n){return String(n).padStart(2,'0');}
let t=0, seg=0;
setInterval(()=>{seg++;document.getElementById('clk').textContent=`${Math.floor(seg/3600)}:${dd(Math.floor(seg/60)%60)}:${dd(seg%60)}`;},1000);

/* --- audio sintetizado compartido --- */
let ac=null, master=null, on=false, RB=null;
function ruido(){if(!RB){const n=ac.sampleRate*3;RB=ac.createBuffer(1,n,ac.sampleRate);const d=RB.getChannelData(0);for(let i=0;i<n;i++)d[i]=Math.random()*2-1;}return RB;}
function lazo(tipo,freq,vol,q){const s=ac.createBufferSource();s.buffer=ruido();s.loop=true;const f=ac.createBiquadFilter();f.type=tipo;f.frequency.value=freq;if(q)f.Q.value=q;const g=ac.createGain();g.gain.value=vol;s.connect(f).connect(g).connect(master);s.start();return {f,g};}
function tono(tipo,freq,vol){const o=ac.createOscillator();o.type=tipo;o.frequency.value=freq;const g=ac.createGain();g.gain.value=vol;o.connect(g).connect(master);o.start();return {o,g};}
function lfo(param,rate,depth){const o=ac.createOscillator();o.frequency.value=rate;const g=ac.createGain();g.gain.value=depth;o.connect(g).connect(param);o.start();}
function golpe(tipo,freq,vol,dur){if(!ac||!on)return;const n=ac.currentTime,s=ac.createBufferSource();s.buffer=ruido();const f=ac.createBiquadFilter();f.type=tipo;f.frequency.value=freq;const g=ac.createGain();g.gain.setValueAtTime(.0001,n);g.gain.exponentialRampToValueAtTime(vol,n+Math.min(.02,dur*.2));g.gain.exponentialRampToValueAtTime(.0001,n+dur);s.connect(f).connect(g).connect(master);s.start(n,Math.random()*1.5,dur+.05);}
function pitido(f0,f1,vol,dur,tipo){if(!ac||!on)return;const n=ac.currentTime,o=ac.createOscillator();o.type=tipo||'sine';o.frequency.setValueAtTime(f0,n);o.frequency.exponentialRampToValueAtTime(f1,n+dur);const g=ac.createGain();g.gain.setValueAtTime(.0001,n);g.gain.exponentialRampToValueAtTime(vol,n+.01);g.gain.exponentialRampToValueAtTime(.0001,n+dur);o.connect(g).connect(master);o.start(n);o.stop(n+dur+.05);}
const btnSnd=document.getElementById('snd');
btnSnd.addEventListener('click',()=>{
  if(!ac){ac=new (window.AudioContext||window.webkitAudioContext)();master=ac.createGain();master.gain.value=.7;master.connect(ac.destination);on=true;sonido();}
  else if(on){ac.suspend();on=false;} else {ac.resume();on=true;}
  btnSnd.textContent=on?'♪ Silenciar':'♪ Activar sonido';
});
function aCanvas(cx,cy){const r=cv.getBoundingClientRect(),sc=Math.max(r.width/W,r.height/H);return [(cx-r.left-(r.width-W*sc)/2)/sc,(cy-r.top-(r.height-H*sc)/2)/sc];}

__JS__
})();
</script></body></html>
"""

# ----------------------------------------------------------------- LIMINAL ---
JS_LIMINAL = r"""
const F=430,VX=500,VY=285,XW=1.2,YC=-.8,YF=1,L=1.5,N=18,ZN=.32,FOG=[196,182,118];
const WALL=[212,192,104],CEIL=[176,166,118],CARP=[124,106,58],DARK=[74,64,32];
function pr(x,y,z){return [VX+x*F/z,VY+y*F/z];}
function col(rgb,z,m){const k=1-Math.exp(-z*.13);m=m||1;return `rgb(${rgb[0]*m*(1-k)+FOG[0]*k|0},${rgb[1]*m*(1-k)+FOG[1]*k|0},${rgb[2]*m*(1-k)+FOG[2]*k|0})`;}
function hs(n){const x=Math.sin(n*127.1+311.7)*43758.5453;return x-Math.floor(x);}
function quad(p,c){ctx.fillStyle=c;poly(ctx,p);}
function linea(p1,p2){ctx.moveTo(p1[0],p1[1]);ctx.lineTo(p2[0],p2[1]);}
let cam=0, ent=null, entNext=500;
function frame(){
  t++; if(!reduce) cam+=.012;
  const base=Math.floor(cam/L), off=cam-base*L;
  ctx.fillStyle=`rgb(${FOG})`; ctx.fillRect(0,0,W,H);
  ctx.save();
  if(!reduce) ctx.translate(Math.sin(t*.021)*5,Math.sin(t*.06)*2.5);
  const luces=[];
  for(let i=N-1;i>=0;i--){
    const idx=base+i, z0=i*L-off+ZN, z1=z0+L;
    if(z1<=ZN) continue;
    const a=Math.max(z0,ZN);
    quad([pr(-XW,YC,a),pr(XW,YC,a),pr(XW,YC,z1),pr(-XW,YC,z1)],col(CEIL,a));
    quad([pr(-XW,YF,a),pr(XW,YF,a),pr(XW,YF,z1),pr(-XW,YF,z1)],col(CARP,a));
    const puerta=hs(idx)<.35, lado=hs(idx+9)<.5?-1:1;
    for(const s of [-1,1]){
      const x=s*XW, conPuerta=puerta&&s===lado, d0=z0+L*.35, d1=z0+L*.75, top=-.25;
      if(conPuerta){
        if(a<d0) quad([pr(x,YC,a),pr(x,YC,d0),pr(x,YF,d0),pr(x,YF,a)],col(WALL,a));
        const b0=Math.max(d0,a);
        if(b0<d1){
          quad([pr(x,YC,b0),pr(x,YC,d1),pr(x,top,d1),pr(x,top,b0)],col(WALL,b0));
          quad([pr(x,top,b0),pr(x,top,d1),pr(x,YF,d1),pr(x,YF,b0)],col(DARK,b0));
          quad([pr(x*1.6,top,d1),pr(x,top,d1),pr(x,YF,d1),pr(x*1.6,YF,d1)],col(WALL,d1,.8));
        }
        const c0=Math.max(d1,a); if(c0<z1) quad([pr(x,YC,c0),pr(x,YC,z1),pr(x,YF,z1),pr(x,YF,c0)],col(WALL,c0));
      } else quad([pr(x,YC,a),pr(x,YC,z1),pr(x,YF,z1),pr(x,YF,a)],col(WALL,a));
      quad([pr(x,YF-.07,a),pr(x,YF-.07,z1),pr(x,YF,z1),pr(x,YF,a)],col(WALL,a,.7));
      ctx.strokeStyle=col(WALL,a,.84); ctx.lineWidth=1; ctx.beginPath();
      for(let k=0;k<6;k++){const z=z0+k*L/6; if(z<=ZN||(conPuerta&&z>d0&&z<d1)) continue; linea(pr(x,YC,z),pr(x,YF-.07,z));}
      ctx.stroke();
    }
    ctx.strokeStyle=col(CEIL,a,.74); ctx.beginPath();
    for(const zz of [z0,z0+L/2]) if(zz>ZN) linea(pr(-XW,YC,zz),pr(XW,YC,zz));
    for(const xx of [-.6,0,.6]) linea(pr(xx,YC,a),pr(xx,YC,z1));
    ctx.stroke();
    const lz0=z0+L*.3, lz1=z0+L*.6;
    if(lz1>ZN){
      const la=Math.max(lz0,ZN); let br=1;
      if(hs(idx+3)<.15) br=Math.random()<.12?.15:(Math.random()<.5?.7:1);
      quad([pr(-.3,YC,la),pr(.3,YC,la),pr(.3,YC,lz1),pr(-.3,YC,lz1)],col([255,250,215],la,br));
      luces.push({z:(la+lz1)/2,br});
    }
  }
  // algo alto y delgado al fondo del pasillo
  if(!reduce&&!ent&&--entNext<=0) ent={z:cam+N*L*.72,life:0};
  if(ent){
    ent.life++; const z=ent.z-cam;
    if(z<4.5||ent.life>260){ent=null; entNext=900+Math.random()*1200;}
    else if(Math.random()>.05){
      const p=pr(0,YF,z), hpx=(YF+.6)*F/z, w=.12*F/z, k=1-Math.exp(-z*.13);
      ctx.fillStyle=`rgba(28,22,10,${Math.min(.95,(1-k)*1.1+.1)})`;
      const yt=p[1]-hpx;
      ctx.beginPath(); ctx.ellipse(p[0],yt+w*.9,w*.55,w*.85,0,0,6.283); ctx.fill();
      ctx.fillRect(p[0]-w/2,yt+w*1.6,w,hpx-w*1.6);
      ctx.fillRect(p[0]-w*.85,yt+w*1.9,w*.25,hpx*.58); ctx.fillRect(p[0]+w*.6,yt+w*1.9,w*.25,hpx*.58);
    }
  }
  ctx.globalCompositeOperation='lighter';
  for(const l of luces){
    const p=pr(0,YC,l.z), r=1.7*F/l.z, k=Math.exp(-l.z*.13);
    const g=ctx.createRadialGradient(p[0],p[1],0,p[0],p[1],r);
    g.addColorStop(0,`rgba(255,240,180,${.12*l.br*k})`); g.addColorStop(1,'rgba(0,0,0,0)');
    ctx.fillStyle=g; ctx.fillRect(p[0]-r,p[1]-r,2*r,2*r);
  }
  ctx.globalCompositeOperation='source-over';
  ctx.restore();
  ctx.fillStyle=`rgba(255,235,150,${.04+.03*Math.sin(t*.013)})`; ctx.fillRect(0,0,W,H);
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
function sonido(){
  const o=ac.createOscillator(); o.type='sawtooth'; o.frequency.value=120;
  const f=ac.createBiquadFilter(); f.type='bandpass'; f.frequency.value=480; f.Q.value=3;
  const g=ac.createGain(); g.gain.value=.045; o.connect(f).connect(g).connect(master); o.start();
  lfo(g.gain,.23,.015); tono('sine',60,.04); lazo('lowpass',450,.025);
  setInterval(()=>{if(Math.random()<.25) golpe('bandpass',2400,.05,.04);},400);
}
"""

# -------------------------------------------------------------- NATURALEZA ---
JS_NATURALEZA = r"""
const LW=1160;
const lejos=capa(LW,H), medio=capa(LW,H), cerca=capa(LW,H);
function rama(c,x,y,a,l,w,d){const x2=x+Math.cos(a)*l,y2=y+Math.sin(a)*l;c.lineWidth=w;c.beginPath();c.moveTo(x,y);c.lineTo(x2,y2);c.stroke();
  if(d>0){rama(c,x2,y2,a-.35-sr()*.35,l*.72,w*.68,d-1);rama(c,x2,y2,a+.35+sr()*.35,l*.72,w*.68,d-1);}}
function arbol(c,x,y,h,osc){c.strokeStyle='#1a170f';rama(c,x,y,-Math.PI/2+(sr()-.5)*.2,h*.34,h*.06,4);
  for(let i=0;i<18;i++){c.fillStyle=`rgba(${(40+sr()*30)*osc|0},${(70+sr()*40)*osc|0},${(28+sr()*16)*osc|0},.88)`;
    c.beginPath();c.arc(x+(sr()-.5)*h*.9,y-h*.62+(sr()-.5)*h*.5,8+sr()*h*.17,0,6.283);c.fill();}}
function enredadera(c,x,y,len){c.strokeStyle='#26381c';c.lineWidth=2;c.beginPath();c.moveTo(x,y);let px=x,py=y;const pts=[];
  for(let k=0;k<len;k+=8){px+=(sr()-.5)*8;py+=8;c.lineTo(px,py);pts.push([px,py]);}c.stroke();
  for(const p of pts) if(sr()<.8){c.fillStyle=sr()<.5?'#3d6128':'#54803a';c.beginPath();c.ellipse(p[0]+(sr()-.5)*8,p[1],3+sr()*3,2+sr()*2,sr()*3,0,6.283);c.fill();}}
function edificio(c,x,w,h,base){
  const y=base-h; c.fillStyle='#2f3128'; c.fillRect(x,y,w,h);
  for(let i=0;i<40;i++){c.fillStyle=`rgba(0,0,0,${sr()*.16})`;c.fillRect(x+sr()*w,y,2+sr()*4,h*sr());}
  for(let wy=y+18;wy<base-40;wy+=34) for(let wx=x+12;wx<x+w-26;wx+=30){
    const r=sr(); c.fillStyle=r<.5?'#0c0f0a':r<.8?'#1a2016':'#3a4a3a'; c.fillRect(wx,wy,16,22);
    if(r<.3){c.fillStyle='rgba(160,180,170,.22)';c.beginPath();c.moveTo(wx,wy);c.lineTo(wx+16,wy);c.lineTo(wx+5,wy+10);c.fill();}}
  c.globalCompositeOperation='destination-out';
  c.beginPath();c.moveTo(x+w*.6,y-1);c.lineTo(x+w+1,y-1);c.lineTo(x+w+1,y+h*.18);c.lineTo(x+w*.82,y+h*.1);c.fill();
  c.globalCompositeOperation='source-over';
  for(let i=0;i<30;i++){c.fillStyle=`rgba(${60+sr()*30|0},${90+sr()*40|0},${40+sr()*20|0},${.3+sr()*.4})`;
    c.beginPath();c.ellipse(x+sr()*w,y+(sr()<.5?sr()*h*.3:h*.7+sr()*h*.3),6+sr()*16,4+sr()*8,0,0,6.283);c.fill();}
  for(let i=0;i<7;i++) enredadera(c,x+sr()*w,y+4,80+sr()*h*.7);
  if(sr()<.7) arbol(c,x+w*.3,y+2,50+sr()*40,1);
}
function auto(c,x,y){
  c.fillStyle='#24271f';
  poly(c,[[x,y],[x+8,y-26],[x+55,y-30],[x+80,y-55],[x+165,y-55],[x+195,y-30],[x+235,y-24],[x+240,y]]);
  c.fillStyle='#0b0c09'; poly(c,[[x+86,y-50],[x+120,y-50],[x+120,y-31],[x+66,y-31]]); poly(c,[[x+128,y-50],[x+160,y-50],[x+185,y-31],[x+128,y-31]]);
  c.fillStyle='#0a0a08'; [x+50,x+190].forEach(wx=>{c.beginPath();c.ellipse(wx,y+2,20,13,0,0,6.283);c.fill();});
  for(let i=0;i<30;i++){c.fillStyle=sr()<.5?`rgba(110,60,25,${.3+sr()*.3})`:`rgba(70,105,40,${.4+sr()*.4})`;
    c.beginPath();c.ellipse(x+20+sr()*200,y-50+sr()*48,4+sr()*10,3+sr()*6,0,0,6.283);c.fill();}
  for(let i=0;i<4;i++) enredadera(c,x+80+sr()*90,y-55,30+sr()*30);
}
(()=>{const c=lejos.getContext('2d'); let x=-10;
  while(x<LW){const w=40+sr()*70,h=120+sr()*200; c.fillStyle='#3d4a37'; c.beginPath(); c.moveTo(x,440); c.lineTo(x,440-h);
    for(let k=1;k<=4;k++) c.lineTo(x+w*k/4,440-h+(sr()-.3)*h*.25); c.lineTo(x+w,440); c.fill();
    c.fillStyle='rgba(30,36,26,.7)'; for(let wy=440-h+20;wy<420;wy+=16) for(let wx=x+6;wx<x+w-8;wx+=12) if(sr()<.6) c.fillRect(wx,wy,5,7);
    if(sr()<.4) arbol(c,x+w/2,440-h+10,40,1.1);
    x+=w+sr()*10;}
  c.globalCompositeOperation='source-atop'; c.fillStyle='rgba(95,110,80,.4)'; c.fillRect(0,0,LW,H);})();
const letrero={x:318,y:228};
(()=>{const c=medio.getContext('2d');
  [[30,210,300],[290,170,230],[500,240,345],[790,190,270],[1000,150,210]].forEach(b=>edificio(c,b[0],b[1],b[2],470));
  c.fillStyle='#262820'; c.fillRect(0,470,LW,22); c.fillStyle='#1c1e17'; for(let x=0;x<LW;x+=40) c.fillRect(x,470,2,22);
  c.strokeStyle='#14160f'; c.lineWidth=5; c.beginPath(); c.moveTo(470,472); c.lineTo(520,330); c.lineTo(560,334); c.stroke();
  enredadera(c,505,370,90);
  c.fillStyle='#14150f'; c.fillRect(letrero.x-6,letrero.y-4,150,32);
  c.globalCompositeOperation='source-atop'; c.fillStyle='rgba(60,72,50,.3)'; c.fillRect(0,0,LW,H);})();
(()=>{const c=cerca.getContext('2d');
  const g=c.createLinearGradient(0,490,0,H); g.addColorStop(0,'#2b2d23'); g.addColorStop(1,'#14150f'); c.fillStyle=g; c.fillRect(0,490,LW,H-490);
  c.fillStyle='rgba(190,170,90,.22)'; for(let x=0;x<LW;x+=90) c.fillRect(x,545,50,4);
  c.strokeStyle='#0f100b'; c.lineWidth=1.5;
  for(let i=0;i<26;i++){let x=sr()*LW,y=495+sr()*100; c.beginPath(); c.moveTo(x,y);
    for(let k=0;k<5;k++){x+=(sr()-.3)*30;y+=(sr()-.5)*8;c.lineTo(x,y);} c.stroke();
    c.fillStyle='#3d5a26'; for(let k=0;k<6;k++) c.fillRect(x-10+sr()*20,y-6+sr()*6,2,5+sr()*6);}
  auto(c,600,522);
  c.fillStyle='#3a3626'; c.fillRect(150,500,140,14); c.fillRect(160,514,8,32); c.fillRect(272,514,8,32);
  c.fillStyle='rgba(200,160,40,.55)'; for(let x=158;x<284;x+=24) poly(c,[[x,500],[x+12,500],[x+4,514],[x-8,514]]);
  enredadera(c,165,500,40);
  arbol(c,60,610,340,.55); arbol(c,1110,610,300,.55);
  for(let i=0;i<40;i++){c.fillStyle=`rgba(${25+sr()*25|0},${45+sr()*35|0},${18+sr()*15|0},.95)`;c.beginPath();c.arc(sr()*LW,588+sr()*30,14+sr()*26,0,6.283);c.fill();}
})();
const niebla=[]; for(let i=0;i<7;i++) niebla.push({x:rnd(0,W),y:rnd(330,560),rx:rnd(180,380),ry:rnd(30,60),v:rnd(.1,.35),a:rnd(.05,.12)});
function nuevaHoja(ini){return {x:rnd(0,W),y:ini?rnd(0,H):-10,vy:rnd(.4,1.1),vx:rnd(-.3,.6),r:rnd(0,6),vr:rnd(-.08,.08),s:rnd(3,6),c:['#6b7a2a','#8a6a24','#4f6b2c','#9a5a1c'][Math.random()*4|0],f:rnd(0,6)};}
const hojas=[]; for(let i=0;i<(reduce?0:45);i++) hojas.push(nuevaHoja(true));
const esporas=[]; for(let i=0;i<30;i++) esporas.push({x:rnd(0,W),y:rnd(250,600),f:rnd(0,6)});
const pasto=[]; for(let i=0;i<170;i++) pasto.push({x:rnd(0,W),h:rnd(14,42),f:rnd(0,6),c:['#2f4a1f','#3d5e26','#4a6b2c'][Math.random()*3|0]});
let zombi=null, zNext=300, bandada=null, bNext=600;
function niebla_(desde,hasta){for(let i=desde;i<hasta;i++){const n=niebla[i]; if(!reduce){n.x+=n.v; if(n.x-n.rx>W) n.x=-n.rx;}
  ctx.save(); ctx.translate(n.x,n.y); ctx.scale(1,n.ry/n.rx);
  const g=ctx.createRadialGradient(0,0,0,0,0,n.rx); g.addColorStop(0,`rgba(170,185,150,${n.a})`); g.addColorStop(1,'rgba(170,185,150,0)');
  ctx.fillStyle=g; ctx.fillRect(-n.rx,-n.rx,2*n.rx,2*n.rx); ctx.restore();}}
function dibujarZombi(x,y,f){
  const bob=Math.abs(Math.sin(f))*2.5; ctx.fillStyle='#0e110b'; ctx.save(); ctx.translate(x,y-bob); ctx.rotate(.12);
  ctx.beginPath(); ctx.arc(3,-44,5,0,6.283); ctx.fill(); ctx.fillRect(-5,-38,10,20);
  ctx.fillRect(4,-35,14,3); ctx.fillRect(4,-30,12,3);
  const p=Math.sin(f)*5; ctx.fillRect(-4+p*.4,-18,4,18); ctx.fillRect(1-p*.4,-18,4,16); ctx.restore();}
function frame(){
  t++;
  const pan=reduce?0:Math.sin(t*.0022)*70;
  let g=ctx.createLinearGradient(0,0,0,H); g.addColorStop(0,'#1b2219'); g.addColorStop(.5,'#3c4a35'); g.addColorStop(.75,'#6b7656'); g.addColorStop(1,'#2a3122');
  ctx.fillStyle=g; ctx.fillRect(0,0,W,H);
  g=ctx.createRadialGradient(700,190,10,700,190,220); g.addColorStop(0,'rgba(220,225,170,.35)'); g.addColorStop(1,'rgba(0,0,0,0)'); ctx.fillStyle=g; ctx.fillRect(0,0,W,H);
  ctx.drawImage(lejos,-80+pan*.25,0);
  niebla_(0,3);
  const om=-80+pan*.55;
  ctx.drawImage(medio,om,0);
  // letrero de hotel que todavía chispea
  ctx.font='bold 24px VT323, monospace'; ctx.textBaseline='top';
  'HOTEL'.split('').forEach((ch,i)=>{
    let encendida=true; if(i===1) encendida=Math.random()<.03; if(i===3) encendida=((t>>3)%7)!==0&&Math.random()>.05;
    ctx.fillStyle=encendida?'#ff5a3c':'#3a1e18'; ctx.shadowColor='#ff5a3c'; ctx.shadowBlur=encendida?12:0;
    ctx.fillText(ch,letrero.x+om+i*28,letrero.y);});
  ctx.shadowBlur=0;
  if(!reduce){ if(!zombi&&--zNext<=0) zombi={x:-30,f:0}; if(zombi){zombi.x+=.28; zombi.f+=.07; dibujarZombi(zombi.x+om,484,zombi.f); if(zombi.x>LW+30){zombi=null;zNext=1200+Math.random()*1200;}} }
  niebla_(3,7);
  ctx.drawImage(cerca,-80+pan,0);
  const viento=Math.sin(t*.01)*3;
  ctx.lineWidth=2;
  for(const b of pasto){const s=reduce?0:Math.sin(t*.03+b.f)*5+viento; ctx.strokeStyle=b.c; ctx.beginPath(); ctx.moveTo(b.x,H); ctx.quadraticCurveTo(b.x+s*.3,H-b.h*.5,b.x+s,H-b.h); ctx.stroke();}
  for(let i=0;i<hojas.length;i++){const h=hojas[i]; h.f+=.03; h.x+=h.vx+Math.sin(h.f)*.6+viento*.1; h.y+=h.vy; h.r+=h.vr;
    if(h.y>H+10) hojas[i]=nuevaHoja(false);
    ctx.save(); ctx.translate(h.x,h.y); ctx.rotate(h.r); ctx.fillStyle=h.c; ctx.beginPath(); ctx.ellipse(0,0,h.s,h.s*.45,0,0,6.283); ctx.fill(); ctx.restore();}
  ctx.globalCompositeOperation='lighter';
  for(const e of esporas){ if(!reduce){e.f+=.02; e.x+=Math.sin(e.f)*.3+.1; e.y-=.15; if(e.y<200){e.y=600;e.x=rnd(0,W);} if(e.x>W)e.x=0;}
    const a=.25+.25*Math.sin(e.f*3); ctx.fillStyle=`rgba(190,255,140,${a*.25})`; ctx.beginPath(); ctx.arc(e.x,e.y,6,0,6.283); ctx.fill();
    ctx.fillStyle=`rgba(220,255,180,${a})`; ctx.beginPath(); ctx.arc(e.x,e.y,1.6,0,6.283); ctx.fill();}
  ctx.globalCompositeOperation='source-over';
  if(!reduce){ if(!bandada&&--bNext<=0){bandada={x:-60,y:rnd(80,220),aves:[...Array(5)].map((_,i)=>({dx:-i*26+rnd(-8,8),dy:(i%2?1:-1)*i*9,f:rnd(0,6)}))};}
    if(bandada){bandada.x+=2.2; ctx.strokeStyle='#0d0f0b'; ctx.lineWidth=2;
      for(const a of bandada.aves){a.f+=.25; const x=bandada.x+a.dx, y=bandada.y+a.dy, w=Math.sin(a.f)*5;
        ctx.beginPath(); ctx.moveTo(x-9,y-w); ctx.lineTo(x,y); ctx.lineTo(x+9,y-w); ctx.stroke();}
      if(bandada.x>W+200){bandada=null;bNext=900+Math.random()*1500;}}}
  ctx.fillStyle='rgba(40,60,30,.12)'; ctx.fillRect(0,0,W,H);
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
function sonido(){
  const v=lazo('bandpass',420,.07,.6); lfo(v.f.frequency,.07,220); lazo('lowpass',180,.03);
  setInterval(()=>{if(!on)return; for(let i=0;i<3;i++) setTimeout(()=>pitido(4300,4100,.022,.05),i*90);},1100);
  setInterval(()=>{if(!on||Math.random()>.35)return; pitido(420,300,.06,.28,'sawtooth'); setTimeout(()=>pitido(400,290,.05,.25,'sawtooth'),360);},6000);
}
"""

# ---------------------------------------------------------------- CASTILLO ---
JS_CASTILLO = r"""
const estrellas=[]; for(let i=0;i<120;i++) estrellas.push({x:sr()*W,y:sr()*330,r:sr()*1.3+.3,f:sr()*6});
const castillo=capa(), frente=capa(), ventanas=[];
function arco(c,x,y,w,h){c.beginPath();c.moveTo(x,y+h);c.lineTo(x,y+w/2);c.arc(x+w/2,y+w/2,w/2,Math.PI,0);c.lineTo(x+w,y+h);c.closePath();}
(()=>{const c=castillo.getContext('2d'), piedra='#1b0b2a', techo='#2a1240';
  c.fillStyle='#0d0616'; c.beginPath(); c.moveTo(0,470); c.bezierCurveTo(250,420,330,372,500,366); c.bezierCurveTo(680,372,760,430,1000,460); c.lineTo(1000,H); c.lineTo(0,H); c.fill();
  function torre(x,w,top,base,alto){
    c.fillStyle=piedra; c.fillRect(x,top,w,base-top);
    c.fillStyle=techo; poly(c,[[x-6,top],[x+w/2,top-alto],[x+w+6,top]]);
    c.strokeStyle=techo; c.lineWidth=2; c.beginPath(); c.moveTo(x+w/2,top-alto); c.lineTo(x+w/2,top-alto-18); c.stroke();
    c.fillStyle=techo; poly(c,[[x+w/2,top-alto-18],[x+w/2+14,top-alto-13],[x+w/2,top-alto-9]]);
    for(let y=top+18;y<base-24;y+=34){const v={x:x+w/2-4,y,w:8,h:14,f:sr()*6,v:.5+sr()*2,morada:sr()<.25,apagada:sr()<.25}; ventanas.push(v); c.fillStyle='#07030c'; arco(c,v.x,v.y,v.w,v.h); c.fill();}
  }
  c.fillStyle=piedra; c.fillRect(270,300,460,85); for(let x=270;x<730;x+=20) c.fillRect(x,290,12,12);
  torre(250,44,250,385,55); torre(706,44,240,385,55); torre(345,54,175,385,80); torre(600,58,155,385,90);
  c.fillStyle=piedra; c.fillRect(420,215,160,170); for(let x=420;x<580;x+=18) c.fillRect(x,205,11,12);
  torre(477,46,120,215,110);
  for(let y=240;y<330;y+=36) for(let x=440;x<570;x+=30){const v={x,y,w:10,h:16,f:sr()*6,v:.5+sr()*2,morada:sr()<.2,apagada:sr()<.3}; ventanas.push(v); c.fillStyle='#07030c'; arco(c,x,y,10,16); c.fill();}
  c.fillStyle='#050208'; c.beginPath(); c.moveTo(478,385); c.lineTo(478,345); c.quadraticCurveTo(500,322,522,345); c.lineTo(522,385); c.fill();
  c.strokeStyle='#22102f'; c.lineWidth=1.5; for(let x=482;x<520;x+=6){c.beginPath(); c.moveTo(x,338); c.lineTo(x,385); c.stroke();}
  c.strokeStyle='rgba(120,70,160,.25)'; c.lineWidth=6; c.beginPath(); c.moveTo(500,388); c.bezierCurveTo(420,430,600,470,470,560); c.lineTo(500,600); c.stroke();
  c.globalCompositeOperation='source-atop'; const g=c.createLinearGradient(250,0,760,0); g.addColorStop(0,'rgba(0,0,0,.25)'); g.addColorStop(1,'rgba(120,255,140,.10)'); c.fillStyle=g; c.fillRect(0,0,W,H);
})();
function ramaM(c,x,y,a,l,w,d){const a2=a+(sr()-.5)*.5, x2=x+Math.cos(a2)*l, y2=y+Math.sin(a2)*l, cx=x+Math.cos(a)*l*.5+(sr()-.5)*l*.3, cy=y+Math.sin(a)*l*.5;
  c.lineWidth=Math.max(1,w); c.beginPath(); c.moveTo(x,y); c.quadraticCurveTo(cx,cy,x2,y2); c.stroke();
  if(d>0){const n=sr()<.3?3:2; for(let i=0;i<n;i++) ramaM(c,x2,y2,a2+(i-(n-1)/2)*(.55+sr()*.35),l*(.62+sr()*.15),w*.65,d-1);}}
function arbolMuerto(c,x,y,h,incl){c.strokeStyle='#05020a'; c.lineCap='round'; ramaM(c,x,y,-Math.PI/2+incl,h*.38,h*.07,6);}
(()=>{const c=frente.getContext('2d');
  c.fillStyle='#07030d'; c.beginPath(); c.moveTo(0,520); c.bezierCurveTo(200,500,350,530,500,540); c.bezierCurveTo(700,550,850,505,1000,515); c.lineTo(1000,H); c.lineTo(0,H); c.fill();
  c.fillStyle='#120a1c'; [[330,540],[380,548],[640,548],[700,540]].forEach(([x,y])=>{c.beginPath(); c.moveTo(x-10,y+12); c.lineTo(x-10,y-8); c.quadraticCurveTo(x,y-20,x+10,y-8); c.lineTo(x+10,y+12); c.fill();});
  c.fillRect(430,520,4,26); c.fillRect(424,528,16,4);
  arbolMuerto(c,95,565,200,-.08); arbolMuerto(c,915,565,220,.1); arbolMuerto(c,215,530,95,.05); arbolMuerto(c,790,526,85,-.06);
})();
const calabazas=[{x:170,y:556,s:22},{x:245,y:572,s:16},{x:520,y:582,s:20},{x:760,y:566,s:24},{x:845,y:582,s:17},{x:612,y:574,s:14}].map(p=>({...p,f:rnd(0,6)}));
function calabaza(p){const s=p.s,x=p.x,y=p.y, fl=.7+.3*Math.sin(t*.2+p.f)+rnd(-.1,.1);
  ctx.globalCompositeOperation='lighter';
  const g=ctx.createRadialGradient(x,y,2,x,y,s*3.2); g.addColorStop(0,`rgba(150,255,90,${.25*fl})`); g.addColorStop(1,'rgba(0,0,0,0)'); ctx.fillStyle=g; ctx.fillRect(x-s*3.2,y-s*3.2,s*6.4,s*6.4);
  ctx.globalCompositeOperation='source-over';
  [[-.55,.62,'#6e2f10'],[.55,.62,'#6e2f10'],[-.25,.7,'#8c3e14'],[.25,.7,'#8c3e14'],[0,.72,'#a44c18']].forEach(([ox,rx,c])=>{ctx.fillStyle=c; ctx.beginPath(); ctx.ellipse(x+ox*s,y,rx*s,s*.78,0,0,6.283); ctx.fill();});
  ctx.fillStyle='#2f4a1a'; ctx.fillRect(x-s*.08,y-s*.98,s*.16,s*.3);
  ctx.fillStyle=`rgba(${170+fl*60|0},255,${90+fl*40|0},${Math.min(1,.75+.25*fl)})`;
  poly(ctx,[[x-s*.45,y-s*.08],[x-s*.15,y-s*.08],[x-s*.3,y-s*.4]]); poly(ctx,[[x+s*.15,y-s*.08],[x+s*.45,y-s*.08],[x+s*.3,y-s*.4]]);
  poly(ctx,[[x-s*.5,y+s*.15],[x-s*.3,y+s*.3],[x-s*.15,y+s*.18],[x,y+s*.35],[x+s*.15,y+s*.18],[x+s*.3,y+s*.3],[x+s*.5,y+s*.15],[x+s*.2,y+s*.48],[x-s*.2,y+s*.48]]);}
const murcielagos=[]; for(let i=0;i<16;i++) murcielagos.push({a:rnd(0,6.28),r:rnd(90,280),cy:rnd(120,240),v:rnd(.004,.012)*(Math.random()<.5?-1:1),f:rnd(0,6),s:rnd(4,9),ry:rnd(.3,.55)});
function murcielago(x,y,s,f){const ala=Math.sin(f)*s*.9; ctx.fillStyle='#05020a'; ctx.beginPath(); ctx.moveTo(x,y);
  ctx.quadraticCurveTo(x-s*1.2,y-ala-s*.2,x-s*2.4,y-ala); ctx.lineTo(x-s*1.6,y-ala*.3+s*.2); ctx.lineTo(x-s*.9,y+s*.3); ctx.lineTo(x,y+s*.4);
  ctx.lineTo(x+s*.9,y+s*.3); ctx.lineTo(x+s*1.6,y-ala*.3+s*.2); ctx.lineTo(x+s*2.4,y-ala); ctx.quadraticCurveTo(x+s*1.2,y-ala-s*.2,x,y); ctx.fill();
  ctx.beginPath(); ctx.arc(x,y+s*.1,s*.35,0,6.283); ctx.fill();}
const nubes=[]; for(let i=0;i<8;i++){const n={x:rnd(-200,W),y:rnd(40,300),v:rnd(.08,.25),p:[]}; for(let k=0;k<6;k++) n.p.push([rnd(-90,90),rnd(-18,18),rnd(30,70)]); nubes.push(n);}
const nieblaV=[]; for(let i=0;i<6;i++) nieblaV.push({x:rnd(0,W),y:rnd(380,580),rx:rnd(160,320),v:rnd(.15,.4)*(Math.random()<.5?-1:1)});
const fuegos=[]; for(let i=0;i<7;i++) fuegos.push({x:rnd(100,900),b:rnd(480,570),f:rnd(0,6)});
let rayo=0, rayoNext=260, rayoPts=[];
function trueno(){ if(!ac||!on) return; setTimeout(()=>golpe('lowpass',160,.6,2.4),600); }
function frame(){
  t++;
  let g=ctx.createLinearGradient(0,0,0,H); g.addColorStop(0,'#0b0313'); g.addColorStop(.45,'#2a0b3d'); g.addColorStop(.8,'#4b1559'); g.addColorStop(1,'#1a0726');
  ctx.fillStyle=g; ctx.fillRect(0,0,W,H);
  for(const e of estrellas){ctx.fillStyle=`rgba(230,220,255,${.4+.4*Math.sin(t*.03+e.f)})`; ctx.fillRect(e.x,e.y,e.r,e.r);}
  g=ctx.createRadialGradient(720,150,40,720,150,270); g.addColorStop(0,'rgba(150,255,140,.28)'); g.addColorStop(1,'rgba(0,0,0,0)'); ctx.fillStyle=g; ctx.fillRect(0,0,W,H);
  ctx.fillStyle='#d6f5c4'; ctx.beginPath(); ctx.arc(720,150,68,0,6.283); ctx.fill();
  ctx.fillStyle='rgba(120,170,110,.35)'; [[700,130,12],[745,165,9],[712,180,6],[750,128,5]].forEach(([x,y,r])=>{ctx.beginPath();ctx.arc(x,y,r,0,6.283);ctx.fill();});
  for(const n of nubes){ if(!reduce){n.x-=n.v; if(n.x<-260) n.x=W+200;}
    for(const p of n.p){ctx.fillStyle='rgba(60,20,82,.33)'; ctx.beginPath(); ctx.arc(n.x+p[0],n.y+p[1],p[2],0,6.283); ctx.fill();}}
  if(!reduce&&--rayoNext<=0){rayo=14; rayoNext=420+Math.random()*700; rayoPts=[[rnd(150,850),0]]; let [x,y]=rayoPts[0]; while(y<330){x+=rnd(-40,40); y+=rnd(20,45); rayoPts.push([x,y]);} trueno();}
  if(rayo>0){rayo--; ctx.fillStyle=`rgba(190,130,255,${rayo>10?.5:rayo/10*.22})`; ctx.fillRect(0,0,W,H);
    if(rayo>8){ctx.strokeStyle='rgba(240,220,255,.95)'; ctx.lineWidth=3; ctx.shadowColor='#c77dff'; ctx.shadowBlur=20; ctx.beginPath();
      rayoPts.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1])); ctx.stroke(); ctx.shadowBlur=0;}}
  ctx.drawImage(castillo,0,0);
  ctx.globalCompositeOperation='lighter';
  for(const w of ventanas){
    if(w.apagada&&Math.sin(t*.01+w.f)<.95) continue;
    const b=Math.max(.1,.55+.45*Math.sin(t*.05*w.v+w.f)+rnd(-.08,.08)), c=w.morada?'199,125,255':'141,255,106';
    ctx.fillStyle=`rgba(${c},${.75*b})`; arco(ctx,w.x,w.y,w.w,w.h); ctx.fill();
    ctx.fillStyle=`rgba(${c},${.1*b})`; ctx.fillRect(w.x-8,w.y-8,w.w+16,w.h+16);}
  ctx.globalCompositeOperation='source-over';
  for(const b of murcielagos){ if(!reduce){b.a+=b.v; b.f+=.35;} murcielago(500+Math.cos(b.a)*b.r,b.cy+Math.sin(b.a)*b.r*b.ry,b.s,b.f);}
  ctx.globalCompositeOperation='lighter';
  for(const n of nieblaV){ if(!reduce){n.x+=n.v; if(n.x>W+n.rx) n.x=-n.rx; if(n.x<-n.rx) n.x=W+n.rx;}
    ctx.save(); ctx.translate(n.x,n.y); ctx.scale(1,.18); const gg=ctx.createRadialGradient(0,0,0,0,0,n.rx);
    gg.addColorStop(0,'rgba(110,255,130,.10)'); gg.addColorStop(1,'rgba(0,0,0,0)'); ctx.fillStyle=gg; ctx.fillRect(-n.rx,-n.rx,2*n.rx,2*n.rx); ctx.restore();}
  ctx.globalCompositeOperation='source-over';
  ctx.drawImage(frente,0,0);
  calabazas.forEach(calabaza);
  ctx.globalCompositeOperation='lighter';
  for(const f of fuegos){ if(!reduce) f.f+=.015; const x=f.x+Math.sin(f.f*1.3)*40, y=f.b+Math.sin(f.f*2.1)*12, a=.35+.25*Math.sin(f.f*5);
    ctx.fillStyle=`rgba(141,255,106,${a*.25})`; ctx.beginPath(); ctx.arc(x,y,9,0,6.283); ctx.fill();
    ctx.fillStyle=`rgba(220,255,200,${a})`; ctx.beginPath(); ctx.arc(x,y,2.4,0,6.283); ctx.fill();}
  ctx.globalCompositeOperation='source-over';
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
function sonido(){
  const v=lazo('bandpass',700,.05,7); lfo(v.f.frequency,.11,320);
  tono('sine',55,.03); tono('sine',82.4,.018); tono('triangle',110,.006);
  setInterval(()=>{if(on&&Math.random()<.3) pitido(1800,1500,.015,.08);},2500);
}
"""

# ------------------------------------------------------------------ ARAÑAS ---
JS_ARANAS = r"""
const TA={
  viuda:{c:'#060506',b:'rgba(255,255,255,.22)',ab:.95,l1:1.3,l2:1.5,lw:.09,marca:true,v:.8},
  tarantula:{c:'#3b2617',b:'rgba(255,190,140,.14)',ab:.85,l1:1.1,l2:1.2,lw:.24,pelo:true,v:.45},
  saltarina:{c:'#151215',b:'rgba(255,255,255,.22)',ab:.68,l1:.7,l2:.7,lw:.2,ojos:true,franjas:true,v:0,salto:true},
  patas:{c:'#7a6a52',b:'rgba(255,255,255,.12)',ab:.42,l1:3,l2:3.4,lw:.05,v:.9},
  lobo:{c:'#5e4731',b:'rgba(255,230,190,.14)',ab:.8,l1:1.45,l2:1.6,lw:.14,franjas:true,v:1.7},
};
const ANG=[.5,1.05,1.75,2.4];
function dibujarArana(c,s){
  const T=TA[s.tipo],k=s.k; c.save(); c.translate(s.x,s.y); c.rotate(s.ang);
  c.shadowColor='rgba(255,70,70,.35)'; c.shadowBlur=4;
  c.strokeStyle=T.c; c.lineCap='round'; c.lineJoin='round';
  for(let lado=-1;lado<=1;lado+=2) for(let i=0;i<4;i++){
    const grupo=(i+(lado>0?1:0))%2, sw=(s.mov||0)*Math.sin(s.fase+grupo*Math.PI)*.22;
    const a=lado*(ANG[i]+sw), dob=lado*(i<2?-.6:.6);
    const bx=Math.cos(a)*k*.3, by=Math.sin(a)*k*.3, kx=bx+Math.cos(a)*k*T.l1, ky=by+Math.sin(a)*k*T.l1;
    const fx=kx+Math.cos(a+dob)*k*T.l2, fy=ky+Math.sin(a+dob)*k*T.l2;
    c.lineWidth=Math.max(1,k*T.lw); c.beginPath(); c.moveTo(bx,by); c.lineTo(kx,ky); c.lineTo(fx,fy); c.stroke();
    if(T.pelo){c.lineWidth=1; c.beginPath();
      for(let h=1;h<6;h++){const u=h/6, px=bx+(kx-bx)*u, py=by+(ky-by)*u, qx=kx+(fx-kx)*u, qy=ky+(fy-ky)*u;
        c.moveTo(px,py); c.lineTo(px-Math.sin(a)*k*.18,py+Math.cos(a)*k*.18); c.moveTo(qx,qy); c.lineTo(qx+Math.sin(a)*k*.15,qy-Math.cos(a)*k*.15);}
      c.stroke();}
  }
  const ax=-k*(.5+T.ab*.62);
  c.fillStyle=T.c; c.beginPath(); c.ellipse(ax,0,k*T.ab,k*T.ab*.8,0,0,6.283); c.fill();
  c.beginPath(); c.ellipse(0,0,k*.5,k*.42,0,0,6.283); c.fill();
  c.shadowBlur=0;
  if(T.pelo){c.strokeStyle='rgba(120,80,50,.6)'; c.lineWidth=1; c.beginPath();
    for(let h=0;h<14;h++){const a=h/14*6.283; c.moveTo(ax+Math.cos(a)*k*T.ab*.9,Math.sin(a)*k*T.ab*.72); c.lineTo(ax+Math.cos(a)*k*T.ab*1.15,Math.sin(a)*k*T.ab*.95);} c.stroke();}
  if(T.franjas){c.fillStyle='rgba(225,210,185,.45)'; c.beginPath(); c.ellipse(ax,0,k*T.ab*.8,k*.07,0,0,6.283); c.fill(); c.beginPath(); c.ellipse(k*.05,0,k*.4,k*.06,0,0,6.283); c.fill();}
  if(T.marca){c.fillStyle='#d4141a'; poly(c,[[ax-k*.32,-k*.22],[ax-k*.32,k*.22],[ax,0]]); poly(c,[[ax+k*.32,-k*.22],[ax+k*.32,k*.22],[ax,0]]);}
  c.fillStyle=T.b; c.beginPath(); c.ellipse(ax-k*T.ab*.15,-k*T.ab*.32,k*T.ab*.38,k*T.ab*.18,-.3,0,6.283); c.fill();
  if(T.ojos){for(const oy of [-1,1]){c.fillStyle='#000'; c.beginPath(); c.arc(k*.36,oy*k*.15,k*.16,0,6.283); c.fill();
    c.fillStyle='rgba(255,255,255,.7)'; c.beginPath(); c.arc(k*.4,oy*k*.15-k*.05,k*.05,0,6.283); c.fill();}}
  else {c.fillStyle='rgba(200,20,20,.85)'; for(const oy of [-1,1]){c.beginPath(); c.arc(k*.38,oy*k*.1,Math.max(.8,k*.05),0,6.283); c.fill();}}
  c.strokeStyle=T.c; c.lineWidth=Math.max(1,k*.08); c.beginPath(); c.moveTo(k*.45,-k*.1); c.lineTo(k*.68,-k*.16); c.moveTo(k*.45,k*.1); c.lineTo(k*.68,k*.16); c.stroke();
  c.restore();
}
function dif(a,b){let d=a-b; while(d>Math.PI)d-=2*Math.PI; while(d<-Math.PI)d+=2*Math.PI; return d;}
function moverArana(s,ancho,alto,mx,my){
  const T=TA[s.tipo];
  if(--s.timer<=0){s.parado=!s.parado&&Math.random()<.4; s.timer=s.parado?40+Math.random()*120:60+Math.random()*200; s.giro=(Math.random()-.5)*.05;}
  let v=T.v*(.5+s.k/16), huye=false;
  const d=Math.hypot(s.x-mx,s.y-my);
  if(d<150){s.ang+=dif(Math.atan2(s.y-my,s.x-mx),s.ang)*.25; v=Math.max(v,1.2)*2.6; huye=true; s.parado=false;}
  else s.ang+=s.giro;
  if(T.salto){s.hop=(s.hop||0)-1; if(s.hop<=0){s.hop=45+Math.random()*90; s.imp=7+(huye?5:0);} s.imp=(s.imp||0)*.85; v=s.imp;}
  const m=30; if(s.x<m||s.x>ancho-m||s.y<m||s.y>alto-m) s.ang+=dif(Math.atan2(alto/2-s.y,ancho/2-s.x),s.ang)*.1;
  if(s.parado&&!huye) v=0;
  s.x+=Math.cos(s.ang)*v; s.y+=Math.sin(s.ang)*v;
  s.x=Math.max(-20,Math.min(ancho+20,s.x)); s.y=Math.max(-20,Math.min(alto+20,s.y));
  s.mov=v>.05&&!T.salto?1:(T.salto&&v>.5?.4:0); s.fase+=.1+v*.3;
}
function nuevaArana(tipo,x,y){return {tipo,x,y,ang:Math.random()*6.28,k:{tarantula:16,patas:6,saltarina:8,viuda:10,lobo:10}[tipo],fase:0,mov:1,timer:0,parado:false,giro:0};}

/* ---- escena: ático con telaraña gigante ---- */
const fondo=capa();
function esquina(c,x,y,sx,sy,r){c.strokeStyle='rgba(200,200,210,.18)'; c.lineWidth=1;
  for(let i=0;i<=6;i++){const a=i/6*Math.PI/2; c.beginPath(); c.moveTo(x,y); c.lineTo(x+sx*Math.cos(a)*r,y+sy*Math.sin(a)*r); c.stroke();}
  for(let k=1;k<=6;k++){const rr=r*k/6; c.beginPath(); for(let i=0;i<=6;i++){const a=i/6*Math.PI/2, px=x+sx*Math.cos(a)*rr*(i%2?.92:1), py=y+sy*Math.sin(a)*rr*(i%2?.92:1); i?c.lineTo(px,py):c.moveTo(px,py);} c.stroke();}}
(()=>{const c=fondo.getContext('2d');
  const g=c.createLinearGradient(0,0,0,H); g.addColorStop(0,'#0b0707'); g.addColorStop(1,'#040202'); c.fillStyle=g; c.fillRect(0,0,W,H);
  for(let x=0;x<W;x+=26){c.fillStyle=`rgba(60,30,30,${.08+sr()*.06})`; c.fillRect(x,0,10,470);}
  for(let i=0;i<14;i++){const x=sr()*W,y=sr()*H,r=30+sr()*90, gg=c.createRadialGradient(x,y,0,x,y,r); gg.addColorStop(0,'rgba(40,25,15,.25)'); gg.addColorStop(1,'rgba(0,0,0,0)'); c.fillStyle=gg; c.fillRect(x-r,y-r,2*r,2*r);}
  c.fillStyle='#120a07'; poly(c,[[0,0],[W,0],[W,40],[0,60]]); c.fillStyle='#0e0806'; poly(c,[[0,60],[180,0],[230,0],[0,120]]); poly(c,[[W,40],[820,0],[770,0],[W,100]]);
  c.fillStyle='#1b2430'; c.fillRect(70,100,110,140); c.fillStyle='#0a0606'; c.fillRect(122,100,6,140); c.fillRect(70,166,110,6);
  c.fillStyle='#0d0807'; c.fillRect(0,470,W,130); c.strokeStyle='#060404'; for(let y=482;y<H;y+=18){c.beginPath(); c.moveTo(0,y); c.lineTo(W,y); c.stroke();}
  esquina(c,0,0,1,1,170); esquina(c,W,0,-1,1,190); esquina(c,0,470,1,-1,80); esquina(c,W,470,-1,-1,90);
})();
const CX=600,CY=250,R=240,NR=18,NS=16;
const rad=[]; for(let i=0;i<NR;i++) rad.push(i/NR*Math.PI*2+(sr()-.5)*.12);
const anclas=rad.map(()=>R*1.35+sr()*60);
const rocio=[]; for(let i=0;i<60;i++) rocio.push({i:(sr()*NR)|0,k:1+((sr()*(NS-1))|0),f:sr()*6});
function pw(a,r){const w=reduce?0:(Math.sin(t*.012)*6+Math.sin(t*.031)*2)*(r/R); return [CX+Math.cos(a)*r+w,CY+Math.sin(a)*r+w*.3];}
function telar(){
  ctx.strokeStyle='rgba(215,215,225,.32)'; ctx.lineWidth=1; ctx.beginPath();
  for(let i=0;i<NR;i++){const p=pw(rad[i],anclas[i]); ctx.moveTo(CX,CY); ctx.lineTo(p[0],p[1]);}
  for(let k=1;k<=NS;k++){const r=R*Math.pow(k/NS,1.1);
    for(let i=0;i<NR;i++){const a0=rad[i], a1=rad[(i+1)%NR]+(i+1===NR?Math.PI*2:0), p0=pw(a0,r), p1=pw(a1,r), m=pw((a0+a1)/2,r*.94);
      if(i===0) ctx.moveTo(p0[0],p0[1]); ctx.quadraticCurveTo(m[0],m[1],p1[0],p1[1]);}}
  ctx.stroke();
  ctx.fillStyle='rgba(225,215,200,.55)';
  [[rad[3],R*1.12],[rad[11],R*1.05]].forEach(([a,r])=>{const p=pw(a,r); ctx.beginPath(); ctx.ellipse(p[0],p[1],9,12,0,0,6.283); ctx.fill();});
  ctx.globalCompositeOperation='lighter';
  for(const d of rocio){const p=pw(rad[d.i],R*Math.pow(d.k/NS,1.1)), b=Math.pow(Math.max(0,Math.sin(t*.04+d.f)),6);
    ctx.fillStyle=`rgba(200,220,255,${.25+.75*b})`; ctx.beginPath(); ctx.arc(p[0],p[1],1.2+b*1.5,0,6.283); ctx.fill();}
  ctx.globalCompositeOperation='source-over';
}
const reina={tipo:'viuda',x:CX,y:CY,ang:-Math.PI/2,k:22,fase:0,mov:0}; let tiembla=0;
const colgantes=[{x:180,tipo:'patas',k:6,f:0},{x:330,tipo:'viuda',k:9,f:2},{x:880,tipo:'saltarina',k:9,f:4},{x:960,tipo:'lobo',k:8,f:1}];
const andantes=['tarantula','lobo','saltarina','patas'].map(tp=>nuevaArana(tp,rnd(100,900),rnd(480,580)));
const polvo=[]; for(let i=0;i<40;i++) polvo.push({x:rnd(70,420),y:rnd(100,470),f:rnd(0,6)});
let mx=-999,my=-999;
document.addEventListener('mousemove',e=>{[mx,my]=aCanvas(e.clientX,e.clientY);});
document.addEventListener('mouseleave',()=>{mx=my=-999;});
function frame(){
  t++;
  ctx.drawImage(fondo,0,0);
  ctx.globalCompositeOperation='lighter';
  const lg=ctx.createLinearGradient(120,100,380,470); lg.addColorStop(0,'rgba(120,150,190,.10)'); lg.addColorStop(1,'rgba(120,150,190,0)');
  ctx.fillStyle=lg; poly(ctx,[[70,100],[180,100],[470,470],[200,470]]);
  for(const p of polvo){ if(!reduce){p.f+=.01; p.x+=Math.sin(p.f)*.15; p.y+=Math.cos(p.f*.7)*.1;} ctx.fillStyle=`rgba(200,210,230,${.15+.15*Math.sin(p.f*4)})`; ctx.fillRect(p.x,p.y,1.5,1.5);}
  ctx.globalCompositeOperation='source-over';
  telar();
  if(!reduce&&Math.random()<.004) tiembla=40;
  if(tiembla>0){tiembla--; reina.mov=1; reina.fase+=.4;} else reina.mov=0;
  dibujarArana(ctx,reina);
  for(const c of colgantes){
    const len=reduce?200:200+Math.sin(t*.006+c.f)*170, sw=reduce?0:Math.sin(t*.02+c.f)*10, x=c.x+sw, y=len+30;
    ctx.strokeStyle='rgba(215,215,225,.35)'; ctx.lineWidth=1; ctx.beginPath(); ctx.moveTo(c.x,0); ctx.lineTo(x,y-c.k); ctx.stroke();
    dibujarArana(ctx,{tipo:c.tipo,x,y,ang:Math.PI/2,k:c.k,fase:t*.1,mov:.3});
  }
  for(const s of andantes){ if(!reduce) moverArana(s,W,H,mx,my); dibujarArana(ctx,s); }
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);

/* ---- arañas caminando por toda la página ---- */
(function invasion(){
  if(reduce) return;
  let P, D; try{P=window.parent; D=P.document; D.body;}catch(e){return;}
  const vieja=D.getElementById('aranas-overlay'); if(vieja) vieja.remove();
  if(P.__aranasMove) D.removeEventListener('mousemove',P.__aranasMove);
  const ov=D.createElement('canvas'); ov.id='aranas-overlay';
  ov.style.cssText='position:fixed;inset:0;width:100vw;height:100vh;pointer-events:none;z-index:9989;';
  D.body.appendChild(ov);
  const oc=ov.getContext('2d');
  let px=-999, py=-999;
  const mover=e=>{px=e.clientX; py=e.clientY;}; P.__aranasMove=mover; D.addEventListener('mousemove',mover);
  document.addEventListener('mousemove',e=>{const r=window.frameElement?window.frameElement.getBoundingClientRect():{left:0,top:0}; px=e.clientX+r.left; py=e.clientY+r.top;});
  function ajustar(){const r=P.devicePixelRatio||1; ov.width=P.innerWidth*r; ov.height=P.innerHeight*r; oc.setTransform(r,0,0,r,0,0);}
  ajustar(); P.addEventListener('resize',ajustar);
  const lista=['viuda','tarantula','saltarina','patas','lobo','viuda','lobo','saltarina','patas'].map(tp=>nuevaArana(tp,Math.random()*P.innerWidth,Math.random()*P.innerHeight));
  let visible=true;
  const b=document.createElement('button'); b.id='ctl2'; b.className='ctl'; b.type='button'; b.textContent='✕ Espantar arañas';
  b.onclick=()=>{visible=!visible; ov.style.display=visible?'block':'none'; b.textContent=visible?'✕ Espantar arañas':'🕷 Dejarlas salir';};
  wrap.appendChild(b);
  function bucle(){
    if(!window.frameElement||!window.frameElement.isConnected||!ov.isConnected){
      ov.remove(); D.removeEventListener('mousemove',mover); P.removeEventListener('resize',ajustar); return;}
    oc.clearRect(0,0,P.innerWidth,P.innerHeight);
    if(visible) for(const s of lista){moverArana(s,P.innerWidth,P.innerHeight,px,py); dibujarArana(oc,s);}
    P.requestAnimationFrame(bucle);
  }
  P.requestAnimationFrame(bucle);
})();
function sonido(){
  tono('sine',40,.04); lazo('lowpass',300,.015);
  setInterval(()=>{if(!on||Math.random()>.4)return; const n=3+Math.random()*6|0; for(let i=0;i<n;i++) setTimeout(()=>golpe('highpass',3000+Math.random()*3000,.05,.015),i*(25+Math.random()*30));},700);
}
"""

ESCENA_CFG = {
    "liminal": {
        "js": JS_LIMINAL, "osd": "CAM 03 &nbsp;▮▮▮▯", "seed": 3001,
        "alt": "Pasillo infinito de paredes amarillas, alfombra húmeda y tubos fluorescentes que parpadean.",
        "css": ".titulo h1{font-family:'VT323',monospace;font-size:clamp(40px,8vw,96px);color:#2a230e;"
               "text-shadow:0 0 14px rgba(255,250,200,.7);} .titulo .meta{color:#3b3214;text-shadow:none;}"
               " .osd{color:#2a230e;text-shadow:0 0 6px rgba(255,250,200,.6);} .vig{background:radial-gradient(ellipse at center,transparent 55%,rgba(40,30,0,.55) 100%);}",
    },
    "naturaleza": {
        "js": JS_NATURALEZA, "osd": "PLAY ► &nbsp;CH 04", "seed": 4242,
        "alt": "Ciudad abandonada tragada por la vegetación: edificios con enredaderas, un auto con musgo y niebla verde.",
        "css": "canvas{object-position:50% 88%;} .titulo h1{font-family:'Special Elite',monospace;text-transform:uppercase;letter-spacing:.04em;color:#e6ecd6;"
               "font-size:clamp(28px,5vw,60px);text-shadow:0 0 18px rgba(120,160,80,.5),2px 2px 0 #0b1007;}"
               " .titulo .meta{color:#c8d6a8;}",
    },
    "castillo": {
        "js": JS_CASTILLO, "osd": "PLAY ► &nbsp;SP", "seed": 3131,
        "alt": "Castillo gigante morado en una colina bajo una luna verde, con árboles muertos, murciélagos y calabazas encendidas.",
        "css": "canvas{object-position:50% 88%;} .titulo h1{font-family:'UnifrakturMaguntia',serif;color:#8dff6a;"
               "text-shadow:0 0 18px rgba(141,255,106,.5),3px 3px 0 #3a1052;} .titulo .meta{color:#d8c4ff;}",
    },
    "aranas": {
        "js": JS_ARANAS, "osd": "PLAY ► &nbsp;SLP", "seed": 8888,
        "alt": "Ático oscuro con una telaraña gigante, una viuda negra en el centro y arañas de varios tipos colgando y caminando.",
        "css": "canvas{object-position:50% 88%;} .titulo h1{font-family:'Creepster',cursive;color:#ff2a2a;text-shadow:0 0 16px rgba(255,0,0,.4),3px 0 0 #2a0000;}",
    },
}

# Estilo de la página de lectura para cada escenario.
TEMA_CSS = {
    "liminal": """<style>
:root{--sangre:#8a7a2a; --sangre-viva:#d8c25a; --linea:#4a4320; --hueso:#efe6c4; --ceniza:#a89c6a;}
.stApp{background:radial-gradient(ellipse at 50% 0%, #3a3414 0%, #12100a 60%) fixed !important;}
.st-key-lector_liminal{background:#d9cc8c !important; border:1px solid #8a7a2a !important; box-shadow:inset 0 0 80px rgba(120,100,20,.35) !important;}
.st-key-lector_liminal p, .st-key-lector_liminal li, .st-key-lector_liminal em{color:#2b2410 !important;}
.st-key-lector_liminal .osd, .st-key-lector_liminal .osd b{color:#5a4e22 !important;}
.st-key-lector_liminal .fin{color:#6b5a1a;}
.st-key-lector_liminal .tag{color:#4a3f18; border-color:#8a7a2a;}
</style>""",
    "naturaleza": """<style>
:root{--sangre:#4f6b2c; --sangre-viva:#9cc25a; --linea:#2a3a1e; --hueso:#dfe3cf; --ceniza:#8e9a7a;}
.stApp{background:radial-gradient(ellipse at 50% 0%, #1c2616 0%, #070a05 60%) fixed !important;}
.st-key-lector_naturaleza{background:linear-gradient(180deg,#121a0e,#0a0f07) !important; border:1px solid #2f4520 !important; border-left:4px solid #6f8f3a !important;}
.st-key-lector_naturaleza p, .st-key-lector_naturaleza li{color:#dfe3cf !important;}
</style>""",
    "castillo": """<style>
:root{--sangre:#5b2a86; --sangre-viva:#8dff6a; --linea:#2e1846; --hueso:#e8defa; --ceniza:#9b8fb3;}
.stApp{background:radial-gradient(ellipse at 50% 0%, #2a0f3f 0%, #07030c 60%) fixed !important;}
.st-key-lector_castillo{background:#0f0618 !important; border:1px solid #4a2470 !important;
  box-shadow:0 0 40px rgba(141,255,106,.08), inset 0 0 60px #000 !important;}
.st-key-lector_castillo p, .st-key-lector_castillo li{color:#e8defa !important;}
.st-key-lector_castillo [data-testid="stMarkdownContainer"] > p:first-child::first-letter{
  font-family:'UnifrakturMaguntia',serif; font-size:3.4em; float:left; line-height:.8; color:#8dff6a; padding:.08em .08em 0 0;}
</style>""",
    "aranas": """<style>
:root{--sangre:#8a0a0a; --sangre-viva:#ff2a2a;}
.stApp{background:radial-gradient(ellipse at 50% 0%, #1a0505 0%, #020101 60%) fixed !important;}
.st-key-lector_aranas{position:relative; background:#080505 !important; border:1px solid #3a1010 !important;}
.st-key-lector_aranas::before{content:""; position:absolute; top:0; right:0; width:180px; height:180px; pointer-events:none; opacity:.35;
  background:url('data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none" stroke="%23ddd" stroke-width=".6"%3E%3Cpath d="M100 0L0 0M100 0L10 40M100 0L30 75M100 0L60 95M100 0L100 100"/%3E%3Cpath d="M80 0Q82 8 92 6Q96 15 100 20M60 0Q62 16 80 13Q88 30 100 40M40 0Q44 24 68 20Q78 44 100 60M20 0Q26 32 56 27Q68 58 100 80"/%3E%3C/svg%3E') no-repeat top right / contain;}
</style>""",
}

# Si el visitante sale de la historia de arañas, se borran las que quedaron en la página.
LIMPIEZA_ARANAS_JS = """
<script>
try{const D=window.parent.document, o=D.getElementById('aranas-overlay'); if(o) o.remove();
if(window.parent.__aranasMove){D.removeEventListener('mousemove',window.parent.__aranasMove); window.parent.__aranasMove=null;}}catch(e){}
</script>
"""


def escena_historia(entrada):
    cfg = ESCENA_CFG[entrada["escena"]]
    meta = "  ".join(x for x in [(entrada.get("extra") or "").upper(), fecha_vhs(entrada["fecha"])] if x)
    return (
        ESCENA_BASE.replace("__JS__", cfg["js"])
        .replace("__TEMA_CSS__", cfg["css"])
        .replace("__OSD__", cfg["osd"])
        .replace("__SEED__", str(cfg["seed"]))
        .replace("__ALT__", esc(cfg["alt"]))
        .replace("__META__", esc(meta))
        .replace("__TITULO__", esc(entrada["titulo"]))
    )


def es_youtube(url):
    return bool(url) and ("youtube.com" in url or "youtu.be" in url)


def mostrar_cassette(entrada):
    ruta = ruta_media(entrada.get("archivo"))
    url = entrada.get("url", "")
    if ruta and ruta.stat().st_size > LIMITE_EMBEBIDO_MB * 1024 * 1024:
        st.audio(str(ruta))
        return
    if not ruta and es_youtube(url):
        st.video(url)
        return
    src = data_uri(ruta) if ruta else url
    if not src:
        st.markdown("<p class='osd'><b>SIN SEÑAL</b> — falta el archivo de audio.</p>", unsafe_allow_html=True)
        return
    cinta = entrada.get("extra") or "CINTA SIN MARCA"
    doc = (
        CASSETTE_HTML.replace("__CINTA__", esc(cinta.upper()))
        .replace("__TITULO__", esc(entrada["titulo"]))
        .replace("__SRC__", esc(src))
    )
    incrustar(doc, 290)


# =============================================================================
# PÁGINAS
# =============================================================================
def pagina_inicio(db):
    aj = db["ajustes"]
    escena = ESCENA_HTML.replace("__TITULO__", esc(aj["titulo"])).replace("__SUBTITULO__", esc(aj["subtitulo"]))
    incrustar(escena, 560)

    st.write("")
    izq, der = st.columns([3, 2], gap="large")

    with izq:
        st.markdown("## Últimas transmisiones")
        recientes = ordenar(db["entradas"])[:6]
        if not recientes:
            st.markdown("<div class='vacio'><div class='osd'>CINTA EN BLANCO</div>"
                        "<p>Publica tu primera entrada desde la Sala de edición.</p></div>", unsafe_allow_html=True)
        for e in recientes:
            with st.container(key=f"fila_{e['id']}"):
                c1, c2, c3 = st.columns([1.3, 4, 1.2], vertical_alignment="center")
                c1.markdown(f"<div class='osd'>{fecha_vhs(e['fecha'])}<br><b>{esc(TIPOS[e['tipo']]['nombre'])}</b></div>",
                            unsafe_allow_html=True)
                c2.markdown(f"<p class='fila-titulo'>{esc(e['titulo'])}</p><p class='fila-resumen'>{esc(e.get('resumen'))}</p>",
                            unsafe_allow_html=True)
                c3.button("Abrir", key=f"abrir_{e['id']}", on_click=ir_a,
                          args=(SECCION_POR_TIPO[e["tipo"]], e["id"] if e["tipo"] in CON_DETALLE else None),
                          use_container_width=True)

    with der:
        st.markdown("## Quién graba")
        st.markdown(f"<div class='bio'><p>{esc(aj['bio'])}</p><div class='firma'>— {esc(aj['autor'])}</div></div>",
                    unsafe_allow_html=True)
        cuenta = {k: len(por_tipo(db, k)) for k in TIPOS}
        st.markdown(
            f"<p class='osd'>En el archivo: {cuenta['historia']} historias, {cuenta['cancion']} canciones, "
            f"{cuenta['video'] + cuenta['imagen']} piezas de metraje, {cuenta['recomendacion']} cintas en el videoclub "
            f"y {cuenta['proyecto']} creaciones en el laboratorio.</p>",
            unsafe_allow_html=True,
        )
        for sec in ["Historias", "Canciones", "Metraje", "Creaciones"]:
            st.button(f"Ir a {sec.lower()}", key=f"ir_{sec}", on_click=ir_a, args=(sec,), use_container_width=True)


def lector(db, entrada):
    historias = por_tipo(db, "historia")
    idx = next((i for i, h in enumerate(historias) if h["id"] == entrada["id"]), 0)
    tema = entrada.get("escena") if entrada.get("escena") in ESCENA_CFG else ""
    st.button("◄ Volver a las historias", on_click=ir_a, args=("Historias", None))
    if tema:
        st.markdown(TEMA_CSS[tema], unsafe_allow_html=True)
        incrustar(escena_historia(entrada), 520)
        st.write("")
    with st.container(key=f"lector_{tema or 'clasico'}"):
        meta = f"{fecha_vhs(entrada['fecha'])} &nbsp; {minutos_lectura(entrada.get('contenido'))} min de lectura"
        if entrada.get("extra"):
            meta = f"<b>{esc(entrada['extra'].upper())}</b> &nbsp; " + meta
        titulo = "" if tema else f"<div class='lector-titulo'>{esc(entrada['titulo'])}</div>"
        st.markdown(f"<div class='osd'>{meta}</div>{titulo}{html_etiquetas(entrada.get('etiquetas'))}",
                    unsafe_allow_html=True)
        portada = ruta_media(entrada.get("portada"))
        if portada:
            st.image(str(portada), use_container_width=True)
        st.write("")
        st.markdown(entrada.get("contenido") or "_Esta historia todavía no tiene texto._")
        st.markdown("<div class='fin'>FIN DE LA CINTA</div>", unsafe_allow_html=True)

    c1, _, c3 = st.columns([1, 1, 1])
    if idx + 1 < len(historias):
        anterior = historias[idx + 1]
        c1.button(f"◄ {anterior['titulo']}", key="ant", on_click=ir_a, args=("Historias", anterior["id"]),
                  use_container_width=True)
    if idx > 0:
        siguiente = historias[idx - 1]
        c3.button(f"{siguiente['titulo']} ►", key="sig", on_click=ir_a, args=("Historias", siguiente["id"]),
                  use_container_width=True)


def pagina_historias(db):
    leyendo = st.session_state.get("leyendo")
    entrada = next((e for e in db["entradas"] if e["id"] == leyendo and e["tipo"] == "historia"), None)
    if entrada:
        lector(db, entrada)
        return

    encabezado("Biblioteca sangrienta", "Relatos escritos por mí. Léelos con la luz apagada.")
    historias = por_tipo(db, "historia")
    buscar = st.text_input("Buscar por título o etiqueta", placeholder="viuda, anghell, rosas…").strip().lower()
    if buscar:
        historias = [h for h in historias
                     if buscar in h["titulo"].lower() or any(buscar in t.lower() for t in h.get("etiquetas", []))
                     or buscar in (h.get("extra") or "").lower()]
    if not historias:
        st.markdown("<div class='vacio'><div class='osd'>NO HAY EXPEDIENTES</div>"
                    "<p>Prueba otra búsqueda o publica una historia nueva desde la Sala de edición.</p></div>",
                    unsafe_allow_html=True)
        return
    for h in historias:
        with st.container(key=f"caso_{h['id']}"):
            coleccion = f"<b>{esc(h['extra'].upper())}</b> &nbsp; " if h.get("extra") else ""
            st.markdown(
                f"<div class='osd'>{coleccion}{fecha_vhs(h['fecha'])} &nbsp; {minutos_lectura(h.get('contenido'))} min</div>"
                f"<div class='caso-titulo'>{esc(h['titulo'])}</div>"
                f"<p>{esc(h.get('resumen'))}</p>{html_etiquetas(h.get('etiquetas'))}"
                + (f"<span class='tag tag-escena'>Escenario: {esc(ESCENAS[h['escena']])}</span>"
                   if h.get("escena") in ESCENA_CFG else ""),
                unsafe_allow_html=True,
            )
            st.button("Leer historia", key=f"leer_{h['id']}", on_click=ir_a, args=("Historias", h["id"]))


def pagina_canciones(db):
    encabezado("Frecuencias muertas", "Canciones grabadas por mí. Dale play y mira girar la cinta.")
    canciones = por_tipo(db, "cancion")
    if not canciones:
        st.markdown("<div class='vacio'><div class='osd'>NO HAY CINTAS</div>"
                    "<p>Sube tu primera canción desde la Sala de edición.</p></div>", unsafe_allow_html=True)
        return
    cols = st.columns(2, gap="large")
    for i, c in enumerate(canciones):
        with cols[i % 2]:
            mostrar_cassette(c)
            st.markdown(f"<div class='osd'>{fecha_vhs(c['fecha'])}</div><p>{esc(c.get('resumen'))}</p>",
                        unsafe_allow_html=True)
            if c.get("contenido"):
                with st.expander("Ver letra"):
                    st.markdown(c["contenido"])
            st.write("")


def pagina_metraje(db):
    encabezado("Metraje recuperado", "Video y fotos rescatados de cintas que no debían existir.")
    piezas = por_tipo(db, "video", "imagen")
    if not piezas:
        st.markdown("<div class='vacio'><div class='osd'>NO SIGNAL</div>"
                    "<p>Todavía no hay metraje. Sube un video o una imagen desde la Sala de edición.</p></div>",
                    unsafe_allow_html=True)
        return
    cols = st.columns(2, gap="large")
    for i, p in enumerate(piezas):
        with cols[i % 2]:
            with st.container(key=f"tape_{p['id']}"):
                modo = "PLAY ►" if p["tipo"] == "video" else "PAUSE ❚❚"
                st.markdown(f"<div class='tape-osd'><span class='play'>{modo}</span><span>{fecha_vhs(p['fecha'])}</span></div>",
                            unsafe_allow_html=True)
                ruta = ruta_media(p.get("archivo"))
                fuente = str(ruta) if ruta else p.get("url")
                if not fuente:
                    st.markdown("<p class='osd'><b>SIN SEÑAL</b></p>", unsafe_allow_html=True)
                elif p["tipo"] == "video":
                    st.video(fuente)
                else:
                    st.image(fuente, use_container_width=True)
                st.markdown(f"### {esc(p['titulo'])}")
                if p.get("contenido") or p.get("resumen"):
                    st.markdown(p.get("contenido") or p.get("resumen"))


def pagina_videoclub(db):
    encabezado("Videoclub maldito", "Lo que veo, juego y recomiendo. Rebobinar antes de devolver.")
    recs = por_tipo(db, "recomendacion")
    if not recs:
        st.markdown("<div class='vacio'><div class='osd'>ESTANTES VACÍOS</div>"
                    "<p>Agrega una recomendación desde la Sala de edición.</p></div>", unsafe_allow_html=True)
        return
    cols = st.columns(3, gap="medium")
    for i, r in enumerate(recs):
        with cols[i % 3]:
            portada = ruta_media(r.get("portada"))
            if portada:
                st.image(str(portada), use_container_width=True)
                st.markdown(f"### {esc(r['titulo'])}")
            else:
                st.markdown(
                    f"<div class='caratula'><div class='banda'>VHS · ARRIENDO</div>"
                    f"<div class='sticker'>Rebobinar antes de devolver</div>"
                    f"<div class='nombre'>{esc(r['titulo'])}</div><div class='formato'>{esc(r.get('extra'))}</div></div>",
                    unsafe_allow_html=True,
                )
            with st.expander("Leer reseña"):
                st.markdown(r.get("contenido") or r.get("resumen") or "Sin reseña todavía.")
            st.write("")


ICONOS_PASO = ["🔎", "🎵", "▶️", "⏳", "✨", "🎧", "📲", "💾"]


def url_segura(url):
    url = (url or "").strip()
    return url if url.lower().startswith(("http://", "https://")) else ""


def dominio(url):
    return re.sub(r"^https?://", "", url or "").rstrip("/")


def html_pantalla(entrada, canal=1):
    """Captura de la app dentro de un monitor CRT. Sin captura, dibuja una pantalla de ejemplo."""
    titulo = esc(entrada["titulo"])
    ch = f"<div class='ch'>CH {canal:02d}</div>"
    portada = ruta_media(entrada.get("portada"))
    if portada:
        return f"<div class='monitor'>{ch}<img src='{data_uri(portada)}' alt='Captura de {titulo}'></div>"
    url = url_segura(entrada.get("url"))
    es_vinilo = entrada.get("mock") == "vinilo"
    disco = "<div class='vinilo'></div>" if es_vinilo else ""
    buscador = "🔎 Buscar canción…" if es_vinilo else "► EN LÍNEA"
    sitio = esc(dominio(url) or "localhost")
    return (
        f"<div class='monitor'>{ch}<div class='mock'>"
        f"<div class='barra'><i></i><i></i><i></i><span class='url'>{sitio}</span></div>"
        f"<div class='cuerpo'>{disco}"
        f"<div class='texto'><div class='nombre-app'>{titulo}</div>"
        f"<div class='buscador'>{buscador}</div></div>"
        f"</div></div></div>"
    )


def html_paso(paso, n):
    ruta = ruta_media(paso.get("imagen"))
    if ruta:
        foto = f"<img src='{data_uri(ruta)}' alt='Foto {n}: {esc(paso.get('texto'))}'>"
    else:
        foto = f"<div class='paso-vacio'>{ICONOS_PASO[(n - 1) % len(ICONOS_PASO)]}</div>"
    return (f"<div class='paso'><div class='paso-num'>FOTO {n}</div><div class='paso-foto'>{foto}</div>"
            f"<p class='paso-texto'>{esc(paso.get('texto'))}</p></div>")


def detalle_creacion(entrada):
    st.button("◄ Volver a creaciones", on_click=ir_a, args=("Creaciones", None))
    encabezado(entrada["titulo"], entrada.get("extra", ""))
    izq, der = st.columns([3, 2], gap="large")
    with izq:
        st.markdown(html_pantalla(entrada), unsafe_allow_html=True)
    with der:
        st.markdown(f"<div class='osd'>{fecha_vhs(entrada['fecha'])}</div>{html_etiquetas(entrada.get('etiquetas'))}",
                    unsafe_allow_html=True)
        st.markdown(entrada.get("contenido") or entrada.get("resumen") or "_Sin descripción todavía._")
        url = url_segura(entrada.get("url"))
        if url:
            st.markdown(
                f"<a class='btn-app' href='{esc(url)}' target='_blank' rel='noopener noreferrer'>Ir a la App Web ►</a>"
                f"<div class='osd'>{esc(dominio(url))}</div>",
                unsafe_allow_html=True,
            )

    pasos = [p for p in entrada.get("pasos") or [] if p.get("texto") or p.get("imagen")]
    if pasos:
        st.write("")
        st.markdown("## Cómo se usa")
        st.markdown("<p class='osd'>Tutorial paso a paso. Sigue las fotos en orden.</p>", unsafe_allow_html=True)
        for inicio in range(0, len(pasos), 4):
            cols = st.columns(4, gap="medium")
            for j, paso in enumerate(pasos[inicio:inicio + 4]):
                with cols[j]:
                    st.markdown(html_paso(paso, inicio + j + 1), unsafe_allow_html=True)
        if url:
            st.write("")
            st.markdown(
                f"<a class='btn-app' href='{esc(url)}' target='_blank' rel='noopener noreferrer'>Ir a la App Web ►</a>",
                unsafe_allow_html=True,
            )


def pagina_creaciones(db):
    leyendo = st.session_state.get("leyendo")
    entrada = next((e for e in db["entradas"] if e["id"] == leyendo and e["tipo"] == "proyecto"), None)
    if entrada:
        detalle_creacion(entrada)
        return

    encabezado("Laboratorio de creaciones",
               "Apps web, código y experimentos hechos por mí. Haz clic en una pantalla para ver el detalle.")
    proyectos = por_tipo(db, "proyecto")
    if not proyectos:
        st.markdown("<div class='vacio'><div class='osd'>LABORATORIO VACÍO</div>"
                    "<p>Agrega tu primera creación desde la Sala de edición.</p></div>", unsafe_allow_html=True)
        return
    cols = st.columns(2, gap="large")
    for i, p in enumerate(proyectos):
        with cols[i % 2]:
            with st.container(key=f"app_{p['id']}"):
                st.markdown(
                    html_pantalla(p, i + 1)
                    + f"<div class='app-nombre'>{esc(p['titulo'])}</div>"
                    + (f"<div class='osd'>{esc(p['extra'])}</div>" if p.get("extra") else "")
                    + f"<p class='app-resumen'>{esc(p.get('resumen'))}</p>"
                    + f"<div class='app-ver'><span>► VER DETALLE</span><span>{fecha_vhs(p['fecha'])}</span></div>",
                    unsafe_allow_html=True,
                )
                st.button(f"Ver detalle de {p['titulo']}", key=f"verapp_{p['id']}", on_click=ir_a,
                          args=("Creaciones", p["id"]), use_container_width=True)


def pagina_oraculo(_db):
    encabezado("Pacto con la estrella negra", "Escribe tu nombre y tu fecha de origen. La cinta dirá el resto.")
    with st.form("oraculo"):
        nombre = st.text_input("Sujeto")
        nacimiento = st.date_input("Origen temporal", value=date(1990, 1, 1),
                                   min_value=date(1920, 1, 1), max_value=date.today())
        sellar = st.form_submit_button("Sellar el pacto")
    if sellar and not nombre.strip():
        st.warning("Escribe un nombre para sellar el pacto.")
    elif sellar:
        n = esc(nombre.strip())
        condenas = [
            f"El universo se oscurece a tu favor, {n}. Una oportunidad nacerá de las sombras.",
            f"Cuidado al dormir, {n}. Alguien de tu pasado acecha desde la estática del televisor.",
            f"Tu origen en {nacimiento.year} dejó una grieta. Algo cruzará esa grieta hacia ti hoy.",
            f"{n}… el fallo en la matriz es inminente. Prepárate para el caos.",
            f"No abras la puerta del balcón esta noche, {n}. Huele a humo y no es la cocina.",
            f"Hay una cinta con tu nombre en el videoclub, {n}. Nadie recuerda haberla grabado.",
        ]
        # La misma persona recibe siempre la misma condena hoy.
        azar = random.Random(f"{nombre.strip().lower()}|{nacimiento}|{date.today()}")
        st.markdown(f"<div class='condena'><div class='osd'>PREDICCIÓN ACEPTADA</div><p>{azar.choice(condenas)}</p></div>",
                    unsafe_allow_html=True)


# ---------------------------- SALA DE EDICIÓN --------------------------------
def formulario_nueva(db):
    tipo = st.selectbox("¿Qué vas a publicar?", list(TIPOS), format_func=lambda k: TIPOS[k]["nombre"])
    cfg = TIPOS[tipo]
    with st.form("nueva_entrada", clear_on_submit=True):
        titulo = st.text_input("Título")
        c1, c2 = st.columns(2)
        fecha = c1.date_input("Fecha", value=date.today(), min_value=date(1900, 1, 1))
        extra = c2.text_input(cfg["extra"]) if cfg["extra"] else ""
        escena = (st.selectbox("Escenario de la página", list(ESCENAS), format_func=ESCENAS.get)
                  if tipo == "historia" else "")
        resumen = st.text_area("Resumen corto (se ve en las listas)", height=80)
        contenido = st.text_area(cfg["contenido"], height=320 if tipo == "historia" else 150)
        etiquetas = st.text_input("Etiquetas, separadas por comas")
        archivo, url = None, ""
        if cfg["ext"]:
            archivo = st.file_uploader(f"Archivo ({', '.join(cfg['ext'])})", type=cfg["ext"])
            url = st.text_input("…o pega un enlace (YouTube, mp3, imagen)")
        elif cfg.get("enlace"):
            url = st.text_input("Enlace a la app web o al código (https://…)")
        etiqueta_portada = "Captura de pantalla de la app (se ve como su foto)" if tipo == "proyecto" else "Portada (opcional)"
        portada = st.file_uploader(etiqueta_portada, type=EXT_IMAGEN) if cfg["portada"] else None
        pasos_txt, fotos_pasos = "", []
        if tipo == "proyecto":
            pasos_txt = st.text_area("Tutorial: un paso por línea", height=120,
                                     placeholder="Ingresa el nombre de la canción\nSelecciona la canción\n…")
            fotos_pasos = st.file_uploader("Fotos del tutorial (una por paso)", type=EXT_IMAGEN,
                                           accept_multiple_files=True,
                                           help="Se ordenan por nombre: llámalas 1.png, 2.png, 3.png…") or []
        publicar = st.form_submit_button("Publicar")

    if not publicar:
        return
    if not titulo.strip():
        st.error("Falta el título.")
        return
    if cfg["ext"] and archivo is None and not url.strip():
        st.error("Sube un archivo o pega un enlace.")
        return
    entrada = {
        "id": uuid.uuid4().hex[:10],
        "tipo": tipo,
        "titulo": titulo.strip(),
        "fecha": fecha.isoformat(),
        "extra": extra.strip(),
        "escena": escena,
        "resumen": resumen.strip(),
        "contenido": contenido.strip(),
        "etiquetas": [t.strip() for t in etiquetas.split(",") if t.strip()],
        "archivo": guardar_archivo(archivo),
        "url": url.strip(),
        "portada": guardar_archivo(portada),
    }
    if tipo == "proyecto":
        entrada["pasos"] = armar_pasos(pasos_txt, fotos_pasos)
    db["entradas"].append(entrada)
    guardar_db(db)
    st.success(f"Publicado: {entrada['titulo']}")
    st.button(f"Ver en {SECCION_POR_TIPO[tipo]}", on_click=ir_a,
              args=(SECCION_POR_TIPO[tipo], entrada["id"] if tipo in CON_DETALLE else None))


def archivo_existente(db):
    filtro = st.selectbox("Mostrar", ["todo"] + list(TIPOS),
                          format_func=lambda k: "Todo" if k == "todo" else TIPOS[k]["nombre"])
    entradas = ordenar([e for e in db["entradas"] if filtro == "todo" or e["tipo"] == filtro])
    if not entradas:
        st.info("No hay entradas de este tipo.")
        return
    for e in entradas:
        cfg = TIPOS[e["tipo"]]
        with st.expander(f"{fecha_vhs(e['fecha'])}  |  {cfg['nombre']}  |  {e['titulo']}"):
            with st.form(f"editar_{e['id']}"):
                titulo = st.text_input("Título", value=e["titulo"])
                c1, c2 = st.columns(2)
                try:
                    f_val = date.fromisoformat(e["fecha"])
                except ValueError:
                    f_val = date.today()
                fecha = c1.date_input("Fecha", value=f_val, min_value=date(1900, 1, 1))
                extra = c2.text_input(cfg["extra"], value=e.get("extra", "")) if cfg["extra"] else ""
                opciones = list(ESCENAS)
                escena = (st.selectbox("Escenario de la página", opciones, format_func=ESCENAS.get,
                                       index=opciones.index(e.get("escena", "")) if e.get("escena", "") in opciones else 0)
                          if e["tipo"] == "historia" else "")
                resumen = st.text_area("Resumen corto", value=e.get("resumen", ""), height=80)
                contenido = st.text_area(cfg["contenido"], value=e.get("contenido", ""),
                                         height=260 if e["tipo"] == "historia" else 130)
                etiquetas = st.text_input("Etiquetas", value=", ".join(e.get("etiquetas", [])))
                url = st.text_input("Enlace", value=e.get("url", "")) if cfg["ext"] or cfg.get("enlace") else ""
                es_proyecto = e["tipo"] == "proyecto"
                portada = (st.file_uploader("Reemplazar captura" if es_proyecto else "Reemplazar portada", type=EXT_IMAGEN)
                           if cfg["portada"] else None)
                pasos_txt, fotos_pasos = "", []
                if es_proyecto:
                    pasos_txt = st.text_area("Tutorial: un paso por línea", height=120,
                                             value="\n".join(p.get("texto", "") for p in e.get("pasos") or []))
                    fotos_pasos = st.file_uploader("Reemplazar fotos del tutorial (todas, una por paso)", type=EXT_IMAGEN,
                                                   accept_multiple_files=True,
                                                   help="Si no subes nada se mantienen las fotos actuales. "
                                                        "Se ordenan por nombre: 1.png, 2.png…") or []
                guardar = st.form_submit_button("Guardar cambios")
            if guardar:
                e.update({
                    "titulo": titulo.strip() or e["titulo"],
                    "fecha": fecha.isoformat(),
                    "extra": extra.strip(),
                    "escena": escena,
                    "resumen": resumen.strip(),
                    "contenido": contenido.strip(),
                    "etiquetas": [t.strip() for t in etiquetas.split(",") if t.strip()],
                    "url": url.strip(),
                })
                if es_proyecto:
                    viejos = e.get("pasos") or []
                    nuevos = armar_pasos(pasos_txt, fotos_pasos, viejos)
                    usadas = {p["imagen"] for p in nuevos}
                    for p in viejos:
                        sobrante = ruta_media(p.get("imagen")) if p.get("imagen") not in usadas else None
                        if sobrante:
                            sobrante.unlink(missing_ok=True)
                    e["pasos"] = nuevos
                if portada is not None:
                    vieja = ruta_media(e.get("portada"))
                    if vieja:
                        vieja.unlink(missing_ok=True)
                    e["portada"] = guardar_archivo(portada)
                guardar_db(db)
                st.success("Cambios guardados.")

            confirmar = st.checkbox("Quiero borrar esta entrada", key=f"conf_{e['id']}")
            if st.button("Borrar definitivamente", key=f"borrar_{e['id']}", disabled=not confirmar):
                borrar_media(e)
                db["entradas"] = [x for x in db["entradas"] if x["id"] != e["id"]]
                guardar_db(db)
                st.rerun()


def ajustes_sitio(db):
    aj = db["ajustes"]
    with st.form("ajustes"):
        titulo = st.text_input("Nombre del blog", value=aj["titulo"])
        subtitulo = st.text_input("Bajada", value=aj["subtitulo"])
        autor = st.text_input("Firma", value=aj["autor"])
        bio = st.text_area("Sobre mí", value=aj["bio"], height=120)
        guardar = st.form_submit_button("Guardar ajustes")
    if guardar:
        aj.update({"titulo": titulo.strip(), "subtitulo": subtitulo.strip(), "autor": autor.strip(), "bio": bio.strip()})
        guardar_db(db)
        st.success("Ajustes guardados.")
    st.download_button("Descargar respaldo (entradas.json)",
                       data=json.dumps(db, ensure_ascii=False, indent=2),
                       file_name="entradas.json", mime="application/json")


def pagina_admin(db):
    encabezado("Sala de edición", "Solo para quien graba. Publica, corrige o borra.")
    if not st.session_state.get("admin"):
        with st.form("login"):
            clave = st.text_input("Contraseña", type="password")
            entrar = st.form_submit_button("Entrar")
        if entrar:
            if clave == clave_admin():
                st.session_state.admin = True
                st.rerun()
            st.error("Contraseña incorrecta.")
        return

    if clave_admin() == CLAVE_POR_DEFECTO:
        st.warning("Estás usando la contraseña por defecto. Define ADMIN_PASSWORD en .streamlit/secrets.toml.")
    tab1, tab2, tab3 = st.tabs(["Nueva entrada", "Archivo", "Ajustes"])
    with tab1:
        formulario_nueva(db)
    with tab2:
        archivo_existente(db)
    with tab3:
        ajustes_sitio(db)
    st.write("")
    if st.button("Cerrar sesión"):
        st.session_state.admin = False
        st.rerun()


# =============================================================================
# APP
# =============================================================================
def main():
    st.markdown(CSS, unsafe_allow_html=True)
    incrustar(SFX_JS, 0)

    db = cargar_db()
    st.session_state.setdefault("nav", "Inicio")
    st.session_state.setdefault("leyendo", None)

    leyendo = next((e for e in db["entradas"] if e["id"] == st.session_state.leyendo), None)
    en_aranas = st.session_state.nav == "Historias" and leyendo is not None and leyendo.get("escena") == "aranas"
    if not en_aranas:
        incrustar(LIMPIEZA_ARANAS_JS, 0)

    with st.sidebar:
        st.markdown("<div class='logo'><div class='cinta'>TAPE 01</div><div class='modo'>PLAY ► SP</div></div>",
                    unsafe_allow_html=True)
        st.radio(
            "Secciones",
            SECCIONES,
            key="nav",
            label_visibility="collapsed",
            format_func=lambda s: f"[ TRACK {SECCIONES.index(s)} ] {s}",
            on_change=lambda: st.session_state.update(leyendo=None),
        )
        st.markdown(f"<div class='pie'><span class='rec'>●</span> REC<br>© {date.today().year} {esc(db['ajustes']['autor'])}</div>",
                    unsafe_allow_html=True)

    paginas = {
        "Inicio": pagina_inicio,
        "Historias": pagina_historias,
        "Canciones": pagina_canciones,
        "Metraje": pagina_metraje,
        "Videoclub": pagina_videoclub,
        "Creaciones": pagina_creaciones,
        "Oráculo": pagina_oraculo,
        "Sala de edición": pagina_admin,
    }
    paginas[st.session_state.nav](db)


main()
