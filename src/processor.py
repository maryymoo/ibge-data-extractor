import zipfile
import os

class Processor:
    def extract_zip(self, file_path, output_dir):
        """Extracts files from a .zip archive to the specified directory."""
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
