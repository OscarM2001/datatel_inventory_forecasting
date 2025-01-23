# app/app.py
import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import streamlit as st
import plotly.express as px
from models.generate_restocking_matrix import RestockingMatrix
from models.compare_sales_and_predictions import CompareSalesAndPredictions
from models.predict_restocking_by_product import PredictRestockingByProduct
from models.predict_by_date import PredictionByDate
from models.oauth_manager import OAuthManager  # Asegúrate de que esta clase esté implementada

def apply_colors(row):
    """
    Aplica colores personalizados para cada estado de reposición.
    """
    if row["Estado de Reposición"] == "Urgente":
        return ['background-color: #FF6F61; color: white' for _ in row]
    elif row["Estado de Reposición"] == "Moderada":
        return ['background-color: #FFD700; color: black' for _ in row]
    elif row["Estado de Reposición"] == "Adecuado":
        return ['background-color: #90EE90; color: black' for _ in row]
    elif row["Estado de Reposición"] == "No prioritario":
        return ['background-color: #FFA500; color: black' for _ in row]
    else:
        return ['background-color: white; color: black' for _ in row]

def simple_logout():
    """
    Cierra la sesión limpiando el estado de la sesión y redirigiendo al usuario.
    """
    st.session_state.clear()  # Limpia toda la sesión
    st.write('<script>window.location.href = "/";</script>', unsafe_allow_html=True)
    st.rerun()  # Reinicia la aplicación para aplicar los cambios

def authenticate_user():
    """
    Maneja el flujo de autenticación usando OAuth2.
    """
    oauth_manager = OAuthManager()

    # Verificar si el token está en la sesión
    if "token" in st.session_state:
        token = st.session_state["token"]

        # Verificar si el token ha caducado y refrescarlo si es necesario
        if "expires_at" in token and token["expires_at"] <= time.time():
            try:
                token = oauth_manager.refresh_access_token(token)
                st.session_state["token"] = token
            except Exception as e:
                st.error(f"Error al refrescar el token: {e}")
                st.session_state.clear()  # Limpia la sesión si hay error
                return False

        # Obtener información del usuario
        user_info = oauth_manager.get_user_info(token)
        st.sidebar.success(f"Bienvenido, {user_info['email']}!")
        
        if st.sidebar.button("Cerrar sesión"):
            simple_logout()

        return True

    # Si no hay token, iniciar autenticación
    query_params = st.query_params

    if "code" in query_params:
        try:
            code = query_params["code"]
            token = oauth_manager.fetch_token(code)
            st.session_state["token"] = token
            st.write('<script>window.location.href = "/";</script>', unsafe_allow_html=True)  # Redirigir después de obtener el token
            st.rerun()
        except Exception as e:
            st.error(f"Error en la autenticación: {e}")
            return False

    # Generar URL de inicio de sesión
    auth_url, state = oauth_manager.get_auth_url()
    st.markdown(f"[Inicia sesión con Google]({auth_url})")
    return False

