from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class Extractor:
    def __init__(self):
        self.driver = self.start_driver()

    def start_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Rodar sem abrir a janela do navegador
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def close_driver(self):
        self.driver.quit()
