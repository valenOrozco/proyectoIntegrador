import pandas as pd
import pathlib

def procesar_datos(df, verbose=True):
    if verbose:
        print("--- LIMPIEZA DE DATOS ---")
        print(f"Registros originales: {len(df)}")
    df = df.drop_duplicates()
    if verbose:
        print(f"Registros tras eliminar duplicados: {len(df)}")
    df = df.dropna()
    if verbose:
        print(f"Registros tras eliminar nulos: {len(df)}")
    if 'fecha' in df.columns:
        df['fecha'] = pd.to_datetime(df['fecha'])
        if verbose:
            print("Columna 'fecha' convertida a datetime.")
    for col in ['malos_pensamientos', 'problemas_ambiente', 'comida_regular']:
        if col in df.columns:
            df[col] = df[col].str.upper()
            if verbose:
                print(f"Columna '{col}' normalizada a mayúsculas.")
    if verbose:
        print("--- TRANSFORMACIÓN DE DATOS ---")
    if 'fecha' in df.columns:
        df['año'] = df['fecha'].dt.year
        if verbose:
            print("Columna 'año' creada a partir de 'fecha'.")
    for col in ['malos_pensamientos', 'problemas_ambiente', 'comida_regular']:
        if col in df.columns:
            df[col + '_num'] = df[col].map({'S': 1, 'N': 0})
            if verbose:
                print(f"Columna '{col}_num' creada (S=1, N=0).")
    if verbose:
        if len(df) == 0:
            print("Advertencia: El DataFrame está vacío después de la limpieza.")
        else:
            print("Datos procesados correctamente.")
    return df

if __name__ == "__main__":
    BASE_DIR = pathlib.Path(__file__).resolve().parents[1]
    DATA_DIR = BASE_DIR / "data"
    ENCUESTAS_PATH = DATA_DIR / "encuestas.csv"
    USUARIAS_PATH = DATA_DIR / "usuarios.json"
    DATOS_PATH = DATA_DIR / "datos.csv"

    df_encuestas = pd.read_csv(ENCUESTAS_PATH, names=[
        "documento", "fecha",
        "malos_pensamientos", "problemas_ambiente", "comida_regular",
        "ansiedad_estrés", "estado_animo"
    ])
    df_usuarias = pd.read_json(USUARIAS_PATH)
    df_completo = pd.merge(df_encuestas, df_usuarias, on="documento", how="left")
    df_procesado = procesar_datos(df_completo, verbose=True)
    df_procesado.to_csv(DATOS_PATH, index=False)
    print(f"Exportación exitosa: {DATOS_PATH}")
