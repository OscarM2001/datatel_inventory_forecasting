import streamlit as st

def landing_page():
    """
    Página comunicativa
    """

    st.markdown(
        """
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                background-color: #f4f4f4;
            }
            .dashboard-title {
                font-family: 'Arial Black', sans-serif;
                font-size: 36px;
                color: #E63946; 
                text-align: center;
            }
            .dashboard-subtitle {
                font-family: 'Arial', sans-serif;
                font-size: 20px;
                color: #457B9D;
                text-align: center;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    # Cierre de sesión en la barra lateral
    with st.sidebar:
            st.title(f"Bienvenido, {st.session_state.get('username', 'Usuario')}!")
            st.write(f"Rol: {st.session_state.get('rol', 'Sin rol')}")
            if st.button("Cerrar Sesión"):
                st.session_state["authenticated"] = False
                st.session_state["username"] = ""
                st.session_state["rol"] = ""
                st.session_state["page"] = "login"
                st.rerun()  # Recarga la app para volver al inicio de sesión

    # Encabezado
    st.title("Previsión de Inventarios con Modelos ARIMA")
    st.subheader("Optimización y gestión predictiva de inventarios utilizando gráficos interactivos")

    # Descripción
    st.markdown(
        """
        Este proyecto tiene como objetivo desarrollar un sistema de predicción y optimización del inventario basado en modelos ARIMA.
        Los gráficos permiten interpretar cómo las predicciones se relacionan con las ventas pasadas y las necesidades futuras de reposición.
        """
    )

    # Gráficos Descriptivos
    st.markdown("### Gráficos Utilizados")

    st.markdown("#### 1. Matriz de Reposición de Inventario")
    st.markdown("Tabla enriquecida que destaca el estado de los productos según su nivel de urgencia.")
    st.image(r"C:\Users\OSCAR\Documents\Tesis\Entregables\datatel_inventory_forecasting\Imagen\Datatel_logo_1.png", caption="Matriz de Reposición de Inventario")

    st.markdown("#### 2. Predicción de Reposición por Fecha")
    st.markdown("Gráfico de líneas que muestra las tendencias de reposición futura.")
    st.image(r"C:\Users\OSCAR\Documents\Tesis\Entregables\datatel_inventory_forecasting\Imagen\Datatel_logo_1.png", caption="Predicción de Reposición por Fecha")

    st.markdown("#### 3. Demanda de Reposición por Producto")
    st.markdown("Gráfico de barras apiladas para visualizar la reposición por producto.")
    st.image(r"C:\Users\OSCAR\Documents\Tesis\Entregables\datatel_inventory_forecasting\Imagen\Datatel_logo_1.png", caption="Demanda de Reposición por Producto")

    st.markdown("#### 4. Ventas Históricas vs. Predicción")
    st.markdown("Gráfico comparativo entre ventas pasadas y predicciones futuras.")
    st.image(r"C:\Users\OSCAR\Documents\Tesis\Entregables\datatel_inventory_forecasting\Imagen\Datatel_logo_1.png", caption="Ventas Históricas vs. Predicción")


