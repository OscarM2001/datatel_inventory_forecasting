import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from db.db_operations import DatabaseOperations
from models.compare_sales_and_predictions import CompareSalesAndPredictions


class PredictRestockingByProduct:
    """
    Clase para predecir la cantidad de reposición por producto y generar un gráfico de barras.
    """

    def __init__(self):
        """
        Inicializa la clase y establece la conexión a la base de datos.
        """
        self.db_ops = DatabaseOperations()
        self.prediction_by_date = CompareSalesAndPredictions()

    def fetch_inventory_data(self):
        """
        Extrae datos de inventario desde la base de datos.
        :return: DataFrame con los datos de inventario.
        """
        return self.db_ops.fetch_inventory_data()

    def fetch_sales_data(self):
        """
        Extrae datos de ventas desde la base de datos.
        :return: DataFrame con los datos de ventas.
        """
        return self.db_ops.fetch_sales_data()

    def predict_restocking_by_product(self, forecast_days=30):
        inventory_data = self.fetch_inventory_data()
        sales_data = self.fetch_sales_data()
        sales_data = self.prediction_by_date.preprocess_sales_data(sales_data)

        restocking_data = []
        for product_id in inventory_data['ID_Producto'].unique():
            forecast_df, _ = self.prediction_by_date.predict_by_date(product_id, forecast_days)
            total_restocking = forecast_df['Predicción'].sum()

            product_name = inventory_data[inventory_data['ID_Producto'] == product_id]['Nombre_Producto'].values[0]
            restocking_data.append({
                'ID_Producto': product_id,
                'Producto': product_name,
                'Cantidad': total_restocking
            })

        return pd.DataFrame(restocking_data)
