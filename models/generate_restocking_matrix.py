# models/restocking_matrix.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import numpy as np
from db.db_operations import DatabaseOperations


class RestockingMatrix:
    """
    Clase para generar la Matriz de Reposición de Inventario utilizando un modelo ARIMA y evaluar su precisión.
    """

    def __init__(self):
        """
        Inicializa la clase y establece la instancia para las operaciones de base de datos.
        """
        self.db_ops = DatabaseOperations()

    def fetch_data(self):
        """
        Extrae los datos de inventario y ventas desde la base de datos.
        :return: Tuple con DataFrames de inventario y ventas.
        """
        inventory_data = self.db_ops.fetch_inventory_data()  # Datos de inventario
        sales_data = self.db_ops.fetch_sales_data()  # Datos históricos de ventas
        return inventory_data, sales_data

    def preprocess_sales_data(self, sales_data):
        """
        Preprocesa los datos de ventas convirtiendo las fechas y estableciendo un índice.
        :param sales_data: DataFrame de ventas.
        :return: DataFrame preprocesado.
        """
        sales_data['Fecha_Venta'] = pd.to_datetime(sales_data['Fecha_Venta'])
        sales_data.set_index('Fecha_Venta', inplace=True)
        return sales_data

    def calculate_error_metrics(self, test, forecast):
        """
        Calcula métricas de error para evaluar la precisión del modelo.
        :param test: Serie real del conjunto de prueba.
        :param forecast: Serie predicha por el modelo.
        :return: Diccionario con las métricas RMSE y MSE.
        """
        mse = mean_squared_error(test, forecast)
        rmse = np.sqrt(mse)
        return {"MSE": mse, "RMSE": rmse}

    def generate_matrix(self):
        """
        Genera la Matriz de Reposición utilizando el modelo ARIMA para predecir la reposición.
        También calcula métricas de error para evaluar la precisión del modelo.
        :return: DataFrame con la matriz de reposición y métricas de error.
        """
        inventory_data, sales_data = self.fetch_data()
        sales_data = self.preprocess_sales_data(sales_data)

        restocking_data = []  # Lista para almacenar los datos procesados

        for product_id in inventory_data['ID_Producto'].unique():
            product_sales = sales_data[sales_data['ID_Producto'] == product_id]['Cantidad_Vendida'].resample('D').sum().fillna(0)
            train_size = int(len(product_sales) * 0.8) # Usar 80% de los datos para entrenamiento
            train = product_sales[:train_size]
            test = product_sales[train_size:]  # Conjunto de prueba (20%)

            # Modelo ARIMA
            if not train.empty:
                model = ARIMA(train, order=(5, 1, 0))
                #print(model)
                fitted_model = model.fit()
                forecast = fitted_model.forecast(steps=len(test))
                # Calcular métricas de error si hay datos de prueba
                error_metrics = {}
                if not test.empty:
                    error_metrics = self.calculate_error_metrics(test, forecast)

                forecast_future = fitted_model.forecast(steps=30)  # Predicción de los próximos 30 días
                #print (forecast_future)
                recommended_restocking = forecast_future.sum()
            else:
                recommended_restocking = 0
                error_metrics = {"MSE": None, "RMSE": None}

            # Información del producto
            product_info = inventory_data[inventory_data['ID_Producto'] == product_id]
            stock_actual = product_info['Stock_Actual'].values[0]
            recommended_minimum = 10
            frequency = product_sales.sum()

            # Determinar el estado del producto
            if int(recommended_restocking) == 0:
                if stock_actual < recommended_minimum:
                    recommended_restocking = recommended_minimum - stock_actual
                    status = "No prioritario"
                else:
                    status = "Adecuado"
            elif stock_actual < recommended_minimum:
                status = "Urgente"
            elif stock_actual < recommended_minimum + 5:
                status = "Moderada"
            else:
                status = "Adecuado"

            if status == "Adecuado":
                recommended_restocking = 0

            # Almacenar los datos procesados
            restocking_data.append([
                product_info['ID_Producto'].values[0],  # Código del producto
                product_info['Nombre_Producto'].values[0],  # Descripción
                stock_actual,  # Inventario actual
                recommended_minimum,  # Stock mínimo recomendado
                int(recommended_restocking),  # Reposición recomendada
                status,  # Estado
                frequency,  # Frecuencia de ventas
                error_metrics.get("MSE"),  # Métrica MSE
                error_metrics.get("RMSE")  # Métrica RMSE
            ])

        # Crear DataFrame final
        restocking_df = pd.DataFrame(restocking_data, columns=[
            "Código del Equipo",
            "Descripción del Equipo",
            "Inventario Actual",
            "Cantidad Mínima Requerida",
            "Cantidad Recomendada de Reposición",
            "Estado de Reposición",
            "Frecuencia de Uso",
            "MSE",
            "RMSE"
        ])

        # Ordenar por estado y frecuencia
        state_order = {"Urgente": 0, "Moderada": 1, "Adecuado": 2, "No prioritario": 3}
        restocking_df['Estado Orden'] = restocking_df['Estado de Reposición'].map(state_order)
        restocking_df.sort_values(by=["Estado Orden", "Frecuencia de Uso"], ascending=[True, False], inplace=True)
        restocking_df.drop(columns=["Estado Orden", "Frecuencia de Uso"], inplace=True)

        return restocking_df
