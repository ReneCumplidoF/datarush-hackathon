#!/usr/bin/env python3
"""
Test script for narrative style analysis.

This script tests the new narrative style of the data analysis agent.
"""

import os
import sys
import pandas as pd
from datetime import datetime

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.extensions.data_analysis_agent.simple_integration import simple_data_analysis_agent


def test_narrative_style():
    """Test the narrative style of the analysis agent."""
    
    print("📖 Testing Narrative Style Analysis...")
    print("=" * 50)
    
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
    
    # Test queries for different narrative styles
    test_queries = [
        "¿Pueden analizar la información de Letonia?",
        "¿Cuáles son las tendencias de pasajeros en España?",
        "¿Cómo está el tráfico aéreo en Francia?",
        "¿Qué datos tienes de Alemania?",
        "¿Puedes analizar los datos de Estados Unidos?",
        "¿Cómo se compara México con otros países?",
        "¿Hay información sobre Canadá?",
        "¿Cuál es el panorama general del tráfico aéreo?",
        "¿Qué países tienen mayor actividad?",
        "¿Cómo influyen los feriados en el tráfico?"
    ]
    
    print(f"📊 Testing with {len(test_queries)} narrative queries...")
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
                # Get narrative summary
                narrative = simple_data_analysis_agent.get_analysis_summary(results)
                print(f"✅ Narrative generated successfully")
                print(f"📖 Analysis Type: {results.get('analysis_type', 'Unknown')}")
                print()
                print("📝 **Narrative Summary:**")
                print(narrative)
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        print("\n" + "=" * 60 + "\n")
    
    print("✅ Narrative style testing completed!")


def test_narrative_quality():
    """Test the quality of narrative generation."""
    
    print("🎯 Testing Narrative Quality...")
    print("=" * 50)
    
    # Test specific narrative elements
    test_cases = [
        {
            "query": "¿Pueden analizar la información de Letonia?",
            "expected_elements": ["Volumen de tráfico", "Actividad mensual", "Período de análisis", "Feriados registrados", "Importancia global", "Tendencia", "Patrones estacionales"]
        },
        {
            "query": "¿Cuál es el panorama general del tráfico aéreo?",
            "expected_elements": ["Escala global", "Cobertura geográfica", "Impacto de feriados", "Distribución promedio", "Hallazgos clave"]
        }
    ]
    
    mock_context = {
        "data_loaded": True,
        "current_filters": {},
        "data": {
            "passengers": pd.DataFrame({
                'ISO3': ['LVA', 'LVA', 'LVA', 'LVA', 'ESP', 'ESP', 'ESP', 'ESP'],
                'Year': [2020, 2021, 2022, 2023, 2020, 2021, 2022, 2023],
                'Month': [1, 1, 1, 1, 1, 1, 1, 1],
                'Total': [1000, 1200, 1400, 1600, 5000, 5500, 6000, 6500]
            }),
            "holidays": pd.DataFrame({
                'ISO3': ['LVA', 'LVA', 'ESP', 'ESP'],
                'Date': ['2020-01-01', '2021-01-01', '2020-01-01', '2021-01-01'],
                'Name': ['New Year', 'New Year', 'Año Nuevo', 'Año Nuevo'],
                'Type': ['Public holiday', 'Public holiday', 'Public holiday', 'Public holiday']
            })
        }
    }
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"🔍 Test Case {i}: {test_case['query']}")
        print("-" * 40)
        
        try:
            # Analyze the query
            results = simple_data_analysis_agent.analyze_user_query(test_case['query'], mock_context)
            
            if results.get("error", False):
                print(f"❌ Error: {results.get('message', 'Unknown error')}")
            else:
                # Get narrative summary
                narrative = simple_data_analysis_agent.get_analysis_summary(results)
                
                # Check for expected elements
                found_elements = []
                missing_elements = []
                
                for element in test_case['expected_elements']:
                    if element in narrative:
                        found_elements.append(element)
                    else:
                        missing_elements.append(element)
                
                print(f"✅ Narrative generated successfully")
                print(f"📊 Found elements: {len(found_elements)}/{len(test_case['expected_elements'])}")
                print(f"   - Found: {', '.join(found_elements)}")
                if missing_elements:
                    print(f"   - Missing: {', '.join(missing_elements)}")
                
                # Show narrative preview
                print(f"\n📝 **Narrative Preview:**")
                lines = narrative.split('\n')
                for line in lines[:10]:  # Show first 10 lines
                    print(line)
                if len(lines) > 10:
                    print("...")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        print("\n" + "=" * 60 + "\n")
    
    print("✅ Narrative quality testing completed!")


if __name__ == "__main__":
    print("🚀 Starting Narrative Style Tests")
    print("=" * 60)
    
    # Test narrative style
    test_narrative_style()
    
    print("\n" + "=" * 60)
    
    # Test narrative quality
    test_narrative_quality()
    
    print("\n🎉 All narrative style tests completed!")
    print("\n📝 The agent now provides narrative-style analysis instead of raw variables.")

