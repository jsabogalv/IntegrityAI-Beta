import os
import sys
import threading
import requests
import pandas as pd
from Normalizar import unificar_y_normalizar_archivos, get_next_file_number

# Mantener la clave de API fija
API_KEY = "Tu CLAVE AQUI"

class TimeoutException(Exception):
    pass

def timeout_handler():
    raise TimeoutException("Query timed out")

def search_organization(api_key, query, timeout=180):
    base_url = "http://api.redflags.eu"
    endpoints = {
        "organization": "/organization",
        "organizations": "/organizations",
        "notice": "/notice",
        "notices": "/notices"
    }

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    result_data = []

    def run_queries():
        try:
            # Consultas a la API
            for endpoint, param_name in [("organizations", "nameLike"),
                                         ("notices", "contractingAuthorityNameLike"),
                                         ("notices", "winnerNameLike"),
                                         ("notices", "textLike")]:
                params = {
                    "count": 10,
                    "page": 1,
                    param_name: query,
                    "access_token": api_key
                }

                response = requests.get(base_url + endpoints[endpoint], params=params, headers=headers)
                response.raise_for_status()
                data = response.json()

                if "result" in data:
                    result_data.extend(data["result"])

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from RedFlags API: {e}")

    thread = threading.Thread(target=run_queries)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        print("Query timed out. Please try again later.")
        thread._stop()
        return None

    return pd.DataFrame(result_data) if result_data else pd.DataFrame()

def execute_api_search(project_dir, nombre_razon_social):
    temp_dir = os.path.join(project_dir, 'DataSet', 'temp', 'API')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    log_dir = temp_dir  # Guardar el log en la misma carpeta de temp
    log_file = os.path.join(log_dir, 'LogAPI.txt')

    try:
        data = search_organization(API_KEY, nombre_razon_social, timeout=180)

        if data.empty:
            raise Exception(f"No se encontraron datos para: {nombre_razon_social}")

        # Nombrar los archivos de salida en la carpeta temporal
        next_number = get_next_file_number(temp_dir, '', 'json')
        temp_save_path = os.path.join(temp_dir, f'{next_number:02d}_DatosLibres.json')
        data.to_json(temp_save_path, orient='records', lines=True)

        # Guardar log
        with open(log_file, 'a') as log:
            log.write(f"Consulta realizada para: {nombre_razon_social}\n")
            log.write(f"Datos guardados temporalmente en: {temp_save_path}\n\n")

        # Normalizar los archivos y moverlos a la carpeta final
        final_save_dir = os.path.join(project_dir, 'DataSet', 'Entrenamiento')
        if not os.path.exists(final_save_dir):
            os.makedirs(final_save_dir)

        unificar_y_normalizar_archivos([temp_save_path], final_save_dir)

    except Exception as e:
        with open(log_file, 'a') as log:
            log.write(f"Error al realizar la consulta para: {nombre_razon_social}\n")
            log.write(f"Error: {str(e)}\n\n")

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        project_dir = sys.argv[1]
        nombre_razon_social = sys.argv[2]
        execute_api_search(project_dir, nombre_razon_social)
    else:
        print("Uso: etapa8.py <directorio_proyecto> <nombre_razon_social>")

# Sección para pruebas manuales (No se ejecuta automáticamente)
# ruta_prueba = "C:/Users/GJ121KC/Music/temporal"
# palabra_busqueda = "ELN"
# print(f"Iniciando prueba con la palabra: {palabra_busqueda}")
# execute_api_search(ruta_prueba, palabra_busqueda)
# print("Prueba completada.")
