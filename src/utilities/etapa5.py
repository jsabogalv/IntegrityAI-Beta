import os
import sys
import subprocess
import pandas as pd

# Agregar la ruta de src al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from web_utilities.url_evaluator import evaluate_and_download, download_dynamic_url

def get_next_filename(directory, base_name, extension):
    i = 1
    while True:
        filename = os.path.join(directory, f"{str(i).zfill(2)}_{base_name}{extension}")
        if not os.path.exists(filename):
            return filename
        i += 1

def download_url_content(url, output_dir, log_path):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    log_data = []

    if pd.isna(url):
        return

    base_name = "URL"
    file_name = get_next_filename(output_dir, base_name, "")

    ext, full_path, success = evaluate_and_download(url, output_dir, file_name)
    if not success:
        ext, full_path, success = download_dynamic_url(url, output_dir, file_name)

    log_data.append([file_name, ext, success, full_path, url])

    log_df = pd.DataFrame(log_data, columns=['File Name', 'Format', 'Success', 'Full Path', 'URL'])
    log_df.to_csv(log_path, index=False, mode='a', header=not os.path.exists(log_path))

if __name__ == "__main__":
    if len(sys.argv) == 3:
        project_dir = sys.argv[1]
        url = sys.argv[2]
        output_dir = os.path.join(project_dir, 'DataSet', 'temp')
        log_path = os.path.join(output_dir, 'log.txt')

        download_url_content(url, output_dir, log_path)
    else:
        print("Uso: etapa5.py <project_dir> <url>")
