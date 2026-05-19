import streamlit as st

# ==========================================================
# PANTALLA DE INGRESO
# ==========================================================
def mostrar_login():
    """
    Muestra la pantalla de ingreso de nombre de usuario.
    Retorna True si el usuario ya ingresó su nombre,
    False si aún no lo ha hecho.
    """

    if "usuario_nombre" in st.session_state and st.session_state.usuario_nombre:
        return True

    # ----------------------------------------------------------
    # Centrar el formulario
    # ----------------------------------------------------------
    col_izq, col_centro, col_der = st.columns([1, 1.5, 1])

    with col_centro:

        st.markdown("<br><br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div style="text-align:center; margin-bottom: 2rem;">
                <h1 style="font-size:1.6rem; margin-bottom:0.3rem;">
                    Gestión de Reclamos ATC
                </h1>
                <p style="color:#5A6A7E; font-size:0.9rem;">
                    Ingresa tu nombre para continuar
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.form("form_login", clear_on_submit=False):
            nombre = st.text_input(
                "Nombre",
                placeholder="Ej: María López",
                label_visibility="collapsed"
            )
            ingresar = st.form_submit_button(
                "Ingresar →",
                use_container_width=True
            )

        if ingresar:
            nombre = nombre.strip()
            if not nombre:
                st.error("Por favor ingresa tu nombre.")
                return False
            if len(nombre) < 2:
                st.error("El nombre debe tener al menos 2 caracteres.")
                return False

            st.session_state.usuario_nombre = nombre
            st.rerun()

    return False
