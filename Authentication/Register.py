import re
import streamlit as st
import requests


class Register:
    """
    Clase para manejar el registro de nuevos usuarios utilizando FastAPI.
    """

    def __init__(self):
        self.api_url = "http://127.0.0.1:8000/register"  # URL base de la API

    def register(self):
        """
        Maneja el flujo de registro de usuarios.
        """
        st.title("Registrar Nuevo Usuario")
        username = st.text_input("Nombre de Usuario", key="reg_username")
        password = st.text_input("Contraseña", type="password", key="reg_password")
        confirm_password = st.text_input("Confirmar Contraseña", type="password", key="reg_confirm_password")
        rol = st.selectbox("Rol", ["admin", "user"], key="reg_role")

        if st.button("Registrar", key="reg_submit"):
            # Validar campos obligatorios
            if not username or not password or not confirm_password:
                st.error("Todos los campos son obligatorios.")
                return False

            # Validar políticas de contraseña
            if not self._validate_password_strength(password):
                return False

            # Validar que las contraseñas coincidan
            if password != confirm_password:
                st.error("Las contraseñas no coinciden.")
                return False

            # Verificar si el usuario ya existe
            if self._user_exists(username):
                st.error("El nombre de usuario ya existe. Por favor, elige otro.")
                return False

            # Crear el usuario en la API
            if self._create_user(username, password, rol):
                st.success("Usuario registrado con éxito. Ahora puedes iniciar sesión.")
                # Redirigir automáticamente al inicio de sesión
                st.session_state["auth_mode"] = "login"
                st.rerun()
            else:
                st.error("Hubo un error al registrar al usuario. Inténtalo nuevamente.")
                return False

        # Botón para regresar al inicio de sesión
        if st.button("Volver al Inicio de Sesión", key="reg_back_to_login"):
            st.session_state["auth_mode"] = "login"
            st.rerun()

        return False

    def _validate_password_strength(self, password):
        """
        Valida que la contraseña cumpla con las políticas de seguridad.
        """
        # Definir las reglas de la política de contraseña
        if len(password) < 8:
            st.error("La contraseña debe tener al menos 8 caracteres.")
            return False
        if not re.search(r"[A-Z]", password):
            st.error("La contraseña debe contener al menos una letra mayúscula.")
            return False
        if not re.search(r"[a-z]", password):
            st.error("La contraseña debe contener al menos una letra minúscula.")
            return False
        if not re.search(r"\d", password):
            st.error("La contraseña debe contener al menos un número.")
            return False
        if not re.search(r"[!@#$%^&*()./]", password):
            st.error("La contraseña debe contener al menos un carácter especial (!@#$%^&*()).")
            return False

        return True

    def _user_exists(self, username):
        """
        Verifica si un usuario ya existe en el sistema a través de la API.
        """
        try:
            response = requests.get(f"{self.api_url}/exists", params={"usuario": username})
            if response.status_code == 200:
                return response.json().get("exists", False)
            else:
                st.error("Error al verificar el usuario. Intenta nuevamente.")
                return True
        except Exception as e:
            st.error(f"Error al conectar con la API: {e}")
            return True

    def _create_user(self, username, password, rol):
        """
        Crea un nuevo usuario en el sistema a través de la API.
        """
        try:
            payload = {"usuario": username, "password": password, "rol": rol}
            response = requests.post(f"{self.api_url}/register", json=payload)
            if response.status_code == 201:
                return True
            else:
                error_message = response.json().get("detail", "Error desconocido")
                st.error(f"Error al registrar el usuario: {error_message}")
                return False
        except Exception as e:
            st.error(f"Error al conectar con la API: {e}")
            return False
