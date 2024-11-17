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
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-background-networking")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-breakpad")
        chrome_options.add_argument("--disable-client-side-phishing-detection")
        chrome_options.add_argument("--disable-component-update")
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--disable-domain-reliability")
        chrome_options.add_argument("--disable-features=AudioServiceOutOfProcess")
        chrome_options.add_argument("--disable-hang-monitor")
        chrome_options.add_argument("--disable-ipc-flooding-protection")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-prompt-on-repost")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-sync")
        chrome_options.add_argument("--force-color-profile=srgb")
        chrome_options.add_argument("--metrics-recording-only")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--safebrowsing-disable-auto-update")
        chrome_options.add_argument("--enable-automation")
        chrome_options.add_argument("--password-store=basic")
        chrome_options.add_argument("--use-mock-keychain")


        
        
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
        time.sleep(5)

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
                time.sleep(5)  # Increase sleep time to ensure download starts