#!/usr/bin/env python3
"""
Test script for the Data Analysis Agent.

This script tests the data analysis agent integration with the DataRush system.
"""

import os
import sys
import pandas as pd
from datetime import datetime

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.extensions.data_analysis_agent.integration import data_analysis_integration


def test_data_analysis_agent():
    """Test the data analysis agent with sample queries."""
    
    print("🧪 Testing Data Analysis Agent...")
    print("=" * 50)
    
    # Test queries
    test_queries = [
        "¿Cuáles son las tendencias de pasajeros en los últimos años?",
        "¿Cómo afectan los feriados al tráfico aéreo?",
        "¿Qué países tienen más pasajeros?",
        "¿Hay patrones estacionales en los datos?",
        "¿Cuál es la correlación entre feriados y pasajeros?"
    ]
    
    # Mock context (simulating DataRush system context)
    mock_context = {
        "data_loaded": True,
        "current_filters": {},
        "filtered_data": {
            "passengers": pd.DataFrame({
                'ISO3': ['USA', 'USA', 'USA', 'MEX', 'MEX', 'MEX'],
                'Year': [2020, 2021, 2022, 2020, 2021, 2022],
                'Month': [1, 1, 1, 1, 1, 1],
                'Total': [1000, 1200, 1400, 800, 900, 1100]
            }),
            "holidays": pd.DataFrame({
                'ISO3': ['USA', 'USA', 'MEX', 'MEX'],
                'Date': ['2020-01-01', '2021-01-01', '2020-01-01', '2021-01-01'],
                'Name': ['New Year', 'New Year', 'Año Nuevo', 'Año Nuevo'],
                'Type': ['Public holiday', 'Public holiday', 'Public holiday', 'Public holiday']
            })
        }
    }
    
    print(f"📊 Available Analysis Types:")
    available_analyses = data_analysis_integration.get_available_analyses()
    for analysis in available_analyses:
        print(f"  - {analysis['name']}: {analysis['description']}")
    print()
    
    # Test each query
    for i, query in enumerate(test_queries, 1):
        print(f"🔍 Test {i}: {query}")
        print("-" * 30)
        
        try:
            # Analyze the query
            results = data_analysis_integration.analyze_user_query(query, mock_context)
            
            if results.get("error", False):
                print(f"❌ Error: {results.get('message', 'Unknown error')}")
            else:
                print(f"✅ Analysis Type: {results.get('analysis_type', 'Unknown')}")
                print(f"📈 Success: {results.get('success', False)}")
                
                # Show summary
                summary = data_analysis_integration.get_analysis_summary(results)
                print(f"📋 Summary:\n{summary}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        print()
    
    print("✅ Data Analysis Agent testing completed!")


def test_agent_tools():
    """Test the individual agent tools."""
    
    print("🔧 Testing Agent Tools...")
    print("=" * 50)
    
    # Mock data
    mock_data = {
        "passengers": pd.DataFrame({
            'ISO3': ['USA', 'USA', 'USA', 'MEX', 'MEX', 'MEX', 'CAN', 'CAN', 'CAN'],
            'Year': [2020, 2021, 2022, 2020, 2021, 2022, 2020, 2021, 2022],
            'Month': [1, 1, 1, 1, 1, 1, 1, 1, 1],
            'Total': [1000, 1200, 1400, 800, 900, 1100, 600, 700, 800]
        }),
        "holidays": pd.DataFrame({
            'ISO3': ['USA', 'USA', 'MEX', 'MEX', 'CAN', 'CAN'],
            'Date': ['2020-01-01', '2021-01-01', '2020-01-01', '2021-01-01', '2020-01-01', '2021-01-01'],
            'Name': ['New Year', 'New Year', 'Año Nuevo', 'Año Nuevo', 'New Year', 'New Year'],
            'Type': ['Public holiday', 'Public holiday', 'Public holiday', 'Public holiday', 'Public holiday', 'Public holiday']
        })
    }
    
    # Test trend analysis
    print("📈 Testing Trend Analysis...")
    try:
        from agents.extensions.data_analysis_agent.tools import analyze_trends
        trend_results = analyze_trends(mock_data)
        print(f"✅ Trend Analysis: {trend_results.get('analysis_type', 'Unknown')}")
        print(f"   Total Passengers: {trend_results.get('total_passengers', 0):,}")
        print(f"   Growth Rate: {trend_results.get('growth_rate', 0):.2%}")
    except Exception as e:
        print(f"❌ Trend Analysis Error: {str(e)}")
    
    # Test holiday impact analysis
    print("\n🎉 Testing Holiday Impact Analysis...")
    try:
        from agents.extensions.data_analysis_agent.tools import analyze_holiday_impact
        holiday_results = analyze_holiday_impact(mock_data)
        print(f"✅ Holiday Impact Analysis: {holiday_results.get('analysis_type', 'Unknown')}")
        print(f"   Correlation: {holiday_results.get('correlation', 0):.3f}")
        print(f"   Total Holidays: {holiday_results.get('total_holidays', 0)}")
    except Exception as e:
        print(f"❌ Holiday Impact Analysis Error: {str(e)}")
    
    # Test geographic analysis
    print("\n🌍 Testing Geographic Analysis...")
    try:
        from agents.extensions.data_analysis_agent.tools import analyze_geographic_distribution
        geo_results = analyze_geographic_distribution(mock_data, top_n=5)
        print(f"✅ Geographic Analysis: {geo_results.get('analysis_type', 'Unknown')}")
        print(f"   Total Countries: {geo_results.get('total_countries', 0)}")
        print(f"   Total Passengers: {geo_results.get('total_passengers', 0):,}")
    except Exception as e:
        print(f"❌ Geographic Analysis Error: {str(e)}")
    
    print("\n✅ Agent Tools testing completed!")


if __name__ == "__main__":
    print("🚀 Starting Data Analysis Agent Tests")
    print("=" * 60)
    
    # Test the integration
    test_data_analysis_agent()
    
    print("\n" + "=" * 60)
    
    # Test the tools
    test_agent_tools()
    
    print("\n🎉 All tests completed!")

