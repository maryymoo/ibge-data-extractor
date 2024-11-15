from extractor import Extractor
from processor import Processor


def main():
    url = "https://www.ibge.gov.br/estatisticas/downloads-estatisticas.html"
    
    extractor = Extractor(url)
    processor = Processor()
   
    extractor.navigate_and_download()
    processor.extract_zip() 
    processor.delete_zip_files() 
    processor_data = processor.process_data()





if __name__ == "__main__":
    main()