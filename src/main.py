from extractor import Extractor

def main():
    url = "https://www.ibge.gov.br/estatisticas/downloads-estatisticas.html"
    extractor = Extractor(url)
    extractor.navigate_and_download()

if __name__ == "__main__":
    main()