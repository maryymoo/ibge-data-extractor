# IBGE Data Extractor

## Description
This project extracts data from the 1991 IBGE Demographic Census and stores it in a MySQL database.

## Requirements
- Docker
- Docker Compose

## How to run

### Using Docker

1. **Clone the repository**:
    ```sh
    git clone git@github.com:maryymoo/ibge-data-extractor.git
    cd ibge-data-extractor
    ```

2. **Build the Docker image**:
    ```sh
    docker-compose build
    ```

3. **Start the services**:
    ```sh
    docker-compose up
    ```

4. **Run the tests** (optional):
    ```sh
    docker-compose run app python -m unittest discover -s tests
    ```




