import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import math
import time
import pandas as pd
from datetime import datetime
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

# ==========================================================
# CLIENTE SUPABASE
# ==========================================================
_client = None

def get_client():
    global _client
    if _client is None:
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _client


# ==========================================================
# MAPA DE COLUMNAS Excel → Supabase
# ==========================================================
EXCEL_A_BD = {
    "CLAVE_UNICA":                                      "clave_unica",
    "TICKET":                                           "ticket",
    "FECHA Y HORA DE LA AVERIA":                        "fecha_averia",
    "FECHA":                                            "fecha",
    "HORA":                                             "hora",
    "FECHA Y HORA DE SOLICITUD":                        "fecha_hora_solicitud",
    "FECHA Y HORA DE INICIO APROXIMADA DEL PROBLEMA":   "fecha_hora_inicio_problema",
    "CÓDIGO IIB":                                       "codigo_iib",
    "CONTRATO":                                         "contrato",
    "CLIENTE":                                          "cliente",
    "USUARIO":                                          "usuario",
    "N° DOCUMENTO DNI / CE":                            "n_documento_dni_ce",
    "CORREO":                                           "correo",
    "TELEFONO":                                         "telefono",
    "GÉNERO":                                           "genero",
    "SERVICIO":                                         "servicio",
    "PROYECTO":                                         "proyecto",
    "LOCALIDAD":                                        "localidad",
    "DISTRITO":                                         "distrito",
    "PROVINCIA":                                        "provincia",
    "DEPARTAMENTO":                                     "departamento",
    "CANAL":                                            "canal",
    "SOLICITUD":                                        "solicitud",
    "PROBLEMA":                                         "problema",
    "ÁREA":                                             "area",
    "FECHA Y HORA DE RESTABLECIMIENTO DEL SERVICIO":    "fecha_hora_restablecimiento",
    "FECHADE RESTABLECIMIENTO DEL SERVICIO":            "fecha_restablecimiento",
    "HORA DE RESTABLECIMIENTO DEL SERVICIO":            "hora_restablecimiento",
    "FECHA CIERRE TICKET":                              "fecha_cierre_ticket",
    "HORA CIERRE TICKET":                               "hora_cierre_ticket",
    "PERIODO QUE INICIA LA AVERIA":                     "periodo_inicia_averia",
    "TIPO ENTIDAD":                                     "tipo_entidad",
    "ORIGEN":                                           "origen",
    "ESTADO":                                           "estado",
    "NOMBRE DE LA IIBB":                                "nombre_iibb",
    "SEÑOR(A)":                                         "senor_a",
    "IDENTIFICADO":                                     "identificado",
    "USUARIO(A)":                                       "usuario_a",
    "FECHA QUE INICIA RECLAMO DE CALIDAD":              "fecha_inicia_reclamo_calidad",
    "CIERE TICKET RECLAMO AVERIA":                      "cierre_ticket_reclamo_averia",
    "FECHA LIMITE RESOLUCION":                          "fecha_limite_resolucion",
    "FECHA LIMITE DE CUMPLIMIENTO":                     "fecha_limite_cumplimiento",
    "FECHA LIMITE ELABORACION CARTA DE CUMPLIMIENTO":   "fecha_limite_elaboracion_carta",
    "RESOLUCION":                                       "resolucion",
    "PASO A CALIDAD":                                   "paso_a_calidad",
    "FECHA PROGRAMADA MANTENIMIENTO RESOLUCIÓN":        "fecha_programada_mantenimiento_res1",
    "FECHA PROGRAMADA MANTENIMIENTO RES":               "fecha_programada_mantenimiento_res2",
    "N° OT":                                            "n_ot",
    "FECHA DE OT":                                      "fecha_ot",
    "SUPERVISOR MANTENIMIENTO":                         "supervisor_mantenimiento",
    "COLABORADOR ENCARGADO":                            "colaborador_encargado",
    "DECLARACION DE RECLAMO":                           "declaracion_reclamo",
    "QUIEN INDICO LA FECHA DE ATENCION EN LA RESOLUCION": "quien_indico_fecha_atencion",
    "CALIDAD CERRADO?":                                 "calidad_cerrado",
    "FECHA DE RESOLUCION":                              "fecha_resolucion",
    "FECHA DE NOTIFICACION DE LA RESOLUCION":           "fecha_notificacion_resolucion",
    "MEDIO DE NOTIFICACION DEL RECLAMO":                "medio_notificacion_reclamo",
    "MOTIVO POR EL CUAL NO CUMPLIO CON EL PLAZO":       "motivo_no_cumplio_plazo",
    "DESCRIPCION DE LA AVERIA":                         "descripcion_averia",
    "FECHA DE CUMPLIMIENTO":                            "fecha_cumplimiento",
    "APLICA CARTA DE CUMPLIMIENTO":                     "aplica_carta_cumplimiento",
    "N° CARTA DE CUMPLIMIENTO":                         "n_carta_cumplimiento",
    "FECHA DE ELABORACION CARTA DE CUMPLIMIENTO":       "fecha_elaboracion_carta",
    "FECHA REMISION CARTA DE CUMPLIMIENTO":             "fecha_remision_carta",
    "MEDIO DE NOTIFICACION LA CARTA DE CUMPLIMIENTO":   "medio_notificacion_carta",
}

