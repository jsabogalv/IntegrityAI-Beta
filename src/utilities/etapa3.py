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

def normalizar_archivo(input_file, output_dir, log_path):
    os.makedirs(output_dir, exist_ok=True)  # Asegúrate de que el directorio de salida existe
    output_file = get_next_filename(output_dir, "DataAudit", ".csv")
    normalizar_script = "E:\\IntegrityAI\\src\\utilities\\Normalizar.py"  # Ruta absoluta del script Normalizar.py
    try:
        result = subprocess.run([sys.executable, normalizar_script, input_file, output_dir], capture_output=True, text=True)
        if result.returncode != 0:
            error_message = f"Normalizar.py failed: {result.stderr}"
            log_result(log_path, f"Error al normalizar el archivo {input_file}: {error_message}")
            raise Exception(error_message)
        success_message = f"Archivo normalizado guardado en {output_file}"
        log_result(log_path, success_message)
        return output_file
    except Exception as e:
        error_message = f"Error al normalizar el archivo {input_file}: {str(e)}"
        print(error_message)
        log_result(log_path, error_message)
        return None

def log_result(log_path, message):
    with open(log_path, 'a') as log_file:
        log_file.write(message + '\n')

if __name__ == "__main__":
    if len(sys.argv) == 3:
        project_dir = sys.argv[1]
        input_file = sys.argv[2]
        output_dir = os.path.join(project_dir, 'DataSet', 'Validar')

        log_path = os.path.join(project_dir, 'DataSet', 'Validar', 'log.txt')

        output_file = normalizar_archivo(input_file, output_dir, log_path)
        if output_file:
            print(f"Archivo normalizado guardado en {output_file}")
        else:
            print("Error al normalizar el archivo")
    else:
        print("Uso: etapa3.py <project_dir> <ruta_del_archivo>")
        print("Ejemplo de prueba interna ejecutado.")
