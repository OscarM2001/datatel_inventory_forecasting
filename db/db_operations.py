import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from db.db_connection import get_db_connection

class DatabaseOperations:
    def __init__(self):
        """
        Inicializa el motor de conexión a la base de datos.
        """
        try:
            self.engine = get_db_connection()  # Motor SQLAlchemy
        except Exception as e:
            raise Exception(f"Error al configurar el motor de conexión: {e}")

    def execute_query(self, query):
        """
        Ejecuta una consulta SQL y devuelve los resultados como un DataFrame.
        :param query: Consulta SQL a ejecutar.
        :return: DataFrame con los resultados de la consulta.
        """
        try:
            return pd.read_sql(query, self.engine)  # Usa directamente el motor
        except Exception as e:
            raise Exception(f"Error al ejecutar la consulta: {e}")

    def fetch_inventory_data(self):
        """
        Extrae datos reales de inventario desde SQL Server.
        """
        query = """
        SELECT 
            ID_Producto, 
            Nombre_Producto, 
            Stock_Actual, 
            Categoria, 
            Precio_Unitario 
        FROM ds_Product_Items
        """
        return self.execute_query(query)

    def fetch_sales_data(self):
        """
        Extrae datos históricos de ventas desde SQL Server.
        """
        query = """
        SELECT Fecha_Venta, ID_Producto, Cantidad_Vendida 
        FROM DATATEL_Ventas_Inventario_Analytical_Dataset
        """
        return self.execute_query(query)
    