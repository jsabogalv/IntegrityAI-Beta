# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 02:54:13 2024

@author: GJ121KC
"""

import os
import sys
import subprocess

def get_next_filename(directory, base_name, extension):
    i = 1
    while True:
        filename = os.path.join(directory, f"{str(i).zfill(2)}_{base_name}{extension}")
        if not os.path.exists(filename):
            return filename
        i += 1

def normalizar_archivos_en_carpeta(input_folder, output_dir, log_path):
    os.makedirs(output_dir, exist_ok=True)  # Asegúrate de que el directorio de salida existe
    normalizar_script = os.path.join(os.path.dirname(__file__), "Normalizar.py")  # Ruta del script Normalizar.py

    input_paths = []
    for root, _, files in os.walk(input_folder):
        if root == input_folder:  # Evita subcarpetas
            for file in files:
                input_paths.append(os.path.join(root, file))

    try:
        result = subprocess.run([sys.executable, normalizar_script, *input_paths, output_dir], capture_output=True, text=True)
        if result.returncode != 0:
            error_message = f"Normalizar.py failed: {result.stderr}"
            log_result(log_path, f"Error al normalizar los archivos en {input_folder}: {error_message}")
            raise Exception(error_message)
        success_message = f"Archivos normalizados guardados en {output_dir}"
        log_result(log_path, success_message)
    except Exception as e:
        error_message = f"Error al normalizar los archivos en {input_folder}: {str(e)}"
        print(error_message)
        log_result(log_path, error_message)

def log_result(log_path, message):
    with open(log_path, 'a') as log_file:
        log_file.write(message + '\n')

if __name__ == "__main__":
    if len(sys.argv) == 2:
        project_dir = sys.argv[1]
        input_folder = os.path.join(project_dir, 'DataSet', 'temp')
        output_dir = os.path.join(project_dir, 'DataSet', 'Validar')

        log_path = get_next_filename(output_dir, "LOG", ".txt")

        normalizar_archivos_en_carpeta(input_folder, output_dir, log_path)
    else:
        print("Uso: etapa9.py <project_dir>")