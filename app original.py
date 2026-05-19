import streamlit as st
import pandas as pd
import numpy as np
from datetime import timedelta
import os

# ---------- CONFIGURACION INICIAL ----------
st.set_page_config(page_title="Gestión de Reclamos", layout="wide")

# ---------- CARGA DE FERIADOS ----------
TABLA_FERIADOS = pd.read_excel("DATA/TABLA FERIADOS.xlsx", sheet_name="DATOS")
FERIADOS = pd.to_datetime(TABLA_FERIADOS["FERIADOS"], errors="coerce").dropna().dt.normalize()

# ---------- FUNCIONES UTILES ----------
def is_business_day(d, holidays):
    if pd.isna(d):
        return False
    d = pd.to_datetime(d).normalize()
    return d.weekday() < 5 and d not in holidays.values

def add_business_days(start_date, days, holidays):
    if pd.isna(start_date):
        return pd.NaT
    cur = pd.to_datetime(start_date).normalize()
    added = 0
    step = 1
    while added < days:
        cur = cur + pd.Timedelta(days=step)
        if is_business_day(cur, holidays):
            added += 1
    return cur

# ---------- INTERFAZ ----------
st.title("Gestión de Reclamos ATC")
col1, col2, col3, col4 = st.columns(4)

archivo_bruto = col1.file_uploader("Seleccionar archivo", type=["xlsx"])
cargar_reporte = col2.button("Cargar Reporte Tickets")
guardar_cambios = col3.button("Guardar Cambios")

# ---------- SESSION STATE ----------
if "df_procesado" not in st.session_state:
    st.session_state.df_procesado = pd.DataFrame()

if "df_filtrado" not in st.session_state:
    st.session_state.df_filtrado = pd.DataFrame()

if "filtros" not in st.session_state:
    st.session_state.filtros = {
        "ticket": "",
        "fecha_averia": None,
        "solicitud": [],
        "estado": []
    }

