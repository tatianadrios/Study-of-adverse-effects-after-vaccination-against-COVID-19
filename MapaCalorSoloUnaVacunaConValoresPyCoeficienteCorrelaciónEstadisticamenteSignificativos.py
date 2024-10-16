import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

try:
    # Leer el archivo Excel
    file_path = r'C:\Users\limav\OneDrive\Documentos\ValoresPCOVIDAnálisis.xlsx'
    df = pd.read_excel(file_path, sheet_name='SCCP')

    # Verificar los nombres de las columnas
    print("Nombres de las columnas:", df.columns)

    # Verificar los primeros datos cargados
    print(df.head())

    # Filtrar solo las filas donde 'Efecto Secundario' no es NaN
    df_filtered = df.dropna(subset=['Efecto Secundario'])

    # Asegurarse de que no hay espacios en los nombres de las columnas
    df.columns = df.columns.str.strip()

    # Verificar nuevamente los nombres de las columnas después de eliminar espacios
    print("Nombres de las columnas después de strip:", df.columns)

    # Filtrar solo las filas con valores P menores o iguales a 0.05 (estadísticamente significativos)
    df_significativos = df_filtered[df_filtered['Pfizer_ValoresP'] <= 0.05]

    # Crear DataFrames separados para valores P y coeficientes de correlación
    df_vacuna_p = df_significativos[['Efecto Secundario', 'Pfizer_ValoresP']].set_index('Efecto Secundario')
    df_vacuna_corr = df_significativos[['Efecto Secundario', 'Pfizer_CoeficienteCorrelación']].set_index('Efecto Secundario')

    # Reemplazar valores cero por NaN en el DataFrame de valores P
    df_vacuna_p = df_vacuna_p.applymap(lambda x: np.nan if x == 0 else x)

    # Crear el gráfico de subplots
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 10))

    # Mapa de calor para los valores P
    sns.heatmap(df_vacuna_p, annot=True, cmap="YlGnBu", cbar=True, ax=axes[0], linewidths=0.5)
    axes[0].set_title('Valores P significativos para Pfizer (≤ 0.05)')
    axes[0].set_xlabel('Vacuna')
    axes[0].set_ylabel('Efectos Secundarios')

    # Mapa de calor para los coeficientes de correlación
    sns.heatmap(df_vacuna_corr, annot=True, cmap="coolwarm", cbar=True, ax=axes[1], linewidths=0.5)
    axes[1].set_title('Coeficientes de Correlación para Pfizer')
    axes[1].set_xlabel('Vacuna')
    axes[1].set_ylabel('Efectos Secundarios')

    # Ajustar el layout
    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"Se produjo un error: {e}")
