import streamlit as st
from db.db_connection import get_db_connection
import pandas as pd
from sqlalchemy import text


class Login:
    """
    Clase para manejar el sistema de autenticación en Streamlit con datos desde la base de datos,
    incluyendo registro de nuevos usuarios.
    """

    def __init__(self):
        self.engine = get_db_connection()  # Motor de conexión a la base de datos

    def login(self):
        """
        Maneja el flujo de inicio de sesión con un logo en la columna derecha y un botón para registrarse.
        """
        if "authenticated" not in st.session_state:
            st.session_state["authenticated"] = False
            st.session_state["username"] = ""
            st.session_state["rol"] = ""

        # Función para manejar el inicio de sesión
        def handle_login():
            if self._validate_credentials(st.session_state.get("username", ""), st.session_state.get("password", "")):
                st.success("Sesión iniciada con éxito.")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")

        if not st.session_state["authenticated"]:
            # Dividir la página en dos columnas
            col1, col2 = st.columns([2, 1])  # La columna izquierda es más ancha

            # Columna izquierda: formulario de inicio de sesión
            with col1:
                st.title("Inicio de Sesión")
                st.text_input("Usuario", key="username")
                st.text_input("Contraseña", type="password", key="password", on_change=handle_login)
                if st.button("Iniciar Sesión"):
                    handle_login()

                # Nuevo bloque: Título y botón para registrarse
                st.write("¿Desea registrarse en la aplicación?")
                if st.button("Registrar", key="register_redirect"):
                    st.session_state["auth_mode"] = "register"  # Cambiar al modo de registro
                    st.rerun()

            # Columna derecha: logo o imagen
            with col2:
                image_path = r"C:\Users\OSCAR\Documents\Tesis\Entregables\datatel_inventory_forecasting\Imagen\Datatel_logo_1.png"
                try:
                    st.image(image_path, caption="Todos los derechos Reservados @2025", use_container_width=True)
                except Exception as e:
                    st.warning(f"No se pudo cargar la imagen: {e}")

            return False

        # Mostrar información del usuario autenticado
        self._display_logged_in_user()
        return True

    def _validate_credentials(self, username, password):
        """
        Valida las credenciales del usuario contra la base de datos.
        """
        try:
            query = f"""
                SELECT usuario, rol 
                FROM usuarios 
                WHERE usuario = '{username}' AND password = '{password}'
            """
            result = pd.read_sql(query, self.engine)

            if not result.empty:
                st.session_state["authenticated"] = True
                st.session_state["username"] = result.iloc[0]["usuario"]
                st.session_state["rol"] = result.iloc[0]["rol"]
                return True
            return False
        except Exception as e:
            st.error(f"Error al validar las credenciales: {e}")
            return False

    def _display_logged_in_user(self):
        """
        Muestra información del usuario autenticado y el botón para cerrar sesión.
        """
        st.sidebar.title(f"Bienvenido, {st.session_state['username']}!")
        st.sidebar.write(f"Rol: {st.session_state['rol']}")
        if st.sidebar.button("Cerrar Sesión"):
            self.logout()

    def logout(self):
        """
        Maneja el flujo de cierre de sesión.
        """
        st.session_state["authenticated"] = False
        st.session_state["username"] = ""
        st.session_state["rol"] = ""
        st.rerun()