def main():
    """
    Configura el Dashboard de Inventarios.
    """
    # Configuración inicial de la página
    st.set_page_config(page_title="Datatel App", layout="wide")
    
    # Autenticación
    st.sidebar.title("Autenticación")
    if not authenticate_user():
        st.warning("Debes iniciar sesión para continuar.")
        return

    st.title("Dashboard de Inventarios")

    # Sección: Matriz de Reposición
    st.header("Matriz de Reposición")
    try:
        restocking = RestockingMatrix()
        restocking_df = restocking.generate_matrix()

        # Mostrar la tabla con métricas adicionales
        st.subheader("Tabla de Matriz de Reposición (con Métricas)")
        styled_df = restocking_df.style.apply(apply_colors, axis=1)

        # Agregar tabla descriptiva
        st.dataframe(styled_df, use_container_width=True)

        # Mostrar métricas globales
        if not restocking_df[['MSE', 'RMSE']].isnull().all().all():
            mse_mean = restocking_df['MSE'].mean(skipna=True)
            rmse_mean = restocking_df['RMSE'].mean(skipna=True)
            st.info(
                f"**Métricas del Modelo ARIMA:**\n"
                f"- **MSE Promedio:** {mse_mean:.2f}\n"
                f"- **RMSE Promedio:** {rmse_mean:.2f}"
            )
    except Exception as e:
        st.error(f"Error al generar la matriz: {e}")

    # Sección: Predicción de Reposición por Fecha
    st.header("Comparación de Ventas y Predicciones")
    try:
        prediction = CompareSalesAndPredictions()

        # Obtener opciones de productos en formato "ID - Nombre"
        product_options = prediction.get_product_options()
        product_options_list = product_options['Producto_Opcion'].tolist()
        product_id_mapping = product_options.set_index('Producto_Opcion')['ID_Producto'].to_dict()

        # Selector de producto
        selected_product_option = st.selectbox("Selecciona un producto:", product_options_list)

        # Obtener el ID real del producto
        selected_product_id = product_id_mapping[selected_product_option]

        # Generar predicción para el producto seleccionado
        forecast_df, product_sales = prediction.predict_by_date(selected_product_id)
        if forecast_df.empty:
            st.warning("No hay datos suficientes para generar predicciones.")
        else:
            # Mostrar ventas históricas junto con la predicción
            st.subheader(f"Comparación de Ventas Históricas y Predicción para:\n {selected_product_option}")
            chart_data = pd.DataFrame({
                "Ventas Históricas": product_sales,
                "Predicción de Reposición": forecast_df.set_index("Fecha")["Predicción"]
            })
            st.line_chart(chart_data, use_container_width=True)
    except Exception as e:
        st.error(f"Error al generar la predicción: {e}")

    # Sección: Predicción de Reposición por Producto
    st.header("Predicción de Reposición por Producto")
    try:
        restocking_by_product = PredictRestockingByProduct()
        product_restocking_df = restocking_by_product.predict_restocking_by_product()

        if product_restocking_df.empty:
            st.warning("No hay datos suficientes para generar predicciones.")
        else:
            # Crear una columna para el tooltip con ID y Nombre del Producto
            product_restocking_df['Producto'] = (
                product_restocking_df['ID_Producto'].astype(str) + " - " + product_restocking_df['Producto']
            )

            # Mostrar el gráfico
            st.subheader("Cantidad Recomendada de Reposición por Producto")
            fig = px.bar(
                product_restocking_df,
                x='ID_Producto',  # Muestra solo el ID en el eje X
                y='Cantidad',
                color='Cantidad',
                color_continuous_scale='Blues',
                labels={'ID_Producto': 'Código del Producto', 'Cantidad': 'Cantidad de Reposición'},
                title="Cantidad Recomendada de Reposición",
                hover_data={'Cantidad': True,'Producto': True,'ID_Producto': False }  # Incluye nombre del producto en el tooltip
            )
            fig.update_layout(
                xaxis_title="Código del Producto",
                yaxis_title="Cantidad Recomendada de Reposición",
                showlegend=False,
                coloraxis_colorbar=dict(
                    title="Cantidad",
                    ticks="outside"
                )
            )
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error al generar la predicción por producto: {e}")

    
    # Sección: Predicción Futura de Reposición
    st.header("Predicción Futura de Reposición")
    try:
        future_prediction = PredictionByDate()

        # Obtener opciones de productos en formato "ID - Nombre"
        product_options = future_prediction.get_product_options()
        product_options_list = product_options['Producto_Opcion'].tolist()
        product_id_mapping = product_options.set_index('Producto_Opcion')['ID_Producto'].to_dict()

        # Selector de producto
        selected_product_option = st.selectbox("Selecciona un producto para predecir:", product_options_list)

        # Obtener el ID real del producto
        selected_product_id = product_id_mapping[selected_product_option]

        # Generar predicción futura para el producto seleccionado
        forecast_df = future_prediction.predict_future(selected_product_id)

        if forecast_df.empty:
            st.warning("No hay datos suficientes para generar predicciones.")
        else:
            st.subheader(f"Predicción Futura para el Producto: {selected_product_option}")
            fig = px.line(
                forecast_df,
                x='Fecha',
                y='Predicción',
                labels={'Fecha': 'Fecha', 'Predicción': 'Cantidad Predicha'},
                title="Predicción de Reposición Futura"
            )
            fig.update_layout(
                xaxis_title="Fecha",
                yaxis_title="Cantidad Predicha",
                legend_title="Predicción"
            )
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error al generar la predicción futura: {e}")
        
if __name__ == "__main__":
    main()
