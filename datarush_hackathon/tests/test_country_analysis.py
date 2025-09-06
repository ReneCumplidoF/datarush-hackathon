#!/usr/bin/env python3
"""
Test script for country-specific analysis.

This script tests the data analysis agent's ability to analyze specific countries.
"""

import os
import sys
import pandas as pd
from datetime import datetime

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.extensions.data_analysis_agent.simple_integration import simple_data_analysis_agent


def test_country_analysis():
    """Test country-specific analysis functionality."""
    
    print("🧪 Testing Country-Specific Analysis...")
    print("=" * 50)
    
    # Test queries for different countries
    test_queries = [
        "¿Pueden analizar la información de Letonia?",
        "¿Cuáles son las tendencias de pasajeros en España?",
        "¿Cómo está el tráfico aéreo en Francia?",
        "¿Qué datos tienes de Alemania?",
        "¿Puedes analizar los datos de Estados Unidos?",
        "¿Cómo se compara México con otros países?",
        "¿Hay información sobre Canadá?"
    ]
    
    # Mock context with sample data
    mock_context = {
        "data_loaded": True,
        "current_filters": {},
        "data": {
            "passengers": pd.DataFrame({
                'ISO3': ['LVA', 'LVA', 'LVA', 'LVA', 'ESP', 'ESP', 'ESP', 'ESP', 'FRA', 'FRA', 'FRA', 'FRA', 'DEU', 'DEU', 'DEU', 'DEU', 'USA', 'USA', 'USA', 'USA', 'MEX', 'MEX', 'MEX', 'MEX', 'CAN', 'CAN', 'CAN', 'CAN'],
                'Year': [2020, 2021, 2022, 2023, 2020, 2021, 2022, 2023, 2020, 2021, 2022, 2023, 2020, 2021, 2022, 2023, 2020, 2021, 2022, 2023, 2020, 2021, 2022, 2023, 2020, 2021, 2022, 2023],
                'Month': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                'Total': [1000, 1200, 1400, 1600, 5000, 5500, 6000, 6500, 8000, 8500, 9000, 9500, 12000, 13000, 14000, 15000, 20000, 22000, 24000, 26000, 3000, 3200, 3400, 3600, 4000, 4200, 4400, 4600]
            }),
            "holidays": pd.DataFrame({
                'ISO3': ['LVA', 'LVA', 'ESP', 'ESP', 'FRA', 'FRA', 'DEU', 'DEU', 'USA', 'USA', 'MEX', 'MEX', 'CAN', 'CAN'],
                'Date': ['2020-01-01', '2021-01-01', '2020-01-01', '2021-01-01', '2020-01-01', '2021-01-01', '2020-01-01', '2021-01-01', '2020-01-01', '2021-01-01', '2020-01-01', '2021-01-01', '2020-01-01', '2021-01-01'],
                'Name': ['New Year', 'New Year', 'Año Nuevo', 'Año Nuevo', 'Jour de l\'An', 'Jour de l\'An', 'Neujahr', 'Neujahr', 'New Year', 'New Year', 'Año Nuevo', 'Año Nuevo', 'New Year', 'New Year'],
                'Type': ['Public holiday', 'Public holiday', 'Public holiday', 'Public holiday', 'Public holiday', 'Public holiday', 'Public holiday', 'Public holiday', 'Public holiday', 'Public holiday', 'Public holiday', 'Public holiday', 'Public holiday', 'Public holiday']
            })
        }
    }
    
    print(f"📊 Testing with {len(test_queries)} country-specific queries...")
    print()
    
    # Test each query
    for i, query in enumerate(test_queries, 1):
        print(f"🔍 Test {i}: {query}")
        print("-" * 40)
        
        try:
            # Analyze the query
            results = simple_data_analysis_agent.analyze_user_query(query, mock_context)
            
            if results.get("error", False):
                print(f"❌ Error: {results.get('message', 'Unknown error')}")
            else:
                print(f"✅ Analysis Type: {results.get('analysis_type', 'Unknown')}")
                print(f"📈 Success: {results.get('success', False)}")
                
                # Show insights
                insights = results.get('insights', [])
                if insights:
                    print(f"💡 Insights:")
                    for insight in insights[:3]:  # Show first 3 insights
                        print(f"   - {insight}")
                
                # Show metrics
                metrics = results.get('metrics', {})
                if metrics:
                    print(f"📊 Key Metrics:")
                    for key, value in list(metrics.items())[:3]:  # Show first 3 metrics
                        if isinstance(value, (int, float)):
                            print(f"   - {key}: {value:,.0f}")
                        else:
                            print(f"   - {key}: {value}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        print()
    
    print("✅ Country-specific analysis testing completed!")


def test_country_detection():
    """Test country detection functionality."""
    
    print("🔍 Testing Country Detection...")
    print("=" * 50)
    
    # Test different ways of mentioning countries
    test_queries = [
        "latvia", "Letonia", "LVA", "LV",
        "spain", "España", "ESP", "ES",
        "france", "Francia", "FRA", "FR",
        "germany", "Alemania", "DEU", "DE",
        "united states", "Estados Unidos", "USA", "US",
        "mexico", "México", "MEX", "MX",
        "canada", "Canadá", "CAN", "CA"
    ]
    
    expected_codes = [
        "LVA", "LVA", "LVA", "LVA",
        "ESP", "ESP", "ESP", "ESP",
        "FRA", "FRA", "FRA", "FRA",
        "DEU", "DEU", "DEU", "DEU",
        "USA", "USA", "USA", "USA",
        "MEX", "MEX", "MEX", "MEX",
        "CAN", "CAN", "CAN", "CAN"
    ]
    
    print(f"📊 Testing {len(test_queries)} country mentions...")
    print()
    
    # Test each query
    for i, (query, expected_code) in enumerate(zip(test_queries, expected_codes), 1):
        print(f"🔍 Test {i}: '{query}' -> Expected: {expected_code}")
        
        try:
            # Create a simple context
            context = {
                "data_loaded": True,
                "data": {
                    "passengers": pd.DataFrame({
                        'ISO3': [expected_code, expected_code],
                        'Year': [2020, 2021],
                        'Month': [1, 1],
                        'Total': [1000, 1200]
                    })
                }
            }
            
            # Analyze the query
            results = simple_data_analysis_agent.analyze_user_query(f"analizar {query}", context)
            
            if results.get("error", False):
                print(f"❌ Error: {results.get('message', 'Unknown error')}")
            else:
                analysis_type = results.get('analysis_type', '')
                if 'country_specific' in analysis_type:
                    country = results.get('metrics', {}).get('country', '')
                    if expected_code in country:
                        print(f"✅ Correctly detected: {country}")
                    else:
                        print(f"⚠️ Detected: {country}, Expected: {expected_code}")
                else:
                    print(f"⚠️ Not detected as country-specific: {analysis_type}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        print()
    
    print("✅ Country detection testing completed!")


if __name__ == "__main__":
    print("🚀 Starting Country Analysis Tests")
    print("=" * 60)
    
    # Test country-specific analysis
    test_country_analysis()
    
    print("\n" + "=" * 60)
    
    # Test country detection
    test_country_detection()
    
    print("\n🎉 All country analysis tests completed!")
    print("\n📝 Note: The agent should now properly detect and analyze specific countries.")