# ---------- PROCESAMIENTO DEL EXCEL BRUTO ----------
if archivo_bruto and cargar_reporte:

    df_bruto = pd.read_excel(archivo_bruto)

    columnas_requeridas_min = [
        "TICKET", "FECHA", "FECHA Y HORA DE LA AVERIA", "USUARIO", "GÉNERO",
        "FECHA CIERRE TICKET", "FECHA LIMITE RESOLUCION", "FECHA Y HORA DE SOLICITUD"
    ]
    for c in columnas_requeridas_min:
        if c not in df_bruto.columns:
            df_bruto[c] = ""

    # Parseo de fechas
    df_bruto["FECHA"] = pd.to_datetime(df_bruto["FECHA"], dayfirst=True, errors="coerce")
    df_bruto["FECHA Y HORA DE LA AVERIA"] = pd.to_datetime(df_bruto.get("FECHA Y HORA DE LA AVERIA"), dayfirst=True, errors="coerce")
    df_bruto["FECHA Y HORA DE SOLICITUD"] = pd.to_datetime(df_bruto.get("FECHA Y HORA DE SOLICITUD"), dayfirst=True, errors="coerce")
    df_bruto["FECHA CIERRE TICKET"] = pd.to_datetime(df_bruto.get("FECHA CIERRE TICKET"), dayfirst=True, errors="coerce")
    df_bruto["FECHA LIMITE RESOLUCION"] = pd.to_datetime(df_bruto.get("FECHA LIMITE RESOLUCION"), dayfirst=True, errors="coerce")

    # ---------- TODAS LAS COLUMNAS DEL CONSOLIDADO ----------
    columnas_requeridas = [
        "TICKET","FECHA Y HORA DE LA AVERIA","FECHA","HORA","FECHA Y HORA DE SOLICITUD",
        "FECHA Y HORA DE INICIO APROXIMADA DEL PROBLEMA","CÓDIGO IIB","CONTRATO","CLIENTE",
        "USUARIO","N° DOCUMENTO DNI / CE","CORREO","TELEFONO","GÉNERO","SERVICIO","PROYECTO",
        "LOCALIDAD","DISTRITO","PROVINCIA","DEPARTAMENTO","CANAL","SOLICITUD","PROBLEMA","ÁREA",
        "FECHA Y HORA DE RESTABLECIMIENTO DEL SERVICIO","FECHADE RESTABLECIMIENTO DEL SERVICIO",
        "HORA DE RESTABLECIMIENTO DEL SERVICIO","FECHA CIERRE TICKET","HORA CIERRE TICKET",
        "PERIODO QUE INICIA LA AVERIA","TIPO ENTIDAD","ORIGEN","ESTADO","NOMBRE DE LA IIBB","GLOSA",
        "SEÑOR(A)","IDENTIFICADO","USUARIO(A)","FECHA QUE INICIA RECLAMO DE CALIDAD",
        "CIERE TICKET RECLAMO AVERIA","PASO A CALIDAD","RESOLUCION","FECHA LIMITE RESOLUCION",
        "FECHA LIMITE DE CUMPLIMIENTO","FECHA LIMITE ELABORACION CARTA DE CUMPLIMIENTO",
        "FECHA PROGRAMADA MANTENIMIENTO RESOLUCIÓN","FECHA PROGRAMADA MANTENIMIENTO RES",
        "N° OT","FECHA DE OT","SUPERVISOR MANTENIMIENTO","COLABORADOR ENCARGADO",
        "DECLARACION DE RECLAMO","QUIEN INDICO LA FECHA DE ATENCION EN LA RESOLUCION",
        "CALIDAD CERRADO?","FECHA DE RESOLUCION","FECHA DE NOTIFICACION DE LA RESOLUCION",
        "MEDIO DE NOTIFICACION DEL RECLAMO","MOTIVO POR EL CUAL NO CUMPLIO CON EL PLAZO",
        "DESCRIPCION DE LA AVERIA","FECHA DE CUMPLIMIENTO","APLICA CARTA DE CUMPLIMIENTO",
        "N° CARTA DE CUMPLIMIENTO","FECHA DE ELABORACION CARTA DE CUMPLIMIENTO",
        "FECHA REMISION CARTA DE CUMPLIMIENTO","MEDIO DE NOTIFICACION LA CARTA DE CUMPLIMIENTO"
    ]
    for c in columnas_requeridas:
        if c not in df_bruto.columns:
            df_bruto[c] = ""

    # ---------- CALCULOS (VALIDADOS, NO SE TOCAN) ----------
    def calc_senor(g):
        if pd.isna(g) or str(g).strip() == "":
            return ""
        return "EL SEÑOR" if str(g).strip().lower() == "hombre" else "LA SEÑORA"
    df_bruto["SEÑOR(A)"] = df_bruto["GÉNERO"].apply(calc_senor)

    def calc_identificado(g):
        if pd.isna(g) or str(g).strip() == "":
            return ""
        return "Identificado" if str(g).strip().lower() == "hombre" else "Identificada"
    df_bruto["IDENTIFICADO"] = df_bruto["GÉNERO"].apply(calc_identificado)

    def calc_usuario_a(g):
        if pd.isna(g) or str(g).strip() == "":
            return ""
        return "EL USUARIO" if str(g).strip().lower() == "hombre" else "LA USUARIA"
    df_bruto["USUARIO(A)"] = df_bruto["GÉNERO"].apply(calc_usuario_a)

    df_bruto["FECHA QUE INICIA RECLAMO DE CALIDAD"] = df_bruto["FECHA"].apply(
        lambda d: (pd.to_datetime(d) + pd.Timedelta(days=3)) if pd.notna(d) else pd.NaT
    )

    df_bruto["CIERE TICKET RECLAMO AVERIA"] = df_bruto["FECHA CIERRE TICKET"].apply(
        lambda x: "PENDIENTE" if (pd.isna(x) or str(x).strip() == "") else "CERRADO"
    )

    df_bruto["FECHA LIMITE RESOLUCION"] = df_bruto["FECHA QUE INICIA RECLAMO DE CALIDAD"].apply(
        lambda d: add_business_days(d, 3, FERIADOS) if pd.notna(d) else pd.NaT
    )
    df_bruto["FECHA LIMITE DE CUMPLIMIENTO"] = df_bruto["FECHA LIMITE RESOLUCION"].apply(
        lambda d: add_business_days(d, 10, FERIADOS) if pd.notna(d) else pd.NaT
    )
    df_bruto["FECHA LIMITE ELABORACION CARTA DE CUMPLIMIENTO"] = df_bruto["FECHA LIMITE RESOLUCION"].apply(
        lambda d: add_business_days(d, 13, FERIADOS) if pd.notna(d) else pd.NaT
    )

    def calc_resol(row):
        f_lim = row.get("FECHA LIMITE RESOLUCION")
        ticket = row.get("TICKET")
        if pd.isna(f_lim) or pd.isna(ticket) or str(ticket).strip() == "":
            return ""
        y = pd.to_datetime(f_lim).year
        y2 = str(y)[-2:]
        return f"RESOLUCION N° {y}-{ticket}- Gilat Expediente {y2}-AT{ticket}"
    df_bruto["RESOLUCION"] = df_bruto.apply(calc_resol, axis=1)

    def calcular_paso(row):
        f_reclamo = row.get("FECHA QUE INICIA RECLAMO DE CALIDAD")
        f_cierre_raw = row.get("FECHA CIERRE TICKET")
        f_cierre = pd.to_datetime(f_cierre_raw, errors="coerce")

        if pd.isna(f_reclamo):
            return "EN REVISIÓN" if (pd.isna(f_cierre) or str(f_cierre_raw).strip() == "") else "NO APLICA"

        hoy = pd.to_datetime("today").normalize()
        delta_days = (pd.to_datetime(f_reclamo).normalize() - hoy).days

        if delta_days <= 0:
            if (pd.isna(f_cierre) or str(f_cierre_raw).strip() == ""):
                return "CALIDAD"
            try:
                f_cierre_dt = pd.to_datetime(f_cierre)
                return "CALIDAD" if f_cierre_dt >= pd.to_datetime(f_reclamo) else "NO APLICA"
            except:
                return ""
        else:
            return "EN REVISIÓN" if (pd.isna(f_cierre) or str(f_cierre_raw).strip() == "") else "NO APLICA"

    df_bruto["PASO A CALIDAD"] = df_bruto.apply(calcular_paso, axis=1)

    # Guardar procesado
    st.session_state.df_procesado = df_bruto.copy()
    st.session_state.df_filtrado = df_bruto.copy()

