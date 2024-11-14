from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class Extractor:
    def __init__(self):
        self.driver = self.start_driver()

    def start_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def download_data(self, url):
        self.driver.get(url)
        # A lógica para encontrar e clicar no botão de download
        download_button = self.driver.find_element_by_xpath("//button[@class='download']")
        download_button.click()

    def close_driver(self):
        self.driver.quit()
