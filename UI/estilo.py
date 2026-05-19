import streamlit as st

# ==========================================================
# PALETA DE COLORES
# Cambia aquí los colores corporativos cuando los tengas
# ==========================================================
COLORES = {
    # Color principal — encabezados, botones primarios, tabs activos
    "primario":         "#1B3A5C",

    # Color secundario — hover, acentos suaves
    "secundario":       "#2E6DA4",

    # Color acento — badges, highlights
    "acento":           "#3498DB",

    # Fondo general de la app
    "fondo":            "#F4F6F9",

    # Fondo de tarjetas y contenedores
    "fondo_card":       "#FFFFFF",

    # Texto principal
    "texto":            "#1A1A2E",

    # Texto secundario / subtítulos
    "texto_suave":      "#5A6A7E",

    # Bordes
    "borde":            "#DDE3EC",

    # Éxito
    "exito":            "#27AE60",

    # Advertencia
    "advertencia":      "#F39C12",

    # Error
    "error":            "#E74C3C",

    # Fondo tabla — fila alternada
    "tabla_par":        "#F8FAFC",
    "tabla_impar":      "#FFFFFF",
    "tabla_header":     "#EBF0F7",
}

# ==========================================================
# TIPOGRAFÍA
# Cambia aquí la fuente si tu empresa tiene una definida
# ==========================================================
FUENTE_URL = "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap"
FUENTE_PRINCIPAL = "'IBM Plex Sans', sans-serif"
FUENTE_MONO = "'IBM Plex Mono', monospace"