BD_A_EXCEL = {v: k for k, v in EXCEL_A_BD.items()}

COLUMNAS_FECHA_BD = {
    "fecha_averia", "fecha", "fecha_hora_solicitud",
    "fecha_hora_inicio_problema", "fecha_hora_restablecimiento",
    "fecha_restablecimiento", "fecha_cierre_ticket",
    "fecha_inicia_reclamo_calidad", "fecha_limite_resolucion",
    "fecha_limite_cumplimiento", "fecha_limite_elaboracion_carta",
    "fecha_programada_mantenimiento_res1", "fecha_programada_mantenimiento_res2",
    "fecha_ot", "fecha_resolucion", "fecha_notificacion_resolucion",
    "fecha_cumplimiento", "fecha_elaboracion_carta", "fecha_remision_carta",
}

COLUMNAS_CALCULADAS = [
    "estado", "solicitud", "fecha_cierre_ticket", "fecha_averia",
    "senor_a", "identificado", "usuario_a",
    "fecha_inicia_reclamo_calidad", "cierre_ticket_reclamo_averia",
    "fecha_limite_resolucion", "fecha_limite_cumplimiento",
    "fecha_limite_elaboracion_carta", "resolucion", "paso_a_calidad",
]

COLUMNAS_MANUALES = [
    "fecha_programada_mantenimiento_res1", "fecha_programada_mantenimiento_res2",
    "n_ot", "fecha_ot", "supervisor_mantenimiento", "colaborador_encargado",
    "declaracion_reclamo", "quien_indico_fecha_atencion", "calidad_cerrado",
    "fecha_resolucion", "fecha_notificacion_resolucion",
    "medio_notificacion_reclamo", "motivo_no_cumplio_plazo",
    "descripcion_averia", "fecha_cumplimiento", "aplica_carta_cumplimiento",
    "n_carta_cumplimiento", "fecha_elaboracion_carta",
    "fecha_remision_carta", "medio_notificacion_carta",
]


# ==========================================================
# UTILIDADES
# ==========================================================
def _limpiar_valor(col, valor):
    """Convierte valores a tipos compatibles con JSON/Supabase."""
    if valor is None:
        return None
    if isinstance(valor, float) and math.isnan(valor):
        return None
    if pd.isna(valor) if not isinstance(valor, (list, dict)) else False:
        return None
    if col in COLUMNAS_FECHA_BD:
        try:
            ts = pd.to_datetime(valor)
            return ts.isoformat()
        except Exception:
            return None
    if hasattr(valor, 'item'):
        valor = valor.item()
    texto = str(valor).strip()
    return texto if texto and texto.lower() != 'nat' and texto.lower() != 'nan' else None


def _df_a_registros(df: pd.DataFrame) -> list:
    """Convierte DataFrame a lista de dicts para Supabase."""
    registros = []
    for _, row in df.iterrows():
        registro = {}
        for col_excel, col_bd in EXCEL_A_BD.items():
            if col_excel in df.columns:
                registro[col_bd] = _limpiar_valor(col_bd, row.get(col_excel))
        if registro.get("clave_unica"):
            registros.append(registro)
    return registros


