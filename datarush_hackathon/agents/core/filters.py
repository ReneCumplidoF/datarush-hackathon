# components/filters.py
import streamlit as st
from typing import Dict, List, Optional
import pandas as pd

class Filters:
    """
    Clase para manejar filtros del tablero de análisis de feriados
    """
    
    def __init__(self):
        self.filters = {}
        self.filter_options = {}
        self.country_mapping = {}  # Mapeo ISO3 -> Nombre de país
    
    def create_sidebar_filters(self, data: Dict) -> Dict:
        """
        Crear interfaz de filtros en el sidebar deslizable
        
        Args:
            data: Diccionario con datos procesados
            
        Returns:
            Dict: Diccionario con filtros aplicados
        """
        if not data:
            st.warning("⚠️ No hay datos disponibles para crear filtros")
            return {}
        
        holidays = data.get('holidays', pd.DataFrame())
        passengers = data.get('passengers', pd.DataFrame())
        countries = data.get('countries', pd.DataFrame())
        
        # Crear mapeo de países ISO3 -> Nombre
        self.country_mapping = self._create_country_mapping(countries)
        
        # Obtener opciones para filtros (solo países con datos de pasajeros)
        self.filter_options = self._get_filter_options(data)
        
        # Filtros Temporales
        with st.expander(" Filtros Temporales", expanded=True):
            # Año
            years = self.filter_options.get('years', [])
            if years:
                year_range = st.slider(
                    "Año",
                    min_value=min(years),
                    max_value=max(years),
                    value=(min(years), max(years)),
                    step=1
                )
                self.filters['year_range'] = year_range
            
            # Mes
            months = self.filter_options.get('months', [])
            if months:
                month_names = {
                    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
                    5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
                    9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
                }
                selected_months = st.multiselect(
                    "Meses",
                    options=months,
                    default=months,
                    format_func=lambda x: f"{month_names.get(x, x)} ({x})"
                )
                self.filters['months'] = selected_months
            
            # Período respecto al feriado
            holiday_period = st.selectbox(
                "Período respecto al feriado",
                options=['Todos', 'Antes', 'Durante', 'Después'],
                index=0
            )
            self.filters['holiday_period'] = holiday_period
        
        # Filtros Geográficos
        with st.expander("🌍 Filtros Geográficos", expanded=True):
            # País - Solo países con datos de pasajeros
            countries_with_data = self.filter_options.get('countries_with_data', [])
            if countries_with_data:
                # Crear opciones con nombres de países
                country_options = []
                for iso3 in countries_with_data:
                    country_name = self.country_mapping.get(iso3, iso3)
                    country_options.append((iso3, f"{country_name} ({iso3})"))
                
                # Ordenar por nombre de país
                country_options.sort(key=lambda x: x[1])
                
                selected_countries = st.multiselect(
                    "Países",
                    options=[opt[0] for opt in country_options],
                    default=countries_with_data[:10] if len(countries_with_data) > 10 else countries_with_data,
                    format_func=lambda x: self.country_mapping.get(x, x),
                    help="Solo se muestran países con datos de pasajeros"
                )
                self.filters['countries'] = selected_countries
            else:
                st.warning("⚠️ No hay países con datos de pasajeros disponibles")
                self.filters['countries'] = []
            
            # Continente (si está disponible)
            continents = self.filter_options.get('continents', [])
            if continents:
                selected_continents = st.multiselect(
                    "Continentes",
                    options=continents,
                    default=continents,
                    help="Selecciona continentes para analizar"
                )
                self.filters['continents'] = selected_continents
        
        # Filtros de Feriados
        with st.expander("🎉 Filtros de Feriados", expanded=True):
            # Tipo de feriado
            holiday_types = self.filter_options.get('holiday_types', [])
            if holiday_types:
                selected_holiday_types = st.multiselect(
                    "Tipo de feriado",
                    options=holiday_types,
                    default=holiday_types,
                    help="Selecciona tipos de feriados"
                )
                self.filters['holiday_types'] = selected_holiday_types
            
            # Categoría cultural (derivada del tipo)
            cultural_categories = self._get_cultural_categories(holiday_types)
            if cultural_categories:
                selected_cultural = st.multiselect(
                    "Categoría cultural",
                    options=cultural_categories,
                    default=cultural_categories,
                    help="Categorías culturales de los feriados"
                )
                self.filters['cultural_categories'] = selected_cultural
        
        # Filtros de Pasajeros
        with st.expander("✈️ Filtros de Pasajeros", expanded=True):
            # Tipo de vuelo
            flight_types = ['Total', 'Domestic', 'International']
            selected_flight_types = st.multiselect(
                "Tipo de vuelo",
                options=flight_types,
                default=['Total'],
                help="Selecciona tipos de vuelo para analizar"
            )
            self.filters['flight_types'] = selected_flight_types
            
            # Volumen de pasajeros
            if not passengers.empty and 'Total' in passengers.columns:
                max_passengers = passengers['Total'].max()
                passenger_range = st.slider(
                    "Volumen de pasajeros (miles)",
                    min_value=0,
                    max_value=int(max_passengers / 1000),
                    value=(0, int(max_passengers / 1000)),
                    step=1,
                    help="Rango de volumen de pasajeros en miles"
                )
                self.filters['passenger_range'] = (passenger_range[0] * 1000, passenger_range[1] * 1000)
        
        # Filtros de Análisis
        with st.expander("📊 Filtros de Análisis", expanded=False):
            # Impacto del feriado
            impact_levels = ['Alto', 'Medio', 'Bajo', 'Negativo']
            selected_impact = st.multiselect(
                "Impacto del feriado",
                options=impact_levels,
                default=impact_levels,
                help="Niveles de impacto de los feriados"
            )
            self.filters['impact_levels'] = selected_impact
            
            # Patrón temporal
            temporal_patterns = ['Adelanto', 'Pico', 'Rebote', 'Sin patrón']
            selected_patterns = st.multiselect(
                "Patrón temporal",
                options=temporal_patterns,
                default=temporal_patterns,
                help="Patrones temporales observados"
            )
            self.filters['temporal_patterns'] = selected_patterns
        
        # Botones de control
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Aplicar Filtros", type="primary"):
                st.rerun()
        
        with col2:
            if st.button(" Limpiar Filtros"):
                self.filters = {}
                st.rerun()
        
        # RETORNAR LOS FILTROS ACTUALES
        return self.filters
    
    def apply_filters(self, data: Dict, filters: Dict) -> Dict:
        """
        Aplicar filtros a los datos
        
        Args:
            data: Datos originales
            filters: Filtros a aplicar
            
        Returns:
            Dict: Datos filtrados
        """
        if not data or not filters:
            return data
        
        filtered_data = data.copy()
        
        # Aplicar filtros a datos de feriados
        if 'holidays' in filtered_data and not filtered_data['holidays'].empty:
            holidays_df = filtered_data['holidays'].copy()
            
            # Filtro por año
            if 'year_range' in filters:
                year_min, year_max = filters['year_range']
                holidays_df = holidays_df[
                    (holidays_df['Year'] >= year_min) & 
                    (holidays_df['Year'] <= year_max)
                ]
            
            # Filtro por mes
            if 'months' in filters and filters['months']:
                holidays_df = holidays_df[holidays_df['Month'].isin(filters['months'])]
            
            # Filtro por países
            if 'countries' in filters and filters['countries']:
                holidays_df = holidays_df[holidays_df['ISO3'].isin(filters['countries'])]
            
            # Filtro por tipo de feriado
            if 'holiday_types' in filters and filters['holiday_types']:
                holidays_df = holidays_df[holidays_df['Type'].isin(filters['holiday_types'])]
            
            filtered_data['holidays'] = holidays_df
        
        # Aplicar filtros a datos de pasajeros
        if 'passengers' in filtered_data and not filtered_data['passengers'].empty:
            passengers_df = filtered_data['passengers'].copy()
            
            # Filtro por año
            if 'year_range' in filters:
                year_min, year_max = filters['year_range']
                passengers_df = passengers_df[
                    (passengers_df['Year'] >= year_min) & 
                    (passengers_df['Year'] <= year_max)
                ]
            
            # Filtro por mes
            if 'months' in filters and filters['months']:
                passengers_df = passengers_df[passengers_df['Month'].isin(filters['months'])]
            
            # Filtro por países
            if 'countries' in filters and filters['countries']:
                passengers_df = passengers_df[passengers_df['ISO3'].isin(filters['countries'])]
            
            # Filtro por volumen de pasajeros
            if 'passenger_range' in filters:
                min_pass, max_pass = filters['passenger_range']
                passengers_df = passengers_df[
                    (passengers_df['Total'] >= min_pass) & 
                    (passengers_df['Total'] <= max_pass)
                ]
            
            filtered_data['passengers'] = passengers_df
        
        return filtered_data
    
    def get_active_filters_summary(self) -> Dict:
        """
        Obtener resumen de filtros activos
        
        Returns:
            Dict: Resumen de filtros aplicados
        """
        summary = {}
        
        for filter_name, filter_value in self.filters.items():
            if filter_value:
                if isinstance(filter_value, list) and len(filter_value) > 0:
                    if filter_name == 'countries':
                        # Mostrar nombres de países en lugar de códigos ISO3
                        country_names = [self.country_mapping.get(iso3, iso3) for iso3 in filter_value]
                        summary[filter_name] = f"{len(filter_value)} países: {', '.join(country_names[:3])}{'...' if len(country_names) > 3 else ''}"
                    else:
                        summary[filter_name] = f"{len(filter_value)} seleccionados"
                elif isinstance(filter_value, tuple) and len(filter_value) == 2:
                    summary[filter_name] = f"{filter_value[0]} - {filter_value[1]}"
                else:
                    summary[filter_name] = str(filter_value)
        
        return summary
    
    def validate_filters(self, filters: Dict) -> bool:
        """
        Validar que los filtros sean correctos
        
        Args:
            filters: Filtros a validar
            
        Returns:
            bool: True si son válidos, False en caso contrario
        """
        try:
            # Validar rango de años
            if 'year_range' in filters:
                year_min, year_max = filters['year_range']
                if year_min > year_max:
                    st.error("❌ El año mínimo no puede ser mayor al máximo")
                    return False
            
            # Validar rango de pasajeros
            if 'passenger_range' in filters:
                min_pass, max_pass = filters['passenger_range']
                if min_pass > max_pass:
                    st.error("❌ El volumen mínimo no puede ser mayor al máximo")
                    return False
            
            return True
            
        except Exception as e:
            st.error(f"❌ Error validando filtros: {str(e)}")
            return False
    
    def _create_country_mapping(self, countries_df: pd.DataFrame) -> Dict[str, str]:
        """
        Crear mapeo de códigos ISO3 a nombres de países
        
        Args:
            countries_df: DataFrame con información de países
            
        Returns:
            Dict: Mapeo ISO3 -> Nombre de país
        """
        mapping = {}
        
        if not countries_df.empty and 'alpha_3' in countries_df.columns and 'name' in countries_df.columns:
            for _, row in countries_df.iterrows():
                iso3 = row['alpha_3']
                name = row['name']
                if pd.notna(iso3) and pd.notna(name):
                    mapping[iso3] = name
        
        return mapping
    
    def _get_filter_options(self, data: Dict) -> Dict:
        """
        Obtener opciones para filtros basadas en los datos
        Solo incluir países que tienen datos de pasajeros
        
        Args:
            data: Datos procesados
            
        Returns:
            Dict: Opciones para cada filtro
        """
        options = {}
        
        # Obtener países con datos de pasajeros
        countries_with_passenger_data = set()
        if 'passengers' in data and not data['passengers'].empty:
            passengers = data['passengers']
            countries_with_passenger_data = set(passengers['ISO3'].unique())
        
        if 'holidays' in data and not data['holidays'].empty:
            holidays = data['holidays']
            options['years'] = sorted(holidays['Year'].unique().tolist())
            options['months'] = sorted(holidays['Month'].unique().tolist())
            # Solo incluir países que tienen datos de pasajeros
            holiday_countries = set(holidays['ISO3'].unique())
            countries_with_data = list(countries_with_passenger_data.intersection(holiday_countries))
            options['countries_with_data'] = sorted(countries_with_data)
            options['holiday_types'] = sorted(holidays['Type'].unique().tolist())
        
        if 'passengers' in data and not data['passengers'].empty:
            passengers = data['passengers']
            if 'years' not in options:
                options['years'] = sorted(passengers['Year'].unique().tolist())
            if 'months' not in options:
                options['months'] = sorted(passengers['Month'].unique().tolist())
            if 'countries_with_data' not in options:
                options['countries_with_data'] = sorted(list(countries_with_passenger_data))
        
        if 'countries' in data and not data['countries'].empty:
            countries = data['countries']
            if 'continent' in countries.columns:
                options['continents'] = sorted(countries['continent'].unique().tolist())
        
        return options
    
    def _get_cultural_categories(self, holiday_types: List[str]) -> List[str]:
        """
        Obtener categorías culturales basadas en tipos de feriados
        
        Args:
            holiday_types: Lista de tipos de feriados
            
        Returns:
            List[str]: Categorías culturales
        """
        cultural_map = {
            'Public holiday': 'Nacional',
            'School holiday': 'Educativo',
            'Local holiday': 'Local',
            'Observance': 'Religioso',
            'Religious': 'Religioso',
            'National': 'Nacional',
            'Cultural': 'Cultural'
        }
        
        categories = set()
        for holiday_type in holiday_types:
            if holiday_type in cultural_map:
                categories.add(cultural_map[holiday_type])
        
        return sorted(list(categories))