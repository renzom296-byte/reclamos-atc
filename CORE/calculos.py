import pandas as pd
import unicodedata

# ==========================================================
# FUNCIONES DE DÍAS HÁBILES
# ==========================================================
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
    while added < days:
        cur = cur + pd.Timedelta(days=1)
        if is_business_day(cur, holidays):
            added += 1
    return cur


# ==========================================================
# BUSCAR COLUMNA CON TOLERANCIA DE ENCODING
# ==========================================================
def _find_col(df: pd.DataFrame, nombre: str) -> str:
    """
    Devuelve el nombre real de la columna en el df
    aunque tenga diferencias de encoding.
    Retorna None si no la encuentra.
    """
    if nombre in df.columns:
        return nombre

    nombre_nfc = unicodedata.normalize("NFC", nombre)
    nombre_nfd = unicodedata.normalize("NFD", nombre)

    for col in df.columns:
        col_nfc = unicodedata.normalize("NFC", col)
        col_nfd = unicodedata.normalize("NFD", col)
        if col_nfc == nombre_nfc or col_nfd == nombre_nfd:
            return col

    return None


# ==========================================================
# GENERAR CLAVE ÚNICA POR FILA
# ==========================================================
def generar_clave_unica(df: pd.DataFrame) -> pd.DataFrame:

    col_ticket = _find_col(df, "TICKET") or "TICKET"
    col_fecha  = _find_col(df, "FECHA Y HORA DE LA AVERIA") or "FECHA Y HORA DE LA AVERIA"

    def _clave(row):
        ticket = str(row.get(col_ticket, "")).strip()

        fecha_averia = row.get(col_fecha)
        if pd.notna(fecha_averia):
            fecha_str = pd.to_datetime(fecha_averia).strftime("%Y-%m-%d_%H%M")
        else:
            fecha_str = "SINF"

        return f"{ticket}_{fecha_str}"

    df["CLAVE_UNICA"] = df.apply(_clave, axis=1)
    return df


# ==========================================================
# CALCULOS PRINCIPALES DEL CONSOLIDADO
# ==========================================================
def aplicar_calculos(df: pd.DataFrame, feriados) -> pd.DataFrame:
    df = df.copy()

    # Generar clave única primero
    df = generar_clave_unica(df)

    # Encontrar columna GÉNERO con tolerancia de encoding
    col_genero = _find_col(df, "GÉNERO")

    # ------------------------------------------------------
    # SEÑOR(A)
    # ------------------------------------------------------
    def calc_senor(g):
        if pd.isna(g) or str(g).strip() == "":
            return ""
        return "EL SEÑOR" if str(g).strip().lower() == "hombre" else "LA SEÑORA"

    if col_genero:
        df["SEÑOR(A)"] = df[col_genero].apply(calc_senor)
    else:
        df["SEÑOR(A)"] = ""

    # ------------------------------------------------------
    # IDENTIFICADO
    # ------------------------------------------------------
    def calc_identificado(g):
        if pd.isna(g) or str(g).strip() == "":
            return ""
        return "Identificado" if str(g).strip().lower() == "hombre" else "Identificada"

    if col_genero:
        df["IDENTIFICADO"] = df[col_genero].apply(calc_identificado)
    else:
        df["IDENTIFICADO"] = ""

    # ------------------------------------------------------
    # USUARIO(A)
    # ------------------------------------------------------
    def calc_usuario_a(g):
        if pd.isna(g) or str(g).strip() == "":
            return ""
        return "EL USUARIO" if str(g).strip().lower() == "hombre" else "LA USUARIA"

    if col_genero:
        df["USUARIO(A)"] = df[col_genero].apply(calc_usuario_a)
    else:
        df["USUARIO(A)"] = ""

    # ------------------------------------------------------
    # FECHA QUE INICIA RECLAMO DE CALIDAD
    # ------------------------------------------------------
    col_fecha = _find_col(df, "FECHA") or "FECHA"
    df["FECHA QUE INICIA RECLAMO DE CALIDAD"] = df[col_fecha].apply(
        lambda d: (pd.to_datetime(d) + pd.Timedelta(days=3)) if pd.notna(d) else pd.NaT
    )

    # ------------------------------------------------------
    # CIERRE TICKET RECLAMO AVERIA
    # ------------------------------------------------------
    col_cierre = _find_col(df, "FECHA CIERRE TICKET") or "FECHA CIERRE TICKET"
    df["CIERE TICKET RECLAMO AVERIA"] = df[col_cierre].apply(
        lambda x: "PENDIENTE" if (pd.isna(x) or str(x).strip() == "") else "CERRADO"
    )

    # ------------------------------------------------------
    # FECHAS LÍMITE
    # ------------------------------------------------------
    df["FECHA LIMITE RESOLUCION"] = df["FECHA QUE INICIA RECLAMO DE CALIDAD"].apply(
        lambda d: add_business_days(d, 3, feriados) if pd.notna(d) else pd.NaT
    )

    df["FECHA LIMITE DE CUMPLIMIENTO"] = df["FECHA LIMITE RESOLUCION"].apply(
        lambda d: add_business_days(d, 10, feriados) if pd.notna(d) else pd.NaT
    )

    df["FECHA LIMITE ELABORACION CARTA DE CUMPLIMIENTO"] = df["FECHA LIMITE RESOLUCION"].apply(
        lambda d: add_business_days(d, 13, feriados) if pd.notna(d) else pd.NaT
    )

    # ------------------------------------------------------
    # RESOLUCIÓN
    # ------------------------------------------------------
    def calc_resol(row):
        f_lim = row.get("FECHA LIMITE RESOLUCION")
        ticket = row.get("TICKET")

        if pd.isna(f_lim) or pd.isna(ticket) or str(ticket).strip() == "":
            return ""

        y = pd.to_datetime(f_lim).year
        y2 = str(y)[-2:]
        return f"RESOLUCION N° {y}-{ticket}- Gilat Expediente {y2}-AT{ticket}"

    df["RESOLUCION"] = df.apply(calc_resol, axis=1)

    # ------------------------------------------------------
    # PASO A CALIDAD
    # Usar nombres reales de columnas encontrados por _find_col
    # ------------------------------------------------------
    nombre_cierre   = _find_col(df, "FECHA CIERRE TICKET") or "FECHA CIERRE TICKET"
    nombre_reclamo  = "FECHA QUE INICIA RECLAMO DE CALIDAD"

    def calcular_paso(row):
        f_reclamo    = row.get(nombre_reclamo)
        f_cierre_raw = row.get(nombre_cierre)
        f_cierre     = pd.to_datetime(f_cierre_raw, errors="coerce")

        if pd.isna(f_reclamo):
            return (
                "EN REVISIÓN"
                if (pd.isna(f_cierre) or str(f_cierre_raw).strip() == "")
                else "NO APLICA"
            )

        hoy = pd.to_datetime("today").normalize()
        delta_days = (pd.to_datetime(f_reclamo).normalize() - hoy).days

        if delta_days <= 0:
            if pd.isna(f_cierre) or str(f_cierre_raw).strip() == "":
                return "CALIDAD"
            try:
                return (
                    "CALIDAD"
                    if pd.to_datetime(f_cierre) >= pd.to_datetime(f_reclamo)
                    else "NO APLICA"
                )
            except Exception:
                return ""
        else:
            return (
                "EN REVISIÓN"
                if (pd.isna(f_cierre) or str(f_cierre_raw).strip() == "")
                else "NO APLICA"
            )

    df["PASO A CALIDAD"] = df.apply(calcular_paso, axis=1)

    return df