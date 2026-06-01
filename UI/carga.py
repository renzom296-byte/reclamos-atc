import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import unicodedata
from CORE.calculos import aplicar_calculos
from database import sincronizar_tickets

def _normalizar_columnas(df: pd.DataFrame) -> pd.DataFrame:
    nombres_esperados = [
        "GÉNERO", "FECHA Y HORA DE LA AVERIA", "FECHA",
        "FECHA CIERRE TICKET", "TICKET", "SOLICITUD", "ESTADO",
        "USUARIO", "CORREO", "LOCALIDAD", "DISTRITO", "PROVINCIA",
        "DEPARTAMENTO", "CÓDIGO IIB", "TIPO ENTIDAD",
        "N° DOCUMENTO DNI / CE", "ÁREA",
    ]

    def normalizar(texto):
        return unicodedata.normalize("NFC", str(texto).strip())

    mapa = {}
    for col_actual in df.columns:
        col_norm = normalizar(col_actual)
        for col_esperada in nombres_esperados:
            if col_norm == normalizar(col_esperada):
                if col_actual != col_esperada:
                    mapa[col_actual] = col_esperada
                break

    if mapa:
        df = df.rename(columns=mapa)

    return df


def cargar_archivo(archivo, feriados, usuario: str = "sistema"):

    df = pd.read_excel(archivo, header=1)

    # Eliminar columnas Unnamed
    df = df.loc[:, ~df.columns.astype(str).str.startswith("Unnamed")]
    
    # Eliminar columna GLOSA si existe
    if "GLOSA" in df.columns:
        df = df.drop(columns=["GLOSA"])

    # Normalizar nombres de columnas
    df = _normalizar_columnas(df)

    # Convertir fechas ANTES de aplicar calculos
    cols_fecha = {
        "FECHA":                     True,
        "FECHA Y HORA DE LA AVERIA": True,
        "FECHA CIERRE TICKET":       True,
    }
    for col, dayfirst in cols_fecha.items():
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], dayfirst=dayfirst, errors="coerce")

    # Aplicar calculos
    df = aplicar_calculos(df, feriados)

    # Sincronizar con Supabase
    sincronizar_tickets(df, usuario)

    return df