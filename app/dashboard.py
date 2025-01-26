import streamlit as st
import pandas as pd
import plotly.express as px
from models.generate_restocking_matrix import RestockingMatrix
from models.compare_sales_and_predictions import CompareSalesAndPredictions
from models.predict_restocking_by_product import PredictRestockingByProduct
from models.predict_by_date import PredictionByDate
import requests

class Dashboard:
    """
    Clase para manejar la visualización y la interacción del Dashboard de Inventarios.
    """

    @staticmethod
    def fetch_inventory():
        response = requests.get("http://127.0.0.1:8000/inventory/all")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Error al obtener los datos de inventario")
            return []

    @staticmethod
    def render_dashboard():
        st.title("Dashboard de Inventarios")
        inventory_data = Dashboard.fetch_inventory()
        if inventory_data:
            st.write("Datos de inventario obtenidos desde la API:")
            st.dataframe(inventory_data)

    @staticmethod
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

    @staticmethod
    def render_dashboard():
        """
        Renderiza el Dashboard de Inventarios.
        """

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

            # Botón para regresar a la Landing Page
            if st.button("Volver a la Landing Page", key="back_to_landing"):
                st.session_state["page"] = "landing"
                st.rerun()

        # Título del dashboard
        st.markdown(
            """
            <style>
                .dashboard-title {
                    font-family: 'Arial Black', sans-serif;
                    font-size: 48px;
                    color: #E63946; /* Color rojo para el texto */
                    text-align: center;
                    margin-top: 20px;
                }
                .arrows {
                    font-size: 60px;
                    color: #E63946; /* Color rojo para las flechas */
                    text-align: center;
                    display: block;
                    line-height: 1;
                }
            </style>
            <div class="arrows">➤➤➤</div>
            <div class="dashboard-title">DATATEL SOLUCIONES</div>
            """,
            unsafe_allow_html=True
        )

        st.title("Predicción de Inventario con Modelo ARIMA")

        # Sección: Matriz de Reposición
        st.header("Matriz de Reposición de inventario")
        try:
            restocking = RestockingMatrix()
            restocking_df = restocking.generate_matrix()

            styled_df = restocking_df.style.apply(Dashboard.apply_colors, axis=1)
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

            product_options = prediction.get_product_options()
            product_options_list = product_options['Producto_Opcion'].tolist()
            product_id_mapping = product_options.set_index('Producto_Opcion')['ID_Producto'].to_dict()

            selected_product_option = st.selectbox("Selecciona un producto:", product_options_list)
            selected_product_id = product_id_mapping[selected_product_option]

            forecast_df, product_sales = prediction.predict_by_date(selected_product_id)
            if forecast_df.empty:
                st.warning("No hay datos suficientes para generar predicciones.")
            else:
                st.subheader(f"Comparación de Ventas Históricas y Predicción para: {selected_product_option}")
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
                product_restocking_df['Producto'] = (
                    product_restocking_df['ID_Producto'].astype(str) + " - " + product_restocking_df['Producto']
                )

                st.subheader("Cantidad Recomendada de Reposición por Producto")
                fig = px.bar(
                    product_restocking_df,
                    x='ID_Producto',
                    y='Cantidad',
                    color='Cantidad',
                    color_continuous_scale='Blues',
                    labels={'ID_Producto': 'Código del Producto', 'Cantidad': 'Cantidad de Reposición'},
                    title="Cantidad Recomendada de Reposición",
                    hover_data={'Cantidad': True, 'Producto': True, 'ID_Producto': False}
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

            product_options = future_prediction.get_product_options()
            product_options_list = product_options['Producto_Opcion'].tolist()
            product_id_mapping = product_options.set_index('Producto_Opcion')['ID_Producto'].to_dict()

            selected_product_option = st.selectbox("Selecciona un producto para predecir:", product_options_list)
            selected_product_id = product_id_mapping[selected_product_option]

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
