import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from Authentication.Login import Login
from Authentication.Register import Register
from frontend import landing_page
from dashboard import Dashboard

# Configuración inicial de la página basada en el estado de la aplicación
if "page" not in st.session_state:
    st.session_state["page"] = "login"

# Define la configuración de la página en función del estado
if st.session_state["page"] == "login":
    st.set_page_config(page_title="Iniciar Sesión - Datatel", layout="centered")
elif st.session_state["page"] == "landing":
    st.set_page_config(page_title="Bienvenido - Datatel", layout="wide")
elif st.session_state["page"] == "dashboard":
    st.set_page_config(page_title="Dashboard - Datatel Soluciones", layout="wide")

def main():
    """
    Controla la navegación entre inicio de sesión, registro, landing page y dashboard.
    """
    # Inicializar el estado de la página y el modo de autenticación
    if "page" not in st.session_state:
        st.session_state["page"] = "login"  # Página inicial: inicio de sesión
    if "auth_mode" not in st.session_state:
        st.session_state["auth_mode"] = "login"  # Modo de autenticación inicial

    # Lógica para manejar cada página
    if st.session_state["page"] == "login":
        auth = Login()
        if st.session_state["auth_mode"] == "register":
            register = Register()
            if register.register():
                st.session_state["auth_mode"] = "login"  # Redirigir al inicio de sesión después de registrarse
                st.rerun()
        elif auth.login():
            st.session_state["page"] = "landing"  # Ir a la landing page después del inicio de sesión
            st.rerun()

    elif st.session_state["page"] == "landing":
        landing_page()
        if st.button("Ir al Dashboard", key="goto_dashboard"):
            st.session_state["page"] = "dashboard"
            st.rerun()

    elif st.session_state["page"] == "dashboard":
        Dashboard.render_dashboard()


if __name__ == "__main__":
    main()