def _registros_a_df(registros: list) -> pd.DataFrame:
    """Convierte lista de dicts de Supabase a DataFrame con nombres Excel."""
    if not registros:
        return pd.DataFrame()
    df = pd.DataFrame(registros)
    # Renombrar columnas BD → Excel
    rename_map = {col_bd: col_excel for col_bd, col_excel in BD_A_EXCEL.items() if col_bd in df.columns}
    df = df.rename(columns=rename_map)
    # Convertir fechas
    for col_excel, col_bd in EXCEL_A_BD.items():
        if col_bd in COLUMNAS_FECHA_BD and col_excel in df.columns:
            df[col_excel] = pd.to_datetime(df[col_excel], errors="coerce")
    return df


# ==========================================================
# OPERACIONES — TICKETS
# ==========================================================
def leer_tickets() -> pd.DataFrame:
    """Lee todos los tickets de Supabase y devuelve DataFrame."""
    client = get_client()
    todos = []
    page = 0
    page_size = 1000

    while True:
        resp = client.table("tickets").select("*").range(
            page * page_size, (page + 1) * page_size - 1
        ).execute()
        if not resp.data:
            break
        todos.extend(resp.data)
        if len(resp.data) < page_size:
            break
        page += 1

    return _registros_a_df(todos)


def sincronizar_tickets(df: pd.DataFrame, usuario: str):
    """
    Sincroniza el DataFrame procesado con Supabase.
    - Tickets nuevos → INSERT
    - Tickets existentes → UPDATE solo campos calculados
    - Campos manuales → NUNCA se tocan
    """
    client = get_client()
    registros = _df_a_registros(df)

    if not registros:
        return

    # Obtener claves existentes en BD
    resp = client.table("tickets").select("clave_unica").execute()
    claves_existentes = {r["clave_unica"] for r in resp.data}

    nuevos    = []
    a_update  = []
    historial = []

    for reg in registros:
        clave = reg.get("clave_unica")
        if not clave:
            continue

        if clave not in claves_existentes:
            # Ticket nuevo
            nuevos.append(reg)
            historial.append({
                "usuario":        usuario,
                "accion":         "TICKET NUEVO",
                "ticket":         reg.get("ticket"),
                "clave_unica":    clave,
                "campo":          "TODOS",
                "valor_anterior": "",
                "valor_nuevo":    "creado desde carga",
            })
        else:
            # Solo actualizar campos calculados
            update = {"clave_unica": clave}
            for col in COLUMNAS_CALCULADAS:
                if col in reg:
                    update[col] = reg[col]
            a_update.append(update)

    # Insertar nuevos en lotes
    BATCH = 100
    for i in range(0, len(nuevos), BATCH):
        lote = nuevos[i:i + BATCH]
        client.table("tickets").insert(lote).execute()
        time.sleep(0.3)

    # Actualizar existentes en lotes
    for i in range(0, len(a_update), BATCH):
        lote = a_update[i:i + BATCH]
        client.table("tickets").upsert(
            lote, on_conflict="clave_unica"
        ).execute()
        time.sleep(0.3)

    # Registrar historial
    if historial:
        for i in range(0, len(historial), BATCH):
            client.table("historial").insert(historial[i:i + BATCH]).execute()
            time.sleep(0.3)


