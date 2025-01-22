import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from db.db_operations import DatabaseOperations


class CompareSalesAndPredictions:
    """
    Clase para generar predicciones de niveles de inventario y reposición por fecha utilizando ARIMA.
    """

    def __init__(self):
        """
        Inicializa la clase y establece la conexión a la base de datos.
        """
        self.db_ops = DatabaseOperations()  # Instancia para manejar operaciones de base de datos.

    def fetch_sales_data(self):
        """
        Extrae datos históricos de ventas desde la base de datos.
        :return: DataFrame con los datos de ventas.
        """
        # Obtener datos de ventas desde la base de datos
        return self.db_ops.fetch_sales_data()

    def fetch_inventory_data(self):
        """
        Extrae datos de inventario para concatenar ID y nombre del producto.
        :return: DataFrame con los datos de inventario.
        """
        return self.db_ops.fetch_inventory_data()

    def preprocess_sales_data(self, sales_data):
        """
        Preprocesa los datos de ventas convirtiendo las fechas y estableciendo un índice.
        :param sales_data: DataFrame de ventas.
        :return: DataFrame preprocesado.
        """
        # Convertir 'Fecha_Venta' a formato datetime
        sales_data['Fecha_Venta'] = pd.to_datetime(sales_data['Fecha_Venta'])
        # Establecer 'Fecha_Venta' como índice para facilitar el análisis
        sales_data.set_index('Fecha_Venta', inplace=True)
        return sales_data

    def get_product_options(self):
        """
        Combina los IDs de los productos con sus nombres para mostrarlos en la interfaz.
        :return: Lista de opciones de productos con formato "ID - Nombre".
        """
        inventory_data = self.fetch_inventory_data()
        inventory_data['Producto_Opcion'] = inventory_data['ID_Producto'].astype(str) + " - " + inventory_data['Nombre_Producto']
        return inventory_data[['ID_Producto', 'Producto_Opcion']]

    def predict_by_date(self, product_id, forecast_days=30):
        """
        Predice los niveles de inventario y reposición por fecha para un producto específico.
        :param product_id: ID del producto a analizar.
        :param forecast_days: Número de días a predecir.
        :return: DataFrame con fechas y predicciones.
        """
        # Obtener y preprocesar los datos de ventas
        sales_data = self.fetch_sales_data()
        sales_data = self.preprocess_sales_data(sales_data)

        # Filtrar las ventas del producto y rellenar días sin ventas
        product_sales = sales_data[sales_data['ID_Producto'] == product_id]['Cantidad_Vendida'].resample('D').sum().fillna(0)

        # Retornar un DataFrame vacío si no hay datos para el producto
        if product_sales.empty:
            return pd.DataFrame({'Fecha': [], 'Predicción': []}), product_sales

        # Dividir los datos en entrenamiento (80%) y prueba (20%)
        train_size = int(len(product_sales) * 0.8)
        train = product_sales[:train_size]

        # Ajustar el modelo ARIMA
        model = ARIMA(train, order=(5, 1, 0))  # Modelo ARIMA con parámetros predefinidos
        fitted_model = model.fit()  # Entrenar el modelo con los datos de entrenamiento

        # Realizar predicciones para los próximos 'forecast_days' días
        forecast = fitted_model.forecast(steps=forecast_days)
        forecast_dates = pd.date_range(start=train.index[-1] + pd.Timedelta(days=1), periods=forecast_days)

        # Crear un DataFrame con las fechas y predicciones
        forecast_df = pd.DataFrame({'Fecha': forecast_dates, 'Predicción': forecast.values})

        return forecast_df, product_sales
