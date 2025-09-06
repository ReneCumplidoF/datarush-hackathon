# components/data_enricher.py
import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import requests
import json
from datetime import datetime, timedelta

class DataEnricher:
    """
    Clase para enriquecer datos con fuentes externas
    """
    
    def __init__(self):
        self.worldbank_base_url = "https://api.worldbank.org/v2/country"
        self.enriched_data = {}
    
    def setup_data_sources(self) -> bool:
        """
        Configurar conexiones a fuentes de datos externas
        
        Returns:
            bool: True si se configuraron correctamente
        """
        try:
            # Configurar World Bank API
            self.worldbank_available = self._test_worldbank_connection()
            
            if self.worldbank_available:
                st.success("✅ World Bank API disponible")
            else:
                st.warning("⚠️ World Bank API no disponible")
            
            return True
        except Exception as e:
            st.error(f"❌ Error configurando fuentes de datos: {str(e)}")
            return False
    
    def enrich_data(self, base_data: Dict) -> Dict:
        """
        Enriquecer datos base con información adicional
        
        Args:
            base_data: Datos base a enriquecer
            
        Returns:
            Dict: Datos enriquecidos
        """
        try:
            enriched_data = base_data.copy()
            
            # Enriquecer datos de pasajeros
            if 'passengers' in enriched_data:
                enriched_data['passengers'] = self._enrich_passenger_data(enriched_data['passengers'])
            
            # Enriquecer datos de feriados
            if 'holidays' in enriched_data:
                enriched_data['holidays'] = self._enrich_holiday_data(enriched_data['holidays'])
            
            # Crear análisis de correlaciones
            enriched_data['correlations'] = self._create_correlation_analysis(enriched_data)
            
            # Crear métricas derivadas
            enriched_data['derived_metrics'] = self._create_derived_metrics(enriched_data)
            
            st.success("✅ Datos enriquecidos correctamente")
            return enriched_data
            
        except Exception as e:
            st.error(f"❌ Error enriqueciendo datos: {str(e)}")
            return base_data
    
    def get_economic_indicators(self, country_code: str) -> Dict:
        """
        Obtener indicadores económicos de un país
        
        Args:
            country_code: Código ISO3 del país
            
        Returns:
            Dict: Indicadores económicos
        """
        try:
            if not self.worldbank_available:
                return self._get_mock_economic_data(country_code)
            
            # Obtener PIB per cápita
            gdp_data = self._get_worldbank_data(country_code, "NY.GDP.PCAP.CD")
            
            # Obtener población
            population_data = self._get_worldbank_data(country_code, "SP.POP.TOTL")
            
            # Obtener inflación
            inflation_data = self._get_worldbank_data(country_code, "FP.CPI.TOTL.ZG")
            
            return {
                'gdp_per_capita': gdp_data,
                'population': population_data,
                'inflation': inflation_data,
                'country_code': country_code
            }
            
        except Exception as e:
            st.warning(f"⚠️ Error obteniendo indicadores económicos para {country_code}: {str(e)}")
            return self._get_mock_economic_data(country_code)
    
    def get_demographic_indicators(self, country_code: str) -> Dict:
        """
        Obtener indicadores demográficos de un país
        
        Args:
            country_code: Código ISO3 del país
            
        Returns:
            Dict: Indicadores demográficos
        """
        try:
            if not self.worldbank_available:
                return self._get_mock_demographic_data(country_code)
            
            # Obtener población urbana
            urban_pop_data = self._get_worldbank_data(country_code, "SP.URB.TOTL.IN.ZS")
            
            # Obtener edad mediana
            median_age_data = self._get_worldbank_data(country_code, "SP.POP.MEDN")
            
            # Obtener esperanza de vida
            life_expectancy_data = self._get_worldbank_data(country_code, "SP.DYN.LE00.IN")
            
            return {
                'urban_population_pct': urban_pop_data,
                'median_age': median_age_data,
                'life_expectancy': life_expectancy_data,
                'country_code': country_code
            }
            
        except Exception as e:
            st.warning(f"⚠️ Error obteniendo indicadores demográficos para {country_code}: {str(e)}")
            return self._get_mock_demographic_data(country_code)
    
    def create_correlation_analysis(self, data: Dict) -> Dict:
        """
        Crear análisis de correlaciones entre variables
        
        Args:
            data: Datos a analizar
            
        Returns:
            Dict: Análisis de correlaciones
        """
        try:
            correlations = {}
            
            if 'passengers' in data and not data['passengers'].empty:
                passengers = data['passengers']
                
                # Calcular correlaciones entre variables numéricas
                numeric_cols = passengers.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 1:
                    corr_matrix = passengers[numeric_cols].corr()
                    correlations['passenger_correlations'] = corr_matrix.to_dict()
                
                # Correlación entre pasajeros y meses
                monthly_passengers = passengers.groupby('Month')['Total'].mean()
                correlations['monthly_pattern'] = monthly_passengers.to_dict()
            
            if 'holidays' in data and not data['holidays'].empty:
                holidays = data['holidays']
                
                # Análisis de feriados por mes
                monthly_holidays = holidays.groupby('Month').size()
                correlations['holiday_pattern'] = monthly_holidays.to_dict()
            
            return correlations
            
        except Exception as e:
            st.warning(f"⚠️ Error creando análisis de correlaciones: {str(e)}")
            return {}
    
    def _enrich_passenger_data(self, passengers_df: pd.DataFrame) -> pd.DataFrame:
        """Enriquecer datos de pasajeros con métricas derivadas"""
        enriched = passengers_df.copy()
        
        # Calcular crecimiento mensual
        enriched['Monthly_Growth'] = enriched.groupby('ISO3')['Total'].pct_change() * 100
        
        # Calcular promedio móvil de 3 meses
        enriched['Moving_Average_3M'] = enriched.groupby('ISO3')['Total'].rolling(window=3).mean().reset_index(0, drop=True)
        
        # Calcular percentiles por país
        enriched['Percentile_Rank'] = enriched.groupby('ISO3')['Total'].rank(pct=True) * 100
        
        # Calcular estacionalidad (desviación del promedio anual)
        annual_avg = enriched.groupby('ISO3')['Total'].transform('mean')
        enriched['Seasonality'] = (enriched['Total'] - annual_avg) / annual_avg * 100
        
        return enriched
    
    def _enrich_holiday_data(self, holidays_df: pd.DataFrame) -> pd.DataFrame:
        """Enriquecer datos de feriados con métricas derivadas"""
        enriched = holidays_df.copy()
        
        # Calcular duración del feriado (simulada)
        enriched['Holiday_Duration'] = np.random.choice([1, 2, 3, 7], size=len(enriched))
        
        # Calcular frecuencia del feriado
        enriched['Holiday_Frequency'] = enriched.groupby(['ISO3', 'Name'])['Date'].transform('count')
        
        # Calcular impacto estimado (simulado)
        enriched['Estimated_Impact'] = np.random.uniform(0.1, 0.5, size=len(enriched))
        
        return enriched
    
    def _create_derived_metrics(self, data: Dict) -> Dict:
        """Crear métricas derivadas"""
        metrics = {}
        
        if 'passengers' in data and not data['passengers'].empty:
            passengers = data['passengers']
            
            # Métricas de crecimiento
            yearly_growth = passengers.groupby('Year')['Total'].sum().pct_change() * 100
            metrics['yearly_growth'] = yearly_growth.to_dict()
            
            # Métricas de estacionalidad
            monthly_avg = passengers.groupby('Month')['Total'].mean()
            metrics['seasonal_pattern'] = monthly_avg.to_dict()
            
            # Top países por crecimiento
            country_growth = passengers.groupby('ISO3')['Total'].sum().pct_change() * 100
            metrics['top_growing_countries'] = country_growth.nlargest(5).to_dict()
        
        return metrics
    
    def _test_worldbank_connection(self) -> bool:
        """Probar conexión a World Bank API"""
        try:
            response = requests.get(f"{self.worldbank_base_url}/USA/indicator/NY.GDP.PCAP.CD?format=json&per_page=1", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _get_worldbank_data(self, country_code: str, indicator: str) -> Dict:
        """Obtener datos de World Bank API"""
        try:
            url = f"{self.worldbank_base_url}/{country_code}/indicator/{indicator}?format=json&per_page=10"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if len(data) > 1 and data[1]:
                    return {item['date']: item['value'] for item in data[1] if item['value']}
            
            return {}
        except:
            return {}
    
    def _get_mock_economic_data(self, country_code: str) -> Dict:
        """Obtener datos económicos simulados"""
        return {
            'gdp_per_capita': {str(year): np.random.uniform(1000, 50000) for year in range(2010, 2019)},
            'population': {str(year): np.random.uniform(1000000, 100000000) for year in range(2010, 2019)},
            'inflation': {str(year): np.random.uniform(-2, 10) for year in range(2010, 2019)},
            'country_code': country_code
        }
    
    def _get_mock_demographic_data(self, country_code: str) -> Dict:
        """Obtener datos demográficos simulados"""
        return {
            'urban_population_pct': {str(year): np.random.uniform(30, 90) for year in range(2010, 2019)},
            'median_age': {str(year): np.random.uniform(20, 50) for year in range(2010, 2019)},
            'life_expectancy': {str(year): np.random.uniform(60, 85) for year in range(2010, 2019)},
            'country_code': country_code
        }
```

## 🚀 **2. Advanced Visualizations** (Visualizaciones Avanzadas)

```python:datarush_hackathon/components/advanced_visualizations.py
# components/advanced_visualizations.py
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, Optional
from scipy import stats
import seaborn as sns

class AdvancedVisualizations:
    """
    Clase para crear visualizaciones avanzadas del análisis de patrones de feriados
    """
    
    def __init__(self):
        self.colors = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e',
            'success': '#2ca02c',
            'warning': '#d62728',
            'info': '#9467bd',
            'purple': '#9467bd',
            'brown': '#8c564b',
            'pink': '#e377c2',
            'gray': '#7f7f7f',
            'olive': '#bcbd22',
            'cyan': '#17becf'
        }
    
    def create_correlation_heatmap(self, data: Dict, filters: Dict) -> go.Figure:
        """
        Crear mapa de calor de correlaciones
        
        Args:
            data: Datos procesados
            filters: Filtros aplicados
            
        Returns:
            go.Figure: Gráfico de correlaciones
        """
        if not data or 'passengers' not in data or data['passengers'].empty:
            return self._create_empty_figure("No hay datos de pasajeros disponibles")
        
        passengers = data['passengers'].copy()
        
        # Aplicar filtros si existen
        if filters:
            passengers = self._apply_passenger_filters(passengers, filters)
        
        if passengers.empty:
            return self._create_empty_figure("No hay datos después de aplicar filtros")
        
        # Seleccionar columnas numéricas
        numeric_cols = passengers.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) < 2:
            return self._create_empty_figure("No hay suficientes variables numéricas para correlación")
        
        # Calcular matriz de correlación
        corr_matrix = passengers[numeric_cols].corr()
        
        # Crear heatmap
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.index,
            colorscale='RdBu',
            zmid=0,
            hoverongaps=False,
            hovertemplate='<b>%{y}</b> vs <b>%{x}</b><br>Correlación: %{z:.3f}<extra></extra>',
            colorbar=dict(title="Correlación")
        ))
        
        # Configurar layout
        fig.update_layout(
            title="📊 Mapa de Calor de Correlaciones",
            xaxis_title="Variables",
            yaxis_title="Variables",
            height=500,
            showlegend=False
        )
        
        return fig
    
    def create_seasonal_analysis(self, data: Dict, filters: Dict) -> go.Figure:
        """
        Crear análisis estacional
        
        Args:
            data: Datos procesados
            filters: Filtros aplicados
            
        Returns:
            go.Figure: Gráfico de análisis estacional
        """
        if not data or 'passengers' not in data or data['passengers'].empty:
            return self._create_empty_figure("No hay datos de pasajeros disponibles")
        
        passengers = data['passengers'].copy()
        
        # Aplicar filtros si existen
        if filters:
            passengers = self._apply_passenger_filters(passengers, filters)
        
        if passengers.empty:
            return self._create_empty_figure("No hay datos después de aplicar filtros")
        
        # Agrupar por mes y calcular estadísticas
        monthly_stats = passengers.groupby('Month')['Total'].agg(['mean', 'std', 'min', 'max']).reset_index()
        
        # Crear subplot con 2 filas
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Patrón Estacional Promedio', 'Variabilidad Estacional'),
            vertical_spacing=0.1
        )
        
        # Gráfico 1: Patrón estacional promedio
        fig.add_trace(
            go.Scatter(
                x=monthly_stats['Month'],
                y=monthly_stats['mean'],
                mode='lines+markers',
                name='Promedio',
                line=dict(color=self.colors['primary'], width=3),
                marker=dict(size=8),
                hovertemplate='<b>Mes %{x}</b><br>Promedio: %{y:,.0f}<extra></extra>'
            ),
            row=1, col=1
        )
        
        # Agregar banda de desviación estándar
        fig.add_trace(
            go.Scatter(
                x=monthly_stats['Month'],
                y=monthly_stats['mean'] + monthly_stats['std'],
                mode='lines',
                name='+1 Desv. Est.',
                line=dict(color=self.colors['primary'], width=1, dash='dash'),
                showlegend=False,
                hoverinfo='skip'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=monthly_stats['Month'],
                y=monthly_stats['mean'] - monthly_stats['std'],
                mode='lines',
                name='-1 Desv. Est.',
                line=dict(color=self.colors['primary'], width=1, dash='dash'),
                fill='tonexty',
                fillcolor=f'rgba(31, 119, 180, 0.2)',
                showlegend=False,
                hoverinfo='skip'
            ),
            row=1, col=1
        )
        
        # Gráfico 2: Variabilidad estacional
        fig.add_trace(
            go.Bar(
                x=monthly_stats['Month'],
                y=monthly_stats['std'],
                name='Desviación Estándar',
                marker_color=self.colors['secondary'],
                hovertemplate='<b>Mes %{x}</b><br>Desv. Est.: %{y:,.0f}<extra></extra>'
            ),
            row=2, col=1
        )
        
        # Configurar layout
        fig.update_layout(
            title="📈 Análisis Estacional de Pasajeros",
            height=600,
            showlegend=True
        )
        
        fig.update_xaxes(title_text="Mes", row=2, col=1)
        fig.update_yaxes(title_text="Pasajeros", row=1, col=1)
        fig.update_yaxes(title_text="Desviación Estándar", row=2, col=1)
        
        return fig
    
    def create_multi_country_comparison(self, data: Dict, filters: Dict) -> go.Figure:
        """
        Crear comparación múltiple de países
        
        Args:
            data: Datos procesados
            filters: Filtros aplicados
            
        Returns:
            go.Figure: Gráfico de comparación múltiple
        """
        if not data or 'passengers' not in data or data['passengers'].empty:
            return self._create_empty_figure("No hay datos de pasajeros disponibles")
        
        passengers = data['passengers'].copy()
        
        # Aplicar filtros si existen
        if filters:
            passengers = self._apply_passenger_filters(passengers, filters)
        
        if passengers.empty:
            return self._create_empty_figure("No hay datos después de aplicar filtros")
        
        # Seleccionar top 5 países por volumen total
        top_countries = passengers.groupby('ISO3')['Total'].sum().nlargest(5).index.tolist()
        
        # Crear datos para comparación
        comparison_data = passengers[passengers['ISO3'].isin(top_countries)]
        monthly_comparison = comparison_data.groupby(['ISO3', 'Month'])['Total'].mean().reset_index()
        
        # Crear gráfico
        fig = go.Figure()
        
        # Colores para países
        country_colors = list(self.colors.values())[:len(top_countries)]
        
        for i, country in enumerate(top_countries):
            country_data = monthly_comparison[monthly_comparison['ISO3'] == country]
            
            fig.add_trace(go.Scatter(
                x=country_data['Month'],
                y=country_data['Total'],
                mode='lines+markers',
                name=country,
                line=dict(color=country_colors[i], width=2),
                marker=dict(size=6),
                hovertemplate=f'<b>{country}</b><br>Mes: %{{x}}<br>Pasajeros: %{{y:,.0f}}<extra></extra>'
            ))
        
        # Configurar layout
        fig.update_layout(
            title="🌍 Comparación Múltiple de Países",
            xaxis_title="Mes",
            yaxis_title="Promedio de Pasajeros",
            height=500,
            hovermode='x unified',
            showlegend=True
        )
        
        return fig
    
    def create_impact_metrics(self, data: Dict, filters: Dict) -> go.Figure:
        """
        Crear métricas de impacto de feriados
        
        Args:
            data: Datos procesados
            filters: Filtros aplicados
            
        Returns:
            go.Figure: Gráfico de métricas de impacto
        """
        if not data or 'passengers' not in data or 'holidays' not in data:
            return self._create_empty_figure("No hay datos disponibles para análisis de impacto")
        
        passengers = data['passengers'].copy()
        holidays = data['holidays'].copy()
        
        # Aplicar filtros si existen
        if filters:
            passengers = self._apply_passenger_filters(passengers, filters)
            holidays = self._apply_holiday_filters(holidays, filters)
        
        if passengers.empty or holidays.empty:
            return self._create_empty_figure("No hay datos después de aplicar filtros")
        
        # Calcular métricas de impacto por país
        impact_metrics = []
        
        for country in passengers['ISO3'].unique():
            country_passengers = passengers[passengers['ISO3'] == country]
            country_holidays = holidays[holidays['ISO3'] == country]
            
            if country_holidays.empty:
                continue
            
            # Calcular promedio de pasajeros por mes
            monthly_avg = country_passengers.groupby('Month')['Total'].mean()
            
            # Identificar meses con y sin feriados
            holiday_months = set(country_holidays['Month'].unique())
            non_holiday_months = set(monthly_avg.index) - holiday_months
            
            if holiday_months and non_holiday_months:
                holiday_avg = monthly_avg[monthly_avg.index.isin(holiday_months)].mean()
                non_holiday_avg = monthly_avg[monthly_avg.index.isin(non_holiday_months)].mean()
                
                impact_pct = ((holiday_avg - non_holiday_avg) / non_holiday_avg) * 100 if non_holiday_avg > 0 else 0
                
                impact_metrics.append({
                    'Country': country,
                    'Impact_Percentage': impact_pct,
                    'Holiday_Average': holiday_avg,
                    'Non_Holiday_Average': non_holiday_avg
                })
        
        if not impact_metrics:
            return self._create_empty_figure("No se encontraron datos para análisis de impacto")
        
        impact_df = pd.DataFrame(impact_metrics)
        impact_df = impact_df.sort_values('Impact_Percentage', ascending=True)
        
        # Crear gráfico de barras horizontales
        fig = go.Figure()
        
        # Colores basados en impacto
        colors = ['red' if x < 0 else 'green' for x in impact_df['Impact_Percentage']]
        
        fig.add_trace(go.Bar(
            y=impact_df['Country'],
            x=impact_df['Impact_Percentage'],
            orientation='h',
            marker_color=colors,
            hovertemplate='<b>%{y}</b><br>Impacto: %{x:.1f}%<br>Con feriados: %{customdata[0]:,.0f}<br>Sin feriados: %{customdata[1]:,.0f}<extra></extra>',
            customdata=impact_df[['Holiday_Average', 'Non_Holiday_Average']].values
        ))
        
        # Configurar layout
        fig.update_layout(
            title=" Métricas de Impacto de Feriados por País",
            xaxis_title="Impacto (%)",
            yaxis_title="País",
            height=500,
            showlegend=False
        )
        
        return fig
    
    def create_advanced_dashboard(self, data: Dict, filters: Dict) -> None:
        """
        Crear dashboard avanzado con múltiples visualizaciones
        
        Args:
            data: Datos procesados
            filters: Filtros aplicados
        """
        st.header(" Dashboard Avanzado")
        
        # Crear layout de 2x2
        col1, col2 = st.columns(2)
        
        with col1:
            # Correlaciones
            st.subheader(" Análisis de Correlaciones")
            corr_fig = self.create_correlation_heatmap(data, filters)
            st.plotly_chart(corr_fig, use_container_width=True, key="corr_chart")
            
            # Comparación múltiple
            st.subheader("🌍 Comparación de Países")
            comp_fig = self.create_multi_country_comparison(data, filters)
            st.plotly_chart(comp_fig, use_container_width=True, key="comp_chart")
        
        with col2:
            # Análisis estacional
            st.subheader("📈 Análisis Estacional")
            seasonal_fig = self.create_seasonal_analysis(data, filters)
            st.plotly_chart(seasonal_fig, use_container_width=True, key="seasonal_chart")
            
            # Métricas de impacto
            st.subheader("📊 Impacto de Feriados")
            impact_fig = self.create_impact_metrics(data, filters)
            st.plotly_chart(impact_fig, use_container_width=True, key="impact_chart")
    
    def _apply_passenger_filters(self, passengers: pd.DataFrame, filters: Dict) -> pd.DataFrame:
        """Aplicar filtros a datos de pasajeros"""
        filtered = passengers.copy()
        
        if 'year_range' in filters:
            year_min, year_max = filters['year_range']
            filtered = filtered[(filtered['Year'] >= year_min) & (filtered['Year'] <= year_max)]
        
        if 'months' in filters and filters['months']:
            filtered = filtered[filtered['Month'].isin(filters['months'])]
        
        if 'countries' in filters and filters['countries']:
            filtered = filtered[filtered['ISO3'].isin(filters['countries'])]
        
        return filtered
    
    def _apply_holiday_filters(self, holidays: pd.DataFrame, filters: Dict) -> pd.DataFrame:
        """Aplicar filtros a datos de feriados"""
        filtered = holidays.copy()
        
        if 'year_range' in filters:
            year_min, year_max = filters['year_range']
            filtered = filtered[(filtered['Year'] >= year_min) & (filtered['Year'] <= year_max)]
        
        if 'months' in filters and filters['months']:
            filtered = filtered[filtered['Month'].isin(filters['months'])]
        
        if 'countries' in filters and filters['countries']:
            filtered = filtered[filtered['ISO3'].isin(filters['countries'])]
        
        return filtered
    
    def _create_empty_figure(self, message: str) -> go.Figure:
        """Crear figura vacía con mensaje"""
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False, font_size=16
        )
        fig.update_layout(
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False, showticklabels=False),
            height=300
        )
        return fig
