#!/usr/bin/env python3
"""
Test script for the simplified DataRush system (without BigQuery).

This script tests the system functionality without BigQuery dependencies.
"""

import os
import sys
import pandas as pd
from datetime import datetime

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_simple_system():
    """Test the simplified system components."""
    
    print("🧪 Testing Simplified DataRush System...")
    print("=" * 50)
    
    # Test 1: Data Loader
    print("1. Testing Data Loader...")
    try:
        from components.data_loader import DataLoader
        data_loader = DataLoader()
        print("✅ Data Loader imported successfully")
        
        # Test loading data
        if data_loader.load_data():
            print("✅ Data loading successful")
            if data_loader.clean_data():
                print("✅ Data cleaning successful")
                data = data_loader.get_processed_data()
                print(f"✅ Data processed: {len(data)} datasets")
            else:
                print("⚠️ Data cleaning failed")
        else:
            print("⚠️ Data loading failed")
    except Exception as e:
        print(f"❌ Data Loader error: {str(e)}")
    
    print()
    
    # Test 2: Filters
    print("2. Testing Filters...")
    try:
        from components.filters import Filters
        filters = Filters()
        print("✅ Filters imported successfully")
    except Exception as e:
        print(f"❌ Filters error: {str(e)}")
    
    print()
    
    # Test 3: Visualizations
    print("3. Testing Visualizations...")
    try:
        from components.visualizations import Visualizations
        visualizations = Visualizations()
        print("✅ Visualizations imported successfully")
    except Exception as e:
        print(f"❌ Visualizations error: {str(e)}")
    
    print()
    
    # Test 4: Chat Agent
    print("4. Testing Chat Agent...")
    try:
        from components.chat_agent import ChatAgent
        chat_agent = ChatAgent()
        print("✅ Chat Agent imported successfully")
    except Exception as e:
        print(f"❌ Chat Agent error: {str(e)}")
    
    print()
    
    # Test 5: Simple BigQuery Integration (without BigQuery)
    print("5. Testing Simple BigQuery Integration...")
    try:
        from components.simple_bigquery_integration import simple_bigquery_integration
        print("✅ Simple BigQuery Integration imported successfully")
        
        # Test with mock data
        mock_data = {
            "passengers": pd.DataFrame({
                'ISO3': ['USA', 'MEX', 'CAN'],
                'Year': [2020, 2021, 2022],
                'Month': [1, 1, 1],
                'Total': [1000, 1200, 1400]
            }),
            "holidays": pd.DataFrame({
                'ISO3': ['USA', 'MEX', 'CAN'],
                'Date': ['2020-01-01', '2021-01-01', '2022-01-01'],
                'Name': ['New Year', 'Año Nuevo', 'New Year'],
                'Type': ['Public holiday', 'Public holiday', 'Public holiday']
            })
        }
        
        validation_results = simple_bigquery_integration.validate_data_quality(mock_data)
        if validation_results.get("error", False):
            print(f"⚠️ Validation error: {validation_results.get('message', 'Unknown error')}")
        else:
            print(f"✅ Data validation successful")
            print(f"   Overall Score: {validation_results.get('overall_score', 0.0):.1%}")
            print(f"   Data Sources: {validation_results.get('quality_metrics', {}).get('data_sources_count', 0)}")
        
    except Exception as e:
        print(f"❌ Simple BigQuery Integration error: {str(e)}")
    
    print()
    
    # Test 6: Data Analysis Agent
    print("6. Testing Data Analysis Agent...")
    try:
        from agents.extensions.data_analysis_agent.simple_integration import simple_data_analysis_agent
        print("✅ Data Analysis Agent imported successfully")
        
        # Test with mock context
        mock_context = {
            "data_loaded": True,
            "data": {
                "passengers": pd.DataFrame({
                    'ISO3': ['USA', 'USA', 'MEX', 'MEX'],
                    'Year': [2020, 2021, 2020, 2021],
                    'Month': [1, 1, 1, 1],
                    'Total': [1000, 1200, 800, 900]
                })
            }
        }
        
        analysis_results = simple_data_analysis_agent.analyze_user_query(
            "¿Cuáles son las tendencias de pasajeros?",
            mock_context
        )
        
        if analysis_results.get("error", False):
            print(f"⚠️ Analysis error: {analysis_results.get('message', 'Unknown error')}")
        else:
            print(f"✅ Data analysis successful")
            print(f"   Analysis Type: {analysis_results.get('analysis_type', 'Unknown')}")
            print(f"   Success: {analysis_results.get('success', False)}")
        
    except Exception as e:
        print(f"❌ Data Analysis Agent error: {str(e)}")
    
    print()
    
    # Test 7: Research Agent
    print("7. Testing Research Agent...")
    try:
        from agents.extensions.research_agent import ResearchAgent
        research_agent = ResearchAgent()
        print("✅ Research Agent imported successfully")
    except Exception as e:
        print(f"❌ Research Agent error: {str(e)}")
    
    print()
    
    # Test 8: Smart Chat Agent
    print("8. Testing Smart Chat Agent...")
    try:
        from agents.extensions.smart_chat_agent import SmartChatAgent
        smart_chat_agent = SmartChatAgent()
        print("✅ Smart Chat Agent imported successfully")
    except Exception as e:
        print(f"❌ Smart Chat Agent error: {str(e)}")
    
    print()
    
    print("✅ Simplified system testing completed!")


