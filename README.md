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

2. **Open your Docker**:
   If you don't have it installed you can download it here: https://www.docker.com/products/docker-desktop/

4. **Build the Docker image and start the services**:
    ```sh
    docker-compose up --build
    ```

5. **Run the tests** (optional):
    ```sh
    docker-compose run app python -m unittest discover -s tests
    ```

## Database Files
The resulting database files are stored in the `data/database` directory. This directory contains all the necessary files for the MySQL database `ibge_data`.

## Accessing the Database
To access the database, you can use the following command to enter the MySQL container:
```sh
docker exec -it <container_id> mysql -u root -p
 ```
Once inside the MySQL prompt, you can use the following commands to view the database and its tables:
```sh
USE ibge_data;
SHOW TABLES;
SELECT * FROM <table_name>;
 ```