def guardar_campos_manuales(df_nuevo: pd.DataFrame, df_anterior: pd.DataFrame, usuario: str):
    """
    Guarda solo los campos manuales editados por el usuario.
    Compara df_nuevo vs df_anterior y actualiza solo lo que cambió.
    """
    client = get_client()
    historial = []
    BATCH = 100
    updates = []

    for _, row_nuevo in df_nuevo.iterrows():
        clave = row_nuevo.get("CLAVE_UNICA")
        if not clave:
            continue

        # Buscar fila anterior por CLAVE_UNICA
        fila_ant = df_anterior[df_anterior["CLAVE_UNICA"] == clave]
        if fila_ant.empty:
            continue
        fila_ant = fila_ant.iloc[0]

        update = {"clave_unica": clave}
        hay_cambios = False

        for col_excel, col_bd in EXCEL_A_BD.items():
            if col_bd not in COLUMNAS_MANUALES:
                continue
            if col_excel not in df_nuevo.columns:
                continue

            val_nuevo = row_nuevo.get(col_excel)
            val_ant   = fila_ant.get(col_excel)

            str_nuevo = str(val_nuevo).strip() if pd.notna(val_nuevo) else ""
            str_ant   = str(val_ant).strip()   if pd.notna(val_ant)   else ""

            if str_nuevo != str_ant:
                update[col_bd] = _limpiar_valor(col_bd, val_nuevo)
                hay_cambios = True
                historial.append({
                    "usuario":        usuario,
                    "accion":         "EDICION",
                    "ticket":         str(row_nuevo.get("TICKET", "")),
                    "clave_unica":    clave,
                    "campo":          col_excel,
                    "valor_anterior": str_ant,
                    "valor_nuevo":    str_nuevo,
                })

        if hay_cambios:
            updates.append(update)

    # Enviar updates
    for i in range(0, len(updates), BATCH):
        client.table("tickets").upsert(
            updates[i:i + BATCH], on_conflict="clave_unica"
        ).execute()
        time.sleep(0.3)

    # Registrar historial
    if historial:
        for i in range(0, len(historial), BATCH):
            client.table("historial").insert(historial[i:i + BATCH]).execute()
            time.sleep(0.3)

    return len(updates)


# ==========================================================
# OPERACIONES — FERIADOS
# ==========================================================
def leer_feriados() -> pd.Series:
    """Lee feriados de Supabase y devuelve Serie de fechas."""
    client = get_client()
    resp = client.table("feriados").select("fecha").execute()
    fechas = pd.to_datetime(
        [r["fecha"] for r in resp.data], errors="coerce"
    ).dropna().normalize()
    return fechas


# ==========================================================
# OPERACIONES — ESTADO DEL SISTEMA
# ==========================================================
def leer_estado() -> dict:
    client = get_client()
    try:
        resp = client.table("estado_sistema").select("*").eq("id", 1).execute()
        if resp.data:
            return resp.data[0]
    except Exception:
        pass
    return {"estado": "libre", "usuario": "", "desde": None}


def escribir_estado(estado: str, usuario: str):
    client = get_client()
    client.table("estado_sistema").upsert({
        "id":      1,
        "estado":  estado,
        "usuario": usuario,
        "desde":   datetime.now().isoformat(),
    }).execute()


def liberar_estado():
    client = get_client()
    client.table("estado_sistema").upsert({
        "id":      1,
        "estado":  "libre",
        "usuario": "",
        "desde":   None,
    }).execute()


def sistema_libre() -> bool:
    return leer_estado()["estado"] == "libre"


# ==========================================================
# OPERACIONES — HISTORIAL
# ==========================================================
def leer_historial() -> pd.DataFrame:
    client = get_client()
    todos = []
    page = 0
    page_size = 1000

    while True:
        resp = client.table("historial").select("*").order(
            "fecha_hora", desc=True
        ).range(page * page_size, (page + 1) * page_size - 1).execute()
        if not resp.data:
            break
        todos.extend(resp.data)
        if len(resp.data) < page_size:
            break
        page += 1

    if not todos:
        return pd.DataFrame()

    df = pd.DataFrame(todos)
    df["fecha_hora"] = pd.to_datetime(df["fecha_hora"], errors="coerce")
    return df


def registrar_documento_generado(ticket: str, clave_unica: str, tipo: str, usuario: str):
    """Registra en historial cuando se genera un documento."""
    client = get_client()
    client.table("historial").insert({
        "usuario":        usuario,
        "accion":         tipo,  # "CARTA GENERADA" o "RESOLUCION GENERADA"
        "ticket":         ticket,
        "clave_unica":    clave_unica,
        "campo":          "-",
        "valor_anterior": "-",
        "valor_nuevo":    f"{tipo}-TICKET-{ticket}.docx",
    }).execute()
