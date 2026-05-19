import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from database import (
    leer_estado, escribir_estado, liberar_estado, sistema_libre
)

ESTADO_LIBRE     = "libre"
ESTADO_CARGANDO  = "cargando"
ESTADO_GUARDANDO = "guardando"

def mostrar_aviso_bloqueo() -> bool:
    estado = leer_estado()

    if estado["estado"] == ESTADO_CARGANDO:
        st.warning(
            f"⚠️ **{estado['usuario']}** está cargando un reporte nuevo. "
            f"Espera que termine antes de guardar cambios."
        )
        return True

    if estado["estado"] == ESTADO_GUARDANDO:
        st.warning(
            f"⚠️ **{estado['usuario']}** está guardando cambios. "
            f"Espera unos segundos e intenta de nuevo."
        )
        return True

    return False