import time
import pandas as pd
import mysql.connector
from mysql.connector import Error

class Database:
    """
    A class to manage database operations including creating databases, tables, and inserting data.
    """

    def __init__(self, host='localhost', user='root', password='password', database='ibge_data'):
        """
        Initializes the Database with connection parameters and connects to the database.

        Args:
            host (str): The database host.
            user (str): The database user.
            password (str): The database password.
            database (str): The name of the database.
        """
        self.database = database
        self.conn = None
        self.connect(host, user, password)

    def connect(self, host, user, password):
        """
        Connects to the database and creates the database if it does not exist.

        Args:
            host (str): The database host.
            user (str): The database user.
            password (str): The database password.
        """
        for _ in range(10):  # Try to connect 10 times
            try:
                self.conn = mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password
                )
                self.create_database()
                self.conn.database = self.database
                break
            except Error as e:
                print(f"Error connecting to the database: {e}")
                self.conn = None
                time.sleep(5)  # Wait for 5 seconds before trying again

    def create_database(self):
        """
        Creates the database if it does not exist.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            cursor.close()
        except Error as e:
            print(f"Error creating database: {e}")

    def create_table(self, table_name, columns):
        """
        Creates a table with the specified columns if it does not exist.

        Args:
            table_name (str): The name of the table.
            columns (list): A list of column names.
        """
        try:
            cursor = self.conn.cursor()
            columns_with_types = ", ".join([f"`{col}` VARCHAR(255)" for col in columns])
            cursor.execute(f"CREATE TABLE IF NOT EXISTS `{table_name}` ({columns_with_types})")
            cursor.close()
        except Error as e:
            print(f"Error creating table {table_name}: {e}")

    def insert_data(self, table_name, columns, data):
        """
        Inserts data into the specified table.

        Args:
            table_name (str): The name of the table.
            columns (list): A list of column names.
            data (list): A list of data rows to insert.
        """
        try:
            cursor = self.conn.cursor()
            placeholders = ", ".join(["%s"] * len(columns))
            columns_joined = ", ".join([f"`{col}`" for col in columns])
            query = f"INSERT INTO `{table_name}` ({columns_joined}) VALUES ({placeholders})"
            cursor.executemany(query, data)
            self.conn.commit()
            cursor.close()
        except Error as e:
            print(f"Error inserting data into table {table_name}: {e}")

    def process_and_insert_data(self, processed_data):
        """
        Processes and inserts data into the database.

        Args:
            processed_data (dict): A dictionary where keys are filenames and values are DataFrames.
        """
        for state, df in processed_data.items():
            # Extract the state abbreviation from the filename
            state_abbr = state.split('.')[0][-2:].lower()
            table_name = f"gini_{state_abbr}"
            
            # Ensure the columns are 'cidade' and 'indice_gini'
            columns = ['cidade', 'indice_gini']
            
            # Replace NaN with None and convert the data to a list of lists
            data = df.where(pd.notnull(df), None).values.tolist()
            
            # Create the table and insert the data
            self.create_table(table_name, columns)
            self.insert_data(table_name, columns, data)

    def close_connection(self):
        """
        Closes the database connection.
        """
        if self.conn is not None:
            self.conn.close()