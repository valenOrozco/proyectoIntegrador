import pandas as pd
from src.procesamientoDatos import procesar_datos

def test_carga():

    df_encuestas = pd.read_csv('data/encuestas.csv', names=[
        "documento", "fecha",
        "malos_pensamientos", "problemas_ambiente", "comida_regular",
        "ansiedad_estrés", "estado_animo"
    ])
    assert not df_encuestas.empty, "El archivo de encuestas está vacío."


    df_usuarias = pd.read_json('data/usuarios.json')
    assert not df_usuarias.empty, "El archivo de usuarias está vacío."


    df_completo = pd.merge(df_encuestas, df_usuarias, on="documento", how="left")
    assert not df_completo.empty, "La unión de datos está vacía."
    print("✔️ Test de carga y unión de datos: OK")
    return df_completo

def test_procesamiento():
    df_completo = test_carga()
    df_procesado = procesar_datos(df_completo)
    assert not df_procesado.empty, "El DataFrame procesado está vacío."
    print("✔️ Test de procesamiento de datos: OK")

if __name__ == "__main__":
    test_procesamiento()

