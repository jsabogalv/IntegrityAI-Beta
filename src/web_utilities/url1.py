"""
Created on Fri Aug  2 12:39:37 2024

@author: GJ121KC
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def download_excel(url):
   
    save_path='E:\\IntegrityAI\\resources\\Master\\DB'
    file_name='M09'
   
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": save_path}
    options.add_experimental_option("prefs", prefs)
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)

    try:
        # Espera explícita para asegurar que el botón de descarga esté disponible
        wait = WebDriverWait(driver, 20)
        excel_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@title="Excel"]')))
        excel_button.click()
        time.sleep(10)  # Esperar a que se complete la descarga

        # Verificar si el archivo ha sido descargado y renombrarlo
        files = os.listdir(save_path)
        for file in files:
            if file.endswith('.xlsx'):
                os.rename(os.path.join(save_path, file), os.path.join(save_path, f"{file_name}.xlsx"))
                print(f"Archivo descargado y guardado como {file_name}.xlsx")
                break
        else:
            print("No se encontró el archivo descargado.")
    except Exception as e:
        print(f"Error al intentar descargar el archivo: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    url = 'https://projects.worldbank.org/en/projects-operations/procurement/debarred-firms'
    download_excel(url)
 