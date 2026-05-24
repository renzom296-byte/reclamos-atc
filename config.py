import os
import streamlit as st

try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
except Exception:
    SUPABASE_URL = "https://mtrebivjuqrzturdvopt.supabase.co"
    SUPABASE_KEY = "eyJhbGc..."

# Ruta raíz — funciona tanto local como en Streamlit Cloud
BASE = "/mount/src/reclamos-atc"
if not os.path.exists(BASE):
    # Local — usa la carpeta donde está config.py
    BASE = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(BASE) == "UI":
        BASE = os.path.dirname(BASE)

RUTAS = {
    "plantillas":      os.path.join(BASE, "DATA", "PLANTILLAS"),
    "plantilla_res":   os.path.join(BASE, "DATA", "PLANTILLAS", "PLANTILLA RESOLUCION 2025 GNP.docx"),
    "plantilla_carta": os.path.join(BASE, "DATA", "PLANTILLAS", "CARTAS DE CUMPLIMIENTO GNP VF - ATC.docx"),
}
ADMIN_USUARIO = None
