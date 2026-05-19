import os
import streamlit as st

# En Streamlit Cloud lee de secrets, en local lee directo
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
except Exception:
    SUPABASE_URL = "https://mtrebivjuqrzturdvopt.supabase.co"
    SUPABASE_KEY = "eyJhbGc..."

BASE = os.path.dirname(os.path.abspath(__file__))
RUTAS = {
    "plantillas":      os.path.join(BASE, "DATA", "PLANTILLAS"),
    "plantilla_res":   os.path.join(BASE, "DATA", "PLANTILLAS", "PLANTILLA RESOLUCION 2025 GNP.docx"),
    "plantilla_carta": os.path.join(BASE, "DATA", "PLANTILLAS", "CARTAS DE CUMPLIMIENTO GNP-ATC.docx"),
}
ADMIN_USUARIO = None
