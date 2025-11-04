# models/database.py
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Carga las variables del archivo .env al entorno de la aplicación
load_dotenv()

def crear_conexion():
    """
    Crea una conexión a la base de datos MySQL usando variables de entorno.
    """
    try:
        conexion = mysql.connector.connect(
            # Lee las variables del entorno (cargadas desde .env)
            host=os.environ.get('DB_HOST'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASS'),
            database=os.environ.get('DB_NAME')
        )

        if conexion.is_connected():
            return conexion

    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None