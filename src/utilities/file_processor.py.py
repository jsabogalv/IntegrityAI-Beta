# E:/IntegrityAI/src/utilities/file_processor.py
import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from docx import Document
from PIL import Image
import io
import json
from tkinter import Tk
from tkinter.filedialog import askdirectory

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def read_excel_file(file_path):
    df = pd.read_excel(file_path)
    return df.to_csv(index=False)

def read_word_file(file_path):
    doc = Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs])

def read_image_file(file_path):
    with open(file_path, 'rb') as file:
        img = Image.open(file)
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format=img.format)
        return img_byte_arr.getvalue()

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.dumps(json.load(file))

def read_files_to_arrow(file_paths):
    data = []
    for file_path in file_paths:
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ['.txt', '.csv']:
            content = read_text_file(file_path)
        elif ext in ['.xls', '.xlsx']:
            content = read_excel_file(file_path)
        elif ext in ['.doc', '.docx']:
            content = read_word_file(file_path)
        elif ext in ['.jpg', '.jpeg', '.png']:
            content = read_image_file(file_path)
        elif ext == '.json':
            content = read_json_file(file_path)
        else:
            continue
        
        data.append((file_path, content))
    
    table = pa.table(data, names=['file_path', 'content'])
    return table

def save_arrow_file(table, save_path):
    pq.write_table(table, save_path)

def create_log_file(log_data, log_path):
    log_df = pd.DataFrame(log_data, columns=["File Path", "Size (bytes)", "Status"])
    log_df.to_csv(log_path, index=False)

def normalize_data(input_directory, output_directory):
    # Recorrer la carpeta de entrada para obtener todos los archivos
    file_paths = []
    for root, _, files in os.walk(input_directory):
        for file in files:
            file_paths.append(os.path.join(root, file))

    log_data = []

    # Leer los archivos y convertirlos a formato Arrow
    data = []
    for file_path in file_paths:
        try:
            ext = os.path.splitext(file_path)[1].lower()
            size = os.path.getsize(file_path)
            if ext in ['.txt', '.csv']:
                content = read_text_file(file_path)
            elif ext in ['.xls', '.xlsx']:
                content = read_excel_file(file_path)
            elif ext in ['.doc', '.docx']:
                content = read_word_file(file_path)
            elif ext in ['.jpg', '.jpeg', '.png']:
                content = read_image_file(file_path)
            elif ext == '.json':
                content = read_json_file(file_path)
            elif ext == '.zip':
                # Descomprimir y procesar archivos dentro del zip
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(input_directory)
                    zip_file_paths = [os.path.join(input_directory, file) for file in zip_ref.namelist()]
                    zip_data = read_files_to_arrow(zip_file_paths)
                    data.extend(zip_data)
                    continue
            else:
                log_data.append((file_path, size, "Failed: Unsupported file format"))
                continue

            data.append((file_path, content))
            log_data.append((file_path, size, "Success"))

        except Exception as e:
            log_data.append((file_path, size, f"Failed: {str(e)}"))

    table = pa.table(data, names=['file_path', 'content'])

    # Crear el archivo Parquet
    save_arrow_file(table, output_directory)

    # Crear el archivo de log
    log_file_path = os.path.join(output_directory, 'log.csv')
    create_log_file(log_data, log_file_path)

    return output_directory, log_file_path