# ==========================================================
# INYECTAR ESTILOS
# Llama esta función al inicio de app.py
# ==========================================================
def aplicar_estilos():

    st.markdown(f'<link href="{FUENTE_URL}" rel="stylesheet">', unsafe_allow_html=True)

    st.markdown(f"""
    <style>

    /* ======================================================
       RESET Y BASE
    ====================================================== */
    html, body, [class*="css"] {{
        font-family: {FUENTE_PRINCIPAL};
        color: {COLORES['texto']};
    }}

    /* ======================================================
       FONDO GENERAL
    ====================================================== */
    .stApp {{
        background-color: {COLORES['fondo']};
    }}

    /* ======================================================
       ENCABEZADO PRINCIPAL (barra superior de Streamlit)
    ====================================================== */
    header[data-testid="stHeader"] {{
        background-color: {COLORES['primario']};
        border-bottom: 2px solid {COLORES['secundario']};
    }}

    /* ======================================================
       TÍTULOS
    ====================================================== */
    h1 {{
        font-family: {FUENTE_PRINCIPAL};
        font-weight: 600;
        font-size: 1.6rem;
        color: {COLORES['primario']};
        padding-bottom: 0.3rem;
        border-bottom: 2px solid {COLORES['acento']};
        margin-bottom: 1.2rem;
    }}

    h2 {{
        font-family: {FUENTE_PRINCIPAL};
        font-weight: 500;
        font-size: 1.2rem;
        color: {COLORES['primario']};
        margin-bottom: 0.8rem;
    }}

    h3 {{
        font-family: {FUENTE_PRINCIPAL};
        font-weight: 500;
        font-size: 1rem;
        color: {COLORES['texto_suave']};
    }}

    /* ======================================================
       PESTAÑAS (TABS)
    ====================================================== */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: {COLORES['fondo_card']};
        border-radius: 8px 8px 0 0;
        border-bottom: 2px solid {COLORES['borde']};
        gap: 0;
        padding: 0 8px;
    }}

    .stTabs [data-baseweb="tab"] {{
        font-family: {FUENTE_PRINCIPAL};
        font-weight: 500;
        font-size: 0.85rem;
        color: {COLORES['texto_suave']};
        padding: 12px 24px;
        border-radius: 8px 8px 0 0;
        border: none;
        background: transparent;
        letter-spacing: 0.03em;
        transition: color 0.2s ease;
    }}

    .stTabs [data-baseweb="tab"]:hover {{
        color: {COLORES['secundario']};
        background-color: {COLORES['tabla_par']};
    }}

    .stTabs [aria-selected="true"] {{
        color: {COLORES['primario']} !important;
        border-bottom: 3px solid {COLORES['acento']} !important;
        background-color: {COLORES['fondo_card']} !important;
        font-weight: 600 !important;
    }}

    .stTabs [data-baseweb="tab-panel"] {{
        background-color: {COLORES['fondo_card']};
        border-radius: 0 0 8px 8px;
        padding: 1.5rem;
        border: 1px solid {COLORES['borde']};
        border-top: none;
    }}

    /* ======================================================
       BOTONES PRIMARIOS
    ====================================================== */
    .stButton > button {{
        font-family: {FUENTE_PRINCIPAL};
        font-weight: 500;
        font-size: 0.85rem;
        background-color: {COLORES['primario']};
        color: #FFFFFF;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1.2rem;
        letter-spacing: 0.02em;
        transition: background-color 0.2s ease, transform 0.1s ease;
        cursor: pointer;
    }}

    .stButton > button:hover {{
        background-color: {COLORES['secundario']};
        transform: translateY(-1px);
    }}

    .stButton > button:active {{
        transform: translateY(0px);
    }}

    /* ======================================================
       BOTONES DE DESCARGA
    ====================================================== */
    .stDownloadButton > button {{
        font-family: {FUENTE_PRINCIPAL};
        font-weight: 500;
        font-size: 0.82rem;
        background-color: {COLORES['fondo_card']};
        color: {COLORES['secundario']};
        border: 1.5px solid {COLORES['secundario']};
        border-radius: 6px;
        padding: 0.4rem 1rem;
        transition: all 0.2s ease;
        width: 100%;
    }}

    .stDownloadButton > button:hover {{
        background-color: {COLORES['secundario']};
        color: #FFFFFF;
    }}

    /* ======================================================
       FILE UPLOADER
    ====================================================== */
    [data-testid="stFileUploader"] {{
        background-color: {COLORES['fondo_card']};
        border: 1.5px dashed {COLORES['borde']};
        border-radius: 8px;
        padding: 0.5rem;
        transition: border-color 0.2s ease;
    }}

    [data-testid="stFileUploader"]:hover {{
        border-color: {COLORES['acento']};
    }}

    /* ======================================================
       INPUTS Y SELECTBOXES
    ====================================================== */
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stMultiSelect > div > div {{
        font-family: {FUENTE_PRINCIPAL};
        font-size: 0.85rem;
        border-radius: 6px;
        border: 1.5px solid {COLORES['borde']};
        background-color: {COLORES['fondo_card']};
        color: {COLORES['texto']};
        transition: border-color 0.2s ease;
    }}

    .stTextInput > div > div > input:focus {{
        border-color: {COLORES['acento']};
        box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.15);
    }}

    /* ======================================================
       TABLA (data editor)
    ====================================================== */
    [data-testid="stDataEditor"] {{
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid {COLORES['borde']};
        font-family: {FUENTE_PRINCIPAL};
        font-size: 0.82rem;
    }}

    /* ======================================================
       EXPANDER
    ====================================================== */
    .streamlit-expanderHeader {{
        font-family: {FUENTE_PRINCIPAL};
        font-weight: 500;
        font-size: 0.88rem;
        color: {COLORES['primario']};
        background-color: {COLORES['tabla_header']};
        border-radius: 6px;
        padding: 0.6rem 1rem;
        border: 1px solid {COLORES['borde']};
    }}

    .streamlit-expanderContent {{
        background-color: {COLORES['fondo_card']};
        border: 1px solid {COLORES['borde']};
        border-top: none;
        border-radius: 0 0 6px 6px;
        padding: 1rem;
    }}

    /* ======================================================
       MENSAJES — success, warning, error, info
    ====================================================== */
    [data-testid="stAlert"] {{
        border-radius: 6px;
        font-family: {FUENTE_PRINCIPAL};
        font-size: 0.85rem;
        border-left-width: 4px;
    }}

    /* ======================================================
       DIVIDER
    ====================================================== */
    hr {{
        border: none;
        border-top: 1px solid {COLORES['borde']};
        margin: 0.8rem 0;
    }}

    /* ======================================================
       CHECKBOX
    ====================================================== */
    .stCheckbox > label {{
        font-family: {FUENTE_PRINCIPAL};
        font-size: 0.85rem;
        color: {COLORES['texto']};
    }}

    /* ======================================================
       CAPTION / TEXTO PEQUEÑO
    ====================================================== */
    .stCaption {{
        font-family: {FUENTE_PRINCIPAL};
        font-size: 0.78rem;
        color: {COLORES['texto_suave']};
    }}

    /* ======================================================
       SUBHEADER
    ====================================================== */
    [data-testid="stMarkdownContainer"] h3 {{
        font-size: 1rem;
        font-weight: 600;
        color: {COLORES['primario']};
        margin-top: 1rem;
    }}

    /* ======================================================
       SCROLLBAR
    ====================================================== */
    ::-webkit-scrollbar {{
        width: 6px;
        height: 6px;
    }}

    ::-webkit-scrollbar-track {{
        background: {COLORES['fondo']};
    }}

    ::-webkit-scrollbar-thumb {{
        background: {COLORES['borde']};
        border-radius: 3px;
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: {COLORES['texto_suave']};
    }}

    /* ======================================================
       OCULTAR ELEMENTOS DEFAULT DE STREAMLIT
    ====================================================== */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    [data-testid="stToolbar"] {{display: none;}}

    </style>
    """, unsafe_allow_html=True)


