# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 07:58:35 2024

@author: GJ121KC
"""

# E:\IntegrityAI\src\utilities\data_utils.py

import pandas as pd

def cargar_datos(ruta_archivo):
    """Carga un archivo CSV y retorna un DataFrame de pandas."""
    return pd.read_csv(ruta_archivo)

def guardar_datos(df, ruta_archivo):
    """Guarda un DataFrame de pandas en un archivo CSV."""
    df.to_csv(ruta_archivo, index=False)
