from extractor import Extractor
from processor import Processor
from database import Database

def main():
    url = "https://www.ibge.gov.br/estatisticas/downloads-estatisticas.html"
    
    extractor = Extractor(url)
    processor = Processor()
    database = Database(host='db', user='root', password='password', database='ibge_data')

    extractor.navigate_and_download()
    processor.extract_zip()
    processor.delete_zip_files()
    processed_data = processor.process_data()
    database.process_and_insert_data(processed_data)
    database.close_connection()
    print("Data processing and insertion completed.")

if __name__ == "__main__":
    main()