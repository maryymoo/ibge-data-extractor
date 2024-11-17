import unittest
from unittest.mock import patch, MagicMock
import os
import pandas as pd
from src.processor import Processor

class TestProcessor(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        self.processor = Processor()
        self.processor.data_dir = "test_data"
        self.processor.extracted_dir = "test_extracted"
        os.makedirs(self.processor.data_dir, exist_ok=True)
        os.makedirs(self.processor.extracted_dir, exist_ok=True)

    def tearDown(self):
        """Clean up the test environment."""
        for directory in [self.processor.data_dir, self.processor.extracted_dir]:
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                os.remove(file_path)
            os.rmdir(directory)

    @patch("src.processor.zipfile.ZipFile")
    def test_extract_zip(self, MockZipFile):
        """Test extracting ZIP files."""
        zip_filename = "test.zip"
        zip_filepath = os.path.join(self.processor.data_dir, zip_filename)
        with open(zip_filepath, "w") as f:
            f.write("Test ZIP content")

        mock_zip = MockZipFile.return_value
        self.processor.extract_zip()
        MockZipFile.assert_called_once_with(zip_filepath, 'r')
        mock_zip.extractall.assert_called_once_with(self.processor.extracted_dir)

    def test_delete_zip_files(self):
        """Test deleting ZIP files."""
        zip_filename = "test.zip"
        zip_filepath = os.path.join(self.processor.data_dir, zip_filename)
        with open(zip_filepath, "w") as f:
            f.write("Test ZIP content")

        self.processor.delete_zip_files()
        self.assertFalse(os.path.exists(zip_filepath))

    def test_delete_extracted_files(self):
        """Test deleting extracted files."""
        extracted_filename = "test.xls"
        extracted_filepath = os.path.join(self.processor.extracted_dir, extracted_filename)
        with open(extracted_filepath, "w") as f:
            f.write("Test extracted content")

        self.processor.delete_extracted_files()
        self.assertFalse(os.path.exists(extracted_filepath))

    @patch("src.processor.pd.read_excel")
    def test_process_data(self, MockReadExcel):
        """Test processing data files."""
        xls_filename = "test.xls"
        xls_filepath = os.path.join(self.processor.extracted_dir, xls_filename)
        with open(xls_filepath, "w") as f:
            f.write("Test XLS content")

        mock_df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        MockReadExcel.return_value = mock_df

        processed_data = self.processor.process_data()
        self.assertIn(xls_filename, processed_data)
        pd.testing.assert_frame_equal(processed_data[xls_filename], mock_df)

if __name__ == "__main__":
    unittest.main()