# ==========================================================
# MAPA DE COLUMNAS
# Traduce nombres del Excel/DataFrame a nombres de la BD
# y viceversa.
# Usado por database.py para INSERT y UPDATE
# ==========================================================

# Excel column name → Supabase column name
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

    # Calculados por Python
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

    # Manuales
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

# Supabase column name → Excel column name (inverso)
BD_A_EXCEL = {v: k for k, v in EXCEL_A_BD.items()}

# ==========================================================
# COLUMNAS CALCULADAS POR PYTHON
# Automate/Python puede actualizar estas al procesar Excel
# ==========================================================
COLUMNAS_CALCULADAS = [
    "senor_a",
    "identificado",
    "usuario_a",
    "fecha_inicia_reclamo_calidad",
    "cierre_ticket_reclamo_averia",
    "fecha_limite_resolucion",
    "fecha_limite_cumplimiento",
    "fecha_limite_elaboracion_carta",
    "resolucion",
    "paso_a_calidad",
    # Campos del input que pueden cambiar
    "estado",
    "solicitud",
    "fecha_cierre_ticket",
    "fecha_averia",
]

# ==========================================================
# COLUMNAS MANUALES
# NUNCA se actualizan al procesar Excel nuevo
# Solo el usuario las puede cambiar desde la app
# ==========================================================
COLUMNAS_MANUALES = [
    "fecha_programada_mantenimiento_res1",
    "fecha_programada_mantenimiento_res2",
    "n_ot",
    "fecha_ot",
    "supervisor_mantenimiento",
    "colaborador_encargado",
    "declaracion_reclamo",
    "quien_indico_fecha_atencion",
    "calidad_cerrado",
    "fecha_resolucion",
    "fecha_notificacion_resolucion",
    "medio_notificacion_reclamo",
    "motivo_no_cumplio_plazo",
    "descripcion_averia",
    "fecha_cumplimiento",
    "aplica_carta_cumplimiento",
    "n_carta_cumplimiento",
    "fecha_elaboracion_carta",
    "fecha_remision_carta",
    "medio_notificacion_carta",
]
