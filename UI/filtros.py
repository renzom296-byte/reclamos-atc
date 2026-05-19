import streamlit as st
import pandas as pd

def aplicar_filtros(df: pd.DataFrame) -> pd.DataFrame:

    with st.expander("🔍 Filtros de búsqueda", expanded=True):

        c1, c2, c3, c4, c5 = st.columns(5)

        ticket = c1.text_input("TICKET", key="f_ticket_gestion")

        solicitud = c2.multiselect(
            "SOLICITUD",
            options=sorted(df["SOLICITUD"].dropna().unique()),
            key="f_solicitud_gestion"
        )

        estado = c3.multiselect(
            "ESTADO",
            options=sorted(df["ESTADO"].dropna().unique()),
            key="f_estado_gestion"
        )

        paso = c4.multiselect(
            "PASO CALIDAD",
            options=sorted(df["PASO A CALIDAD"].dropna().unique()),
            key="f_paso_gestion"
        )

        fecha_averia = c5.date_input(
            "FECHA DE AVERÍA",
            value=None,
            key="f_fecha_gestion"
        )

    # =========================
    # Aplicación de filtros
    # =========================
    df_filtrado = df.copy()

    if ticket:
        df_filtrado = df_filtrado[
            df_filtrado["TICKET"].astype(str).str.contains(ticket, na=False)
        ]

    if solicitud:
        df_filtrado = df_filtrado[df_filtrado["SOLICITUD"].isin(solicitud)]

    if estado:
        df_filtrado = df_filtrado[df_filtrado["ESTADO"].isin(estado)]

    if paso:
        df_filtrado = df_filtrado[df_filtrado["PASO A CALIDAD"].isin(paso)]

    if fecha_averia:
        df_filtrado = df_filtrado[
            df_filtrado["FECHA Y HORA DE LA AVERIA"].dt.date == fecha_averia
        ]

    return df_filtrado
