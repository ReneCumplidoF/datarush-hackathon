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

"""Tools for the data analysis agent.

This module contains tools that the data analysis agent can use to perform
various data analysis tasks on the DataRush dataset.
"""

import os
import sys
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Add the parent directory to the path for importing components
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

# from google.adk.tools import Tool

# Fallback for when google.adk is not available
try:
    from google.adk.tools import Tool
    ADK_AVAILABLE = True
except ImportError:
    ADK_AVAILABLE = False
    # Create a mock Tool class
    class Tool:
        def __init__(self, name, description, func):
            self.name = name
            self.description = description
            self.func = func
from components.data_loader import DataLoader
from components.filters import Filters
from components.visualizations import Visualizations


def analyze_trends(
    data: Dict[str, Any],
    filters: Dict[str, Any] = None,
    time_period: str = "monthly"
) -> Dict[str, Any]:
    """Analyze trends in passenger data over time.
    
    Args:
        data: Dictionary containing the loaded data
        filters: Optional filters to apply
        time_period: Time period for analysis (monthly, yearly, etc.)
        
    Returns:
        Dictionary containing trend analysis results
    """
    try:
        passengers_df = data.get('passengers')
        if passengers_df is None or passengers_df.empty:
            return {"error": "No passenger data available"}
        
        # Apply filters if provided
        if filters:
            filter_obj = Filters()
            passengers_df = filter_obj.apply_filters({'passengers': passengers_df}, filters)['passengers']
        
        # Group by time period
        if time_period == "monthly":
            grouped = passengers_df.groupby(['Year', 'Month'])['Total'].sum().reset_index()
            grouped['Date'] = pd.to_datetime(grouped[['Year', 'Month']].assign(day=1))
        elif time_period == "yearly":
            grouped = passengers_df.groupby('Year')['Total'].sum().reset_index()
            grouped['Date'] = pd.to_datetime(grouped['Year'], format='%Y')
        else:
            grouped = passengers_df.groupby(['Year', 'Month'])['Total'].sum().reset_index()
            grouped['Date'] = pd.to_datetime(grouped[['Year', 'Month']].assign(day=1))
        
        # Calculate trend metrics
        total_passengers = grouped['Total'].sum()
        avg_period = grouped['Total'].mean()
        growth_rate = _calculate_growth_rate(grouped)
        peak_period = grouped.loc[grouped['Total'].idxmax()]
        low_period = grouped.loc[grouped['Total'].idxmin()]
        
        # Create visualization
        fig = px.line(grouped, x='Date', y='Total', 
                     title=f'Tendencias de Pasajeros - {time_period.title()}',
                     labels={'Total': 'Total Pasajeros', 'Date': 'Fecha'})
        fig.update_layout(xaxis_title='Fecha', yaxis_title='Total Pasajeros')
        
        return {
            "analysis_type": "trend_analysis",
            "time_period": time_period,
            "total_passengers": total_passengers,
            "avg_per_period": avg_period,
            "growth_rate": growth_rate,
            "peak_period": peak_period.to_dict(),
            "low_period": low_period.to_dict(),
            "visualization": fig.to_json(),
            "data_points": len(grouped)
        }
        
    except Exception as e:
        return {"error": f"Error in trend analysis: {str(e)}"}


