import os
import streamlit as st

try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
except Exception:
    SUPABASE_URL = "https://mtrebivjuqrzturdvopt.supabase.co"
    SUPABASE_KEY = "eyJhbGc..."

# Ruta absoluta basada en la ubicación de app.py en Streamlit Cloud
BASE = os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Verificar si estamos en Streamlit Cloud
if os.path.exists("/mount/src"):
    # Buscar la carpeta del proyecto en /mount/src
    proyectos = os.listdir("/mount/src")
    if proyectos:
        BASE = os.path.join("/mount/src", proyectos[0])
else:
    BASE = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(BASE) == "UI":
        BASE = os.path.dirname(BASE)

RUTAS = {
    "plantillas":      os.path.join(BASE, "DATA", "PLANTILLAS"),
    "plantilla_res":   os.path.join(BASE, "DATA", "PLANTILLAS", "PLANTILLA RESOLUCION 2025 GNP.docx"),
    "plantilla_carta": os.path.join(BASE, "DATA", "PLANTILLAS", "CARTAS DE CUMPLIMIENTO GNP-ATC.docx"),
}
ADMIN_USUARIO = None
