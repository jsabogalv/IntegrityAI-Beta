import os
import sys
import json
import requests

# Clave de API de Google Custom Search
API_KEY = 'TU CLAVE AQUI'
CX = 'TU CLAVE AQUI''

# Términos de búsqueda
SEARCH_TERMS = [
    "malversación", "fraude", "gobernar", "escándalo", "demanda", "corrupción", 
    "esquema", "soborno", "bancarrota", "ilegal", "sanción", "lavado de dinero",
    "Investigación", "crimen", "detención", "terror", "contrabando", "evasión",
    "violación", "embezzle", "fraud", "govern", "scandal", "lawsuit",
    "corrupt", "scheme", "brib", "bankrupt", "illegal", "sanction",
    "money launder", "investigat", "crim", "arrest", "terror", "smuggl",
    "evasion", "violat"
]

def search_news(target_name, base_path):
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    
    for term in SEARCH_TERMS:
        query = f"{target_name} {term}"
        response = requests.get(
            'https://www.googleapis.com/customsearch/v1',
            params={
                'key': API_KEY,
                'cx': CX,
                'q': query,
                'num': 1  # Cambiar a 1 para reducir el número de resultados
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            sanitized_query = query.replace(' ', '_')
            result_path = os.path.join(base_path, f"{sanitized_query}_results.json")

            with open(result_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            print(f"Resultados para '{query}' guardados en {result_path}")
        else:
            print(f"Error en la búsqueda para '{query}': {response.status_code} - {response.json()}")

if __name__ == "__main__":
    # Ejemplo de ejecución dentro del mismo archivo para fines de prueba
    target_name = "Alvaro Uribe"  # Cambia esto al nombre real que quieras buscar
    save_path = "C:/Users/GJ121KC/Pictures/temporal"  # Cambia esto a la ruta real donde quieres guardar los resultados
    
    search_news(target_name, save_path)
    
    # Código para ejecución desde la línea de comandos
    if len(sys.argv) == 3:
        target_name = sys.argv[1]
        save_path = sys.argv[2]
        search_news(target_name, save_path)
    else:
        print("Uso: etapa2.py <target_name> <save_path>")
        print("Ejemplo de prueba interna ejecutado.")
