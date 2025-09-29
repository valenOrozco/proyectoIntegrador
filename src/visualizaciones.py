
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from procesamientoDatos import procesar_datos


df = pd.read_csv('../data/datos.csv')
df_procesado = procesar_datos(df)

plt.figure(figsize=(8, 5))
sns.histplot(df_procesado['precio'], bins=30, kde=True)
plt.title('Distribución de precios')
plt.xlabel('Precio')
plt.ylabel('Frecuencia')
plt.show()

plt.figure(figsize=(10, 8))
sns.heatmap(df_procesado.corr(numeric_only=True), annot=True, cmap='coolwarm')
plt.title('Mapa de calor de correlaciones')
plt.show()