from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base   
import json
import urllib.parse
import os

Base = declarative_base()

def get_db_connection():
    """
    Establece y retorna un motor de conexión a la base de datos SQL Server usando SQLAlchemy con autenticación de Windows.
    La configuración se obtiene desde un archivo JSON.
    """
    try:
        # Verificar si el archivo de configuración existe
        config_path = os.path.join("data", "database_config.json")
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"El archivo de configuración '{config_path}' no se encuentra.")

        # Cargar configuración desde el archivo JSON
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)

        # Validar claves necesarias
        required_keys = ['server', 'database', 'driver']
        for key in required_keys:
            if key not in config:
                raise KeyError(f"Falta la clave requerida '{key}' en el archivo de configuración.")

        # Crear una cadena de conexión para autenticación de Windows
        connection_string = (
            f"mssql+pyodbc://@"
            f"{config['server']}/{config['database']}?driver={urllib.parse.quote(config['driver'])}&Trusted_Connection=yes"
        )

        # Crear motor SQLAlchemy
        engine = create_engine(connection_string, fast_executemany=True)
        print("Conexión exitosa a la base de datos.")
        return engine
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        raise


# Dependencia para usar en FastAPI
def get_db_session():
    """
    Retorna una sesión de base de datos usando SQLAlchemy.
    """
    engine = get_db_connection()
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return Session()


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