# ==========================================================
#                           FILTROS
# ==========================================================

if not st.session_state.df_procesado.empty:

    st.subheader("Filtros")

    fcol1, fcol2, fcol3, fcol4, fcol5, fcol6 = st.columns([1.2, 1.2, 1.6, 1.2, 1.4, 1])

    # 1. TICKET (textbox)
    ticket_filtro = fcol1.text_input("TICKET", st.session_state.filtros.get("ticket",""))

    # 2. FECHA DE AVERIA
    fecha_averia_filtro = fcol2.date_input(
        "Fecha de Avería",
        st.session_state.filtros.get("fecha_averia")
    )

    # 3. SOLICITUD
    solicitud_lista = sorted(st.session_state.df_procesado["SOLICITUD"].dropna().unique())
    solicitud_filtro = fcol3.multiselect(
        "Tipo de Solicitud",
        options=solicitud_lista,
        default=st.session_state.filtros.get("solicitud", [])
    )

    # 4. ESTADO
    estado_lista = sorted(st.session_state.df_procesado["ESTADO"].dropna().unique())
    estado_filtro = fcol4.multiselect(
        "Estado de Ticket",
        options=estado_lista,
        default=st.session_state.filtros.get("estado", [])
    )

    # 5. PASO A CALIDAD
    paso_lista = sorted(st.session_state.df_procesado["PASO A CALIDAD"].dropna().unique())
    paso_filtro = fcol5.multiselect(
        "Ticket Calidad",
        options=paso_lista,
        default=st.session_state.filtros.get("paso_calidad", [])
    )

    aplicar = fcol6.button("Aplicar Filtros")
    borrar = fcol6.button("Borrar Filtros")

    if aplicar:
        df = st.session_state.df_procesado.copy()

        # Guardar estado
        st.session_state.filtros["ticket"] = ticket_filtro
        st.session_state.filtros["fecha_averia"] = fecha_averia_filtro
        st.session_state.filtros["solicitud"] = solicitud_filtro
        st.session_state.filtros["estado"] = estado_filtro
        st.session_state.filtros["paso_calidad"] = paso_filtro

        # Aplicar filtros
        if ticket_filtro:
            df = df[df["TICKET"].astype(str).str.contains(str(ticket_filtro).strip(), na=False)]

        if fecha_averia_filtro:
            df = df[df["FECHA Y HORA DE LA AVERIA"].dt.date == fecha_averia_filtro]

        if solicitud_filtro:
            df = df[df["SOLICITUD"].isin(solicitud_filtro)]

        if estado_filtro:
            df = df[df["ESTADO"].isin(estado_filtro)]
       
        if paso_filtro:
            df = df[df["PASO A CALIDAD"].isin(paso_filtro)]

        st.session_state.df_filtrado = df

    if borrar:
        st.session_state.filtros = {
            "ticket": "",
            "fecha_averia": None,
            "solicitud": [],
            "estado": [],
            "paso_calidad": []
        }
        st.session_state.df_filtrado = st.session_state.df_procesado.copy()
        st.rerun()

