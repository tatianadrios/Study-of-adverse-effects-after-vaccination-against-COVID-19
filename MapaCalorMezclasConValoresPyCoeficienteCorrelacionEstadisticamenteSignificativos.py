import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

try:
    # Leer el archivo Excel
    file_path = r'C:\Users\jumbo\Dropbox\PC\Downloads\ValoresPCOVIDAnálisis (2).xlsx'
    df = pd.read_excel(file_path, sheet_name='mezclas')

    # Verificar los primeros datos cargados
    print(df.head())

    # Verificar estructura del DataFrame
    print(df.columns)

    # Asegurarse de que la columna 'Efecto Secundario' exista y esté correctamente configurada
    if 'Efecto Secundario' in df.columns:
        df.set_index('Efecto Secundario', inplace=True)
    else:
        raise ValueError("'Efecto Secundario' no es una columna en el DataFrame.")

    # Identificar las columnas de valores P y coeficientes de correlación
    #vacunas = ['Pfizer', 'Sinovac', 'Janssen', 'AstraZeneca', 'Moderna']
    vacunas = ['SV-SV-MD','MD-MD-PF','JS-PF','PF-PF-SV','PF-PF-AZ','PF-PF-MD-MD']	

    
    
    # Crear DataFrames para valores P y coeficientes de correlación
    df_p_values = df[[f'{vacuna}_ValoresP' for vacuna in vacunas]]
    df_correlations = df[[f'{vacuna}_CoeficienteCorrelación' for vacuna in vacunas]]

    # Reemplazar valores cero por NaN
    df_p_values = df_p_values.applymap(lambda x: np.nan if x == 0 else x)
    df_correlations = df_correlations.applymap(lambda x: np.nan if x == 0 else x)

    # Filtrar solo las filas con valores P menores o iguales a 0.05 (estadísticamente significativos)
    df_significativos_p = df_p_values[df_p_values.le(0.05).any(axis=1)]

    # Para coeficientes de correlación, no se aplica un filtro basado en el valor p
    df_correlations_filtered = df_correlations.loc[df_significativos_p.index]

    # Verificar si hay valores faltantes o no numéricos
    print("Valores faltantes en valores P:\n", df_p_values.isna().sum())
    print("Valores faltantes en coeficientes de correlación:\n", df_correlations.isna().sum())

    # Crear el gráfico de subplots para valores P y coeficientes de correlación
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(18, 10))

    # Mapa de calor para los valores P significativos
    sns.heatmap(df_significativos_p, annot=True, cmap="YlGnBu", cbar=True, ax=axes[0])
    axes[0].set_title('Mapa de Calor de Valores P Significativos (≤ 0.05)')
    axes[0].set_xlabel('Vacunas')
    axes[0].set_ylabel('Efectos Secundarios')

    # Mapa de calor para los coeficientes de correlación correspondientes
    sns.heatmap(df_correlations_filtered, annot=True, cmap="coolwarm", cbar=True, ax=axes[1])
    axes[1].set_title('Mapa de Calor de Coeficientes de Correlación')
    axes[1].set_xlabel('Vacunas')
    axes[1].set_ylabel('Efectos Secundarios')

    # Ajustar el layout
    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"Se produjo un error: {e}")

