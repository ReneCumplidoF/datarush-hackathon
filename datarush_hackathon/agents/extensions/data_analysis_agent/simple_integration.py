# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple integration module for the Data Analysis Agent with DataRush system.

This module provides a simplified integration that works without external dependencies.
"""

import os
import sys
from typing import Dict, Any, Optional, List
import streamlit as st
import pandas as pd
import numpy as np

# Add the parent directory to the path for importing components
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from components.data_loader import DataLoader
from components.filters import Filters
from components.visualizations import Visualizations


class SimpleDataAnalysisAgent:
    """
    Simple Data Analysis Agent that works without external dependencies.
    """
    
    def __init__(self):
        self.data_loader = DataLoader()
        self.filters = Filters()
        self.visualizations = Visualizations()
        self.analysis_cache = {}
    
    def analyze_user_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyze a user query using simple data analysis.
        
        Args:
            query: User query to analyze
            context: Optional context from the DataRush system
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            # Prepare context for the analysis
            agent_context = self._prepare_agent_context(context)
            
            # Analyze the query
            analysis_results = self._analyze_query(query, agent_context)
            
            return analysis_results
            
        except Exception as e:
            st.error(f"❌ Error in data analysis: {str(e)}")
            return {
                "error": True,
                "message": f"Error in data analysis: {str(e)}",
                "analysis_type": "error"
            }
    
    def _prepare_agent_context(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Prepare context for the data analysis.
        
        Args:
            context: Context from the DataRush system
            
        Returns:
            Dictionary containing prepared context
        """
        agent_context = {
            "data_loaded": False,
            "data": {},
            "current_filters": {},
            "analysis_timestamp": None
        }
        
        # Debug: Show context information
        if context:
            st.write("🔍 **Debug - Contexto recibido:**")
            st.write(f"- data_loaded: {context.get('data_loaded', 'No definido')}")
            st.write(f"- data keys: {list(context.get('data', {}).keys()) if context.get('data') else 'No data'}")
            st.write(f"- filters: {context.get('current_filters', 'No definido')}")
        
        # Use data from context if available (from DataRush system)
        if context and context.get("data_loaded", False):
            agent_context["data"] = context.get("data", {})
            agent_context["data_loaded"] = True
            agent_context["current_filters"] = context.get("current_filters", {})
            agent_context["analysis_timestamp"] = pd.Timestamp.now().isoformat()
            
            # Debug: Show data details
            if agent_context["data"]:
                st.write("📊 **Debug - Datos disponibles:**")
                for key, value in agent_context["data"].items():
                    if hasattr(value, 'shape'):
                        st.write(f"- {key}: {value.shape} (DataFrame)")
                    else:
                        st.write(f"- {key}: {type(value)}")
        else:
            # Fallback: Load data if not available in context
            st.write("⚠️ **Debug - Usando fallback para cargar datos**")
            try:
                if self.data_loader.load_data() and self.data_loader.clean_data():
                    agent_context["data"] = self.data_loader.get_processed_data()
                    agent_context["data_loaded"] = True
            except Exception as e:
                st.warning(f"⚠️ Error loading data: {str(e)}")
        
        # Apply current filters if available
        if context and "current_filters" in context:
            agent_context["current_filters"] = context["current_filters"]
        
        # Add any additional context
        if context:
            agent_context.update(context)
        
        return agent_context
    
    def _analyze_query(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the query using simple data analysis.
        
        Args:
            query: User query
            context: Analysis context
            
        Returns:
            Dictionary containing analysis results
        """
        query_lower = query.lower()
        
        # Check for specific country mentions first
        country_codes = {
            'latvia': 'LVA', 'letonia': 'LVA', 'lva': 'LVA', 'lv': 'LVA',
            'estonia': 'EST', 'estonia': 'EST', 'est': 'EST', 'ee': 'EST',
            'lithuania': 'LTU', 'lituania': 'LTU', 'ltu': 'LTU', 'lt': 'LTU',
            'spain': 'ESP', 'españa': 'ESP', 'esp': 'ESP', 'es': 'ESP',
            'france': 'FRA', 'francia': 'FRA', 'fra': 'FRA', 'fr': 'FRA',
            'germany': 'DEU', 'alemania': 'DEU', 'deu': 'DEU', 'de': 'DEU',
            'italy': 'ITA', 'italia': 'ITA', 'ita': 'ITA', 'it': 'ITA',
            'portugal': 'PRT', 'prt': 'PRT', 'pt': 'PRT',
            'poland': 'POL', 'polonia': 'POL', 'pol': 'POL', 'pl': 'POL',
            'czech': 'CZE', 'republica checa': 'CZE', 'cze': 'CZE', 'cz': 'CZE',
            'slovakia': 'SVK', 'eslovaquia': 'SVK', 'svk': 'SVK', 'sk': 'SVK',
            'hungary': 'HUN', 'hungria': 'HUN', 'hun': 'HUN', 'hu': 'HUN',
            'romania': 'ROU', 'rumania': 'ROU', 'rou': 'ROU', 'ro': 'ROU',
            'bulgaria': 'BGR', 'bulgaria': 'BGR', 'bgr': 'BGR', 'bg': 'BGR',
            'croatia': 'HRV', 'croacia': 'HRV', 'hrv': 'HRV', 'hr': 'HRV',
            'slovenia': 'SVN', 'eslovenia': 'SVN', 'svn': 'SVN', 'si': 'SVN',
            'greece': 'GRC', 'grecia': 'GRC', 'grc': 'GRC', 'gr': 'GRC',
            'cyprus': 'CYP', 'chipre': 'CYP', 'cyp': 'CYP', 'cy': 'CYP',
            'malta': 'MLT', 'mlt': 'MLT', 'mt': 'MLT',
            'luxembourg': 'LUX', 'luxemburgo': 'LUX', 'lux': 'LUX', 'lu': 'LUX',
            'belgium': 'BEL', 'belgica': 'BEL', 'bel': 'BEL', 'be': 'BEL',
            'netherlands': 'NLD', 'holanda': 'NLD', 'nld': 'NLD', 'nl': 'NLD',
            'austria': 'AUT', 'austria': 'AUT', 'aut': 'AUT', 'at': 'AUT',
            'switzerland': 'CHE', 'suiza': 'CHE', 'che': 'CHE', 'ch': 'CHE',
            'denmark': 'DNK', 'dinamarca': 'DNK', 'dnk': 'DNK', 'dk': 'DNK',
            'sweden': 'SWE', 'suecia': 'SWE', 'swe': 'SWE', 'se': 'SWE',
            'finland': 'FIN', 'finlandia': 'FIN', 'fin': 'FIN', 'fi': 'FIN',
            'norway': 'NOR', 'noruega': 'NOR', 'nor': 'NOR', 'no': 'NOR',
            'iceland': 'ISL', 'islandia': 'ISL', 'isl': 'ISL', 'is': 'ISL',
            'ireland': 'IRL', 'irlanda': 'IRL', 'irl': 'IRL', 'ie': 'IRL',
            'united kingdom': 'GBR', 'reino unido': 'GBR', 'gbr': 'GBR', 'gb': 'GBR',
            'united states': 'USA', 'estados unidos': 'USA', 'usa': 'USA', 'us': 'USA',
            'canada': 'CAN', 'canada': 'CAN', 'can': 'CAN', 'ca': 'CAN',
            'mexico': 'MEX', 'mexico': 'MEX', 'mex': 'MEX', 'mx': 'MEX'
        }
        
        mentioned_country = None
        for country_name, country_code in country_codes.items():
            if country_name in query_lower:
                mentioned_country = country_code
                break
        
        # Determine analysis type based on query
        if mentioned_country:
            return self._analyze_country_specific(query, context, mentioned_country)
        elif any(word in query_lower for word in ['tendencia', 'evolución', 'crecimiento', 'decrecimiento', 'cambio']):
            return self._analyze_trends(query, context)
        elif any(word in query_lower for word in ['feriado', 'holiday', 'impacto', 'efecto', 'influencia']):
            return self._analyze_holiday_impact(query, context)
        elif any(word in query_lower for word in ['país', 'países', 'región', 'geográfico', 'ubicación']):
            return self._analyze_geographic(query, context)
        elif any(word in query_lower for word in ['estacional', 'temporada', 'mes', 'año', 'período']):
            return self._analyze_seasonal(query, context)
        elif any(word in query_lower for word in ['estadística', 'promedio', 'mediana', 'desviación', 'correlación']):
            return self._analyze_statistical(query, context)
        elif any(word in query_lower for word in ['comparar', 'comparación', 'vs', 'versus', 'diferencia']):
            return self._analyze_comparison(query, context)
        else:
            return self._analyze_general(query, context)
    
    def _analyze_country_specific(self, query: str, context: Dict[str, Any], country_code: str) -> Dict[str, Any]:
        """Analyze data for a specific country."""
        try:
            data = context.get('data', {})
            passengers_df = data.get('passengers')
            holidays_df = data.get('holidays')
            
            if passengers_df is None or passengers_df.empty:
                return {
                    "analysis_type": "country_specific_analysis",
                    "error": True,
                    "message": f"No passenger data available for analysis"
                }
            
            # Filter data for specific country
            country_data = passengers_df[passengers_df['ISO3'] == country_code]
            if country_data.empty:
                return {
                    "analysis_type": "country_specific_analysis",
                    "error": True,
                    "message": f"No data found for country code: {country_code}"
                }
            
            # Calculate country-specific metrics
            country_passengers = country_data['Total'].sum()
            country_avg_monthly = country_data.groupby('Month')['Total'].mean().mean()
            country_years = country_data['Year'].nunique()
            country_months = country_data['Month'].nunique()
            
            # Get country holidays
            country_holidays = 0
            if holidays_df is not None and not holidays_df.empty:
                country_holidays = len(holidays_df[holidays_df['ISO3'] == country_code])
            
            # Calculate growth rate
            yearly_data = country_data.groupby('Year')['Total'].sum().reset_index()
            growth_rate = self._calculate_growth_rate(yearly_data)
            
            # Get peak and low months
            monthly_data = country_data.groupby('Month')['Total'].sum().reset_index()
            if not monthly_data.empty:
                peak_month = monthly_data.loc[monthly_data['Total'].idxmax()]
                low_month = monthly_data.loc[monthly_data['Total'].idxmin()]
                peak_month_name = self._get_month_name(peak_month['Month'])
                low_month_name = self._get_month_name(low_month['Month'])
            else:
                peak_month_name = "N/A"
                low_month_name = "N/A"
            
            # Calculate percentage of total
            total_passengers = passengers_df['Total'].sum()
            percentage_of_total = (country_passengers / total_passengers * 100) if total_passengers > 0 else 0
            
            # Generate insights
            country_name = self._get_country_name(country_code)
            insights = [
                f"Análisis específico para {country_name} ({country_code})",
                f"El país registró {country_passengers:,.0f} pasajeros en total",
                f"Con un promedio mensual de {country_avg_monthly:,.0f} pasajeros",
                f"Los datos abarcan {country_years} años de información",
                f"Incluyendo {country_months} meses con datos disponibles",
                f"Se identificaron {country_holidays} feriados que influyen en el tráfico",
                f"Representando el {percentage_of_total:.1f}% del tráfico global",
                f"Mostrando una tasa de crecimiento del {growth_rate:.1%}",
                f"Con mayor actividad en {peak_month_name}",
                f"Y menor actividad en {low_month_name}"
            ]
            
            return {
                "analysis_type": "country_specific_analysis",
                "query": query,
                "insights": insights,
                "metrics": {
                    "country": f"{country_name} ({country_code})",
                    "country_passengers": country_passengers,
                    "country_avg_monthly": country_avg_monthly,
                    "country_years": country_years,
                    "country_months": country_months,
                    "country_holidays": country_holidays,
                    "percentage_of_total": percentage_of_total,
                    "growth_rate": growth_rate,
                    "peak_month": peak_month_name,
                    "low_month": low_month_name
                },
                "data_summary": {
                    "data_loaded": context.get('data_loaded', False),
                    "analysis_timestamp": pd.Timestamp.now().isoformat(),
                    "country_analyzed": f"{country_name} ({country_code})"
                },
                "success": True
            }
            
        except Exception as e:
            return {
                "analysis_type": "country_specific_analysis",
                "error": True,
                "message": f"Error in country-specific analysis: {str(e)}"
            }
    
    def _analyze_trends(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze trends in the data."""
        try:
            data = context.get('data', {})
            passengers_df = data.get('passengers')
            
            if passengers_df is None or passengers_df.empty:
                return {
                    "analysis_type": "trend_analysis",
                    "error": True,
                    "message": "No passenger data available for trend analysis"
                }
            
            # Apply filters if available
            if context.get('current_filters'):
                filtered_data = self.filters.apply_filters(data, context['current_filters'])
                passengers_df = filtered_data.get('passengers', passengers_df)
            
            # Group by year and month for trend analysis
            monthly_trends = passengers_df.groupby(['Year', 'Month'])['Total'].sum().reset_index()
            monthly_trends['Date'] = pd.to_datetime(monthly_trends[['Year', 'Month']].assign(day=1))
            
            # Calculate trend metrics
            total_passengers = monthly_trends['Total'].sum()
            avg_monthly = monthly_trends['Total'].mean()
            growth_rate = self._calculate_growth_rate(monthly_trends)
            peak_period = monthly_trends.loc[monthly_trends['Total'].idxmax()]
            low_period = monthly_trends.loc[monthly_trends['Total'].idxmin()]
            
            # Generate insights
            insights = [
                f"El total de pasajeros analizados es {total_passengers:,.0f}",
                f"El promedio mensual es {avg_monthly:,.0f} pasajeros",
                f"La tasa de crecimiento es {growth_rate:.1%}",
                f"El período pico es {self._get_month_name(peak_period['Month'])} {int(peak_period['Year'])} con {peak_period['Total']:,.0f} pasajeros",
                f"El período más bajo es {self._get_month_name(low_period['Month'])} {int(low_period['Year'])} con {low_period['Total']:,.0f} pasajeros"
            ]
            
            return {
                "analysis_type": "trend_analysis",
                "query": query,
                "insights": insights,
                "metrics": {
                    "total_passengers": total_passengers,
                    "avg_monthly": avg_monthly,
                    "growth_rate": growth_rate,
                    "peak_period": peak_period.to_dict(),
                    "low_period": low_period.to_dict()
                },
                "data_summary": {
                    "period_analyzed": f"{monthly_trends['Year'].min()}-{monthly_trends['Year'].max()}",
                    "months_analyzed": len(monthly_trends),
                    "countries_analyzed": passengers_df['ISO3'].nunique()
                },
                "success": True
            }
            
        except Exception as e:
            return {
                "analysis_type": "trend_analysis",
                "error": True,
                "message": f"Error in trend analysis: {str(e)}"
            }
    
    def _analyze_holiday_impact(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze holiday impact on passenger traffic."""
        try:
            data = context.get('data', {})
            passengers_df = data.get('passengers')
            holidays_df = data.get('holidays')
            
            if passengers_df is None or passengers_df.empty:
                return {
                    "analysis_type": "holiday_impact_analysis",
                    "error": True,
                    "message": "No passenger data available for holiday impact analysis"
                }
            
            if holidays_df is None or holidays_df.empty:
                return {
                    "analysis_type": "holiday_impact_analysis",
                    "error": True,
                    "message": "No holiday data available for holiday impact analysis"
                }
            
            # Apply filters if available
            if context.get('current_filters'):
                filtered_data = self.filters.apply_filters(data, context['current_filters'])
                passengers_df = filtered_data.get('passengers', passengers_df)
                holidays_df = filtered_data.get('holidays', holidays_df)
            
            # Process holiday data
            holidays_df['Date'] = pd.to_datetime(holidays_df['Date'])
            holidays_df['Month'] = holidays_df['Date'].dt.month
            holidays_df['Year'] = holidays_df['Date'].dt.year
            
            # Group holidays by month and year
            holiday_counts = holidays_df.groupby(['Year', 'Month']).size().reset_index(name='HolidayCount')
            
            # Group passengers by month and year
            passenger_monthly = passengers_df.groupby(['Year', 'Month'])['Total'].sum().reset_index()
            
            # Merge data
            combined_data = pd.merge(passenger_monthly, holiday_counts, on=['Year', 'Month'], how='left')
            combined_data['HolidayCount'] = combined_data['HolidayCount'].fillna(0)
            
            # Calculate correlation
            correlation = combined_data['Total'].corr(combined_data['HolidayCount'])
            
            # Generate insights
            insights = [
                f"Se analizaron {len(holidays_df)} feriados en {holidays_df['ISO3'].nunique()} países",
                f"La correlación entre feriados y pasajeros es {correlation:.3f}",
                f"El mes con más feriados es {combined_data.loc[combined_data['HolidayCount'].idxmax(), 'Month']}",
                f"El mes con menos feriados es {combined_data.loc[combined_data['HolidayCount'].idxmin(), 'Month']}"
            ]
            
            return {
                "analysis_type": "holiday_impact_analysis",
                "query": query,
                "insights": insights,
                "metrics": {
                    "correlation": correlation,
                    "total_holidays": len(holidays_df),
                    "countries_with_holidays": holidays_df['ISO3'].nunique(),
                    "data_points": len(combined_data)
                },
                "data_summary": {
                    "period_analyzed": f"{combined_data['Year'].min()}-{combined_data['Year'].max()}",
                    "months_analyzed": len(combined_data),
                    "avg_holidays_per_month": combined_data['HolidayCount'].mean()
                },
                "success": True
            }
            
        except Exception as e:
            return {
                "analysis_type": "holiday_impact_analysis",
                "error": True,
                "message": f"Error in holiday impact analysis: {str(e)}"
            }
    
    def _analyze_geographic(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze geographic distribution of data."""
        try:
            data = context.get('data', {})
            passengers_df = data.get('passengers')
            
            if passengers_df is None or passengers_df.empty:
                return {
                    "analysis_type": "geographic_analysis",
                    "error": True,
                    "message": "No passenger data available for geographic analysis"
                }
            
            # Apply filters if available
            if context.get('current_filters'):
                filtered_data = self.filters.apply_filters(data, context['current_filters'])
                passengers_df = filtered_data.get('passengers', passengers_df)
            
            # Analyze by country
            country_analysis = passengers_df.groupby('ISO3')['Total'].agg(['sum', 'mean', 'count']).reset_index()
            country_analysis = country_analysis.sort_values('sum', ascending=False)
            
            # Get top countries
            top_countries = country_analysis.head(10)
            
            # Generate insights
            insights = [
                f"Se analizaron {len(country_analysis)} países",
                f"El país con más pasajeros es {top_countries.iloc[0]['ISO3']} con {top_countries.iloc[0]['sum']:,.0f}",
                f"El país con menos pasajeros es {country_analysis.iloc[-1]['ISO3']} con {country_analysis.iloc[-1]['sum']:,.0f}",
                f"Los top 5 países representan {top_countries.head(5)['sum'].sum() / country_analysis['sum'].sum():.1%} del total"
            ]
            
            return {
                "analysis_type": "geographic_analysis",
                "query": query,
                "insights": insights,
                "metrics": {
                    "total_countries": len(country_analysis),
                    "top_countries": top_countries.to_dict('records'),
                    "total_passengers": country_analysis['sum'].sum(),
                    "avg_per_country": country_analysis['sum'].mean()
                },
                "data_summary": {
                    "countries_analyzed": len(country_analysis),
                    "total_passengers": country_analysis['sum'].sum(),
                    "avg_per_country": country_analysis['sum'].mean()
                },
                "success": True
            }
            
        except Exception as e:
            return {
                "analysis_type": "geographic_analysis",
                "error": True,
                "message": f"Error in geographic analysis: {str(e)}"
            }
    
    def _analyze_seasonal(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze seasonal patterns in the data."""
        try:
            data = context.get('data', {})
            passengers_df = data.get('passengers')
            
            if passengers_df is None or passengers_df.empty:
                return {
                    "analysis_type": "seasonal_analysis",
                    "error": True,
                    "message": "No passenger data available for seasonal analysis"
                }
            
            # Apply filters if available
            if context.get('current_filters'):
                filtered_data = self.filters.apply_filters(data, context['current_filters'])
                passengers_df = filtered_data.get('passengers', passengers_df)
            
            # Group by month for seasonal analysis
            seasonal_data = passengers_df.groupby('Month')['Total'].agg(['sum', 'mean', 'std']).reset_index()
            seasonal_data['MonthName'] = seasonal_data['Month'].apply(self._get_month_name)
            
            # Calculate seasonal metrics
            peak_month = seasonal_data.loc[seasonal_data['sum'].idxmax()]
            low_month = seasonal_data.loc[seasonal_data['sum'].idxmin()]
            seasonal_variation = (seasonal_data['sum'].max() - seasonal_data['sum'].min()) / seasonal_data['sum'].mean()
            
            # Generate insights
            insights = [
                f"El mes pico es {peak_month['MonthName']} con {peak_month['sum']:,.0f} pasajeros",
                f"El mes más bajo es {low_month['MonthName']} con {low_month['sum']:,.0f} pasajeros",
                f"La variación estacional es {seasonal_variation:.1%}",
                f"El promedio de pasajeros por mes es {seasonal_data['sum'].mean():,.0f}"
            ]
            
            return {
                "analysis_type": "seasonal_analysis",
                "query": query,
                "insights": insights,
                "metrics": {
                    "peak_month": peak_month.to_dict(),
                    "low_month": low_month.to_dict(),
                    "seasonal_variation": seasonal_variation,
                    "monthly_stats": seasonal_data.to_dict('records')
                },
                "data_summary": {
                    "months_analyzed": len(seasonal_data),
                    "total_passengers": seasonal_data['sum'].sum(),
                    "avg_per_month": seasonal_data['sum'].mean()
                },
                "success": True
            }
            
        except Exception as e:
            return {
                "analysis_type": "seasonal_analysis",
                "error": True,
                "message": f"Error in seasonal analysis: {str(e)}"
            }
    
    def _analyze_statistical(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform statistical analysis on the data."""
        try:
            data = context.get('data', {})
            passengers_df = data.get('passengers')
            
            if passengers_df is None or passengers_df.empty:
                return {
                    "analysis_type": "statistical_analysis",
                    "error": True,
                    "message": "No passenger data available for statistical analysis"
                }
            
            # Apply filters if available
            if context.get('current_filters'):
                filtered_data = self.filters.apply_filters(data, context['current_filters'])
                passengers_df = filtered_data.get('passengers', passengers_df)
            
            # Calculate descriptive statistics
            stats = passengers_df['Total'].describe()
            
            # Calculate additional metrics
            median = passengers_df['Total'].median()
            mode = passengers_df['Total'].mode().iloc[0] if not passengers_df['Total'].mode().empty else 0
            skewness = passengers_df['Total'].skew()
            kurtosis = passengers_df['Total'].kurtosis()
            
            # Generate insights
            insights = [
                f"El promedio de pasajeros es {stats['mean']:,.0f}",
                f"La mediana es {median:,.0f}",
                f"La moda es {mode:,.0f}",
                f"La desviación estándar es {stats['std']:,.0f}",
                f"El rango es {stats['max'] - stats['min']:,.0f}",
                f"La asimetría es {skewness:.3f}",
                f"La curtosis es {kurtosis:.3f}"
            ]
            
            return {
                "analysis_type": "statistical_analysis",
                "query": query,
                "insights": insights,
                "metrics": {
                    "descriptive_stats": stats.to_dict(),
                    "median": median,
                    "mode": mode,
                    "skewness": skewness,
                    "kurtosis": kurtosis
                },
                "data_summary": {
                    "total_records": len(passengers_df),
                    "total_passengers": passengers_df['Total'].sum(),
                    "countries_analyzed": passengers_df['ISO3'].nunique()
                },
                "success": True
            }
            
        except Exception as e:
            return {
                "analysis_type": "statistical_analysis",
                "error": True,
                "message": f"Error in statistical analysis: {str(e)}"
            }
    
    def _analyze_comparison(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze comparison between different entities."""
        try:
            data = context.get('data', {})
            passengers_df = data.get('passengers')
            
            if passengers_df is None or passengers_df.empty:
                return {
                    "analysis_type": "comparison_analysis",
                    "error": True,
                    "message": "No passenger data available for comparison analysis"
                }
            
            # Apply filters if available
            if context.get('current_filters'):
                filtered_data = self.filters.apply_filters(data, context['current_filters'])
                passengers_df = filtered_data.get('passengers', passengers_df)
            
            # Analyze by country
            country_analysis = passengers_df.groupby('ISO3')['Total'].agg(['sum', 'mean', 'count']).reset_index()
            country_analysis = country_analysis.sort_values('sum', ascending=False)
            
            # Get top countries
            top_countries = country_analysis.head(10)
            
            # Generate insights
            insights = [
                f"Se analizaron {len(country_analysis)} países",
                f"El país con más pasajeros es {top_countries.iloc[0]['ISO3']} con {top_countries.iloc[0]['sum']:,.0f}",
                f"El país con menos pasajeros es {country_analysis.iloc[-1]['ISO3']} con {country_analysis.iloc[-1]['sum']:,.0f}",
                f"La diferencia entre el país con más y menos pasajeros es {top_countries.iloc[0]['sum'] - country_analysis.iloc[-1]['sum']:,.0f}"
            ]
            
            return {
                "analysis_type": "comparison_analysis",
                "query": query,
                "insights": insights,
                "metrics": {
                    "total_countries": len(country_analysis),
                    "top_country": top_countries.iloc[0].to_dict(),
                    "bottom_country": country_analysis.iloc[-1].to_dict(),
                    "country_stats": country_analysis.to_dict('records')
                },
                "data_summary": {
                    "countries_analyzed": len(country_analysis),
                    "total_passengers": country_analysis['sum'].sum(),
                    "avg_per_country": country_analysis['sum'].mean()
                },
                "success": True
            }
            
        except Exception as e:
            return {
                "analysis_type": "comparison_analysis",
                "error": True,
                "message": f"Error in comparison analysis: {str(e)}"
            }
    
    def _analyze_general(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform general analysis on the data."""
        try:
            data = context.get('data', {})
            passengers_df = data.get('passengers')
            holidays_df = data.get('holidays')
            countries_df = data.get('countries')
            
            # Calculate general metrics
            total_passengers = passengers_df['Total'].sum() if passengers_df is not None and not passengers_df.empty else 0
            total_holidays = len(holidays_df) if holidays_df is not None and not holidays_df.empty else 0
            countries_analyzed = passengers_df['ISO3'].nunique() if passengers_df is not None and not passengers_df.empty else 0
            
            # Check if query mentions specific country
            query_lower = query.lower()
            country_mentioned = None
            for country_code in ['latvia', 'letonia', 'lva', 'lv']:
                if country_code in query_lower:
                    country_mentioned = 'LVA'
                    break
            
            # If specific country mentioned, provide country-specific analysis
            if country_mentioned and passengers_df is not None and not passengers_df.empty:
                country_data = passengers_df[passengers_df['ISO3'] == country_mentioned]
                if not country_data.empty:
                    country_passengers = country_data['Total'].sum()
                    country_avg_monthly = country_data.groupby('Month')['Total'].mean().mean()
                    country_years = country_data['Year'].nunique()
                    
                    # Get country holidays
                    country_holidays = 0
                    if holidays_df is not None and not holidays_df.empty:
                        country_holidays = len(holidays_df[holidays_df['ISO3'] == country_mentioned])
                    
                    insights = [
                        f"**Análisis específico para Letonia (LVA):**",
                        f"Total de pasajeros: {country_passengers:,.0f}",
                        f"Promedio mensual: {country_avg_monthly:,.0f} pasajeros",
                        f"Años analizados: {country_years}",
                        f"Feriados registrados: {country_holidays}",
                        f"Representa el {country_passengers/total_passengers*100:.1f}% del total de pasajeros" if total_passengers > 0 else "No hay datos de comparación"
                    ]
                    
                    return {
                        "analysis_type": "country_specific_analysis",
                        "query": query,
                        "insights": insights,
                        "metrics": {
                            "country": "Letonia (LVA)",
                            "country_passengers": country_passengers,
                            "country_avg_monthly": country_avg_monthly,
                            "country_years": country_years,
                            "country_holidays": country_holidays,
                            "percentage_of_total": country_passengers/total_passengers*100 if total_passengers > 0 else 0
                        },
                        "data_summary": {
                            "data_loaded": context.get('data_loaded', False),
                            "analysis_timestamp": pd.Timestamp.now().isoformat(),
                            "country_analyzed": "Letonia (LVA)"
                        },
                        "success": True
                    }
            
            # General analysis for all data
            insights = [
                f"El análisis abarca {total_passengers:,.0f} pasajeros en total",
                f"Identificando {total_holidays} feriados que influyen en el tráfico",
                f"Cubriendo {countries_analyzed} países diferentes",
                f"Con un promedio de {total_passengers / countries_analyzed:,.0f} pasajeros por país" if countries_analyzed > 0 else "Sin datos de países disponibles"
            ]
            
            # Add more specific insights if data is available
            if passengers_df is not None and not passengers_df.empty:
                year_range = f"{passengers_df['Year'].min()}-{passengers_df['Year'].max()}"
                insights.append(f"Período de análisis: {year_range}")
                
                # Top countries
                top_countries = passengers_df.groupby('ISO3')['Total'].sum().sort_values(ascending=False).head(3)
                if not top_countries.empty:
                    top_countries_str = ", ".join([f"{country} ({passengers:,.0f})" for country, passengers in top_countries.items()])
                    insights.append(f"Los países con mayor tráfico son: {top_countries_str}")
            
            return {
                "analysis_type": "general_analysis",
                "query": query,
                "insights": insights,
                "metrics": {
                    "total_passengers": total_passengers,
                    "total_holidays": total_holidays,
                    "countries_analyzed": countries_analyzed
                },
                "data_summary": {
                    "data_loaded": context.get('data_loaded', False),
                    "analysis_timestamp": pd.Timestamp.now().isoformat()
                },
                "success": True
            }
            
        except Exception as e:
            return {
                "analysis_type": "general_analysis",
                "error": True,
                "message": f"Error in general analysis: {str(e)}"
            }
    
    def _calculate_growth_rate(self, data: pd.DataFrame) -> float:
        """Calculate growth rate from time series data."""
        try:
            if len(data) < 2:
                return 0.0
            
            first_value = data['Total'].iloc[0]
            last_value = data['Total'].iloc[-1]
            
            if first_value == 0:
                return 0.0
            
            return (last_value - first_value) / first_value
        except:
            return 0.0
    
    def _get_month_name(self, month_num: int) -> str:
        """Get month name from month number."""
        month_names = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
            5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
            9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }
        return month_names.get(month_num, f'Mes {month_num}')
    
    def _get_country_name(self, country_code: str) -> str:
        """Get country name from country code."""
        country_names = {
            'LVA': 'Letonia', 'EST': 'Estonia', 'LTU': 'Lituania',
            'ESP': 'España', 'FRA': 'Francia', 'DEU': 'Alemania',
            'ITA': 'Italia', 'PRT': 'Portugal', 'POL': 'Polonia',
            'CZE': 'República Checa', 'SVK': 'Eslovaquia', 'HUN': 'Hungría',
            'ROU': 'Rumania', 'BGR': 'Bulgaria', 'HRV': 'Croacia',
            'SVN': 'Eslovenia', 'GRC': 'Grecia', 'CYP': 'Chipre',
            'MLT': 'Malta', 'LUX': 'Luxemburgo', 'BEL': 'Bélgica',
            'NLD': 'Países Bajos', 'AUT': 'Austria', 'CHE': 'Suiza',
            'DNK': 'Dinamarca', 'SWE': 'Suecia', 'FIN': 'Finlandia',
            'NOR': 'Noruega', 'ISL': 'Islandia', 'IRL': 'Irlanda',
            'GBR': 'Reino Unido', 'USA': 'Estados Unidos', 'CAN': 'Canadá',
            'MEX': 'México'
        }
        return country_names.get(country_code, country_code)
    
    def get_available_analyses(self) -> List[Dict[str, str]]:
        """Get list of available analysis types."""
        return [
            {
                "type": "trend_analysis",
                "name": "Análisis de Tendencias",
                "description": "Analiza patrones temporales y tasas de crecimiento en los datos de pasajeros"
            },
            {
                "type": "holiday_impact_analysis",
                "name": "Análisis de Impacto de Feriados",
                "description": "Estudia la correlación entre feriados y tráfico de pasajeros"
            },
            {
                "type": "geographic_analysis",
                "name": "Análisis Geográfico",
                "description": "Analiza la distribución de datos entre diferentes países"
            },
            {
                "type": "seasonal_analysis",
                "name": "Análisis Estacional",
                "description": "Identifica patrones estacionales en los datos"
            },
            {
                "type": "statistical_analysis",
                "name": "Análisis Estadístico",
                "description": "Realiza estadísticas descriptivas y correlaciones"
            },
            {
                "type": "comparison_analysis",
                "name": "Análisis de Comparación",
                "description": "Compara datos entre países, meses o períodos"
            }
        ]
    
    def get_analysis_summary(self, analysis_results: Dict[str, Any]) -> str:
        """Get a formatted summary of the analysis results."""
        # Handle case where analysis_results might be a string
        if isinstance(analysis_results, str):
            return analysis_results
        
        # Handle case where analysis_results is not a dict
        if not isinstance(analysis_results, dict):
            return f"❌ Error: Resultado de análisis en formato inesperado: {type(analysis_results)}"
        
        if analysis_results.get("error", False):
            return f"❌ Error: {analysis_results.get('message', 'Error desconocido')}"
        
        analysis_type = analysis_results.get("analysis_type", "unknown")
        insights = analysis_results.get("insights", [])
        metrics = analysis_results.get("metrics", {})
        
        # Create narrative summary based on analysis type
        if analysis_type == "country_specific_analysis":
            return self._create_country_narrative(insights, metrics)
        elif analysis_type == "general_analysis":
            return self._create_general_narrative(insights, metrics)
        elif analysis_type == "trend_analysis":
            return self._create_trend_narrative(insights, metrics)
        elif analysis_type == "holiday_impact_analysis":
            return self._create_holiday_narrative(insights, metrics)
        elif analysis_type == "geographic_analysis":
            return self._create_geographic_narrative(insights, metrics)
        elif analysis_type == "seasonal_analysis":
            return self._create_seasonal_narrative(insights, metrics)
        elif analysis_type == "statistical_analysis":
            return self._create_statistical_narrative(insights, metrics)
        elif analysis_type == "comparison_analysis":
            return self._create_comparison_narrative(insights, metrics)
        else:
            return self._create_default_narrative(insights, metrics)
    
    def _create_country_narrative(self, insights: List[str], metrics: Dict[str, Any]) -> str:
        """Create a narrative summary for country-specific analysis."""
        country = metrics.get("country", "el país")
        total_passengers = metrics.get("country_passengers", 0)
        avg_monthly = metrics.get("country_avg_monthly", 0)
        years_analyzed = metrics.get("country_years", 0)
        holidays = metrics.get("country_holidays", 0)
        percentage = metrics.get("percentage_of_total", 0)
        growth_rate = metrics.get("growth_rate", 0)
        peak_month = metrics.get("peak_month", "N/A")
        low_month = metrics.get("low_month", "N/A")
        
        narrative = f"## 📊 Análisis de {country}\n\n"
        
        # Main findings
        narrative += f"**Descubrimientos principales:**\n\n"
        narrative += f"• **Volumen de tráfico**: {country} registró un total de **{total_passengers:,.0f} pasajeros** durante el período analizado.\n\n"
        
        if avg_monthly > 0:
            narrative += f"• **Actividad mensual**: El país mantiene un promedio de **{avg_monthly:,.0f} pasajeros por mes**, mostrando una actividad aérea consistente.\n\n"
        
        if years_analyzed > 0:
            narrative += f"• **Período de análisis**: Los datos abarcan **{years_analyzed} años**, proporcionando una perspectiva temporal sólida.\n\n"
        
        if holidays > 0:
            narrative += f"• **Feriados registrados**: Se identificaron **{holidays} feriados** que podrían influir en los patrones de viaje.\n\n"
        
        if percentage > 0:
            narrative += f"• **Importancia global**: {country} representa el **{percentage:.1f}%** del tráfico aéreo total analizado.\n\n"
        
        if growth_rate != 0:
            if growth_rate > 0:
                narrative += f"• **Tendencia positiva**: El país muestra un **crecimiento del {growth_rate:.1%}** en el tráfico aéreo.\n\n"
            else:
                narrative += f"• **Tendencia negativa**: El país experimenta una **disminución del {abs(growth_rate):.1%}** en el tráfico aéreo.\n\n"
        
        if peak_month != "N/A" and low_month != "N/A":
            narrative += f"• **Patrones estacionales**: El mes de mayor actividad es **{peak_month}**, mientras que **{low_month}** registra la menor actividad.\n\n"
        
        # Additional insights
        if insights:
            narrative += "**Observaciones adicionales:**\n\n"
            for insight in insights[1:]:  # Skip the first insight as it's already covered
                if "**" not in insight:  # Skip formatted insights
                    narrative += f"• {insight}\n"
        
        return narrative
    
    def _create_general_narrative(self, insights: List[str], metrics: Dict[str, Any]) -> str:
        """Create a narrative summary for general analysis."""
        total_passengers = metrics.get("total_passengers", 0)
        total_holidays = metrics.get("total_holidays", 0)
        countries_analyzed = metrics.get("countries_analyzed", 0)
        
        narrative = "## 🌍 Análisis General del Tráfico Aéreo\n\n"
        
        narrative += f"**Panorama general:**\n\n"
        narrative += f"• **Escala global**: El análisis abarca **{total_passengers:,.0f} pasajeros** en total, representando una muestra significativa del tráfico aéreo mundial.\n\n"
        
        if countries_analyzed > 0:
            narrative += f"• **Cobertura geográfica**: Se analizaron **{countries_analyzed} países**, proporcionando una visión comprehensiva de los patrones de viaje internacionales.\n\n"
        
        if total_holidays > 0:
            narrative += f"• **Impacto de feriados**: Se identificaron **{total_holidays} feriados** que influyen en los patrones de viaje, mostrando la importancia de los eventos culturales y nacionales en el tráfico aéreo.\n\n"
        
        if total_passengers > 0 and countries_analyzed > 0:
            avg_per_country = total_passengers / countries_analyzed
            narrative += f"• **Distribución promedio**: Cada país registra un promedio de **{avg_per_country:,.0f} pasajeros**, indicando la diversidad en la actividad aérea entre regiones.\n\n"
        
        # Additional insights
        if insights:
            narrative += "**Hallazgos clave:**\n\n"
            for insight in insights:
                if "**" not in insight:  # Skip formatted insights
                    narrative += f"• {insight}\n"
        
        return narrative
    
    def _create_trend_narrative(self, insights: List[str], metrics: Dict[str, Any]) -> str:
        """Create a narrative summary for trend analysis."""
        narrative = "## 📈 Análisis de Tendencias\n\n"
        narrative += "**Evolución del tráfico aéreo:**\n\n"
        
        if insights:
            for insight in insights:
                narrative += f"• {insight}\n"
        
        return narrative
    
    def _create_holiday_narrative(self, insights: List[str], metrics: Dict[str, Any]) -> str:
        """Create a narrative summary for holiday impact analysis."""
        narrative = "## 🎉 Impacto de Feriados en el Tráfico Aéreo\n\n"
        narrative += "**Influencia de eventos especiales:**\n\n"
        
        if insights:
            for insight in insights:
                narrative += f"• {insight}\n"
        
        return narrative
    
    def _create_geographic_narrative(self, insights: List[str], metrics: Dict[str, Any]) -> str:
        """Create a narrative summary for geographic analysis."""
        narrative = "## 🌍 Análisis Geográfico\n\n"
        narrative += "**Distribución regional del tráfico:**\n\n"
        
        if insights:
            for insight in insights:
                narrative += f"• {insight}\n"
        
        return narrative
    
    def _create_seasonal_narrative(self, insights: List[str], metrics: Dict[str, Any]) -> str:
        """Create a narrative summary for seasonal analysis."""
        narrative = "## 🗓️ Análisis Estacional\n\n"
        narrative += "**Patrones temporales del tráfico:**\n\n"
        
        if insights:
            for insight in insights:
                narrative += f"• {insight}\n"
        
        return narrative
    
    def _create_statistical_narrative(self, insights: List[str], metrics: Dict[str, Any]) -> str:
        """Create a narrative summary for statistical analysis."""
        narrative = "## 📊 Análisis Estadístico\n\n"
        narrative += "**Métricas y correlaciones:**\n\n"
        
        if insights:
            for insight in insights:
                narrative += f"• {insight}\n"
        
        return narrative
    
    def _create_comparison_narrative(self, insights: List[str], metrics: Dict[str, Any]) -> str:
        """Create a narrative summary for comparison analysis."""
        narrative = "## ⚖️ Análisis Comparativo\n\n"
        narrative += "**Comparación entre entidades:**\n\n"
        
        if insights:
            for insight in insights:
                narrative += f"• {insight}\n"
        
        return narrative
    
    def _create_default_narrative(self, insights: List[str], metrics: Dict[str, Any]) -> str:
        """Create a default narrative summary."""
        narrative = "## 📋 Análisis de Datos\n\n"
        narrative += "**Resultados del análisis:**\n\n"
        
        if insights:
            for insight in insights:
                narrative += f"• {insight}\n"
        
        return narrative


# Create a global instance for easy access
simple_data_analysis_agent = SimpleDataAnalysisAgent()
