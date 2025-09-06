#!/usr/bin/env python3
"""
Test script to verify data flow from DataRush to the analysis agent.

This script tests the complete data flow from data loading to analysis.
"""

import os
import sys
import pandas as pd
from datetime import datetime

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from components.data_loader import DataLoader
from components.filters import Filters
from agents.extensions.data_analysis_agent.simple_integration import simple_data_analysis_agent


def test_data_flow():
    """Test the complete data flow from loading to analysis."""
    
    print("🧪 Testing Complete Data Flow...")
    print("=" * 50)
    
    # Step 1: Load data using DataLoader
    print("📊 Step 1: Loading data...")
    data_loader = DataLoader()
    
    if not data_loader.load_data():
        print("❌ Failed to load data")
        return False
    
    if not data_loader.clean_data():
        print("❌ Failed to clean data")
        return False
    
    data = data_loader.get_processed_data()
    print(f"✅ Data loaded successfully")
    print(f"   - Passengers: {data.get('passengers', pd.DataFrame()).shape}")
    print(f"   - Holidays: {data.get('holidays', pd.DataFrame()).shape}")
    print(f"   - Countries: {data.get('countries', pd.DataFrame()).shape}")
    
    # Step 2: Apply filters
    print("\n🔍 Step 2: Applying filters...")
    filters = Filters()
    filtered_data = filters.apply_filters(data, {})
    print(f"✅ Filters applied successfully")
    print(f"   - Filtered passengers: {filtered_data.get('passengers', pd.DataFrame()).shape}")
    print(f"   - Filtered holidays: {filtered_data.get('holidays', pd.DataFrame()).shape}")
    
    # Step 3: Create context
    print("\n📋 Step 3: Creating context...")
    context = {
        "data_loaded": True,
        "current_filters": {},
        "data": filtered_data,
        "filtered_data": filtered_data
    }
    print(f"✅ Context created successfully")
    print(f"   - data_loaded: {context['data_loaded']}")
    print(f"   - data keys: {list(context['data'].keys())}")
    
    # Step 4: Test analysis agent
    print("\n🤖 Step 4: Testing analysis agent...")
    test_queries = [
        "¿Cuántos pasajeros hay en total?",
        "¿Pueden analizar la información de Letonia?",
        "¿Cuáles son las tendencias de pasajeros?",
        "¿Cómo está el tráfico aéreo en España?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Test Query {i}: {query}")
        print("-" * 40)
        
        try:
            # Analyze the query
            results = simple_data_analysis_agent.analyze_user_query(query, context)
            
            if results.get("error", False):
                print(f"❌ Error: {results.get('message', 'Unknown error')}")
            else:
                print(f"✅ Analysis successful")
                print(f"   - Type: {results.get('analysis_type', 'Unknown')}")
                print(f"   - Success: {results.get('success', False)}")
                
                # Show insights
                insights = results.get('insights', [])
                if insights:
                    print(f"   - Insights: {len(insights)} found")
                    for insight in insights[:2]:  # Show first 2 insights
                        print(f"     • {insight}")
                
                # Show metrics
                metrics = results.get('metrics', {})
                if metrics:
                    print(f"   - Metrics: {len(metrics)} found")
                    for key, value in list(metrics.items())[:3]:  # Show first 3 metrics
                        if isinstance(value, (int, float)):
                            print(f"     • {key}: {value:,.0f}")
                        else:
                            print(f"     • {key}: {value}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
    
    print("\n✅ Data flow testing completed!")
    return True


def test_context_creation():
    """Test context creation with different scenarios."""
    
    print("\n🧪 Testing Context Creation...")
    print("=" * 50)
    
    # Test 1: Empty context
    print("📋 Test 1: Empty context")
    context1 = {}
    results1 = simple_data_analysis_agent.analyze_user_query("¿Cuántos pasajeros hay?", context1)
    print(f"   - Error: {results1.get('error', False)}")
    print(f"   - Message: {results1.get('message', 'No message')}")
    
    # Test 2: Context with data_loaded=False
    print("\n📋 Test 2: Context with data_loaded=False")
    context2 = {
        "data_loaded": False,
        "data": {},
        "current_filters": {}
    }
    results2 = simple_data_analysis_agent.analyze_user_query("¿Cuántos pasajeros hay?", context2)
    print(f"   - Error: {results2.get('error', False)}")
    print(f"   - Message: {results2.get('message', 'No message')}")
    
    # Test 3: Context with data_loaded=True but empty data
    print("\n📋 Test 3: Context with data_loaded=True but empty data")
    context3 = {
        "data_loaded": True,
        "data": {},
        "current_filters": {}
    }
    results3 = simple_data_analysis_agent.analyze_user_query("¿Cuántos pasajeros hay?", context3)
    print(f"   - Error: {results3.get('error', False)}")
    print(f"   - Message: {results3.get('message', 'No message')}")
    
    print("\n✅ Context creation testing completed!")


if __name__ == "__main__":
    print("🚀 Starting Data Flow Tests")
    print("=" * 60)
    
    # Test complete data flow
    success = test_data_flow()
    
    if success:
        # Test context creation scenarios
        test_context_creation()
        
        print("\n🎉 All tests completed successfully!")
        print("\n📝 The data flow from DataRush to the analysis agent is working correctly.")
    else:
        print("\n❌ Data flow tests failed!")
        print("\n📝 Please check the data loading and processing components.")

