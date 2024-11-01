# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 07:51:13 2024

@author: GJ121KC
"""



import pandas as pd

def procesar_tabla(path):
    """
    Función para procesar un archivo Excel y retornar un DataFrame filtrado.

    :param path: Ruta del archivo Excel a procesar.
    :return: DataFrame filtrado con dos columnas: 'Clave' y 'Valor'.
    """

    # Cargar el archivo Excel
    df = pd.read_excel(path, header=None)

    # Contar cuántas columnas tiene la primera fila
    num_columns = df.iloc[0].count()

    # Tomar las columnas según el número de columnas en la primera fila
    keys = df.iloc[0, :num_columns].values  # Datos de la primera fila
    values = df.iloc[1, :num_columns].values  # Datos de la segunda fila

    # Crear un nuevo DataFrame con dos columnas
    df_final = pd.DataFrame({
        'Clave': keys,
        'Valor': values
    })

    # Convertir todos los valores de la columna 'Valor' a texto para asegurarse de que str.contains funcione correctamente
    df_final['Valor'] = df_final['Valor'].astype(str)

    # Primer filtro: Eliminar filas donde 'Valor' contenga 'FALSE' o esté en blanco
    df_final = df_final[
        (df_final['Valor'].notna()) &
        (df_final['Valor'].str.strip() != '') &
        (~df_final['Valor'].str.contains(r'\bFALSE\b', case=False, na=False))
    ]

    # Segundo filtro: Eliminar filas donde 'Valor' diga 'nan'
    df_final = df_final[df_final['Valor'].str.lower() != 'nan']

    return df_final
