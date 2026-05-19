import streamlit as st
import pandas as pd

from UI.carga import cargar_archivo
from UI.filtros import aplicar_filtros
from UI.tabla import mostrar_tabla
from UI.guardar import guardar_consolidado
from UI.documentos import mostrar_resoluciones
from UI.carta_cumplimiento import mostrar_carta_cumplimiento
from UI.estilo import aplicar_estilos
from UI.login import mostrar_login
from UI.estado import (
    mostrar_aviso_bloqueo,
    ESTADO_CARGANDO,
    ESTADO_GUARDANDO
)
from database import (
    leer_tickets, leer_feriados,
    escribir_estado, liberar_estado, sistema_libre
)

# ==========================================================
# CONFIGURACIÓN APP
# ==========================================================
st.set_page_config(page_title="Gestión de Reclamos ATC", layout="wide")
aplicar_estilos()

# ==========================================================
# LOGIN
# ==========================================================
if not mostrar_login():
    st.stop()

usuario = st.session_state.usuario_nombre

st.markdown(
    f"""
    <div style="position:fixed; top:14px; right:80px; z-index:999;
                font-size:0.8rem; color:#fff; background:#1B3A5C;
                padding:4px 12px; border-radius:20px;">
        👤 {usuario}
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# FERIADOS DESDE SUPABASE
# ==========================================================
@st.cache_data(ttl=3600)
def cargar_feriados():
    return leer_feriados()

FERIADOS = cargar_feriados()

# ==========================================================
# SESSION STATE
# ==========================================================
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()

if "df_anterior" not in st.session_state:
    st.session_state.df_anterior = pd.DataFrame()

if "vista_activa" not in st.session_state:
    st.session_state.vista_activa = "inicio"

# ==========================================================
# CARGAR TICKETS DESDE SUPABASE AL INICIAR
# ==========================================================
if st.session_state.df.empty:
    with st.spinner("Cargando consolidado..."):
        st.session_state.df = leer_tickets()
        st.session_state.df_anterior = st.session_state.df.copy()

# ==========================================================
# PANTALLA INICIAL
# ==========================================================
if st.session_state.vista_activa == "inicio":

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align:center; margin-bottom:2rem;">
            <h1 style="font-size:1.8rem; margin-bottom:0.4rem;">
                Gestión de Reclamos ATC
            </h1>
            <p style="color:#5A6A7E; font-size:0.95rem;">
                ¿Qué deseas hacer hoy?
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            """
            <div style="background:#fff; border:1px solid #DDE3EC;
                        border-radius:10px; padding:1.5rem; text-align:center;
                        margin-bottom:0.5rem;">
                <div style="font-size:2rem; margin-bottom:0.8rem;">📂</div>
                <p style="font-weight:600; font-size:1rem; color:#1B3A5C; margin-bottom:0.4rem;">
                    Cargar nuevo reporte</p>
                <p style="font-size:0.82rem; color:#5A6A7E;">
                    Sube un Excel para procesar y actualizar la base</p>
            </div>
            """, unsafe_allow_html=True
        )
        if st.button("Ir a Cargar reporte →", key="btn_carga", use_container_width=True):
            st.session_state.vista_activa = "carga"
            st.rerun()

    with c2:
        st.markdown(
            """
            <div style="background:#fff; border:1px solid #DDE3EC;
                        border-radius:10px; padding:1.5rem; text-align:center;
                        margin-bottom:0.5rem;">
                <div style="font-size:2rem; margin-bottom:0.8rem;">📋</div>
                <p style="font-weight:600; font-size:1rem; color:#1B3A5C; margin-bottom:0.4rem;">
                    Actualizar consolidado</p>
                <p style="font-size:0.82rem; color:#5A6A7E;">
                    Revisa y edita los campos manuales</p>
            </div>
            """, unsafe_allow_html=True
        )
        if st.button("Ir a Consolidado →", key="btn_consolidado", use_container_width=True):
            st.session_state.vista_activa = "consolidado"
            st.rerun()

    with c3:
        st.markdown(
            """
            <div style="background:#fff; border:1px solid #DDE3EC;
                        border-radius:10px; padding:1.5rem; text-align:center;
                        margin-bottom:0.5rem;">
                <div style="font-size:2rem; margin-bottom:0.8rem;">📄</div>
                <p style="font-weight:600; font-size:1rem; color:#1B3A5C; margin-bottom:0.4rem;">
                    Carta de cumplimiento</p>
                <p style="font-size:0.82rem; color:#5A6A7E;">
                    Genera y descarga cartas para los tickets</p>
            </div>
            """, unsafe_allow_html=True
        )
        if st.button("Ir a Cartas →", key="btn_cartas", use_container_width=True):
            st.session_state.vista_activa = "cartas"
            st.rerun()

    with c4:
        st.markdown(
            """
            <div style="background:#fff; border:1px solid #DDE3EC;
                        border-radius:10px; padding:1.5rem; text-align:center;
                        margin-bottom:0.5rem;">
                <div style="font-size:2rem; margin-bottom:0.8rem;">⚠️</div>
                <p style="font-weight:600; font-size:1rem; color:#1B3A5C; margin-bottom:0.4rem;">
                    Generar Resolución</p>
                <p style="font-size:0.82rem; color:#5A6A7E;">
                    Usar solo si el sistema principal falla</p>
            </div>
            """, unsafe_allow_html=True
        )
        if st.button("Ir a Resoluciones →", key="btn_resoluciones", use_container_width=True):
            st.session_state.vista_activa = "resoluciones"
            st.rerun()

    st.stop()

# ==========================================================
# BOTÓN VOLVER
# ==========================================================
def _btn_volver():
    if st.button("← Volver al inicio", key="btn_volver"):
        st.session_state.vista_activa = "inicio"
        st.rerun()

# ==========================================================
# VISTA 1 — CARGAR NUEVO REPORTE
# ==========================================================
if st.session_state.vista_activa == "carga":

    _btn_volver()
    st.title("Cargar nuevo reporte")

    bloqueado = mostrar_aviso_bloqueo()

    archivo = st.file_uploader(
        "Selecciona el archivo Excel a procesar",
        type=["xlsx"],
        disabled=bloqueado
    )

    if st.button(
        "⚙️ Procesar y actualizar consolidado",
        disabled=bloqueado or archivo is None,
        key="btn_procesar"
    ):
        if not sistema_libre():
            st.error("⛔ El sistema está ocupado. Intenta en unos momentos.")
        else:
            try:
                escribir_estado(ESTADO_CARGANDO, usuario)
                with st.spinner("Procesando reporte y sincronizando con Supabase..."):
                    df_nuevo = cargar_archivo(archivo, FERIADOS, usuario)
                    st.session_state.df = leer_tickets()
                    st.session_state.df_anterior = st.session_state.df.copy()
                st.success("✅ Reporte procesado. Puedes ir a Actualizar consolidado para revisar.")
            except Exception as e:
                st.error(f"❌ Error al procesar: {e}")
            finally:
                liberar_estado()

# ==========================================================
# VISTA 2 — ACTUALIZAR CONSOLIDADO
# ==========================================================
elif st.session_state.vista_activa == "consolidado":

    _btn_volver()
    st.title("Actualizar consolidado")

    bloqueado = mostrar_aviso_bloqueo()

    if st.session_state.df.empty:
        st.info("No hay consolidado disponible. Primero carga un reporte.")
        st.stop()

    col_info, col_btn = st.columns([7, 3])
    with col_info:
        st.caption("💡 Edita los campos manuales y presiona Guardar cuando termines.")
    with col_btn:
        guardar = st.button(
            "💾 Guardar cambios",
            disabled=bloqueado,
            use_container_width=True,
            key="btn_guardar"
        )

    st.divider()

    df_filtrado = aplicar_filtros(st.session_state.df)
    df_editado  = mostrar_tabla(df_filtrado)
    st.session_state.df.update(df_editado)

    st.divider()
    col_info2, col_btn2 = st.columns([7, 3])
    with col_info2:
        st.caption("Los cambios no se guardan automáticamente.")
    with col_btn2:
        guardar_abajo = st.button(
            "💾 Guardar cambios",
            disabled=bloqueado,
            use_container_width=True,
            key="btn_guardar_abajo"
        )

    if guardar or guardar_abajo:
        if not sistema_libre():
            st.error("⛔ El sistema está ocupado. Intenta en unos momentos.")
        else:
            try:
                escribir_estado(ESTADO_GUARDANDO, usuario)
                guardar_consolidado(
                    st.session_state.df,
                    st.session_state.df_anterior,
                    usuario
                )
                st.session_state.df_anterior = st.session_state.df.copy()
            except Exception as e:
                st.error(f"❌ Error al guardar: {e}")
            finally:
                liberar_estado()

# ==========================================================
# VISTA 3 — GENERAR RESOLUCIÓN
# ==========================================================
elif st.session_state.vista_activa == "resoluciones":

    _btn_volver()
    st.title("Generar Resolución")
    st.caption("⚠️ Usar solo si el sistema principal falla.")
    mostrar_resoluciones()

# ==========================================================
# VISTA 4 — CARTA DE CUMPLIMIENTO
# ==========================================================
elif st.session_state.vista_activa == "cartas":

    _btn_volver()
    st.title("Carta de Cumplimiento")
    mostrar_carta_cumplimiento()