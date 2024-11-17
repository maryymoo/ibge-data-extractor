import os
import zipfile
import pandas as pd
from typing import Dict

class Processor:
    """
    A class to process data files, including extracting ZIP files and processing XLS files.
    """

    def __init__(self):
        """
        Initializes the Processor with directories for data and extracted files.
        """
        self.data_dir = os.path.join(os.getcwd(), 'data')
        self.extracted_dir = os.path.join(self.data_dir, 'extracted')
        os.makedirs(self.extracted_dir, exist_ok=True)

    def extract_zip(self) -> str:
        """
        Extracts all .zip files in the data directory to the extracted directory.

        Returns:
            str: The path to the extracted directory.
        """
        for filename in os.listdir(self.data_dir):
            if filename.endswith(".zip"):
                file_path = os.path.join(self.data_dir, filename)
                print(f"Extracting: {file_path}")
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(self.extracted_dir)
        return self.extracted_dir

    def delete_zip_files(self):
        """
        Deletes all .zip files in the data directory.
        """
        for filename in os.listdir(self.data_dir):
            if filename.endswith(".zip"):
                file_path = os.path.join(self.data_dir, filename)
                print(f"Deleting: {file_path}")
                os.remove(file_path)

    def process_data(self) -> Dict[str, pd.DataFrame]:
        """
        Processes all .xls files in the extracted directory and returns a dictionary of DataFrames.

        Returns:
            Dict[str, pd.DataFrame]: A dictionary where the keys are filenames and the values are DataFrames.
        """
        processed_data = {}
        print(f"Checking extracted directory: {self.extracted_dir}")
        for filename in os.listdir(self.extracted_dir):
            print(f"Found file: {filename}")
            if filename.lower().endswith(".xls"):
                file_path = os.path.join(self.extracted_dir, filename)
                print(f"Processing file: {file_path}")
                try:
                    df = pd.read_excel(file_path)
                    processed_data[filename] = df
                    print(f"Successfully processed: {filename}")
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
        return processed_data