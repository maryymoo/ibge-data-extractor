import mysql.connector

class Database:
    def __init__(self, host='db', user='root', password='password', database='test_db'):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

    def close_connection(self):
        self.conn.close()