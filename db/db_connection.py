from sqlalchemy import create_engine
import json
import urllib.parse


def get_db_connection():
    """
    Establece y retorna un motor de conexión a la base de datos SQL Server usando SQLAlchemy con autenticación de Windows.
    La configuración se obtiene desde el archivo JSON.
    """
    try:
        # Cargar configuración desde el archivo JSON
        with open('data/database_config.json', 'r') as config_file:
            config = json.load(config_file)

        # Crear una cadena de conexión para autenticación de Windows
        connection_string = (
            f"mssql+pyodbc://@"
            f"{config['server']}/{config['database']}?"
            f"driver={urllib.parse.quote(config['driver'])}&Trusted_Connection=yes"
        )

        # Crear motor SQLAlchemy
        engine = create_engine(connection_string, fast_executemany=True)  # Optimiza para lotes grandes
        print("Conexión exitosa a la base de datos.")
        return engine
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        raise

# Prueba la conexión
if __name__ == "__main__":
    try:
        engine = get_db_connection()
        connection = engine.connect()
        print("Conexión establecida con éxito.")
        connection.close()
        print("Conexión cerrada correctamente.")
    except Exception as ex:
        print(f"Error general: {ex}")