def analyze_holiday_impact(
    data: Dict[str, Any],
    filters: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Analyze the impact of holidays on passenger traffic.
    
    Args:
        data: Dictionary containing the loaded data
        filters: Optional filters to apply
        
    Returns:
        Dictionary containing holiday impact analysis results
    """
    try:
        passengers_df = data.get('passengers')
        holidays_df = data.get('holidays')
        
        if passengers_df is None or passengers_df.empty:
            return {"error": "No passenger data available"}
        
        if holidays_df is None or holidays_df.empty:
            return {"error": "No holiday data available"}
        
        # Apply filters if provided
        if filters:
            filter_obj = Filters()
            filtered_data = filter_obj.apply_filters(data, filters)
            passengers_df = filtered_data.get('passengers')
            holidays_df = filtered_data.get('holidays')
        
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
        
        # Create visualization
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(x=combined_data['Month'], y=combined_data['Total'], 
                      name='Pasajeros', line=dict(color='blue')),
            secondary_y=False,
        )
        
        fig.add_trace(
            go.Scatter(x=combined_data['Month'], y=combined_data['HolidayCount'], 
                      name='Feriados', line=dict(color='red')),
            secondary_y=True,
        )
        
        fig.update_xaxes(title_text="Mes")
        fig.update_yaxes(title_text="Total Pasajeros", secondary_y=False)
        fig.update_yaxes(title_text="Número de Feriados", secondary_y=True)
        fig.update_layout(title_text="Impacto de Feriados en Pasajeros")
        
        return {
            "analysis_type": "holiday_impact_analysis",
            "correlation": correlation,
            "total_holidays": len(holidays_df),
            "countries_with_holidays": holidays_df['ISO3'].nunique(),
            "visualization": fig.to_json(),
            "data_points": len(combined_data)
        }
        
    except Exception as e:
        return {"error": f"Error in holiday impact analysis: {str(e)}"}


def analyze_geographic_distribution(
    data: Dict[str, Any],
    filters: Dict[str, Any] = None,
    top_n: int = 20
) -> Dict[str, Any]:
    """Analyze geographic distribution of passenger data.
    
    Args:
        data: Dictionary containing the loaded data
        filters: Optional filters to apply
        top_n: Number of top countries to include
        
    Returns:
        Dictionary containing geographic analysis results
    """
    try:
        passengers_df = data.get('passengers')
        if passengers_df is None or passengers_df.empty:
            return {"error": "No passenger data available"}
        
        # Apply filters if provided
        if filters:
            filter_obj = Filters()
            filtered_data = filter_obj.apply_filters(data, filters)
            passengers_df = filtered_data.get('passengers')
        
        # Analyze by country
        country_analysis = passengers_df.groupby('ISO3')['Total'].agg(['sum', 'mean', 'count']).reset_index()
        country_analysis = country_analysis.sort_values('sum', ascending=False)
        
        # Get top countries
        top_countries = country_analysis.head(top_n)
        
        # Create visualization
        fig = px.treemap(top_countries, 
                        path=['ISO3'], 
                        values='sum',
                        title=f'Distribución Geográfica de Pasajeros (Top {top_n})',
                        labels={'sum': 'Total Pasajeros'})
        
        return {
            "analysis_type": "geographic_analysis",
            "total_countries": len(country_analysis),
            "top_countries": top_countries.to_dict('records'),
            "total_passengers": country_analysis['sum'].sum(),
            "avg_per_country": country_analysis['sum'].mean(),
            "visualization": fig.to_json(),
            "data_points": len(country_analysis)
        }
        
    except Exception as e:
        return {"error": f"Error in geographic analysis: {str(e)}"}


def analyze_seasonal_patterns(
    data: Dict[str, Any],
    filters: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Analyze seasonal patterns in passenger data.
    
    Args:
        data: Dictionary containing the loaded data
        filters: Optional filters to apply
        
    Returns:
        Dictionary containing seasonal analysis results
    """
    try:
        passengers_df = data.get('passengers')
        if passengers_df is None or passengers_df.empty:
            return {"error": "No passenger data available"}
        
        # Apply filters if provided
        if filters:
            filter_obj = Filters()
            filtered_data = filter_obj.apply_filters(data, filters)
            passengers_df = filtered_data.get('passengers')
        
        # Group by month for seasonal analysis
        seasonal_data = passengers_df.groupby('Month')['Total'].agg(['sum', 'mean', 'std']).reset_index()
        seasonal_data['MonthName'] = seasonal_data['Month'].apply(_get_month_name)
        
        # Calculate seasonal metrics
        peak_month = seasonal_data.loc[seasonal_data['sum'].idxmax()]
        low_month = seasonal_data.loc[seasonal_data['sum'].idxmin()]
        seasonal_variation = (seasonal_data['sum'].max() - seasonal_data['sum'].min()) / seasonal_data['sum'].mean()
        
        # Create visualization
        fig = px.bar(seasonal_data, x='MonthName', y='sum', 
                    title='Análisis Estacional de Pasajeros',
                    labels={'sum': 'Total Pasajeros', 'MonthName': 'Mes'})
        fig.update_layout(xaxis_title='Mes', yaxis_title='Total Pasajeros')
        
        return {
            "analysis_type": "seasonal_analysis",
            "peak_month": peak_month.to_dict(),
            "low_month": low_month.to_dict(),
            "seasonal_variation": seasonal_variation,
            "monthly_stats": seasonal_data.to_dict('records'),
            "visualization": fig.to_json(),
            "data_points": len(seasonal_data)
        }
        
    except Exception as e:
        return {"error": f"Error in seasonal analysis: {str(e)}"}


def perform_statistical_analysis(
    data: Dict[str, Any],
    filters: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Perform statistical analysis on passenger data.
    
    Args:
        data: Dictionary containing the loaded data
        filters: Optional filters to apply
        
    Returns:
        Dictionary containing statistical analysis results
    """
    try:
        passengers_df = data.get('passengers')
        if passengers_df is None or passengers_df.empty:
            return {"error": "No passenger data available"}
        
        # Apply filters if provided
        if filters:
            filter_obj = Filters()
            filtered_data = filter_obj.apply_filters(data, filters)
            passengers_df = filtered_data.get('passengers')
        
        # Calculate descriptive statistics
        stats = passengers_df['Total'].describe()
        
        # Calculate additional metrics
        median = passengers_df['Total'].median()
        mode = passengers_df['Total'].mode().iloc[0] if not passengers_df['Total'].mode().empty else 0
        skewness = passengers_df['Total'].skew()
        kurtosis = passengers_df['Total'].kurtosis()
        
        # Create histogram
        fig = px.histogram(passengers_df, x='Total', 
                         title='Distribución de Pasajeros',
                         labels={'Total': 'Total Pasajeros', 'count': 'Frecuencia'})
        fig.update_layout(xaxis_title='Total Pasajeros', yaxis_title='Frecuencia')
        
        return {
            "analysis_type": "statistical_analysis",
            "descriptive_stats": stats.to_dict(),
            "median": median,
            "mode": mode,
            "skewness": skewness,
            "kurtosis": kurtosis,
            "visualization": fig.to_json(),
            "data_points": len(passengers_df)
        }
        
    except Exception as e:
        return {"error": f"Error in statistical analysis: {str(e)}"}


def compare_countries(
    data: Dict[str, Any],
    filters: Dict[str, Any] = None,
    countries: List[str] = None,
    top_n: int = 10
) -> Dict[str, Any]:
    """Compare passenger data across countries.
    
    Args:
        data: Dictionary containing the loaded data
        filters: Optional filters to apply
        countries: Specific countries to compare (if None, uses top N)
        top_n: Number of top countries to include if countries not specified
        
    Returns:
        Dictionary containing country comparison results
    """
    try:
        passengers_df = data.get('passengers')
        if passengers_df is None or passengers_df.empty:
            return {"error": "No passenger data available"}
        
        # Apply filters if provided
        if filters:
            filter_obj = Filters()
            filtered_data = filter_obj.apply_filters(data, filters)
            passengers_df = filtered_data.get('passengers')
        
        # Filter by specific countries if provided
        if countries:
            passengers_df = passengers_df[passengers_df['ISO3'].isin(countries)]
        
        # Analyze by country
        country_analysis = passengers_df.groupby('ISO3')['Total'].agg(['sum', 'mean', 'count']).reset_index()
        country_analysis = country_analysis.sort_values('sum', ascending=False)
        
        # Get top countries
        top_countries = country_analysis.head(top_n)
        
        # Create visualization
        fig = px.bar(top_countries, x='ISO3', y='sum', 
                    title=f'Comparación de Pasajeros por País (Top {top_n})',
                    labels={'sum': 'Total Pasajeros', 'ISO3': 'País'})
        fig.update_layout(xaxis_title='País', yaxis_title='Total Pasajeros')
        
        return {
            "analysis_type": "comparison_analysis",
            "total_countries": len(country_analysis),
            "top_countries": top_countries.to_dict('records'),
            "total_passengers": country_analysis['sum'].sum(),
            "avg_per_country": country_analysis['sum'].mean(),
            "visualization": fig.to_json(),
            "data_points": len(country_analysis)
        }
        
    except Exception as e:
        return {"error": f"Error in country comparison: {str(e)}"}


def _calculate_growth_rate(data: pd.DataFrame) -> float:
    """Calculate growth rate from time series data.
    
    Args:
        data: DataFrame with time series data
        
    Returns:
        float: Growth rate as a percentage
    """
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


def _get_month_name(month_num: int) -> str:
    """Get month name from month number.
    
    Args:
        month_num: Month number (1-12)
        
    Returns:
        str: Month name in Spanish
    """
    month_names = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
        5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
        9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    return month_names.get(month_num, f'Mes {month_num}')


# Create tool instances
analyze_trends_tool = Tool(
    name="analyze_trends",
    description="Analyze trends in passenger data over time",
    func=analyze_trends
)

analyze_holiday_impact_tool = Tool(
    name="analyze_holiday_impact",
    description="Analyze the impact of holidays on passenger traffic",
    func=analyze_holiday_impact
)

analyze_geographic_distribution_tool = Tool(
    name="analyze_geographic_distribution",
    description="Analyze geographic distribution of passenger data",
    func=analyze_geographic_distribution
)

analyze_seasonal_patterns_tool = Tool(
    name="analyze_seasonal_patterns",
    description="Analyze seasonal patterns in passenger data",
    func=analyze_seasonal_patterns
)

perform_statistical_analysis_tool = Tool(
    name="perform_statistical_analysis",
    description="Perform statistical analysis on passenger data",
    func=perform_statistical_analysis
)

compare_countries_tool = Tool(
    name="compare_countries",
    description="Compare passenger data across countries",
    func=compare_countries
)