def test_data_validation():
    """Test data validation functionality."""
    
    print("🔍 Testing Data Validation...")
    print("=" * 50)
    
    try:
        from components.simple_bigquery_integration import simple_bigquery_integration
        
        # Create test data
        test_data = {
            "passengers": pd.DataFrame({
                'ISO3': ['USA', 'USA', 'MEX', 'MEX', 'CAN', 'CAN'],
                'Year': [2020, 2021, 2020, 2021, 2020, 2021],
                'Month': [1, 1, 1, 1, 1, 1],
                'Total': [1000, 1200, 800, 900, 600, 700]
            }),
            "holidays": pd.DataFrame({
                'ISO3': ['USA', 'USA', 'MEX', 'MEX', 'CAN', 'CAN'],
                'Date': ['2020-01-01', '2021-01-01', '2020-01-01', '2021-01-01', '2020-01-01', '2021-01-01'],
                'Name': ['New Year', 'New Year', 'Año Nuevo', 'Año Nuevo', 'New Year', 'New Year'],
                'Type': ['Public holiday', 'Public holiday', 'Public holiday', 'Public holiday', 'Public holiday', 'Public holiday']
            }),
            "countries": pd.DataFrame({
                'alpha_2': ['US', 'MX', 'CA'],
                'alpha_3': ['USA', 'MEX', 'CAN'],
                'name': ['United States', 'Mexico', 'Canada']
            })
        }
        
        # Run validation
        validation_results = simple_bigquery_integration.validate_data_quality(test_data)
        
        if validation_results.get("error", False):
            print(f"❌ Validation failed: {validation_results.get('message', 'Unknown error')}")
        else:
            print(f"✅ Validation successful!")
            print(f"   Overall Score: {validation_results.get('overall_score', 0.0):.1%}")
            
            # Show quality metrics
            quality_metrics = validation_results.get('quality_metrics', {})
            print(f"   Completeness: {quality_metrics.get('overall_completeness', 0.0):.1%}")
            print(f"   Consistency: {quality_metrics.get('overall_consistency', 0.0):.1%}")
            print(f"   Accuracy: {quality_metrics.get('overall_accuracy', 0.0):.1%}")
            print(f"   Total Issues: {quality_metrics.get('total_issues', 0)}")
            
            # Show recommendations
            recommendations = validation_results.get('recommendations', [])
            if recommendations:
                print(f"   Recommendations:")
                for i, rec in enumerate(recommendations, 1):
                    print(f"     {i}. {rec}")
            
            # Generate report
            report = simple_bigquery_integration.get_validation_report()
            print(f"\n📋 Validation Report Preview:")
            print(report[:500] + "..." if len(report) > 500 else report)
        
    except Exception as e:
        print(f"❌ Data validation error: {str(e)}")


if __name__ == "__main__":
    print("🚀 Starting Simplified DataRush System Tests")
    print("=" * 60)
    
    # Test system components
    test_simple_system()
    
    print("\n" + "=" * 60)
    
    # Test data validation
    test_data_validation()
    
    print("\n🎉 All tests completed!")
    print("\n📝 Note: This system works without BigQuery dependencies.")
    print("   All functionality is available using local data only.")

