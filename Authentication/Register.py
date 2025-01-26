from sqlalchemy import text
import streamlit as st
from db.db_connection import get_db_connection


class Register:
    """
    Clase para manejar el registro de nuevos usuarios.
    """

    def __init__(self):
        self.engine = get_db_connection()  # Motor de conexión a la base de datos

    def register(self):
        """
        Maneja el flujo de registro de usuarios.
        """
        st.title("Registrar Nuevo Usuario")
        username = st.text_input("Nombre de Usuario")
        password = st.text_input("Contraseña", type="password")
        confirm_password = st.text_input("Confirmar Contraseña", type="password")
        rol = st.selectbox("Rol", ["admin", "user"])

        if st.button("Registrar"):
            if not username or not password or not confirm_password:
                st.error("Todos los campos son obligatorios.")
                return False

            if password != confirm_password:
                st.error("Las contraseñas no coinciden.")
                return False

            if self._user_exists(username):
                st.error("El nombre de usuario ya existe. Por favor, elige otro.")
                return False

            if self._create_user(username, password, rol):
                st.success("Usuario registrado con éxito. Ahora puedes iniciar sesión.")
                # Redirigir automáticamente al inicio de sesión
                st.session_state["auth_mode"] = "login"
                st.rerun()
            else:
                st.error("Hubo un error al registrar al usuario. Inténtalo nuevamente.")
                return False
            
        # Botón para regresar al inicio de sesión
        if st.button("Volver al Inicio de Sesión", key="back_to_login"):
            st.session_state["auth_mode"] = "login"
            st.rerun()
            
        return False

    def _user_exists(self, username):
    
        try:
            query = text("SELECT COUNT(*) AS count FROM usuarios WHERE usuario = :usuario")
            with self.engine.connect() as connection:
                result = connection.execute(query, {"usuario": username}).fetchone()
            # Acceder al primer índice de la tupla, que es el resultado del COUNT(*)
            return result[0] > 0
        except Exception as e:
            st.error(f"Error al verificar si el usuario existe: {e}")
            return True


    def _create_user(self, username, password, rol):
        """
        Crea un nuevo usuario en la base de datos.
        """
        try:
            query = text("""
                INSERT INTO usuarios (usuario, password, rol)
                VALUES (:usuario, :password, :rol)
            """)
            with self.engine.connect() as connection:
                connection.execute(query, {"usuario": username, "password": password, "rol": rol})
                connection.commit()  # Asegura que los cambios se guarden
            return True
        except Exception as e:
            st.error(f"Error al crear el usuario: {e}")
            return False
