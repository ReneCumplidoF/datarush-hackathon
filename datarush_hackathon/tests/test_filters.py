"""
Tests para el componente Filters
===============================

Tests unitarios para la clase Filters.
"""

import pytest
import sys
import os
import pandas as pd

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.filters import Filters

class TestFilters:
    """Tests para la clase Filters"""
    
    def setup_method(self):
        """Configuración inicial para cada test"""
        self.filters = Filters()
        
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
    
    def test_init(self):
        """Test inicialización de la clase"""
        assert self.filters.filters == {}
        assert self.filters.filter_options == {}
        assert self.filters.country_mapping == {}
    
    def test_create_sidebar_filters_with_data(self):
        """Test creación de filtros con datos válidos"""
        filters = self.filters.create_sidebar_filters(self.sample_data)
        assert isinstance(filters, dict)
        # Los filtros deben contener las claves esperadas
        expected_keys = ['year_range', 'months', 'countries', 'continents', 'holiday_types']
        for key in expected_keys:
            assert key in filters
    
    def test_create_sidebar_filters_without_data(self):
        """Test creación de filtros sin datos"""
        filters = self.filters.create_sidebar_filters({})
        assert filters == {}
        
        filters = self.filters.create_sidebar_filters(None)
        assert filters == {}
    
    def test_apply_filters(self):
        """Test aplicación de filtros"""
        # Crear filtros
        filters = self.filters.create_sidebar_filters(self.sample_data)
        
        # Aplicar filtros
        filtered_data = self.filters.apply_filters(self.sample_data, filters)
        assert filtered_data is not None
        assert isinstance(filtered_data, dict)
        
        # Verificar que los datos filtrados mantienen la estructura
        assert 'holidays' in filtered_data
        assert 'passengers' in filtered_data
        assert 'countries' in filtered_data
    
    def test_apply_filters_with_empty_data(self):
        """Test aplicación de filtros con datos vacíos"""
        filters = self.filters.create_sidebar_filters(self.sample_data)
        filtered_data = self.filters.apply_filters({}, filters)
        assert filtered_data == {}
        
        filtered_data = self.filters.apply_filters(None, filters)
        assert filtered_data is None
    
    def test_validate_filters(self):
        """Test validación de filtros"""
        # Filtros válidos
        valid_filters = {
            'year_range': [2020, 2021],
            'months': [1, 2, 3],
            'countries': ['USA', 'CAN'],
            'continents': ['North America'],
            'holiday_types': ['Public holiday']
        }
        assert self.filters.validate_filters(valid_filters) == True
        
        # Filtros inválidos
        invalid_filters = {
            'invalid_key': 'invalid_value'
        }
        assert self.filters.validate_filters(invalid_filters) == False
        
        # Filtros None
        assert self.filters.validate_filters(None) == False
    
    def test_get_active_filters_summary(self):
        """Test resumen de filtros activos"""
        filters = {
            'year_range': [2020, 2021],
            'months': [1, 2, 3],
            'countries': ['USA', 'CAN'],
            'continents': ['North America'],
            'holiday_types': ['Public holiday']
        }
        
        summary = self.filters.get_active_filters_summary()
        assert isinstance(summary, dict)
    
    def test_filter_by_year_range(self):
        """Test filtrado por rango de años"""
        filters = {
            'year_range': [2020, 2020],
            'months': [1, 12],
            'countries': ['USA', 'CAN', 'MEX'],
            'continents': ['North America'],
            'holiday_types': ['Public holiday']
        }
        
        filtered_data = self.filters.apply_filters(self.sample_data, filters)
        assert filtered_data is not None
        
        # Verificar que solo se incluyen datos de 2020
        if not filtered_data['passengers'].empty:
            assert all(year == 2020 for year in filtered_data['passengers']['Year'])
    
    def test_filter_by_countries(self):
        """Test filtrado por países"""
        filters = {
            'year_range': [2020, 2020],
            'months': [1, 12],
            'countries': ['USA'],
            'continents': ['North America'],
            'holiday_types': ['Public holiday']
        }
        
        filtered_data = self.filters.apply_filters(self.sample_data, filters)
        assert filtered_data is not None
        
        # Verificar que solo se incluyen datos de USA
        if not filtered_data['passengers'].empty:
            assert all(country == 'USA' for country in filtered_data['passengers']['ISO3'])
    
    def test_filter_by_holiday_types(self):
        """Test filtrado por tipos de feriado"""
        filters = {
            'year_range': [2020, 2020],
            'months': [1, 12],
            'countries': ['USA', 'CAN', 'MEX'],
            'continents': ['North America'],
            'holiday_types': ['Public holiday']
        }
        
        filtered_data = self.filters.apply_filters(self.sample_data, filters)
        assert filtered_data is not None
        
        # Verificar que solo se incluyen feriados públicos
        if not filtered_data['holidays'].empty:
            assert all(holiday_type == 'Public holiday' for holiday_type in filtered_data['holidays']['Type'])
    
    def test_filter_combination(self):
        """Test combinación de múltiples filtros"""
        filters = {
            'year_range': [2020, 2020],
            'months': [1],
            'countries': ['USA'],
            'continents': ['North America'],
            'holiday_types': ['Public holiday']
        }
        
        filtered_data = self.filters.apply_filters(self.sample_data, filters)
        assert filtered_data is not None
        
        # Verificar que se aplican todos los filtros
        if not filtered_data['passengers'].empty:
            assert all(year == 2020 for year in filtered_data['passengers']['Year'])
            assert all(month == 1 for month in filtered_data['passengers']['Month'])
            assert all(country == 'USA' for country in filtered_data['passengers']['ISO3'])
    
    def test_performance_with_large_dataset(self):
        """Test rendimiento con dataset grande"""
        import time
        
        # Crear dataset más grande
        large_data = {
            'holidays': pd.DataFrame({
                'ISO3': ['USA'] * 1000 + ['CAN'] * 1000 + ['MEX'] * 1000,
                'Date': ['2020-01-01'] * 1000 + ['2020-01-01'] * 1000 + ['2020-01-01'] * 1000,
                'Year': [2020] * 3000,
                'Month': [1] * 1000 + [2] * 1000 + [3] * 1000,
                'Name': ['Holiday'] * 3000,
                'Type': ['Public holiday'] * 3000
            }),
            'passengers': pd.DataFrame({
                'ISO3': ['USA'] * 1000 + ['CAN'] * 1000 + ['MEX'] * 1000,
                'Year': [2020] * 3000,
                'Month': [1] * 1000 + [2] * 1000 + [3] * 1000,
                'Total': [1000] * 3000,
                'Domestic': [800] * 3000,
                'International': [200] * 3000
            }),
            'countries': pd.DataFrame({
                'ISO3': ['USA', 'CAN', 'MEX'],
                'name': ['United States', 'Canada', 'Mexico'],
                'continent': ['North America', 'North America', 'North America']
            })
        }
        
        # Medir tiempo de creación de filtros
        start_time = time.time()
        filters = self.filters.create_sidebar_filters(large_data)
        filter_time = time.time() - start_time
        
        # Verificar que es rápido (menos de 2 segundos)
        assert filter_time < 2.0, f"La creación de filtros tomó {filter_time:.2f} segundos, que es demasiado lento"
        
        # Medir tiempo de aplicación de filtros
        start_time = time.time()
        filtered_data = self.filters.apply_filters(large_data, filters)
        apply_time = time.time() - start_time
        
        # Verificar que es rápido (menos de 3 segundos)
        assert apply_time < 3.0, f"La aplicación de filtros tomó {apply_time:.2f} segundos, que es demasiado lento"
