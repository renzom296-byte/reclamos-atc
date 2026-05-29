import streamlit as st
import pandas as pd

COLUMNAS_FIJAS = [
    "TICKET",
    "FECHA Y HORA DE LA AVERIA",
    "SOLICITUD",
    "ESTADO",
    "PASO A CALIDAD"
]

COLUMNAS_MANUALES = [
    "FECHA PROGRAMADA MANTENIMIENTO RESOLUCIÓN",
    "FECHA PROGRAMADA MANTENIMIENTO RES",
    "N° OT",
    "FECHA DE OT",
    "SUPERVISOR MANTENIMIENTO",
    "COLABORADOR ENCARGADO",
    "DECLARACION DE RECLAMO",
    "QUIEN INDICO LA FECHA DE ATENCION EN LA RESOLUCION",
    "CALIDAD CERRADO?",
    "FECHA DE RESOLUCION",
    "FECHA DE NOTIFICACION DE LA RESOLUCION",
    "MEDIO DE NOTIFICACION DEL RECLAMO",
    "MOTIVO POR EL CUAL NO CUMPLIO CON EL PLAZO",
    "DESCRIPCION DE LA AVERIA",
    "FECHA DE CUMPLIMIENTO",
    "APLICA CARTA DE CUMPLIMIENTO",
    "N° CARTA DE CUMPLIMIENTO",
    "FECHA DE ELABORACION CARTA DE CUMPLIMIENTO",
    "FECHA REMISION CARTA DE CUMPLIMIENTO",
    "MEDIO DE NOTIFICACION LA CARTA DE CUMPLIMIENTO"
]

COLUMNAS_FECHA = [
    "FECHA Y HORA DE LA AVERIA",
    "FECHA",
    "FECHA CIERRE TICKET",
    "FECHA QUE INICIA RECLAMO DE CALIDAD",
    "FECHA LIMITE RESOLUCION",
    "FECHA LIMITE DE CUMPLIMIENTO",
    "FECHA LIMITE ELABORACION CARTA DE CUMPLIMIENTO",
    "FECHA PROGRAMADA MANTENIMIENTO RESOLUCIÓN",
    "FECHA PROGRAMADA MANTENIMIENTO RES",
    "FECHA DE OT",
    "FECHA DE RESOLUCION",
    "FECHA DE NOTIFICACION DE LA RESOLUCION",
    "FECHA DE CUMPLIMIENTO",
    "FECHA DE ELABORACION CARTA DE CUMPLIMIENTO",
    "FECHA REMISION CARTA DE CUMPLIMIENTO"
]

COLUMNAS_MANUALES_TEXTO = [
    col for col in COLUMNAS_MANUALES
    if col not in COLUMNAS_FECHA
]


def mostrar_tabla(df: pd.DataFrame) -> pd.DataFrame:

    if df.empty:
        return df

    for col in COLUMNAS_MANUALES:
        if col not in df.columns:
            df[col] = pd.NaT if col in COLUMNAS_FECHA else ""

    # Forzar fechas a datetime
    for col in COLUMNAS_FECHA:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Forzar columnas manuales de texto a str
    # Evita error cuando vienen como float del Excel (ej: N° OT = 12345.0)
    for col in COLUMNAS_MANUALES_TEXTO:
        if col in df.columns:
            df[col] = df[col].apply(
                lambda x: "" if pd.isna(x)
                else str(int(x)) if isinstance(x, float) and x == int(x)
                else str(x).strip()
            )

    columnas_opcionales = [col for col in df.columns if col not in COLUMNAS_FIJAS]

    with st.expander("⚙️ Seleccionar columnas a mostrar", expanded=False):
        st.caption("Columnas fijas: TICKET, FECHA Y HORA DE LA AVERIA, SOLICITUD, ESTADO, PASO A CALIDAD")
        st.caption("Las columnas manuales seleccionadas siempre serán editables.")
        cols_seleccionadas = st.multiselect(
            "Columnas opcionales:",
            options=columnas_opcionales,
            default=[col for col in COLUMNAS_MANUALES if col in columnas_opcionales],
            key="selector_columnas"
        )

    columnas_mostrar = (
        [col for col in COLUMNAS_FIJAS if col in df.columns] +
        [col for col in cols_seleccionadas if col in df.columns]
    )

    df_vista = df[columnas_mostrar].copy()

    column_config = {}

    for col in df_vista.columns:
        if col in COLUMNAS_FECHA:
            column_config[col] = st.column_config.DateColumn(
                col,
                format="DD/MM/YYYY",
                disabled=col not in COLUMNAS_MANUALES
            )
        elif col in COLUMNAS_MANUALES:
            column_config[col] = st.column_config.TextColumn(col, disabled=False)
        else:
            column_config[col] = st.column_config.TextColumn(col, disabled=True)

    st.caption("💡 Recuerda presionar **Guardar Cambios** para conservar las ediciones. · {len(df_vista)} ticket(s) mostrados"")
    st.caption(f"{len(df_vista)} ticket(s) mostrados")

    df_editado = st.data_editor(
        df_vista,
        use_container_width=True,
        hide_index=True,
        column_config=column_config,
        key="tabla_gestion"
    )

    df_completo = df.copy()
    df_completo.update(df_editado)

    return df_completo