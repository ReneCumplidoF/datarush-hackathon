"""
Tests de Integración para DataRush Holiday Pattern Analysis
==========================================================

Tests que verifican la integración entre componentes del sistema.
"""

import pytest
import sys
import os
import pandas as pd

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.data_loader import DataLoader
from components.filters import Filters
from components.visualizations import Visualizations

class TestIntegration:
    """Tests de integración entre componentes"""
    
    def setup_method(self):
        """Configuración inicial para cada test"""
        self.data_loader = DataLoader()
        self.filters = Filters()
        self.visualizations = Visualizations()
        
        # Datos de prueba
        self.sample_data = {
            'holidays': pd.DataFrame({
                'ISO3': ['USA', 'CAN', 'MEX', 'USA', 'CAN'],
                'Date': ['2020-01-01', '2020-01-01', '2020-01-01', '2020-12-25', '2020-12-25'],
                'Year': [2020, 2020, 2020, 2020, 2020],
                'Month': [1, 1, 1, 12, 12],
                'Name': ['New Year', 'New Year', 'New Year', 'Christmas', 'Christmas'],
                'Type': ['Public holiday', 'Public holiday', 'Public holiday', 'Public holiday', 'Public holiday']
            }),
            'passengers': pd.DataFrame({
                'ISO3': ['USA', 'CAN', 'MEX', 'USA', 'CAN'],
                'Year': [2020, 2020, 2020, 2020, 2020],
                'Month': [1, 1, 1, 12, 12],
                'Total': [1000, 500, 300, 1200, 600],
                'Domestic': [800, 400, 250, 900, 450],
                'International': [200, 100, 50, 300, 150]
            }),
            'countries': pd.DataFrame({
                'ISO3': ['USA', 'CAN', 'MEX'],
                'name': ['United States', 'Canada', 'Mexico'],
                'continent': ['North America', 'North America', 'North America']
            })
        }
    
    def test_data_loader_filters_integration(self):
        """Test integración entre DataLoader y Filters"""
        # Cargar datos
        assert self.data_loader.load_data() == True
        assert self.data_loader.clean_data() == True
        
        # Obtener datos procesados
        data = self.data_loader.get_processed_data()
        assert data is not None
        
        # Crear filtros
        filters = self.filters.create_sidebar_filters(data)
        assert isinstance(filters, dict)
        
        # Aplicar filtros
        filtered_data = self.filters.apply_filters(data, filters)
        assert filtered_data is not None
    
    def test_filters_visualizations_integration(self):
        """Test integración entre Filters y Visualizations"""
        # Crear filtros con datos de prueba
        filters = self.filters.create_sidebar_filters(self.sample_data)
        
        # Crear visualizaciones
        heatmap = self.visualizations.create_heatmap_country_month(self.sample_data, filters)
        assert heatmap is not None
        
        trend = self.visualizations.create_trend_analysis(self.sample_data, filters)
        assert trend is not None
        
        impact = self.visualizations.create_holiday_impact(self.sample_data, filters)
        assert impact is not None
        
        kpi = self.visualizations.create_kpi_metrics(self.sample_data, filters)
        assert kpi is not None
    
    def test_end_to_end_workflow(self):
        """Test flujo completo end-to-end"""
        # 1. Cargar datos
        assert self.data_loader.load_data() == True
        assert self.data_loader.clean_data() == True
        data = self.data_loader.get_processed_data()
        assert data is not None
        
        # 2. Crear filtros
        filters = self.filters.create_sidebar_filters(data)
        assert isinstance(filters, dict)
        
        # 3. Aplicar filtros
        filtered_data = self.filters.apply_filters(data, filters)
        assert filtered_data is not None
        
        # 4. Crear visualizaciones
        visualizations = [
            self.visualizations.create_heatmap_country_month(filtered_data, filters),
            self.visualizations.create_trend_analysis(filtered_data, filters),
            self.visualizations.create_holiday_impact(filtered_data, filters),
            self.visualizations.create_kpi_metrics(filtered_data, filters)
        ]
        
        # Verificar que todas las visualizaciones se crearon
        for viz in visualizations:
            assert viz is not None
    
    def test_error_handling_integration(self):
        """Test manejo de errores en integración"""
        # Test con datos vacíos
        empty_data = {}
        filters = self.filters.create_sidebar_filters(empty_data)
        assert filters == {}
        
        # Test con datos None
        filters = self.filters.create_sidebar_filters(None)
        assert filters == {}
        
        # Test con filtros inválidos
        invalid_filters = {'invalid_key': 'invalid_value'}
        filtered_data = self.filters.apply_filters(self.sample_data, invalid_filters)
        assert filtered_data is not None  # Debe manejar filtros inválidos graciosamente
    
    def test_data_consistency(self):
        """Test consistencia de datos entre componentes"""
        # Cargar datos
        assert self.data_loader.load_data() == True
        assert self.data_loader.clean_data() == True
        data = self.data_loader.get_processed_data()
        
        # Verificar que los datos tienen la estructura esperada
        assert 'holidays' in data
        assert 'passengers' in data
        assert 'countries' in data
        
        # Verificar que los DataFrames no están vacíos
        assert not data['holidays'].empty
        assert not data['passengers'].empty
        assert not data['countries'].empty
        
        # Verificar que los filtros pueden procesar los datos
        filters = self.filters.create_sidebar_filters(data)
        assert isinstance(filters, dict)
        
        # Verificar que las visualizaciones pueden procesar los datos
        heatmap = self.visualizations.create_heatmap_country_month(data, filters)
        assert heatmap is not None
    
    def test_performance_integration(self):
        """Test rendimiento de integración"""
        import time
        
        # Cargar datos
        start_time = time.time()
        assert self.data_loader.load_data() == True
        assert self.data_loader.clean_data() == True
        data = self.data_loader.get_processed_data()
        load_time = time.time() - start_time
        
        # Verificar que la carga no toma demasiado tiempo (menos de 5 segundos)
        assert load_time < 5.0, f"La carga de datos tomó {load_time:.2f} segundos, que es demasiado lento"
        
        # Crear filtros
        start_time = time.time()
        filters = self.filters.create_sidebar_filters(data)
        filter_time = time.time() - start_time
        
        # Verificar que la creación de filtros es rápida (menos de 1 segundo)
        assert filter_time < 1.0, f"La creación de filtros tomó {filter_time:.2f} segundos, que es demasiado lento"
        
        # Crear visualizaciones
        start_time = time.time()
        self.visualizations.create_heatmap_country_month(data, filters)
        self.visualizations.create_trend_analysis(data, filters)
        self.visualizations.create_holiday_impact(data, filters)
        self.visualizations.create_kpi_metrics(data, filters)
        viz_time = time.time() - start_time
        
        # Verificar que las visualizaciones se crean rápidamente (menos de 3 segundos)
        assert viz_time < 3.0, f"La creación de visualizaciones tomó {viz_time:.2f} segundos, que es demasiado lento"
