# tests/test_data_loader.py
import unittest
import pandas as pd
import os
import sys

# Agregar el directorio padre al path para importar componentes
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):
    
    def setUp(self):
        """Configurar tests"""
        self.data_loader = DataLoader("datos/")
    
    def test_init(self):
        """Test inicialización"""
        self.assertEqual(self.data_loader.data_path, "datos/")
        self.assertIsNone(self.data_loader.holidays_data)
        self.assertIsNone(self.data_loader.passengers_data)
        self.assertIsNone(self.data_loader.countries_data)
    
    def test_load_data_missing_files(self):
        """Test carga con archivos faltantes"""
        # Crear directorio temporal vacío
        os.makedirs("test_datos", exist_ok=True)
        data_loader = DataLoader("test_datos/")
        
        # Debe fallar si no hay archivos
        result = data_loader.load_data()
        self.assertFalse(result)
        
        # Limpiar
        os.rmdir("test_datos")
    
    def test_clean_data_without_load(self):
        """Test limpieza sin datos cargados"""
        result = self.data_loader.clean_data()
        self.assertFalse(result)
    
    def test_get_processed_data_without_process(self):
        """Test obtener datos sin procesar"""
        result = self.data_loader.get_processed_data()
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()