import os
import shutil
import pandas as pd

def generate_project(project_name, tipo_proyecto, identificacion_tercero, info_validar, enfoque_forense, datos_libres, banderas_rojas, tipo_proyecto_options, identificacion_tercero_options, datos_libres_options, banderas_rojas_options, search_web, nombre, cc_nit):
    template_path = "E:/IntegrityAI/template/NewProyect"
    new_project_path = f"E:/IntegrityAI/projects/{project_name}"

    if os.path.exists(new_project_path):
        return "El proyecto ya existe"

    try:
        # Copiar el template a la nueva ubicación
        shutil.copytree(template_path, new_project_path)

        # Crear el archivo Excel inputs.xlsx con la información del proyecto
        inputs_file_path = os.path.join(new_project_path, "inputs.xlsx")
        
        # Crear un diccionario con todas las opciones
        data = {
            "Nombre del Proyecto": project_name,
            "Tipo de Proyecto Forensic": "true" if tipo_proyecto == "Forensic" else "false",
            "Tipo de Proyecto SECOPII": "true" if tipo_proyecto == "SECOPII" else "false",
            "Identificación del Tercero Natural": "true" if identificacion_tercero == "Natural" else "false",
            "Identificación del Tercero Jurídica": "true" if identificacion_tercero == "Jurídica" else "false",
            "Identificación del Tercero General": "true" if identificacion_tercero == "General" else "false",
            "Nombre": nombre,
            "CC/NIT": cc_nit,
            "Búsqueda WEB": "true" if search_web else "false",
            "Información a Validar": info_validar,
            "Enfoque Forense": enfoque_forense,
        }

        # Agregar datos libres y banderas rojas al diccionario
        for option in datos_libres_options:
            data[f"Datos Libres {option}"] = "true" if option in datos_libres else "false"
        
        for option in banderas_rojas_options:
            data[f"Banderas Rojas {option}"] = "true" if option in banderas_rojas else "false"

        # Convertir el diccionario en un DataFrame de pandas
        df = pd.DataFrame([data])

        # Guardar el DataFrame en un archivo Excel
        df.to_excel(inputs_file_path, index=False)

        return "El proyecto ha sido creado"
    except Exception as e:
        return f"Error al generar el proyecto: {e}"
