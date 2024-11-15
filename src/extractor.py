import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

class Extractor:
    def __init__(self, url):
        self.url = url
        self.driver = self._setup_driver()

    def _setup_driver(self):
        # Configures and returns the WebDriver with custom download directory.
        download_dir = os.path.join(os.getcwd(), 'data')
        os.makedirs(download_dir, exist_ok=True)

        chrome_options = webdriver.ChromeOptions()
        prefs = {
            'download.default_directory': download_dir,
            'download.prompt_for_download': False,
            'directory_upgrade': True,
            'safebrowsing.enabled': True
        }
        chrome_options.add_experimental_option('prefs', prefs)

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def navigate_and_download(self):
        try:
            self.driver.get(self.url)
            time.sleep(10)
            self._click_element_by_id("Censos_anchor")
            self._click_element_by_id("Censos/Censo_Demografico_1991_anchor")
            self._click_element_by_id("Censos/Censo_Demografico_1991/Indice_de_Gini_anchor")
            self._download_zip_files()
        finally:
            self.driver.quit()

    def _click_element_by_id(self, element_id):
        element = self.driver.find_element(By.ID, element_id)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        ActionChains(self.driver).move_to_element(element).click().perform()
        time.sleep(5)

    def _download_zip_files(self):
        # Find all elements within the current directory
        elements = self.driver.find_elements(By.CSS_SELECTOR, "li[aria-level='5'] a.jstree-anchor")
        for element in elements:
            text = element.text
            if text.endswith(".zip"):
                print(f"Downloading: {text}")
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                ActionChains(self.driver).move_to_element(element).click().perform()
                time.sleep(5)  # Increase sleep time to ensure download starts