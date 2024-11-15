import unittest
from unittest.mock import MagicMock, patch
from selenium.webdriver.remote.webelement import WebElement
from src.extractor import Extractor

class TestExtractor(unittest.TestCase):
    def setUp(self):
        """Initial configuration for the tests"""
        self.url = "https://www.ibge.gov.br/estatisticas/downloads-estatisticas.html"
        self.extractor = Extractor(self.url)
        
        # Mocking the Selenium driver to avoid the need to open the real browser
        self.extractor.driver = MagicMock()

    @patch('src.extractor.ChromeDriverManager')
    @patch('src.extractor.webdriver.Chrome')
    def test_setup_driver(self, MockChrome, MockChromeDriverManager):
        """Test the _setup_driver method"""
        MockChromeDriverManager().install.return_value = 'path/to/chromedriver'
        self.extractor._setup_driver()
        MockChrome.assert_called_once()

    @patch('src.extractor.ActionChains')
    def test_click_element_by_id(self, MockActionChains):
        """Test the _click_element_by_id method"""
        # Mock the WebElement
        element = MagicMock(spec=WebElement)
        self.extractor.driver.find_element.return_value = element

        # Mock the ActionChains
        action_chains_mock = MockActionChains.return_value

        # Mock the methods of ActionChains
        action_chains_mock.move_to_element.return_value = action_chains_mock
        action_chains_mock.click.return_value = action_chains_mock

        # Execute the click action
        self.extractor._click_element_by_id("Censos_anchor")

        # Verify calls
        action_chains_mock.move_to_element.assert_called_once_with(element)
        action_chains_mock.click.assert_called_once()
        action_chains_mock.perform.assert_called_once()

    @patch('src.extractor.ActionChains')
    def test_download_zip_files(self, MockActionChains):
        """Test the _download_zip_files method"""
        # Mock the WebElement
        element = MagicMock(spec=WebElement)
        element.text = "file.zip"
        self.extractor.driver.find_elements.return_value = [element]

        # Mock the ActionChains
        action_chains_mock = MockActionChains.return_value

        # Mock the methods of ActionChains
        action_chains_mock.move_to_element.return_value = action_chains_mock
        action_chains_mock.click.return_value = action_chains_mock

        # Execute the download action
        self.extractor._download_zip_files()

        # Verify calls
        action_chains_mock.move_to_element.assert_called_once_with(element)
        action_chains_mock.click.assert_called_once()
        action_chains_mock.perform.assert_called_once()

    @patch('src.extractor.Extractor._click_element_by_id')
    @patch('src.extractor.Extractor._download_zip_files')
    def test_navigate_and_download(self, mock_download_zip_files, mock_click_element_by_id):
        """Test the navigate_and_download method"""
        self.extractor.navigate_and_download()
        mock_click_element_by_id.assert_any_call("Censos_anchor")
        mock_click_element_by_id.assert_any_call("Censos/Censo_Demografico_1991_anchor")
        mock_click_element_by_id.assert_any_call("Censos/Censo_Demografico_1991/Indice_de_Gini_anchor")
        mock_download_zip_files.assert_called_once()

if __name__ == "__main__":
    unittest.main()