#!/usr/bin/env python3
"""
Test script for the Simple Data Analysis Agent.

This script tests the simple data analysis agent integration with the DataRush system.
"""

import os
import sys
import pandas as pd
from datetime import datetime

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.extensions.data_analysis_agent.simple_integration import simple_data_analysis_agent


def test_simple_data_analysis_agent():
    """Test the simple data analysis agent with sample queries."""
    
    print("🧪 Testing Simple Data Analysis Agent...")
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
        "data": {
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
    }
    
    print(f"📊 Available Analysis Types:")
    available_analyses = simple_data_analysis_agent.get_available_analyses()
    for analysis in available_analyses:
        print(f"  - {analysis['name']}: {analysis['description']}")
    print()
    
    # Test each query
    for i, query in enumerate(test_queries, 1):
        print(f"🔍 Test {i}: {query}")
        print("-" * 30)
        
        try:
            # Analyze the query
            results = simple_data_analysis_agent.analyze_user_query(query, mock_context)
            
            if results.get("error", False):
                print(f"❌ Error: {results.get('message', 'Unknown error')}")
            else:
                print(f"✅ Analysis Type: {results.get('analysis_type', 'Unknown')}")
                print(f"📈 Success: {results.get('success', False)}")
                
                # Show summary
                summary = simple_data_analysis_agent.get_analysis_summary(results)
                print(f"📋 Summary:\n{summary}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        print()
    
    print("✅ Simple Data Analysis Agent testing completed!")


def test_agent_with_real_data():
    """Test the agent with real data loading."""
    
    print("🔧 Testing Agent with Real Data Loading...")
    print("=" * 50)
    
    try:
        # Test with real data loading
        results = simple_data_analysis_agent.analyze_user_query(
            "¿Cuáles son las tendencias de pasajeros?",
            {"data_loaded": False}  # This will trigger data loading
        )
        
        if results.get("error", False):
            print(f"⚠️ Expected error (no data loaded): {results.get('message', 'Unknown error')}")
        else:
            print(f"✅ Unexpected success: {results.get('analysis_type', 'Unknown')}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    print("✅ Real data loading test completed!")


if __name__ == "__main__":
    print("🚀 Starting Simple Data Analysis Agent Tests")
    print("=" * 60)
    
    # Test the agent with mock data
    test_simple_data_analysis_agent()
    
    print("\n" + "=" * 60)
    
    # Test with real data loading
    test_agent_with_real_data()
    
    print("\n🎉 All tests completed!")

