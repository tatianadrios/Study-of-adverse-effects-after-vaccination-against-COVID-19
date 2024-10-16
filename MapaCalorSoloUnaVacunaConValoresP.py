import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

try:
    # Leer el archivo Excel
    file_path = r'C:\Users\limav\OneDrive\Documentos\ValoresPCOVIDAnálisis.xlsx'
    df_p_values = pd.read_excel(file_path, sheet_name='SCCP')

    # Verificar los primeros datos cargados
    print(df_p_values.head())

    # Verificar estructura del DataFrame
    print(df_p_values.columns)

    # Asegurarse de que la columna 'Efecto Secundario' exista y esté correctamente configurada
    if 'Efecto Secundario' in df_p_values.columns:
        df_p_values.set_index('Efecto Secundario', inplace=True)
    else:
        raise ValueError("'Efecto Secundario' no es una columna en el DataFrame.")

    # Reemplazar valores cero por NaN
    df_p_values = df_p_values.applymap(lambda x: np.nan if x == 0 else x)

    # Filtrar solo la columna de la vacuna que quieres analizar
    vacuna_especifica = 'Pfizer'  
    df_vacuna = df_p_values[[vacuna_especifica]]

    # Verificar si hay valores faltantes o no numéricos
    print(df_vacuna.dtypes)
    print("Valores faltantes:\n", df_vacuna.isna().sum())

    # Crear el mapa de calor para la vacuna específica
    plt.figure(figsize=(6, 10))
    sns.heatmap(df_vacuna, annot=True, cmap="YlGnBu", cbar=True)

    # Agregar títulos y etiquetas
    plt.title(f'Mapa de Calor de Valores P para {vacuna_especifica}')
    plt.xlabel('Vacuna')
    plt.ylabel('Efectos Secundarios')
    plt.show()

except Exception as e:
    print(f"Se produjo un error: {e}")

