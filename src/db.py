
import sqlite3
import pandas as pd
import json

conn = sqlite3.connect('../data/aurora.db')


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

with open('../data/usuarios.json', encoding='utf-8') as f:
    usuarias = json.load(f)
for u in usuarias:
    conn.execute('''
    INSERT OR IGNORE INTO usuarias VALUES (?, ?, ?, ?, ?, ?)
    ''', (u['documento'], u['nombre'], u['apellidos'], u['edad'], u['correo'], u['telefono']))

df_encuestas = pd.read_csv('../data/encuestas.csv', names=[
    "documento", "fecha",
    "malos_pensamientos", "problemas_ambiente", "comida_regular",
    "ansiedad_estrés", "estado_animo"
])
for _, row in df_encuestas.iterrows():
    conn.execute('''
    INSERT INTO encuestas VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', tuple(row))

conn.commit()

df = pd.read_sql_query('''
SELECT e.*, u.nombre, u.apellidos, u.edad, u.correo, u.telefono
FROM encuestas e
LEFT JOIN usuarias u ON e.documento = u.documento
''', conn)

conn.close()


from procesamientoDatos import procesar_datos
df_procesado = procesar_datos(df)
df_procesado.to_csv('../data/datos.csv', index=False)