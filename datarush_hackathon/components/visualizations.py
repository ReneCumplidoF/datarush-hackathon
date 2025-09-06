# components/visualizations.py
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, Optional
import numpy as np

class Visualizations:
    """
    Clase para crear visualizaciones del análisis de patrones de feriados
    """
    
    def __init__(self):
        self.colors = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e',
            'success': '#2ca02c',
            'warning': '#d62728',
            'info': '#9467bd'
        }
    
    def create_heatmap_country_month(self, data: Dict, filters: Dict) -> go.Figure:
        """
        Crear mapa de calor: Países vs Meses
        
        Args:
            data: Datos procesados
            filters: Filtros aplicados
            
        Returns:
            go.Figure: Gráfico de mapa de calor
        """
        if not data or 'passengers' not in data or data['passengers'].empty:
            return self._create_empty_figure("No hay datos de pasajeros disponibles")
        
        passengers = data['passengers'].copy()
        
        # Verificar que tenemos datos válidos
        if passengers['Total'].isna().all() or passengers['Total'].sum() == 0:
            return self._create_empty_figure("Los datos de pasajeros no contienen valores válidos")
        
        # Aplicar filtros si existen
        if filters:
            passengers = self._apply_passenger_filters(passengers, filters)
        
        if passengers.empty:
            return self._create_empty_figure("No hay datos después de aplicar filtros")
        
        # Agrupar por país y mes
        heatmap_data = passengers.groupby(['ISO3', 'Month'])['Total'].sum().reset_index()
        
        if heatmap_data.empty:
            return self._create_empty_figure("No hay datos después de aplicar filtros")
        
        # Crear pivot table para el heatmap
        pivot_data = heatmap_data.pivot(index='ISO3', columns='Month', values='Total')
        
        # Crear el heatmap
        fig = go.Figure(data=go.Heatmap(
            z=pivot_data.values,
            x=pivot_data.columns,
            y=pivot_data.index,
            colorscale='Viridis',
            hoverongaps=False,
            hovertemplate='<b>%{y}</b><br>Mes: %{x}<br>Pasajeros: %{z:,.0f}<extra></extra>',
            colorbar=dict(title="Pasajeros")
        ))
        
        # Configurar layout
        fig.update_layout(
            title=" Mapa de Calor: Patrones Estacionales por País",
            xaxis_title="Mes",
            yaxis_title="País (ISO3)",
            height=600,
            showlegend=False
        )
        
        return fig
    
    def create_trend_analysis(self, data: Dict, filters: Dict) -> go.Figure:
        """
        Crear gráfico de líneas: Tendencias Temporales
        
        Args:
            data: Datos procesados
            filters: Filtros aplicados
            
        Returns:
            go.Figure: Gráfico de tendencias
        """
        if not data or 'passengers' not in data or data['passengers'].empty:
            return self._create_empty_figure("No hay datos de pasajeros disponibles")
        
        passengers = data['passengers'].copy()
        
        # Verificar que tenemos datos válidos
        if passengers['Total'].isna().all() or passengers['Total'].sum() == 0:
            return self._create_empty_figure("Los datos de pasajeros no contienen valores válidos")
        
        # Aplicar filtros si existen
        if filters:
            passengers = self._apply_passenger_filters(passengers, filters)
        
        if passengers.empty:
            return self._create_empty_figure("No hay datos después de aplicar filtros")
        
        # Agrupar por año y mes para tendencia mensual
        monthly_trend = passengers.groupby(['Year', 'Month'])['Total'].sum().reset_index()
        monthly_trend['Date'] = pd.to_datetime(monthly_trend[['Year', 'Month']].assign(Day=1))
        
        # Crear el gráfico de líneas
        fig = go.Figure()
        
        # Línea principal de tendencia
        fig.add_trace(go.Scatter(
            x=monthly_trend['Date'],
            y=monthly_trend['Total'],
            mode='lines+markers',
            name='Total Pasajeros',
            line=dict(color=self.colors['primary'], width=3),
            marker=dict(size=6),
            hovertemplate='<b>%{x|%Y-%m}</b><br>Pasajeros: %{y:,.0f}<extra></extra>'
        ))
        
        # Agregar línea de tendencia suavizada
        if len(monthly_trend) > 1:
            z = np.polyfit(range(len(monthly_trend)), monthly_trend['Total'], 1)
            p = np.poly1d(z)
            fig.add_trace(go.Scatter(
                x=monthly_trend['Date'],
                y=p(range(len(monthly_trend))),
                mode='lines',
                name='Tendencia',
                line=dict(color=self.colors['warning'], width=2, dash='dash'),
                hovertemplate='<b>Tendencia</b><br>%{x|%Y-%m}<br>%{y:,.0f}<extra></extra>'
            ))
        
        # Configurar layout
        fig.update_layout(
            title=" Análisis de Tendencias Temporales",
            xaxis_title="Fecha",
            yaxis_title="Total de Pasajeros",
            height=400,
            hovermode='x unified',
            showlegend=True
        )
        
        return fig
    
    def create_holiday_impact(self, data: Dict, filters: Dict, max_countries: int = None) -> go.Figure:
        """
        Crear gráfico de barras: Top Países por Volumen de Pasajeros
        
        Args:
            data: Datos procesados
            filters: Filtros aplicados
            max_countries: Número máximo de países a mostrar (None = todos)
            
        Returns:
            go.Figure: Gráfico de impacto de feriados
        """
        if not data or 'passengers' not in data:
            return self._create_empty_figure("No hay datos de pasajeros disponibles")
        
        passengers = data['passengers'].copy()
        
        # Verificar que tenemos datos válidos de pasajeros
        if passengers.empty or passengers['Total'].isna().all() or passengers['Total'].sum() == 0:
            return self._create_empty_figure("Los datos de pasajeros no contienen valores válidos")
        
        # Aplicar filtros si existen
        if filters:
            passengers = self._apply_passenger_filters(passengers, filters)
        
        if passengers.empty:
            return self._create_empty_figure("No hay datos de pasajeros después de aplicar filtros")
        
        # Crear análisis simple: Top países por volumen total
        country_analysis = passengers.groupby('ISO3')['Total'].agg(['sum', 'mean', 'count']).reset_index()
        country_analysis.columns = ['Country', 'Total_Passengers', 'Avg_Passengers', 'Records']
        
        # Debug: Mostrar información sobre los datos
        st.write(f"🔍 Debug: Total países encontrados: {len(country_analysis)}")
        st.write(f"🔍 Debug: Países con datos: {country_analysis['Country'].tolist()[:10]}...")
        
        # NO filtrar por Records - mostrar todos los países
        # country_analysis = country_analysis[country_analysis['Records'] >= 3]  # ELIMINADO
        
        if country_analysis.empty:
            return self._create_empty_figure("No hay países con datos")
        
        # Ordenar por total de pasajeros
        country_analysis = country_analysis.sort_values('Total_Passengers', ascending=False)
        
        # Limitar número de países si es necesario
        if max_countries:
            country_analysis = country_analysis.head(max_countries)
        
        # Crear el gráfico de barras
        fig = go.Figure()
        
        # Barra principal
        fig.add_trace(go.Bar(
            x=country_analysis['Country'],
            y=country_analysis['Total_Passengers'],
            name='Total Pasajeros',
            marker_color=self.colors['primary'],
            hovertemplate='<b>%{x}</b><br>Total Pasajeros: %{y:,.0f}<br>Promedio: %{customdata:,.0f}<extra></extra>',
            customdata=country_analysis['Avg_Passengers']
        ))
        
        # Configurar layout
        title = "✈️ Top Países por Volumen de Pasajeros"
        if max_countries:
            title += f" (Top {max_countries})"
        else:
            title += f" ({len(country_analysis)} países)"
        
        fig.update_layout(
            title=title,
            xaxis_title="País (ISO3)",
            yaxis_title="Total de Pasajeros",
            height=500,
            hovermode='x unified'
        )
        
        return fig
    
    def create_kpi_metrics(self, data: Dict, filters: Dict) -> Dict:
        """
        Crear métricas KPI
        
        Args:
            data: Datos procesados
            filters: Filtros aplicados
            
        Returns:
            Dict: Métricas KPI
        """
        if not data:
            return {}
        
        passengers = data.get('passengers', pd.DataFrame())
        holidays = data.get('holidays', pd.DataFrame())
        
        # Aplicar filtros si existen
        if filters and not passengers.empty:
            passengers = self._apply_passenger_filters(passengers, filters)
        if filters and not holidays.empty:
            holidays = self._apply_holiday_filters(holidays, filters)
        
        # Calcular métricas
        metrics = {}
        
        if not passengers.empty and not passengers['Total'].isna().all():
            # Métricas de pasajeros
            metrics['total_passengers'] = passengers['Total'].sum()
            metrics['avg_passengers'] = passengers['Total'].mean()
            metrics['max_passengers'] = passengers['Total'].max()
            metrics['countries_with_data'] = passengers['ISO3'].nunique()
            
            # Crecimiento interanual
            if 'Year' in passengers.columns:
                yearly_data = passengers.groupby('Year')['Total'].sum()
                if len(yearly_data) > 1:
                    growth = ((yearly_data.iloc[-1] - yearly_data.iloc[0]) / yearly_data.iloc[0]) * 100
                    metrics['yearly_growth'] = growth
        
        if not holidays.empty:
            # Métricas de feriados
            metrics['total_holidays'] = len(holidays)
            metrics['countries_with_holidays'] = holidays['ISO3'].nunique()
            metrics['holiday_types'] = holidays['Type'].nunique()
            
            # Feriados por mes
            if 'Month' in holidays.columns:
                monthly_holidays = holidays.groupby('Month').size()
                metrics['peak_holiday_month'] = monthly_holidays.idxmax()
                metrics['peak_holiday_count'] = monthly_holidays.max()
        
        return metrics
    
    def update_visualizations(self, data: Dict, filters: Dict) -> None:
        """
        Actualizar todas las visualizaciones
        
        Args:
            data: Datos procesados
            filters: Filtros aplicados
        """
        # Crear layout de columnas
        col1, col2 = st.columns(2)
        
        with col1:
            # Mapa de calor
            st.subheader("🌍 Patrones Estacionales")
            heatmap_fig = self.create_heatmap_country_month(data, filters)
            st.plotly_chart(heatmap_fig, use_container_width=True, key="heatmap_chart")
            
            # Análisis de tendencias
            st.subheader("📈 Tendencias Temporales")
            trend_fig = self.create_trend_analysis(data, filters)
            st.plotly_chart(trend_fig, use_container_width=True, key="trend_chart")
        
        with col2:
            # Top países por volumen
            st.subheader("✈️ Top Países por Volumen")
            
            # Control para número de países
            col2_1, col2_2 = st.columns([2, 1])
            with col2_1:
                max_countries = st.selectbox(
                    "Países a mostrar:",
                    options=[10, 20, 50, 100, None],
                    index=0,
                    format_func=lambda x: f"Top {x}" if x else "Todos",
                    help="Selecciona cuántos países mostrar en el gráfico"
                )
            with col2_2:
                st.write("")  # Espacio en blanco para alineación
            
            impact_fig = self.create_holiday_impact(data, filters, max_countries)
            st.plotly_chart(impact_fig, use_container_width=True, key="impact_chart")
            
            # Métricas KPI
            st.subheader("📊 Métricas Clave")
            metrics = self.create_kpi_metrics(data, filters)
            self._display_kpi_metrics(metrics)
    
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
        
        if 'passenger_range' in filters:
            min_pass, max_pass = filters['passenger_range']
            filtered = filtered[(filtered['Total'] >= min_pass) & (filtered['Total'] <= max_pass)]
        
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
        
        if 'holiday_types' in filters and filters['holiday_types']:
            filtered = filtered[filtered['Type'].isin(filters['holiday_types'])]
        
        return filtered
    
    def _display_kpi_metrics(self, metrics: Dict) -> None:
        """Mostrar métricas KPI en formato de cards"""
        if not metrics:
            st.warning("No hay métricas disponibles")
            return
        
        # Crear columnas para las métricas
        cols = st.columns(2)
        
        with cols[0]:
            if 'total_passengers' in metrics:
                st.metric(
                    "Total Pasajeros",
                    f"{metrics['total_passengers']:,.0f}",
                    delta=f"{metrics.get('yearly_growth', 0):.1f}%" if 'yearly_growth' in metrics else None
                )
            
            if 'countries_with_data' in metrics:
                st.metric("Países con Datos", metrics['countries_with_data'])
        
        with cols[1]:
            if 'total_holidays' in metrics:
                st.metric("Total Feriados", metrics['total_holidays'])
            
            if 'peak_holiday_month' in metrics:
                month_names = {
                    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
                    5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
                    9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
                }
                st.metric(
                    "Mes Pico de Feriados",
                    month_names.get(metrics['peak_holiday_month'], metrics['peak_holiday_month'])
                )
    
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