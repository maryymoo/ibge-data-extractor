# **IBGE Data Extractor**

## **Overview**

This project automates the process of extracting, processing, and persisting data from the 1991 IBGE Demographic Census, specifically the Gini Index data for Brazilian states. The data is extracted from the IBGE website, processed, and then stored in a MySQL database. The application is built with a focus on **Object-Oriented Programming (OOP)** and adheres to **SOLID** principles, ensuring a modular, scalable, and maintainable codebase. The project is containerized using **Docker** for seamless deployment.

## **Requirements**

- Docker
- Docker Compose

## **How to Run**

### **Using Docker**

1. **Clone the repository:**

   ```bash
   git clone git@github.com:maryymoo/ibge-data-extractor.git
   cd ibge-data-extractor
   ```

2. **Install Docker**  
   If you don’t have Docker installed, you can download it [here](https://www.docker.com/products/docker-desktop/).

3. **Build the Docker image and start the services:**

   ```bash
   docker-compose up --build
   ```

   This will build the Docker image and run the services (Python app and MySQL database) inside containers.

4. **Run tests (optional):**

   ```bash
   docker-compose run app python -m unittest discover -s tests -p "test_<choose file>.py"
   ```

   This command runs unit tests to verify that the functionality of the Extractor and Database classes works as expected.


## **Database Files**

The resulting database files are stored in the `data/database` directory. This directory contains all the necessary files for the MySQL database (`ibge_data`).


## **Accessing the Database**

To access the MySQL database inside the Docker container, run the following command:

```bash
docker exec -it <container_id> mysql -u root -p
```

Once inside the MySQL prompt, you can view the database and its tables:

```sql
USE ibge_data;
SHOW TABLES;
SELECT * FROM <table_name>;
```


## **Project Structure**

The project is organized into the following directory structure:

```
.
├── src/                     # Source code files
|   ├── extractor.py         # Extractor class, handles downloading data from IBGE
|   ├── processor.py         # Processor class, handles extracting and processing data
|   ├── database.py          # Database class, handles database operations
|   ├── main.py              # Main project pipeline that orchestrates the entire process
├── data/                    # Directory for storing downloaded data and database files
|   ├── database/            # Directory for MySQL database files
|   ├── extracted/           # Directory for extracted files from ZIP archives
|   └── *.zip                # Downloaded ZIP files from IBGE
├── tests/                   # Directory for unit tests
|   ├── test-extractor.py    # Unit tests for the Extractor class
|   ├── test-database.py     # Unit tests for the Database class
├── Dockerfile               # Docker container configuration for the application
├── .dockerignore            # Specifies files and directories to ignore when building the Docker image
├── .gitignore               # Specifies files and directories to ignore in Git
├── docker-compose.yml       # Orchestrates the services for the app and database in Docker
├── requirements.txt         # Project dependencies for Python environment
├── dev-requirements.txt     # Development dependencies for testing, linters, etc.
├── README.md                # Project documentation with setup instructions
```


## **Class Details**

### **1. Extractor**

- **Responsibility:** The `Extractor` class automates the navigation and downloading of ZIP files containing the IBGE census data.
- **Main Methods:**
    - `__init__(self, url)`: Initializes the WebDriver and the download directory.
    - `navigate_and_download(self)`: Navigates the IBGE website, identifies download links, and downloads the ZIP files.

### **2. Processor**

- **Responsibility:** The `Processor` class handles the extraction and processing of the downloaded data into a structured format suitable for database insertion.
- **Main Methods:**
    - `extract_zip(self)`: Extracts the downloaded ZIP files.
    - `process_data(self)`: Converts the `.xls` files into pandas DataFrames.
    - `delete_zip_files(self)`: Deletes the ZIP files after extraction.
    - `delete_extracted_files(self)`: Deletes the extracted files after processing.

### **3. Database**

- **Responsibility:** The `Database` class manages MySQL operations, including the creation of the database, creation of tables, and insertion of processed data.
- **Main Methods:**
    - `create_database(self)`: Creates the `ibge_data` database if it doesn't exist.
    - `create_table(self, table_name, columns)`: Creates tables in the database with a defined schema.
    - `insert_data(self, table_name, columns, data)`: Inserts processed data into the corresponding tables.
    - `process_and_insert_data(self, processed_data)`: Integrates the processed data and inserts it into the database.


## **Setup and Execution**

### **Dependencies**

Project dependencies are listed in the `requirements.txt` file:

```
pandas==2.2.3
selenium==4.26.1
webdriver-manager==4.0.2
xlrd==2.0.1
mysql-connector-python==9.1.0
certifi==2023.7.22
```

### **Containerization**

The project is configured to run via Docker. Use the `Dockerfile` and `docker-compose.yml` files to build and run the services.

1. **Build the container and start the application:**

   ```bash
   docker-compose up --build
   ```

   This command starts the MySQL database container and the Python application container.


## **Database Structure**

Each Brazilian state has its own table in the database, named `gini_<state>` (e.g., `gini_ac` for Acre). The table schema is as follows:

### **Table Schema**

| Column        | Type        | Description                         |
|---------------|-------------|-------------------------------------|
| `cidade`      | VARCHAR(255)| City name                          |
| `indice_gini` | VARCHAR(255)| Gini Index value                   |


## **Adopted Principles**

1. **Object-Oriented Programming (OOP) & SOLID:**
    - **Single Responsibility Principle (SRP):** Each class has a clear responsibility, focusing on one task.
    - **Open/Closed Principle (OCP):** The system is open for extension but closed for modification, making it easy to add new features.
    - **Substitutability:** Classes can be substituted without affecting the overall system.

2. **Containerization:**
    - Using Docker ensures reproducible environments, isolating the application and the MySQL database to avoid conflicts.

3. **Full Automation:**
    - The entire process, from downloading the data to persisting it in a MySQL database, is fully automated.


## **How to Contribute**

1. Fork the repository on GitHub.
2. Create a new branch for your feature:

   ```bash
   git checkout -b my-feature
   ```

3. Make incremental commits with your changes.
4. Open a pull request describing your changes.
