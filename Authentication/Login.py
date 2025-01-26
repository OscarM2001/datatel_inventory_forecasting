import streamlit as st
import requests


class Login:
    """
    Clase para manejar el sistema de autenticación en Streamlit utilizando FastAPI.
    """

    def __init__(self):
        self.api_url = "http://127.0.0.1:8000/auth"  # URL base de la API de FastAPI
    
    def login(self):
        """
        Maneja el flujo de inicio de sesión con un logo en la columna derecha y un botón para registrarse.
        """
        # Inicializar el estado de la sesión si no existe
        if "authenticated" not in st.session_state:
            st.session_state["authenticated"] = False
            st.session_state["username"] = ""
            st.session_state["rol"] = ""

        # Función para manejar el inicio de sesión
        def handle_login():
            """
            Llama a la API para validar las credenciales del usuario.
            """
            input_username = st.session_state.get("input_username", "")
            input_password = st.session_state.get("input_password", "")
            if self._validate_credentials(input_username, input_password):
                st.success("Sesión iniciada con éxito.")
                st.rerun()  # Recargar la app tras iniciar sesión
            

        if not st.session_state["authenticated"]:
            # Dividir la página en dos columnas
            col1, col2 = st.columns([2, 1])  # La columna izquierda es más ancha

            # Columna izquierda: formulario de inicio de sesión
            with col1:
                st.title("Inicio de Sesión")
                st.text_input("Usuario", key="input_username")  # Usa una clave diferente para el widget
                st.text_input("Contraseña", type="password", key="input_password")  # Usa una clave diferente para el widget
                # Botón para iniciar sesión
                if st.button("Iniciar Sesión"):
                    handle_login()

                # Opción de registro
                st.write("¿Desea registrarse en la aplicación?")
                if st.button("Registrar", key="register_redirect"):
                    st.session_state["auth_mode"] = "register"  # Cambiar al modo de registro
                    st.rerun()  # Recargar la app para mostrar el registro

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
        Valida las credenciales del usuario mediante una solicitud a la API.
        """
        try:
            # Enviar credenciales a la API
            response = requests.post(
                f"{self.api_url}/login", 
                json={"usuario": username, "password": password}  # Ajustado para coincidir con la API
            )
            if response.status_code == 200:
                # Actualizar el estado de la sesión en caso de éxito
                data = response.json()
                st.session_state["authenticated"] = True
                st.session_state["username"] = data["usuario"]
                st.session_state["rol"] = data["rol"]
                return True
            elif response.status_code == 401:
                st.error("Credenciales incorrectas.")
                return False
            else:
                st.error(f"Error desconocido: {response.status_code}")
                return False
        except Exception as e:
            st.error(f"Error al conectar con la API: {e}")
            return False

    def _display_logged_in_user(self):
        """
        Muestra información del usuario autenticado y el botón para cerrar sesión.
        """
        st.sidebar.title(f"Bienvenido, {st.session_state['username']}!")
        st.sidebar.write(f"Rol: {st.session_state['rol']}")
        # Botón para cerrar sesión
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
