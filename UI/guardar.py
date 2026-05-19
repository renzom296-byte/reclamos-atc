import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from database import guardar_campos_manuales

def guardar_consolidado(df_nuevo, df_anterior, usuario: str):
    """
    Guarda solo los campos manuales editados en Supabase.
    Compara df_nuevo vs df_anterior campo por campo.
    """
    n_cambios = guardar_campos_manuales(df_nuevo, df_anterior, usuario)

    if n_cambios > 0:
        st.success(f"✅ {n_cambios} ticket(s) actualizado(s) correctamente.")
    else:
        st.info("No se detectaron cambios para guardar.")