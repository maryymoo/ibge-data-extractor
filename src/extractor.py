import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager


class Extractor:
    def __init__(self, url):
        # Starts the browser and configures the URL.
        self.url = url
        self.driver = self._setup_driver()

    def _setup_driver(self):
        # Configures and returns the WebDriver.
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        return driver

    def navigate_and_download(self):
        # Navigates the page and downloads the necessary files.
        try:
            # Accesses the main URL.
            self.driver.get(self.url)
            time.sleep(5)

            # Navigates through specific elements.
            self._click_element_by_id("Censos_anchor")
            self._click_element_by_id("Censos/Censo_Demografico_1991_anchor")
            self._click_element_by_id("Censos/Censo_Demografico_1991/Indice_de_Gini_anchor")

            # Finds and downloads .zip files.
            self._download_zip_files("a.jstree-anchor")

        finally:
            self.driver.quit()

    def _click_element_by_id(self, element_id):
        # Finds the element by ID and clicks on it.
        element = self.driver.find_element(By.ID, element_id)
        ActionChains(self.driver).move_to_element(element).click().perform()
        time.sleep(3)

    def _download_zip_files(self, selector):
        # Downloads all .zip files found by the CSS selector.
        links = self.driver.find_elements(By.CSS_SELECTOR, selector)
        for link in links:
            href = link.get_attribute("href")
            if href and href.endswith(".zip"):
                print(f"Downloading: {href}")
                self.driver.get(href)
                time.sleep(2)

