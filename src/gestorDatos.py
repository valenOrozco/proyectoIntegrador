import pandas as pd
import mysql.connector
from mysql.connector import Error

sql_file_path = './ejercicioclase.sql'
conn = None
df = pd.DataFrame()

try:
    with open(sql_file_path, 'r', encoding='latin-1') as f:
        sql_query = f.read()
except FileNotFoundError:
    print(f"Error: No se encontró el archivo en la ruta: {sql_file_path}")
    sql_query = None

if sql_query:
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="",
            database="TiendaElectronicos"
        )
        df = pd.read_sql(sql_query, conn)
        print("¡Consulta ejecutada exitosamente! Muestra:")
        print(df.head())
    except Error as e:
        print(f"Error al conectar o ejecutar la consulta: {e}")
    finally:
        if conn is not None and conn.is_connected():
            conn.close()
            print("\nConexión a la base de datos cerrada.")