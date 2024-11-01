import requests
import os
import json
import re

def generar_variantes_documento(documento):
    # Normalizar el documento eliminando puntos y comas
    documento_normalizado = re.sub(r'[.,]', '', documento)

    # Generar variantes con puntos y comas
    documento_con_puntos = "{:,.0f}".format(int(documento_normalizado)).replace(",", ".")
    documento_con_comas = "{:,}".format(int(documento_normalizado))

    return documento_normalizado, documento_con_puntos, documento_con_comas

def construir_clausula_where(documento_proveedor=None, departamento=None, desde=None, hasta=None):
    where_clauses = []

    if documento_proveedor:
        # Generar variantes del documento
        doc_normalizado, doc_con_puntos, doc_con_comas = generar_variantes_documento(documento_proveedor)
        
        # Crear una cláusula WHERE para cada variante
        documento_clauses = [
            f"documento_proveedor='{doc_normalizado}'",
            f"documento_proveedor='{doc_con_puntos}'",
            f"documento_proveedor='{doc_con_comas}'"
        ]
        where_clauses.append(f"({' OR '.join(documento_clauses)})")
    
    if departamento:
        where_clauses.append(f"departamento='{departamento}'")
    
    if desde and hasta:
        where_clauses.append(f"fecha_de_inicio_del_contrato between '{desde}' and '{hasta}'")
    
    return " AND ".join(where_clauses) if where_clauses else None

def descargar_secop(output_path, documento_proveedor=None, departamento=None, desde=None, hasta=None):
    # URL del recurso de Socrata (SECOP II)
    url = "https://www.datos.gov.co/resource/jbjy-vk9h.json"

    # Parámetros iniciales para la consulta
    params = {
        "$limit": 10000,  # Número máximo de registros por solicitud
        "$offset": 0      # Inicializar el desplazamiento
    }

    # Construir el filtro de consulta
    where_clause = construir_clausula_where(documento_proveedor, departamento, desde, hasta)
    if where_clause:
        params["$where"] = where_clause

    # Crear el directorio si no existe
    os.makedirs(output_path, exist_ok=True)

    file_count = 1
    all_data = []

    while True:
        try:
            # Realizar la solicitud GET a la API de Socrata
            response = requests.get(url, params=params)
            response.raise_for_status()  # Levanta una excepción si la respuesta tiene un código de error

            data = response.json()
            
            if not data:
                # Si no hay más datos, salir del bucle
                break
            
            # Agregar los datos a la lista completa
            all_data.extend(data)
            
            # Incrementar el offset para la siguiente iteración
            params["$offset"] += params["$limit"]
            
        except requests.exceptions.RequestException as e:
            print(f"Error al realizar la solicitud: {e}")
            break
    
    # Guardar todos los datos en un solo archivo JSON
    if all_data:
        output_file_path = os.path.join(output_path, f"SECOP.json")
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)
        print(f"Datos guardados en: {output_file_path}")
    else:
        print("No se encontraron datos que coincidan con los filtros proporcionados.")
