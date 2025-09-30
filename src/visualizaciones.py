import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from procesamientoDatos import procesar_datos

import pathlib
BASE_DIR = pathlib.Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATOS_PATH = DATA_DIR / "datos.csv"
df = pd.read_csv(DATOS_PATH)
df_procesado = procesar_datos(df, verbose=False)

plt.figure(figsize=(8, 5))
sns.histplot(df_procesado['edad'], bins=10, kde=True, stat='count')
plt.title('Distribución de edades')
plt.xlabel('Edad')
plt.ylabel('Frecuencia')
plt.tight_layout()
plt.savefig(DATA_DIR / "histograma_edad.png")
plt.close()


for pregunta in ['malos_pensamientos', 'problemas_ambiente', 'comida_regular']:
    plt.figure(figsize=(8, 5))
    for valor in df_procesado[pregunta].unique():
        subset = df_procesado[df_procesado[pregunta] == valor]
        sns.histplot(subset['edad'], bins=10, kde=True, label=f"{pregunta}={valor}", alpha=0.5, stat='count')
    plt.title(f'Histograma de edad según respuesta a {pregunta}')
    plt.xlabel('Edad')
    plt.ylabel('Frecuencia')
    plt.legend()
    plt.tight_layout()
    plt.savefig(DATA_DIR / f"histograma_edad_{pregunta}.png")
    plt.close()

for pregunta in ['ansiedad_estrés', 'estado_animo']:
    plt.figure(figsize=(8, 5))
    sns.histplot(df_procesado[pregunta], bins=10, kde=True, stat='count')
    plt.title(f'Histograma de {pregunta}')
    plt.xlabel(pregunta)
    plt.ylabel('Frecuencia')
    plt.tight_layout()
    plt.savefig(DATA_DIR / f"histograma_{pregunta}.png")
    plt.close()

print("Visualizaciones listas. Ya puedes ver las estadísticas de tus pacientes")