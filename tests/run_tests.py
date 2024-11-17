import unittest

# Importar os módulos de teste
from tests.test_extractor import TestExtractor
from tests.test_processor import TestProcessor
from tests.test_database import TestDatabase

# Criar um suite de testes
def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestExtractor))
    test_suite.addTest(unittest.makeSuite(TestProcessor))
    test_suite.addTest(unittest.makeSuite(TestDatabase))
    return test_suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())