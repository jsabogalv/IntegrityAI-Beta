import os
import sys
import pandas as pd

# Agregar la ruta de src al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from web_utilities.url_evaluator import evaluate_and_download, download_dynamic_url

def download_bandera_rojas():
    excel_path = os.path.join(os.path.dirname(__file__), '../../resources/inputs_opc/Banderas Rojas.xlsx')
    save_path = 'E:/IntegrityAI/resources/Master/BR'
    log_path = os.path.join(save_path, 'Log.xlsx')

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Eliminar archivos previos en la carpeta de destino
    for file in os.listdir(save_path):
        os.remove(os.path.join(save_path, file))

    # Leer el archivo de Excel sin encabezados
    data = pd.read_excel(excel_path, sheet_name='Sheet1', header=None)

    # Verificar si las columnas B y C existen
    if data.shape[1] < 3:
        print("El archivo de Excel no tiene suficientes columnas. Se requieren al menos columnas B y C.")
        return

    urls = data.iloc[:, 1].dropna().tolist()  # URLs están en la columna B (índice 1)
    file_names = data.iloc[:, 2].dropna().tolist()  # Nombres de archivos están en la columna C (índice 2)

    log_data = []

    for url, file_name in zip(urls, file_names):
        ext, full_path, success = evaluate_and_download(url, save_path, file_name)
        if not success:
            ext, full_path, success = download_dynamic_url(url, save_path, file_name)

        log_data.append([file_name, ext, success, full_path, url])

    log_df = pd.DataFrame(log_data, columns=['File Name', 'Format', 'Success', 'Full Path', 'URL'])
    log_df.to_excel(log_path, index=False)

if __name__ == "__main__":
    download_bandera_rojas()
