# components/advanced_filters.py
import streamlit as st
import pandas as pd
from typing import Dict, List, Optional, Tuple
import numpy as np
from datetime import datetime, timedelta

class AdvancedFilters:
    """
    Clase para manejar filtros avanzados del tablero de análisis de feriados
    """
    
    def __init__(self):
        self.advanced_filters = {}
        self.filter_options = {}
    
    def create_advanced_filters(self, data: Dict) -> Dict:
        """
        Crear interfaz de filtros avanzados
        
        Args:
            data: Datos procesados
            
        Returns:
            Dict: Diccionario con filtros avanzados aplicados
        """
        if not data:
            st.warning("⚠️ No hay datos disponibles para crear filtros avanzados")
            return {}
        
        holidays = data.get('holidays', pd.DataFrame())
        passengers = data.get('passengers', pd.DataFrame())
        countries = data.get('countries', pd.DataFrame())
        
        # Obtener opciones para filtros avanzados
        self.filter_options = self._get_advanced_filter_options(data)
        
        st.header("🔧 Filtros Avanzados")
        
        # Filtros Temporales Avanzados
        with st.expander("⏰ Filtros Temporales Avanzados", expanded=True):
            self._create_advanced_temporal_filters(holidays, passengers)
        
        # Filtros Geográficos Avanzados
        with st.expander("🌍 Filtros Geográficos Avanzados", expanded=True):
            self._create_advanced_geographic_filters(countries)
        
        # Filtros de Feriados Avanzados
        with st.expander("🎉 Filtros de Feriados Avanzados", expanded=True):
            self._create_advanced_holiday_filters(holidays)
        
        # Filtros de Pasajeros Avanzados
        with st.expander("✈️ Filtros de Pasajeros Avanzados", expanded=True):
            self._create_advanced_passenger_filters(passengers)
        
        # Filtros de Análisis Avanzados
        with st.expander("📊 Filtros de Análisis Avanzados", expanded=True):
            self._create_advanced_analysis_filters(holidays, passengers)
        
        # Botones de control
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("�� Aplicar Filtros Avanzados", type="primary"):
                st.rerun()
        
        with col2:
            if st.button("�� Limpiar Filtros Avanzados"):
                self.advanced_filters = {}
                st.rerun()
        
        with col3:
            if st.button("💾 Guardar Combinación"):
                self._save_filter_combination()
                st.success("✅ Combinación guardada")
        
        return self.advanced_filters
    
    def _create_advanced_temporal_filters(self, holidays: pd.DataFrame, passengers: pd.DataFrame) -> None:
        """Crear filtros temporales avanzados"""
        if holidays.empty or passengers.empty:
            return
        
        # Trimestre
        quarters = {
            1: 'Q1 (Ene-Mar)', 2: 'Q1 (Ene-Mar)', 3: 'Q1 (Ene-Mar)',
            4: 'Q2 (Abr-Jun)', 5: 'Q2 (Abr-Jun)', 6: 'Q2 (Abr-Jun)',
            7: 'Q3 (Jul-Sep)', 8: 'Q3 (Jul-Sep)', 9: 'Q3 (Jul-Sep)',
            10: 'Q4 (Oct-Dic)', 11: 'Q4 (Oct-Dic)', 12: 'Q4 (Oct-Dic)'
        }
        
        quarter_options = ['Q1', 'Q2', 'Q3', 'Q4']
        selected_quarters = st.multiselect(
            "Trimestre",
            options=quarter_options,
            default=quarter_options,
            help="Selecciona trimestres para analizar"
        )
        self.advanced_filters['quarters'] = selected_quarters
        
        # Día de la semana
        weekdays = {
            'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles',
            'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
        }
        
        weekday_options = list(weekdays.keys())
        selected_weekdays = st.multiselect(
            "Día de la semana",
            options=weekday_options,
            default=weekday_options,
            format_func=lambda x: weekdays[x],
            help="Selecciona días de la semana"
        )
        self.advanced_filters['weekdays'] = selected_weekdays
        
        # Semana del año
        if 'Date' in holidays.columns:
            holidays['Week'] = holidays['Date'].dt.isocalendar().week
            week_range = (holidays['Week'].min(), holidays['Week'].max())
            
            week_range_selected = st.slider(
                "Semana del año",
                min_value=week_range[0],
                max_value=week_range[1],
                value=week_range,
                step=1,
                help="Rango de semanas del año"
            )
            self.advanced_filters['week_range'] = week_range_selected
        
        # Rango personalizado de fechas
        if 'Date' in holidays.columns:
            date_range = st.date_input(
                "Rango personalizado de fechas",
                value=(holidays['Date'].min().date(), holidays['Date'].max().date()),
                help="Selecciona un rango personalizado de fechas"
            )
            if len(date_range) == 2:
                self.advanced_filters['date_range'] = date_range
    
    def _create_advanced_geographic_filters(self, countries: pd.DataFrame) -> None:
        """Crear filtros geográficos avanzados"""
        if countries.empty:
            return
        
        # Región (simulada basada en continente)
        if 'continent' in countries.columns:
            regions = {
                'North America': 'Norte',
                'South America': 'Sur', 
                'Europe': 'Este',
                'Asia': 'Este',
                'Africa': 'Sur',
                'Oceania': 'Oeste'
            }
            
            region_options = list(set(regions.values()))
            selected_regions = st.multiselect(
                "Región",
                options=region_options,
                default=region_options,
                help="Selecciona regiones geográficas"
            )
            self.advanced_filters['regions'] = selected_regions
        
        # Zona horaria (simulada)
        timezones = ['UTC-12', 'UTC-8', 'UTC-5', 'UTC-3', 'UTC+0', 'UTC+1', 'UTC+3', 'UTC+5', 'UTC+8', 'UTC+9', 'UTC+12']
        selected_timezones = st.multiselect(
            "Zona horaria",
            options=timezones,
            default=timezones,
            help="Selecciona zonas horarias"
        )
        self.advanced_filters['timezones'] = selected_timezones
        
        # Idioma oficial (simulado)
        languages = ['Español', 'Inglés', 'Francés', 'Alemán', 'Italiano', 'Portugués', 'Chino', 'Japonés', 'Árabe']
        selected_languages = st.multiselect(
            "Idioma oficial",
            options=languages,
            default=languages,
            help="Selecciona idiomas oficiales"
        )
        self.advanced_filters['languages'] = selected_languages
        
        # Moneda (simulada)
        currencies = ['USD', 'EUR', 'MXN', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF', 'CNY', 'BRL']
        selected_currencies = st.multiselect(
            "Moneda",
            options=currencies,
            default=currencies,
            help="Selecciona monedas"
        )
        self.advanced_filters['currencies'] = selected_currencies
    
    def _create_advanced_holiday_filters(self, holidays: pd.DataFrame) -> None:
        """Crear filtros de feriados avanzados"""
        if holidays.empty:
            return
        
        # Duración del feriado (simulada)
        durations = ['1 día', '2-3 días', '1 semana', 'Más de 1 semana']
        selected_durations = st.multiselect(
            "Duración del feriado",
            options=durations,
            default=durations,
            help="Selecciona duraciones de feriados"
        )
        self.advanced_filters['holiday_durations'] = selected_durations
        
        # Frecuencia
        frequencies = ['Anual', 'Bienal', 'Irregular', 'Único']
        selected_frequencies = st.multiselect(
            "Frecuencia",
            options=frequencies,
            default=frequencies,
            help="Selecciona frecuencias de feriados"
        )
        self.advanced_filters['holiday_frequencies'] = selected_frequencies
        
        # Día especial
        special_days = ['Half-day holiday', 'Working day replacement', 'Bank holiday', 'Public holiday']
        selected_special_days = st.multiselect(
            "Día especial",
            options=special_days,
            default=special_days,
            help="Selecciona tipos de días especiales"
        )
        self.advanced_filters['special_days'] = selected_special_days
    
    def _create_advanced_passenger_filters(self, passengers: pd.DataFrame) -> None:
        """Crear filtros de pasajeros avanzados"""
        if passengers.empty or 'Total' not in passengers.columns:
            return
        
        # Estacionalidad
        # Calcular percentiles para determinar estacionalidad
        monthly_avg = passengers.groupby('Month')['Total'].mean()
        p25 = monthly_avg.quantile(0.25)
        p75 = monthly_avg.quantile(0.75)
        
        seasons = {
            'Alta temporada': f'>{p75:.0f} pasajeros/mes',
            'Temporada media': f'{p25:.0f}-{p75:.0f} pasajeros/mes',
            'Baja temporada': f'<{p25:.0f} pasajeros/mes'
        }
        
        season_options = list(seasons.keys())
        selected_seasons = st.multiselect(
            "Estacionalidad",
            options=season_options,
            default=season_options,
            format_func=lambda x: f"{x} ({seasons[x]})",
            help="Selecciona niveles de estacionalidad"
        )
        self.advanced_filters['seasons'] = selected_seasons
        
        # Percentiles
        percentiles = ['P25', 'P50', 'P75', 'P90', 'P95']
        selected_percentiles = st.multiselect(
            "Percentiles",
            options=percentiles,
            default=percentiles,
            help="Selecciona percentiles de distribución"
        )
        self.advanced_filters['percentiles'] = selected_percentiles
        
        # Crecimiento
        if 'Year' in passengers.columns:
            yearly_growth = passengers.groupby('Year')['Total'].sum().pct_change() * 100
            growth_categories = {
                'Positivo': 'Crecimiento > 0%',
                'Negativo': 'Crecimiento < 0%',
                'Estable': 'Crecimiento ≈ 0%'
            }
            
            growth_options = list(growth_categories.keys())
            selected_growth = st.multiselect(
                "Crecimiento",
                options=growth_options,
                default=growth_options,
                format_func=lambda x: f"{x} ({growth_categories[x]})",
                help="Selecciona categorías de crecimiento"
            )
            self.advanced_filters['growth_categories'] = selected_growth
    
    def _create_advanced_analysis_filters(self, holidays: pd.DataFrame, passengers: pd.DataFrame) -> None:
        """Crear filtros de análisis avanzados"""
        if holidays.empty or passengers.empty:
            return
        
        # Consistencia
        consistency_options = ['Patrón consistente', 'Patrón variable', 'Patrón único']
        selected_consistency = st.multiselect(
            "Consistencia",
            options=consistency_options,
            default=consistency_options,
            help="Selecciona niveles de consistencia en los patrones"
        )
        self.advanced_filters['consistency'] = selected_consistency
        
        # Fuente de datos
        data_sources = ['Oficial', 'Otras fuentes']
        selected_sources = st.multiselect(
            "Fuente de datos",
            options=data_sources,
            default=data_sources,
            help="Selecciona fuentes de datos"
        )
        self.advanced_filters['data_sources'] = selected_sources
    
    def apply_advanced_filters(self, data: Dict, filters: Dict) -> Dict:
        """
        Aplicar filtros avanzados a los datos
        
        Args:
            data: Datos originales
            filters: Filtros avanzados a aplicar
            
        Returns:
            Dict: Datos filtrados
        """
        if not data or not filters:
            return data
        
        filtered_data = data.copy()
        
        # Aplicar filtros temporales avanzados
        if 'holidays' in filtered_data and not filtered_data['holidays'].empty:
            holidays_df = filtered_data['holidays'].copy()
            
            # Filtro por trimestre
            if 'quarters' in filters and filters['quarters']:
                quarter_map = {1: 'Q1', 2: 'Q1', 3: 'Q1', 4: 'Q2', 5: 'Q2', 6: 'Q2',
                              7: 'Q3', 8: 'Q3', 9: 'Q3', 10: 'Q4', 11: 'Q4', 12: 'Q4'}
                holidays_df['Quarter'] = holidays_df['Month'].map(quarter_map)
                holidays_df = holidays_df[holidays_df['Quarter'].isin(filters['quarters'])]
            
            # Filtro por día de la semana
            if 'weekdays' in filters and filters['weekdays']:
                holidays_df = holidays_df[holidays_df['Weekday'].isin(filters['weekdays'])]
            
            # Filtro por rango de fechas
            if 'date_range' in filters and len(filters['date_range']) == 2:
                start_date, end_date = filters['date_range']
                holidays_df = holidays_df[
                    (holidays_df['Date'].dt.date >= start_date) & 
                    (holidays_df['Date'].dt.date <= end_date)
                ]
            
            filtered_data['holidays'] = holidays_df
        
        # Aplicar filtros a datos de pasajeros
        if 'passengers' in filtered_data and not filtered_data['passengers'].empty:
            passengers_df = filtered_data['passengers'].copy()
            
            # Filtro por trimestre
            if 'quarters' in filters and filters['quarters']:
                quarter_map = {1: 'Q1', 2: 'Q1', 3: 'Q1', 4: 'Q2', 5: 'Q2', 6: 'Q2',
                              7: 'Q3', 8: 'Q3', 9: 'Q3', 10: 'Q4', 11: 'Q4', 12: 'Q4'}
                passengers_df['Quarter'] = passengers_df['Month'].map(quarter_map)
                passengers_df = passengers_df[passengers_df['Quarter'].isin(filters['quarters'])]
            
            # Filtro por estacionalidad
            if 'seasons' in filters and filters['seasons']:
                monthly_avg = passengers_df.groupby('Month')['Total'].mean()
                p25 = monthly_avg.quantile(0.25)
                p75 = monthly_avg.quantile(0.75)
                
                season_conditions = []
                if 'Alta temporada' in filters['seasons']:
                    season_conditions.append(passengers_df['Total'] > p75)
                if 'Temporada media' in filters['seasons']:
                    season_conditions.append((passengers_df['Total'] >= p25) & (passengers_df['Total'] <= p75))
                if 'Baja temporada' in filters['seasons']:
                    season_conditions.append(passengers_df['Total'] < p25)
                
                if season_conditions:
                    combined_condition = season_conditions[0]
                    for condition in season_conditions[1:]:
                        combined_condition = combined_condition | condition
                    passengers_df = passengers_df[combined_condition]
            
            filtered_data['passengers'] = passengers_df
        
        return filtered_data
    
    def _get_advanced_filter_options(self, data: Dict) -> Dict:
        """Obtener opciones para filtros avanzados"""
        options = {}
        
        if 'holidays' in data and not data['holidays'].empty:
            holidays = data['holidays']
            options['quarters'] = ['Q1', 'Q2', 'Q3', 'Q4']
            options['weekdays'] = holidays['Weekday'].unique().tolist()
        
        if 'passengers' in data and not data['passengers'].empty:
            passengers = data['passengers']
            options['seasons'] = ['Alta temporada', 'Temporada media', 'Baja temporada']
            options['percentiles'] = ['P25', 'P50', 'P75', 'P90', 'P95']
        
        return options
    
    def validate_advanced_filters(self, filters: Dict) -> bool:
        """Validar filtros avanzados"""
        try:
            # Validar rango de fechas
            if 'date_range' in filters and len(filters['date_range']) == 2:
                start_date, end_date = filters['date_range']
                if start_date > end_date:
                    st.error("❌ La fecha de inicio no puede ser mayor a la fecha de fin")
                    return False
            
            return True
        except Exception as e:
            st.error(f"❌ Error validando filtros avanzados: {str(e)}")
            return False
    
    def get_filter_combinations(self) -> List[Dict]:
        """Obtener combinaciones de filtros guardadas"""
        # Implementar lógica para cargar combinaciones guardadas
        return []
    
    def _save_filter_combination(self) -> None:
        """Guardar combinación de filtros actual"""
        # Implementar lógica para guardar combinaciones
        pass
