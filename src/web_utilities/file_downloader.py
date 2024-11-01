# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 05:36:11 2024

@author: GJ121KC
"""

import os
import requests

def download_file(url, save_path):
    """
    Descarga un archivo desde una URL y lo guarda en la ruta especificada.
    
    :param url: URL del archivo a descargar
    :param save_path: Ruta donde se guardará el archivo descargado
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Verifica si hay algún error en la solicitud
        
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        print(f"Archivo descargado correctamente: {save_path}")
    except Exception as e:
        print(f"Error al descargar el archivo: {e}")
