import os
import sys
import pandas as pd

# Agregar la ruta de src al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utilities.Normalizar import unificar_y_normalizar_archivos

def get_next_file_number(directory, prefix, extension):
    existing_files = [f for f in os.listdir(directory) if f.startswith(prefix) and f.endswith(extension)]
    if not existing_files:
        return 1
    numbers = [int(f.split('_')[0]) for f in existing_files]
    return max(numbers) + 1

def procesar_y_normalizar_archivos_banderas_rojas(excel_path, input_data, master_db_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Leer el archivo de Excel
    data = pd.read_excel(excel_path, header=None)

    archivos_a_normalizar = []

    log_entries = []  # Para almacenar los detalles de los archivos procesados

    for key, value in input_data.items():
        if key.startswith("Banderas Rojas -") and value:
            # Obtener el nombre del input seleccionado
            selected_input = key.replace("Banderas Rojas - ", "").strip()

            # Buscar en la columna A el nombre seleccionado y obtener el nombre del archivo en la columna C
            matching_rows = data[data.iloc[:, 0].str.strip() == selected_input]
            if not matching_rows.empty:
                file_names = matching_rows.iloc[:, 2].dropna().tolist()

                for file_name_prefix in file_names:
                    # Buscar archivos que comiencen con el nombre dado
                    matching_files = [f for f in os.listdir(master_db_path) if f.startswith(file_name_prefix)]
                    if matching_files:
                        for matching_file in matching_files:
                            source_path = os.path.join(master_db_path, matching_file)
                            archivos_a_normalizar.append(source_path)
                            log_entries.append(f"Archivo agregado para normalización: {matching_file}")
                    else:
                        log_entries.append(f"No se encontraron archivos que comiencen con {file_name_prefix} en {master_db_path}")
            else:
                log_entries.append(f"No se encontraron archivos para la entrada seleccionada: {selected_input}")

    # Unificar y normalizar archivos
    if archivos_a_normalizar:
        next_number = get_next_file_number(output_dir, '', 'parquet')
        output_file_path = os.path.join(output_dir, f'{next_number:02d}_BanderasRojas.parquet')
        unificar_y_normalizar_archivos(archivos_a_normalizar, output_dir)
        log_entries.append(f"Archivos normalizados guardados en {output_file_path}")
    else:
        log_entries.append("No se encontraron archivos para normalizar.")

    # Guardar log con numeración
    next_log_number = get_next_file_number(output_dir, '', 'txt')
    log_path = os.path.join(output_dir, f'{next_log_number:02d}_BanderasRojas_log.txt')
    with open(log_path, 'w') as log_file:
        for entry in log_entries:
            log_file.write(entry + '\n')

    print(f"Log de archivos guardado en {log_path}")

if __name__ == "__main__":
    if len(sys.argv) >= 4:
        project_dir = sys.argv[1]
        input_data = eval(sys.argv[2])
        excel_path = sys.argv[3]
        
        master_db_path = os.path.join(os.path.dirname(__file__), '../../resources/Master/BR')
        output_dir = os.path.join(project_dir, 'DataSet', 'Entrenamiento')
        
        procesar_y_normalizar_archivos_banderas_rojas(excel_path, input_data, master_db_path, output_dir)
    else:
        print("Uso: etapa7.py <project_dir> <input_data_dict> <excel_path>")
