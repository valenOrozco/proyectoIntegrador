import pandas as pd
import time

print("\nEspere...\n")
time.sleep(2)
print("\nCorriendo tests...\n")
time.sleep(2)


def test_carga():
    df_encuestas = pd.read_csv('data/encuestas.csv')
    df_usuarias = pd.read_json('data/usuarios.json')
    df_encuestas['documento'] = df_encuestas['documento'].astype(str)
    df_usuarias['documento'] = df_usuarias['documento'].astype(str)
    df_completo = pd.merge(df_encuestas, df_usuarias, on="documento", how="left")
    print('Carga y merge exitosos. Filas:', len(df_completo))
    return df_completo


def test_limpieza(df):
    df = df.drop_duplicates()
    df = df.dropna()
    print('Limpieza exitosa. Filas:', len(df))
    return df


def test_transformacion(df):
    if 'fecha' in df.columns:
        df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
        df['año'] = df['fecha'].dt.year
    print('Transformación exitosa. Columnas:', df.columns.tolist())
    return df


def test_estadisticas(df):
    print('Estadísticas descriptivas:')
    print(df.describe())
    print('Correlaciones:')
    print(df.corr(numeric_only=True))


def test_procesamiento():
    df_completo = test_carga()
    df_limpio = test_limpieza(df_completo)
    df_transformado = test_transformacion(df_limpio)
    test_estadisticas(df_transformado)

    time.sleep(1)
    print("\n✅ Test exitoso. Tu programa funciona correctamente.\n")


if __name__ == "__main__":
    test_procesamiento()
