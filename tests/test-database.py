import unittest
from src.database import Database
import time

class TestDatabase(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        # Esperar o MySQL iniciar
        time.sleep(10)
        self.db = Database(
            host='db',  # Use o nome do serviço definido no docker-compose.yml
            user='root',
            password='password',
            database='test_db'
        )

    def tearDown(self):
        """Clean up the test environment."""
        self.db.close_connection()

    def test_connection(self):
        """Test if the database connection is established."""
        self.assertIsNotNone(self.db.conn)

    def test_execute_query(self):
        """Test executing a simple query."""
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT DATABASE()")
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        cursor.close()

if __name__ == '__main__':
    unittest.main()