# ==========================================================
#                       MOSTRAR TABLA EDITABLE
# ==========================================================

if not st.session_state.df_procesado.empty:

    df_show = st.session_state.df_filtrado.copy()

    ocultas = ["GLOSA"]

    # Lista explícita de columnas manuales (solo estas deben ser editables)
    manual_columns = [
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

    # Columnas visibles (mantuve la lista validada por ti)
    columnas_visibles = [
        "TICKET",
        "FECHA Y HORA DE LA AVERIA",
        "SOLICITUD",
        "FECHA CIERRE TICKET",
        "ESTADO",
        "FECHA QUE INICIA RECLAMO DE CALIDAD",
        "PASO A CALIDAD",
        "FECHA LIMITE RESOLUCION",
        "FECHA LIMITE DE CUMPLIMIENTO",
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

    # Asegurar que las columnas solicitadas existan en el dataframe (evita KeyError)
    columnas_visibles = [c for c in columnas_visibles if c in df_show.columns]

    # Determinar columnas realmente editables (intersección con las visibles)
    editable_cols = [c for c in manual_columns if c in columnas_visibles]

    # Columnas a deshabilitar = todas las visibles menos las editables
    disabled_columns = [c for c in columnas_visibles if c not in editable_cols]

    # Mostrar editor y capturar resultado (st.data_editor devuelve el dataframe editado)
    df_editado = st.data_editor(
        df_show[columnas_visibles],
        disabled=disabled_columns,
        use_container_width=True
    )

    # Si el usuario hizo cambios, actualizar el df_procesado y df_filtrado en session_state
    # (coinciden los índices si no se reindexó)
    if df_editado is not None:
        try:
            # Actualizar filas/columnas modificadas en df_procesado
            st.session_state.df_procesado.loc[df_editado.index, df_editado.columns] = df_editado
            # Mantener df_filtrado sincronizado (por si se sigue trabajando sobre la vista filtrada)
            st.session_state.df_filtrado.loc[df_editado.index, df_editado.columns] = df_editado
        except Exception:
            # En caso de índice no coincidente, hacemos un merge por posición (fallback)
            # Reemplazamos por posición: (sobrescribe las filas visibles)
            for i, idx in enumerate(df_show.index):
                st.session_state.df_procesado.loc[idx, df_editado.columns] = df_editado.iloc[i].values
                st.session_state.df_filtrado.loc[idx, df_editado.columns] = df_editado.iloc[i].values

# ==========================================================
#                       GUARDAR CAMBIOS (VALIDADO)
# ==========================================================

if guardar_cambios:

    if st.session_state.df_procesado.empty:
        st.warning("No hay datos procesados para guardar. Cargue un archivo primero.")
    else:
        carpeta = "DATA/CONSOLIDADO"   # YA EXISTE, NO SE CREA

        # Fecha del día
        fecha_hoy = pd.to_datetime("today").strftime("%Y-%m-%d")

        # Buscar correlativo existente
        archivos = [
            f for f in os.listdir(carpeta)
            if f.startswith(f"CONSOLIDADO_{fecha_hoy}")
        ]

        if len(archivos) == 0:
            correlativo = 1
        else:
            nums = []
            for a in archivos:
                try:
                    num = int(a.split("-")[-1].replace(".xlsx", ""))
                    nums.append(num)
                except:
                    pass
            correlativo = max(nums) + 1 if nums else 1

        correlativo_str = str(correlativo).zfill(3)

        nombre_archivo = f"CONSOLIDADO_{fecha_hoy}-{correlativo_str}.xlsx"
        ruta_guardado = os.path.join(carpeta, nombre_archivo)

        st.session_state.df_procesado.to_excel(ruta_guardado, index=False)

        st.success(f"Datos guardados correctamente en: {ruta_guardado}")