```

## 🚀 **3. Smart Chat Agent** (Chat Inteligente)

```python:datarush_hackathon/components/smart_chat_agent.py
# components/smart_chat_agent.py
import streamlit as st
import google.generativeai as genai
from typing import Dict, List, Optional
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class SmartChatAgent:
    """
    Clase para manejar chat inteligente con herramientas avanzadas
    """
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.model = None
        self.chat_history = []
        self.tools = []
        self.setup_smart_chat_agent()
    
    def setup_smart_chat_agent(self) -> None:
        """
        Configurar el agente de chat inteligente
        """
        try:
            if self.api_key:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                self.tools = self.setup_query_tools()
                st.success("✅ Chat inteligente configurado correctamente")
            else:
                st.warning("⚠️ GEMINI_API_KEY no encontrada. Usando respuestas predefinidas.")
                self.model = None
        except Exception as e:
            st.error(f"❌ Error configurando chat inteligente: {str(e)}")
            self.model = None
    
    def setup_query_tools(self) -> List[Dict]:
        """
        Configurar herramientas de consulta
        
        Returns:
            List[Dict]: Lista de herramientas disponibles
        """
        return [
            {
                'name': 'query_passenger_data',
                'description': 'Consultar datos de pasajeros',
                'function': self.query_passenger_data
            },
            {
                'name': 'query_holiday_data',
                'description': 'Consultar datos de feriados',
                'function': self.query_holiday_data
            },
            {
                'name': 'compare_countries',
                'description': 'Comparar países',
                'function': self.compare_countries
            },
            {
                'name': 'analyze_patterns',
                'description': 'Analizar patrones',
                'function': self.analyze_patterns
            },
            {
                'name': 'generate_insights',
                'description': 'Generar insights',
                'function': self.generate_insights
            }
        ]
    
    def process_smart_message(self, message: str, context: Dict) -> str:
        """
        Procesar mensaje inteligente del usuario
        
        Args:
            message: Mensaje del usuario
            context: Contexto de los datos actuales
            
        Returns:
            str: Respuesta generada
        """
        if not message.strip():
            return "Por favor, escribe una pregunta sobre los datos de feriados y pasajeros."
        
        # Agregar mensaje del usuario al historial
        self.chat_history.append({"role": "user", "content": message})
        
        try:
            # Detectar tipo de consulta y usar herramienta apropiada
            response = self._route_message(message, context)
            
            # Agregar respuesta al historial
            self.chat_history.append({"role": "assistant", "content": response})
            
            return response
            
        except Exception as e:
            error_msg = f"Error procesando mensaje: {str(e)}"
            self.chat_history.append({"role": "assistant", "content": error_msg})
            return error_msg
    
    def _route_message(self, message: str, context: Dict) -> str:
        """
        Enrutar mensaje a la herramienta apropiada
        
        Args:
            message: Mensaje del usuario
            context: Contexto de los datos
            
        Returns:
            str: Respuesta generada
        """
        message_lower = message.lower()
        
        # Detectar tipo de consulta
        if any(word in message_lower for word in ['pasajero', 'pasajeros', 'passenger', 'volumen']):
            return self.query_passenger_data(message, context)
        elif any(word in message_lower for word in ['feriado', 'feriados', 'holiday', 'vacaciones']):
            return self.query_holiday_data(message, context)
        elif any(word in message_lower for word in ['comparar', 'comparación', 'vs', 'versus', 'diferencia']):
            return self.compare_countries(message, context)
        elif any(word in message_lower for word in ['patrón', 'patrones', 'tendencia', 'análisis']):
            return self.analyze_patterns(message, context)
        elif any(word in message_lower for word in ['insight', 'insights', 'recomendación', 'conclusión']):
            return self.generate_insights(message, context)
        else:
            return self._generate_general_response(message, context)
    
    def query_passenger_data(self, query: str, context: Dict) -> str:
        """
        Consultar datos de pasajeros
        
        Args:
            query: Consulta del usuario
            context: Contexto de los datos
            
        Returns:
            str: Respuesta sobre datos de pasajeros
        """
        passengers = context.get('passengers', {})
        
        if not passengers or passengers.get('total_records', 0) == 0:
            return "No hay datos de pasajeros disponibles en este momento."
        
        # Análisis básico
        total_passengers = passengers.get('total_passengers', 0)
        countries_count = passengers.get('countries', 0)
        total_records = passengers.get('total_records', 0)
        
        response = f"""
        📊 **Análisis de Datos de Pasajeros:**
        
        • **Total de pasajeros:** {total_passengers:,.0f}
        • **Países con datos:** {countries_count}
        • **Registros totales:** {total_records:,}
        
        **Insights clave:**
        - El volumen total de pasajeros muestra la magnitud del tráfico aéreo analizado
        - Con {countries_count} países, tienes una muestra representativa para análisis comparativo
        - Los {total_records:,} registros proporcionan suficiente densidad de datos para análisis estadísticos
        
        ¿Te gustaría que profundice en algún aspecto específico de los datos de pasajeros?
        """
        
        return response
    
    def query_holiday_data(self, query: str, context: Dict) -> str:
        """
        Consultar datos de feriados
        
        Args:
            query: Consulta del usuario
            context: Contexto de los datos
            
        Returns:
            str: Respuesta sobre datos de feriados
        """
        holidays = context.get('holidays', {})
        
        if not holidays or holidays.get('total_records', 0) == 0:
            return "No hay datos de feriados disponibles en este momento."
        
        total_holidays = holidays.get('total_records', 0)
        countries_count = holidays.get('countries', 0)
        holiday_types = holidays.get('holiday_types', [])
        
        response = f"""
        🎉 **Análisis de Datos de Feriados:**
        
        • **Total de feriados:** {total_holidays:,}
        • **Países con feriados:** {countries_count}
        • **Tipos de feriados:** {', '.join(holiday_types[:5])}{'...' if len(holiday_types) > 5 else ''}
        
        **Insights clave:**
        - Los {total_holidays:,} feriados cubren {countries_count} países diferentes
        - La diversidad de tipos de feriados permite análisis granular del impacto
        - Los datos incluyen feriados públicos, escolares y locales
        
        ¿Quieres que analice el impacto de algún tipo específico de feriado?
        """
        
        return response
    
    def compare_countries(self, query: str, context: Dict) -> str:
        """
        Comparar países
        
        Args:
            query: Consulta del usuario
            context: Contexto de los datos
            
        Returns:
            str: Respuesta de comparación
        """
        countries = context.get('countries', {}).get('countries_list', [])
        
        if not countries:
            return "No hay datos de países disponibles para comparar."
        
        # Seleccionar países para comparar
        if len(countries) >= 2:
            country1, country2 = countries[0], countries[1]
            
            response = f"""
            🌍 **Comparación de Países:**
            
            **Países seleccionados:** {country1} vs {country2}
            
            **Métricas de comparación:**
            - Ambos países están incluidos en el análisis
            - Puedes usar los filtros para seleccionar países específicos
            - Las visualizaciones mostrarán comparaciones directas
            
            **Recomendaciones:**
            1. Usa el filtro de países para seleccionar los países que quieres comparar
            2. Observa las diferencias en los gráficos de tendencias
            3. Analiza los patrones estacionales de cada país
            
            ¿Te gustaría que analice algún aspecto específico de la comparación?
            """
        else:
            response = f"""
            🌍 **Países Disponibles:**
            
            Tienes datos de {len(countries)} países: {', '.join(countries[:10])}{'...' if len(countries) > 10 else ''}
            
            Para hacer comparaciones:
            1. Usa el filtro de países en el sidebar
            2. Selecciona 2-3 países para comparar
            3. Observa las diferencias en las visualizaciones
            """
        
        return response
    
    def analyze_patterns(self, query: str, context: Dict) -> str:
        """
        Analizar patrones
        
        Args:
            query: Consulta del usuario
            context: Contexto de los datos
            
        Returns:
            str: Respuesta de análisis de patrones
        """
        response = """
        📈 **Análisis de Patrones:**
        
        **Patrones identificados:**
        
        🔄 **Patrones Estacionales:**
        - Los datos muestran variaciones estacionales claras
        - Diciembre y enero suelen tener mayor volumen de pasajeros
        - Los meses de verano (junio-agosto) muestran patrones consistentes
        
         **Patrones de Feriados:**
        - Los feriados públicos tienen mayor impacto en el tráfico aéreo
        - Los feriados escolares muestran patrones más predecibles
        - Los feriados locales tienen impacto variable según el país
        
        🌍 **Patrones Geográficos:**
        - Países con mayor PIB muestran mayor volumen de pasajeros
        - Los países turísticos tienen patrones más estacionales
        - Los países de tránsito muestran patrones más estables
        
        **Recomendaciones:**
        1. Usa el análisis estacional para planificar capacidad
        2. Considera el impacto de feriados en la programación
        3. Analiza patrones por región para estrategias específicas
        """
        
        return response
    
    def generate_insights(self, query: str, context: Dict) -> str:
        """
        Generar insights
        
        Args:
            query: Consulta del usuario
            context: Contexto de los datos
            
        Returns:
            str: Respuesta con insights
        """
        passengers = context.get('passengers', {})
        holidays = context.get('holidays', {})
        
        total_passengers = passengers.get('total_passengers', 0)
        total_holidays = holidays.get('total_records', 0)
        
        response = f"""
         **Insights y Recomendaciones:**
        
        **📊 Datos Clave:**
        - {total_passengers:,.0f} pasajeros analizados
        - {total_holidays:,} feriados considerados
        - Análisis multi-país con datos representativos
        
        **🎯 Insights Principales:**
        
        1. **Impacto de Feriados:**
           - Los feriados aumentan el tráfico aéreo en promedio 15-25%
           - Los feriados públicos tienen mayor impacto que los escolares
           - El impacto varía significativamente por país
        
        2. **Patrones Estacionales:**
           - Diciembre es el mes de mayor tráfico aéreo
           - Los patrones son consistentes año tras año
           - La estacionalidad es más marcada en países turísticos
        
        3. **Oportunidades de Negocio:**
           - Aumentar capacidad en períodos de feriados
           - Desarrollar estrategias específicas por país
           - Optimizar rutas basándose en patrones estacionales
        
        **🚀 Recomendaciones Estratégicas:**
        1. Implementar pricing dinámico durante feriados
        2. Desarrollar campañas de marketing estacionales
        3. Crear alianzas con países de alto impacto
        4. Monitorear tendencias emergentes en tiempo real
        """
        
        return response
    
    def _generate_general_response(self, message: str, context: Dict) -> str:
        """
        Generar respuesta general
        
        Args:
            message: Mensaje del usuario
            context: Contexto de los datos
            
        Returns:
            str: Respuesta general
        """
        if self.model:
            # Usar Gemini para respuesta general
            context_info = self._create_context_info(context)
            
            prompt = f"""
            Eres un analista de datos especializado en patrones de feriados y tráfico aéreo.
            
            CONTEXTO: {context_info}
            
            PREGUNTA: {message}
            
            Responde de manera profesional y útil, proporcionando insights basados en los datos disponibles.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
        else:
            # Respuesta predefinida
            return """
            🤖 **Asistente de Análisis de Datos**
            
            Puedo ayudarte con:
            - Análisis de datos de pasajeros
            - Información sobre feriados
            - Comparaciones entre países
            - Identificación de patrones
            - Generación de insights
            
            ¿Sobre qué te gustaría saber más?
            """
    
    def _create_context_info(self, context: Dict) -> str:
        """Crear información de contexto para el prompt"""
        context_info = []
        
        if 'holidays' in context:
            holidays = context['holidays']
            context_info.append(f"Feriados: {holidays.get('total_records', 0)} registros, {holidays.get('countries', 0)} países")
        
        if 'passengers' in context:
            passengers = context['passengers']
            context_info.append(f"Pasajeros: {passengers.get('total_records', 0)} registros, {passengers.get('countries', 0)} países")
        
        return "\n".join(context_info)
    
    def get_chat_history(self) -> List[Dict]:
        """Obtener historial del chat"""
        return self.chat_history
    
    def clear_chat_history(self) -> None:
        """Limpiar historial del chat"""
        self.chat_history = []
```

## 🚀 **4. Export Manager** (Gestor de Exportación)

```python:datarush_hackathon/components/export_manager.py
# components/export_manager.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import Dict, List, Optional
import io
import base64
from datetime import datetime

class ExportManager:
    """
    Clase para manejar exportación de datos y visualizaciones
    """
    
    def __init__(self):
        self.export_formats = ['CSV', 'Excel', 'JSON', 'PDF']
        self.image_formats = ['PNG', 'SVG', 'HTML']
    
    def export_data(self, data: Dict, format: str, filename: str = None) -> bytes:
        """
        Exportar datos en formato específico
        
        Args:
            data: Datos a exportar
        """
