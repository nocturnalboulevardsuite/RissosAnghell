"""
EL RINCÓN DE RISSOS — Blog personal estilo lost media / VHS / años 80.

Estructura:
  - Inicio: escena animada (callejón de ladrillos + terraza en llamas) y últimas entradas.
  - Historias: relatos propios con lector tipo expediente.
  - Canciones: reproductor de cassette con carretes que giran.
  - Metraje: videos e imágenes en marco VHS.
  - Videoclub: recomendaciones de películas/series.
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
}

SECCIONES = ["Inicio", "Historias", "Canciones", "Metraje", "Videoclub", "Oráculo", "Sala de edición"]
SECCION_POR_TIPO = {
    "historia": "Historias",
    "cancion": "Canciones",
    "video": "Metraje",
    "imagen": "Metraje",
    "recomendacion": "Videoclub",
}
MESES = ["ENE.", "FEB.", "MAR.", "ABR.", "MAY.", "JUN.", "JUL.", "AGO.", "SEP.", "OCT.", "NOV.", "DIC."]

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
    "entradas": [
        {
            "id": "demo-viuda",
            "tipo": "historia",
            "titulo": "La viuda negra",
            "fecha": "2026-10-13",
            "extra": "Anghell",
            "resumen": "Algo baja desde el techo cada noche. El hilo está manchado de óxido.",
            "contenido": (
                "Las patas crujen en la oscuridad.\n\n"
                "El hilo de seda baja desde el techo, manchado de óxido, y se detiene "
                "a la altura de mis ojos. Cada noche baja un poco más. Cada noche el "
                "cuarto huele más a hierro.\n\n"
                "*Texto de ejemplo: edítalo o bórralo desde la Sala de edición.*"
            ),
            "etiquetas": ["anghell", "arañas"],
            "archivo": "",
            "url": "",
            "portada": "",
        },
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
    return db


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
    for campo in ("archivo", "portada"):
        ruta = ruta_media(entrada.get(campo, ""))
        if ruta:
            ruta.unlink(missing_ok=True)


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
@import url('https://fonts.googleapis.com/css2?family=Creepster&family=Special+Elite&family=VT323&display=swap');

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
.st-key-lector{
  max-width:46rem; margin:0 auto; background:#0b0506; border:1px solid var(--linea);
  padding:2.4rem clamp(1.2rem, 4vw, 3rem) 2rem; box-shadow:0 0 60px rgba(0,0,0,.8) inset;
}
.st-key-lector p, .st-key-lector li{font-size:1.12rem; line-height:1.9; color:#e3d8cb;}
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

/* Oráculo */
.condena{border:1px solid var(--sangre); background:rgba(179,6,15,.08); padding:1.6rem; text-align:center; margin-top:1.2rem;}
.condena .osd{font-size:1.4rem; color:var(--sangre-viva);}
.condena p{font-size:1.3rem;}

/* Vacío */
.vacio{border:1px dashed var(--linea); padding:2rem; text-align:center;}
.vacio .osd{font-size:1.6rem; color:var(--sangre-viva);}

@media (prefers-reduced-motion: reduce){
  .stApp::before, .stApp::after, .glitch::before, .glitch::after, .pie .rec{animation:none !important;}
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
                          args=(SECCION_POR_TIPO[e["tipo"]], e["id"] if e["tipo"] == "historia" else None),
                          use_container_width=True)

    with der:
        st.markdown("## Quién graba")
        st.markdown(f"<div class='bio'><p>{esc(aj['bio'])}</p><div class='firma'>— {esc(aj['autor'])}</div></div>",
                    unsafe_allow_html=True)
        cuenta = {k: len(por_tipo(db, k)) for k in TIPOS}
        st.markdown(
            f"<p class='osd'>En el archivo: {cuenta['historia']} historias, {cuenta['cancion']} canciones, "
            f"{cuenta['video'] + cuenta['imagen']} piezas de metraje y {cuenta['recomendacion']} cintas en el videoclub.</p>",
            unsafe_allow_html=True,
        )
        for sec in ["Historias", "Canciones", "Metraje"]:
            st.button(f"Ir a {sec.lower()}", key=f"ir_{sec}", on_click=ir_a, args=(sec,), use_container_width=True)


def lector(db, entrada):
    historias = por_tipo(db, "historia")
    idx = next((i for i, h in enumerate(historias) if h["id"] == entrada["id"]), 0)
    st.button("◄ Volver a las historias", on_click=ir_a, args=("Historias", None))
    with st.container(key="lector"):
        meta = f"{fecha_vhs(entrada['fecha'])} &nbsp; {minutos_lectura(entrada.get('contenido'))} min de lectura"
        if entrada.get("extra"):
            meta = f"<b>{esc(entrada['extra'].upper())}</b> &nbsp; " + meta
        st.markdown(f"<div class='osd'>{meta}</div><div class='lector-titulo'>{esc(entrada['titulo'])}</div>"
                    f"{html_etiquetas(entrada.get('etiquetas'))}", unsafe_allow_html=True)
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
                f"<p>{esc(h.get('resumen'))}</p>{html_etiquetas(h.get('etiquetas'))}",
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
        resumen = st.text_area("Resumen corto (se ve en las listas)", height=80)
        contenido = st.text_area(cfg["contenido"], height=320 if tipo == "historia" else 150)
        etiquetas = st.text_input("Etiquetas, separadas por comas")
        archivo, url = None, ""
        if cfg["ext"]:
            archivo = st.file_uploader(f"Archivo ({', '.join(cfg['ext'])})", type=cfg["ext"])
            url = st.text_input("…o pega un enlace (YouTube, mp3, imagen)")
        portada = st.file_uploader("Portada (opcional)", type=EXT_IMAGEN) if cfg["portada"] else None
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
        "resumen": resumen.strip(),
        "contenido": contenido.strip(),
        "etiquetas": [t.strip() for t in etiquetas.split(",") if t.strip()],
        "archivo": guardar_archivo(archivo),
        "url": url.strip(),
        "portada": guardar_archivo(portada),
    }
    db["entradas"].append(entrada)
    guardar_db(db)
    st.success(f"Publicado: {entrada['titulo']}")
    st.button(f"Ver en {SECCION_POR_TIPO[tipo]}", on_click=ir_a,
              args=(SECCION_POR_TIPO[tipo], entrada["id"] if tipo == "historia" else None))


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
                resumen = st.text_area("Resumen corto", value=e.get("resumen", ""), height=80)
                contenido = st.text_area(cfg["contenido"], value=e.get("contenido", ""),
                                         height=260 if e["tipo"] == "historia" else 130)
                etiquetas = st.text_input("Etiquetas", value=", ".join(e.get("etiquetas", [])))
                url = st.text_input("Enlace", value=e.get("url", "")) if cfg["ext"] else ""
                portada = st.file_uploader("Reemplazar portada", type=EXT_IMAGEN) if cfg["portada"] else None
                guardar = st.form_submit_button("Guardar cambios")
            if guardar:
                e.update({
                    "titulo": titulo.strip() or e["titulo"],
                    "fecha": fecha.isoformat(),
                    "extra": extra.strip(),
                    "resumen": resumen.strip(),
                    "contenido": contenido.strip(),
                    "etiquetas": [t.strip() for t in etiquetas.split(",") if t.strip()],
                    "url": url.strip(),
                })
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
        "Oráculo": pagina_oraculo,
        "Sala de edición": pagina_admin,
    }
    paginas[st.session_state.nav](db)


main()
