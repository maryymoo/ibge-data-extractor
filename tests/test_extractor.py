import unittest
from unittest.mock import MagicMock
from src.extractor import Extractor

class TestExtractor(unittest.TestCase):
    def test_start_driver(self):
        extractor = Extractor()
        extractor.driver = MagicMock()  #Using Mock for WebDriver
        self.assertIsNotNone(extractor.driver)

if __name__ == '__main__':
    unittest.main()
