"""
Tests para el componente Visualizations
=======================================

Tests unitarios para la clase Visualizations.
"""

import pytest
import sys
import os
import pandas as pd

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.visualizations import Visualizations

class TestVisualizations:
    """Tests para la clase Visualizations"""
    
    def setup_method(self):
        """Configuración inicial para cada test"""
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
        
        self.sample_filters = {
            'year_range': [2020, 2020],
            'months': [1, 12],
            'countries': ['USA', 'CAN', 'MEX'],
            'continents': ['North America'],
            'holiday_types': ['Public holiday']
        }
    
    def test_init(self):
        """Test inicialización de la clase"""
        assert hasattr(self.visualizations, 'colors')
        assert isinstance(self.visualizations.colors, dict)
        assert 'primary' in self.visualizations.colors
    
    def test_create_heatmap_country_month(self):
        """Test creación de mapa de calor país-mes"""
        heatmap = self.visualizations.create_heatmap_country_month(self.sample_data, self.sample_filters)
        assert heatmap is not None
        assert hasattr(heatmap, 'data')
        assert hasattr(heatmap, 'layout')
    
    def test_create_heatmap_with_empty_data(self):
        """Test creación de mapa de calor con datos vacíos"""
        empty_data = {
            'holidays': pd.DataFrame(),
            'passengers': pd.DataFrame(),
            'countries': pd.DataFrame()
        }
        heatmap = self.visualizations.create_heatmap_country_month(empty_data, self.sample_filters)
        assert heatmap is not None
    
    def test_create_trend_analysis(self):
        """Test creación de análisis de tendencias"""
        trend = self.visualizations.create_trend_analysis(self.sample_data, self.sample_filters)
        assert trend is not None
        assert hasattr(trend, 'data')
        assert hasattr(trend, 'layout')
    
    def test_create_trend_with_empty_data(self):
        """Test creación de análisis de tendencias con datos vacíos"""
        empty_data = {
            'holidays': pd.DataFrame(),
            'passengers': pd.DataFrame(),
            'countries': pd.DataFrame()
        }
        trend = self.visualizations.create_trend_analysis(empty_data, self.sample_filters)
        assert trend is not None
    
    def test_create_holiday_impact(self):
        """Test creación de gráfico de impacto de feriados"""
        impact = self.visualizations.create_holiday_impact(self.sample_data, self.sample_filters)
        assert impact is not None
        assert hasattr(impact, 'data')
        assert hasattr(impact, 'layout')
    
    def test_create_holiday_impact_with_empty_data(self):
        """Test creación de gráfico de impacto con datos vacíos"""
        empty_data = {
            'holidays': pd.DataFrame(),
            'passengers': pd.DataFrame(),
            'countries': pd.DataFrame()
        }
        impact = self.visualizations.create_holiday_impact(empty_data, self.sample_filters)
        assert impact is not None
    
    def test_create_kpi_metrics(self):
        """Test creación de métricas KPI"""
        kpi = self.visualizations.create_kpi_metrics(self.sample_data, self.sample_filters)
        assert kpi is not None
        assert hasattr(kpi, 'data')
        assert hasattr(kpi, 'layout')
    
    def test_create_kpi_with_empty_data(self):
        """Test creación de métricas KPI con datos vacíos"""
        empty_data = {
            'holidays': pd.DataFrame(),
            'passengers': pd.DataFrame(),
            'countries': pd.DataFrame()
        }
        kpi = self.visualizations.create_kpi_metrics(empty_data, self.sample_filters)
        assert kpi is not None
    
    def test_update_visualizations(self):
        """Test actualización de visualizaciones"""
        # Este método debe existir y ser callable
        assert hasattr(self.visualizations, 'update_visualizations')
        assert callable(self.visualizations.update_visualizations)
        
        # Debe manejar datos vacíos sin errores
        empty_data = {
            'holidays': pd.DataFrame(),
            'passengers': pd.DataFrame(),
            'countries': pd.DataFrame()
        }
        try:
            self.visualizations.update_visualizations(empty_data, self.sample_filters)
        except Exception as e:
            pytest.fail(f"update_visualizations falló con datos vacíos: {e}")
    
    def test_visualization_with_none_data(self):
        """Test visualizaciones con datos None"""
        # Debe manejar datos None sin errores
        try:
            self.visualizations.create_heatmap_country_month(None, self.sample_filters)
            self.visualizations.create_trend_analysis(None, self.sample_filters)
            self.visualizations.create_holiday_impact(None, self.sample_filters)
            self.visualizations.create_kpi_metrics(None, self.sample_filters)
        except Exception as e:
            pytest.fail(f"Las visualizaciones fallaron con datos None: {e}")
    
    def test_visualization_with_none_filters(self):
        """Test visualizaciones con filtros None"""
        # Debe manejar filtros None sin errores
        try:
            self.visualizations.create_heatmap_country_month(self.sample_data, None)
            self.visualizations.create_trend_analysis(self.sample_data, None)
            self.visualizations.create_holiday_impact(self.sample_data, None)
            self.visualizations.create_kpi_metrics(self.sample_data, None)
        except Exception as e:
            pytest.fail(f"Las visualizaciones fallaron con filtros None: {e}")
    
    def test_visualization_performance(self):
        """Test rendimiento de las visualizaciones"""
        import time
        
        # Medir tiempo de creación de cada visualización
        start_time = time.time()
        heatmap = self.visualizations.create_heatmap_country_month(self.sample_data, self.sample_filters)
        heatmap_time = time.time() - start_time
        
        start_time = time.time()
        trend = self.visualizations.create_trend_analysis(self.sample_data, self.sample_filters)
        trend_time = time.time() - start_time
        
        start_time = time.time()
        impact = self.visualizations.create_holiday_impact(self.sample_data, self.sample_filters)
        impact_time = time.time() - start_time
        
        start_time = time.time()
        kpi = self.visualizations.create_kpi_metrics(self.sample_data, self.sample_filters)
        kpi_time = time.time() - start_time
        
        # Verificar que cada visualización se crea rápidamente (menos de 2 segundos)
        assert heatmap_time < 2.0, f"El mapa de calor tomó {heatmap_time:.2f} segundos, que es demasiado lento"
        assert trend_time < 2.0, f"El análisis de tendencias tomó {trend_time:.2f} segundos, que es demasiado lento"
        assert impact_time < 2.0, f"El gráfico de impacto tomó {impact_time:.2f} segundos, que es demasiado lento"
        assert kpi_time < 2.0, f"Las métricas KPI tomaron {kpi_time:.2f} segundos, que es demasiado lento"
    
    def test_visualization_data_structure(self):
        """Test estructura de datos de las visualizaciones"""
        heatmap = self.visualizations.create_heatmap_country_month(self.sample_data, self.sample_filters)
        trend = self.visualizations.create_trend_analysis(self.sample_data, self.sample_filters)
        impact = self.visualizations.create_holiday_impact(self.sample_data, self.sample_filters)
        kpi = self.visualizations.create_kpi_metrics(self.sample_data, self.sample_filters)
        
        # Verificar que todas las visualizaciones tienen la estructura esperada
        for viz in [heatmap, trend, impact, kpi]:
            assert hasattr(viz, 'data')
            assert hasattr(viz, 'layout')
            assert hasattr(viz, 'update_layout')
            assert hasattr(viz, 'add_trace')
    
    def test_visualization_with_different_filters(self):
        """Test visualizaciones con diferentes tipos de filtros"""
        # Filtros vacíos
        empty_filters = {}
        heatmap = self.visualizations.create_heatmap_country_month(self.sample_data, empty_filters)
        assert heatmap is not None
        
        # Filtros con valores específicos
        specific_filters = {
            'year_range': [2020, 2020],
            'months': [1],
            'countries': ['USA'],
            'continents': ['North America'],
            'holiday_types': ['Public holiday']
        }
        heatmap = self.visualizations.create_heatmap_country_month(self.sample_data, specific_filters)
        assert heatmap is not None
        
        # Filtros con valores inválidos
        invalid_filters = {
            'year_range': [9999, 9999],
            'months': [99],
            'countries': ['INVALID'],
            'continents': ['INVALID'],
            'holiday_types': ['INVALID']
        }
        heatmap = self.visualizations.create_heatmap_country_month(self.sample_data, invalid_filters)
        assert heatmap is not None