# ==========================================================
# COMPONENTES REUTILIZABLES
# ==========================================================

def badge_estado(estado: str) -> str:
    """Retorna HTML de un badge coloreado según el estado."""
    colores_badge = {
        "CERRADO":      ("#D5F5E3", "#1E8449"),
        "PENDIENTE":    ("#FDEBD0", "#A04000"),
        "CALIDAD":      ("#D6EAF8", "#1A5276"),
        "EN REVISIÓN":  ("#FEF9E7", "#9A7D0A"),
        "NO APLICA":    ("#F2F3F4", "#717D7E"),
    }
    val = str(estado).strip().upper()
    bg, fg = colores_badge.get(val, ("#F2F3F4", "#717D7E"))
    return (
        f'<span style="background-color:{bg}; color:{fg}; '
        f'padding:2px 10px; border-radius:12px; '
        f'font-size:0.75rem; font-weight:600; '
        f'font-family:{FUENTE_PRINCIPAL};">'
        f'{estado}</span>'
    )


def encabezado_seccion(titulo: str, subtitulo: str = ""):
    """Encabezado visual para cada sección."""
    sub_html = (
        f'<p style="color:{COLORES["texto_suave"]}; '
        f'font-size:0.82rem; margin:0 0 1rem 0;">{subtitulo}</p>'
        if subtitulo else ""
    )
    st.markdown(
        f"""
        <div style="margin-bottom:1rem;">
            <h2 style="
                font-family:{FUENTE_PRINCIPAL};
                font-weight:600;
                font-size:1.1rem;
                color:{COLORES['primario']};
                margin:0 0 2px 0;
                padding-bottom:6px;
                border-bottom:2px solid {COLORES['acento']};
            ">{titulo}</h2>
            {sub_html}
        </div>
        """,
        unsafe_allow_html=True
    )


def tarjeta(contenido_html: str):
    """Envuelve contenido en una tarjeta con sombra suave."""
    st.markdown(
        f"""
        <div style="
            background:{COLORES['fondo_card']};
            border:1px solid {COLORES['borde']};
            border-radius:8px;
            padding:1rem 1.2rem;
            margin-bottom:0.8rem;
        ">
            {contenido_html}
        </div>
        """,
        unsafe_allow_html=True
    )