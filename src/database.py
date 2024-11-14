import mysql.connector
import os

def get_db_connection():
    # Get the environment variables defined in the Docker Compose
    db_host = os.getenv("DB_HOST", "localhost")
    db_user = os.getenv("DB_USER", "user")
    db_password = os.getenv("DB_PASSWORD", "userpassword")
    db_name = os.getenv("DB_NAME", "ibge_data")

    # Connect to the MySQL database
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    return connection
