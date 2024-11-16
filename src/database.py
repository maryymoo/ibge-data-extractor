import os
import time
import pandas as pd
import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self, host='localhost', user='root', password='password', database='ibge_data'):
        self.database = database
        self.conn = None
        self.connect(host, user, password)

    def connect(self, host, user, password):
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
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            cursor.close()
        except Error as e:
            print(f"Error creating database: {e}")

    def create_table(self, table_name, columns):
        try:
            cursor = self.conn.cursor()
            columns_with_types = ", ".join([f"`{col}` VARCHAR(255)" for col in columns])
            cursor.execute(f"CREATE TABLE IF NOT EXISTS `{table_name}` ({columns_with_types})")
            cursor.close()
        except Error as e:
            print(f"Error creating table {table_name}: {e}")

    def insert_data(self, table_name, columns, data):
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
        for state, df in processed_data.items():
            # Extract the state abbreviation from the filename
            state_abbr = state.split('.')[0][-2:].lower()
            table_name = f"gini_{state_abbr}"
            
            # Ensure the columns are 'cidade' and 'indice_gini'
            columns = ['cidade', 'indice_gini']
            
            # Replace NaN with None and convert the data to a list of lists
            data = df.where(pd.notnull(df), None).values.tolist()
            
            # Criar a tabela e inserir os dados
            self.create_table(table_name, columns)
            self.insert_data(table_name, columns, data)

    def close_connection(self):
        if self.conn is not None:
            self.conn.close()