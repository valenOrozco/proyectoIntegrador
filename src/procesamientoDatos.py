import pandas as pd

def procesar_datos(df):
    df = df.drop_duplicates()
    df = df.dropna()
    if 'fecha' in df.columns:
        df['fecha'] = pd.to_datetime(df['fecha'])
        df['año'] = df['fecha'].dt.year
    print("Estadísticas descriptivas:")
    print(df.describe())
    print("\nCorrelaciones:")
    print(df.corr(numeric_only=True))
    return df


df_encuestas = pd.read_csv('../data/encuestas.csv', names=[
    "documento", "fecha",
    "malos_pensamientos", "problemas_ambiente", "comida_regular",
    "ansiedad_estrés", "estado_animo"
])

df_usuarias = pd.read_json('../data/usuarios.json')


df_completo = pd.merge(df_encuestas, df_usuarias, on="documento", how="left")


df_procesado = procesar_datos(df_completo)


df_procesado.to_csv('../data/datos.csv', index=False)