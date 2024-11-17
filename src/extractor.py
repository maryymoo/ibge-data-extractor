import os, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class Extractor:
    """
    A class to extract data from a specified URL using Selenium WebDriver.
    """

    def __init__(self, url):
        """
        Initializes the Extractor with the given URL and sets up the WebDriver.

        Args:
            url (str): The URL to navigate to and extract data from.
        """
        self.url = url
        self.driver = self._setup_driver()

    def _setup_driver(self):
        """
        Configures and returns the WebDriver with custom download directory.

        Returns:
            WebDriver: Configured Selenium WebDriver instance.
        """
        download_dir = os.path.join(os.getcwd(), 'data')
        os.makedirs(download_dir, exist_ok=True)

        chrome_options = Options()
        chrome_arguments = [
            "--headless",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--remote-debugging-port=9222",
            "--disable-software-rasterizer",
            "--disable-extensions",
            "--disable-background-networking",
            "--disable-background-timer-throttling",
            "--disable-backgrounding-occluded-windows",
            "--disable-breakpad",
            "--disable-client-side-phishing-detection",
            "--disable-component-update",
            "--disable-default-apps",
            "--disable-domain-reliability",
            "--disable-features=AudioServiceOutOfProcess",
            "--disable-hang-monitor",
            "--disable-ipc-flooding-protection",
            "--disable-popup-blocking",
            "--disable-prompt-on-repost",
            "--disable-renderer-backgrounding",
            "--disable-sync",
            "--force-color-profile=srgb",
            "--metrics-recording-only",
            "--no-first-run",
            "--safebrowsing-disable-auto-update",
            "--enable-automation",
            "--password-store=basic",
            "--use-mock-keychain"
        ]

        for arg in chrome_arguments:
            chrome_options.add_argument(arg)
        
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
        """
        Navigates to the URL and performs the download actions.
        """
        self.driver.get(self.url)
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "Censos_anchor"))
        )
        self._click_element_by_id("Censos_anchor")
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "Censos/Censo_Demografico_1991_anchor"))
        )
        self._click_element_by_id("Censos/Censo_Demografico_1991_anchor")
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "Censos/Censo_Demografico_1991/Indice_de_Gini_anchor"))
        )
        self._click_element_by_id("Censos/Censo_Demografico_1991/Indice_de_Gini_anchor")
        self._download_zip_files()
        self.driver.quit()

    def _click_element_by_id(self, element_id):
        """
        Clicks an element by its ID.

        Args:
            element_id (str): The ID of the element to click.
        """
        element = self.driver.find_element(By.ID, element_id)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        ActionChains(self.driver).move_to_element(element).click().perform()

    def _download_zip_files(self):
        """
        Downloads all ZIP files found in the specified elements.
        """
        elements = self.driver.find_elements(By.CSS_SELECTOR, "li[aria-level='5'] a.jstree-anchor")
        for element in elements:
            text = element.text
            if text.endswith(".zip"):
                print(f"Downloading: {text}")
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                ActionChains(self.driver).move_to_element(element).click().perform()
                time.sleep(0.3)  # Increase sleep time to ensure download starts