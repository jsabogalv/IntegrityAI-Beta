import os
import requests
import mimetypes
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def evaluate_and_download(url, save_path, file_name):
    """
    Evaluates the type of URL and downloads the content accordingly.
    """
    try:
        response = requests.get(url, stream=True)
        content_type = response.headers.get('content-type')

        if 'application/pdf' in content_type:
            ext = '.pdf'
        elif 'text/html' in content_type:
            ext = '.html'
        elif 'application/json' in content_type:
            ext = '.json'
        elif 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' in content_type:
            ext = '.xlsx'
        elif 'application/xml' in content_type:
            ext = '.xml'
        else:
            ext = mimetypes.guess_extension(content_type)
            if ext is None:
                ext = '.txt'

        full_path = os.path.join(save_path, f"{file_name}{ext}")

        with open(full_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    file.write(chunk)

        return ext, full_path, True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None, None, False

def download_dynamic_url(url, save_path, file_name):
    """
    Downloads content from a dynamic URL by interacting with the page using Selenium.
    """
    driver = None
    try:
        # Set up the WebDriver
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.get(url)

        # Locate the HTML button and click it (you may need to adjust this based on the actual page structure)
        html_button = driver.find_element(By.XPATH, '//button[text()="Html"]')
        html_button.click()

        # Wait for the download to complete
        driver.implicitly_wait(1000)

        # Get the new URL after clicking the button
        new_url = driver.current_url

        # Download the new URL content
        response = requests.get(new_url, stream=True)
        content_type = response.headers.get('content-type')

        if 'application/pdf' in content_type:
            ext = '.pdf'
        elif 'text/html' in content_type:
            ext = '.html'
        elif 'application/json' in content_type:
            ext = '.json'
        elif 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' in content_type:
            ext = '.xlsx'
        elif 'application/xml' in content_type:
            ext = '.xml'
        else:
            ext = mimetypes.guess_extension(content_type)
            if ext is None:
                ext = '.txt'

        full_path = os.path.join(save_path, f"{file_name}{ext}")

        with open(full_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    file.write(chunk)

        return ext, full_path, True
    except Exception as e:
        print(f"Error downloading dynamic URL {url}: {e}")
        return None, None, False
    finally:
        if driver:
            driver.quit()
