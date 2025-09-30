import sqlite3
import pandas as pd
import json
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "aurora.db"
USUARIAS_PATH = DATA_DIR / "usuarios.json"
ENCUESTAS_PATH = DATA_DIR / "encuestas.csv"
DATOS_PATH = DATA_DIR / "datos.csv"

for ruta, nombre in zip([USUARIAS_PATH, ENCUESTAS_PATH], ["usuarios.json", "encuestas.csv"]):
    if not ruta.exists():
        print(f"Error: El archivo {nombre} no existe en la carpeta data.")
        sys.exit(1)

try:
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
    CREATE TABLE IF NOT EXISTS usuarias (
        documento TEXT PRIMARY KEY,
        nombre TEXT,
        apellidos TEXT,
        edad INTEGER,
        correo TEXT,
        telefono TEXT
    )
    ''')
    conn.execute('''
    CREATE TABLE IF NOT EXISTS encuestas (
        documento TEXT,
        fecha TEXT,
        malos_pensamientos TEXT,
        problemas_ambiente TEXT,
        comida_regular TEXT,
        ansiedad_estrés INTEGER,
        estado_animo INTEGER,
        FOREIGN KEY(documento) REFERENCES usuarias(documento)
    )
    ''')
except Exception as e:
    print(f"Error al inicializar la base de datos: {e}")
    sys.exit(1)

try:
    with open(USUARIAS_PATH, encoding='utf-8') as f:
        usuarias = json.load(f)
    for u in usuarias:
        for clave in ["documento", "nombre", "apellidos", "edad", "correo", "telefono"]:
            if clave not in u:
                print(f"ERROR: Falta la clave '{clave}' en un usuario: {u}")
                sys.exit(1)
        conn.execute('''
        INSERT OR IGNORE INTO usuarias VALUES (?, ?, ?, ?, ?, ?)
        ''', (u['documento'], u['nombre'], u['apellidos'], u['edad'], u['correo'], u['telefono']))
except Exception as e:
    print(f"ERROR al cargar usuarios: {e}")
    sys.exit(1)

try:
    df_encuestas = pd.read_csv(ENCUESTAS_PATH)
    columnas_requeridas = [
        "documento", "fecha",
        "malos_pensamientos", "problemas_ambiente", "comida_regular",
        "ansiedad_estrés", "estado_animo"
    ]
    for col in columnas_requeridas:
        if col not in df_encuestas.columns:
            print(f"Falta la columna '{col}' en encuestas.csv")
            sys.exit(1)
    for _, row in df_encuestas.iterrows():
        conn.execute('''
        INSERT INTO encuestas VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', tuple(row[col] for col in columnas_requeridas))
except Exception as e:
    print(f"Error al cargar encuestas: {e}")
    sys.exit(1)

conn.commit()

# Consulta y exportación
try:
    query = '''
    SELECT e.*, u.nombre, u.apellidos, u.edad, u.correo, u.telefono
    FROM encuestas e
    LEFT JOIN usuarias u ON e.documento = u.documento
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    print("\n--- Datos para análisis ---")
    print(df.head(10))
    print(f"Total de registros combinados: {len(df)}")
    print("\n--- Estadísticas ---\n")
    print(df.describe(include='all'))
    print("\n--- Correlaciones ---\n")
    print(df.corr(numeric_only=True))
except Exception as e:
    print(f"ERROR{e}")
    sys.exit(1)

try:
    def safe_import_procesar_datos():
        import importlib.util
        mod_path = BASE_DIR / "src" / "procesamientoDatos.py"
        spec = importlib.util.spec_from_file_location("procesamientoDatos", mod_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.procesar_datos

    procesar_datos = safe_import_procesar_datos()
    df_procesado = procesar_datos(df)
    df_procesado.to_csv(DATOS_PATH, index=False)
    print(f"Exportación exitosa: {DATOS_PATH}")
except Exception as e:
    print(f"ERROR al procesar y exportar datos: {e}")
    sys.exit(1)