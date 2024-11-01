import os
import sys
import pandas as pd

# Agregar la ruta de src al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from web_utilities.url_evaluator import evaluate_and_download, download_dynamic_url

def download_databases():
    excel_path = os.path.join(os.path.dirname(__file__), '../../resources/inputs_opc/DataBase.xlsx')
    save_path = os.path.join(os.path.dirname(__file__), '../../resources/Master/DB')
    log_path = os.path.join(os.path.dirname(__file__), '../../resources/Master/DB/Log.xlsx')

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Leer el archivo de Excel
    data = pd.read_excel(excel_path, header=None)
    
    if data.shape[1] < 6:
        skip_flags = [None] * len(data)  # Crear una lista de Nones si la columna F no existe
    else:
        skip_flags = data.iloc[:, 5].tolist()  # Indicadores de omisión están en la columna F
    
    urls = data.iloc[:, 2].tolist()  # URLs están en la columna C
    file_names = data.iloc[:, 4].tolist()  # Nombres de archivos están en la columna E

    log_data = []

    for url, file_name, skip_flag in zip(urls, file_names, skip_flags):
        if pd.isna(url) or pd.isna(file_name) or skip_flag == 'X':
            continue  # Saltar filas con URL o nombre de archivo nulo, o con flag de omisión

        if url == 'https://projects.worldbank.org/en/projects-operations/procurement/debarred-firms':
            from web_utilities.url1 import download_excel
            download_excel(url)
            ext = '.xlsx'
            full_path = os.path.join(save_path, "M09.xlsx")
            success = True
        else:
            ext, full_path, success = evaluate_and_download(url, save_path, file_name)
            if not success:
                ext, full_path, success = download_dynamic_url(url, save_path, file_name)

        log_data.append([file_name, ext, success, full_path, url])

    log_df = pd.DataFrame(log_data, columns=['File Name', 'Format', 'Success', 'Full Path', 'URL'])
    log_df.to_excel(log_path, index=False)

if __name__ == "__main__":
    download_databases()
