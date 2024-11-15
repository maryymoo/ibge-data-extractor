from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

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
        try:
            self.driver.get(url)
            # Logic to find and click on the download button
            download_button = self.driver.find_element_by_xpath("//button[@class='download']")
            download_button.click()
        except NoSuchElementException:
            print("Error: Download button not found.")

    def close_driver(self):
        self.driver.quit()
