#!/usr/bin/env python3
"""
Test script for Business Advisor Agent.

This script tests the business advisor agent's ability to provide
recommendations based on air traffic patterns and holiday data.
"""

import os
import sys
import pandas as pd
from datetime import datetime

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.extensions.business_advisor_agent.simple_integration import simple_business_advisor


def test_business_advisor():
    """Test the business advisor agent functionality."""
    
    print("💼 Testing Business Advisor Agent...")
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
    
    # Test queries for different business sectors
    test_queries = [
        "Necesito recomendaciones para mi negocio de turismo",
        "¿Qué me recomiendas para mi restaurante?",
        "Tengo una tienda de retail, ¿qué estrategias me sugieres?",
        "Soy dueño de un hotel, ¿cómo puedo aprovechar el tráfico aéreo?",
        "Tengo un negocio de transporte, ¿qué me recomiendas?",
        "Mi empresa es de entretenimiento, ¿qué estrategias me sugieres?",
        "Ofrezco servicios profesionales, ¿cómo puedo optimizar mi negocio?",
        "Organizo eventos, ¿qué me recomiendas?",
        "Tengo un café, ¿cómo puedo aprovechar los feriados?",
        "Mi negocio es de logística, ¿qué estrategias me sugieres?"
    ]
    
    print(f"📊 Testing with {len(test_queries)} business queries...")
    print()
    
    # Test each query
    for i, query in enumerate(test_queries, 1):
        print(f"🔍 Test {i}: {query}")
        print("-" * 40)
        
        try:
            # Analyze the query
            results = simple_business_advisor.analyze_business_query(query, mock_context)
            
            if results.get("error", False):
                print(f"❌ Error: {results.get('message', 'Unknown error')}")
            else:
                print(f"✅ Analysis successful")
                print(f"📊 Business Sector: {results.get('business_sector', 'Unknown')}")
                print(f"📈 Success: {results.get('success', False)}")
                
                # Show business summary
                summary = simple_business_advisor.get_business_summary(results)
                print(f"\n📝 **Business Summary:**")
                print(summary)
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        print("\n" + "=" * 60 + "\n")
    
    print("✅ Business advisor testing completed!")


def test_business_sector_detection():
    """Test business sector detection functionality."""
    
    print("🔍 Testing Business Sector Detection...")
    print("=" * 50)
    
    # Test different ways of mentioning business sectors
    test_queries = [
        "turismo", "hotel", "hospedaje", "viaje", "vacaciones", "turista",
        "retail", "tienda", "comercio", "venta", "productos", "shopping",
        "restaurante", "comida", "gastronomía", "cocina", "bar", "café",
        "transporte", "taxi", "uber", "logística", "delivery", "envío",
        "entretenimiento", "cine", "teatro", "museo", "parque", "diversión",
        "servicio", "consultoría", "profesional", "asesoría", "clínica", "oficina",
        "evento", "fiesta", "boda", "conferencia", "celebración", "festival"
    ]
    
    expected_sectors = [
        "turismo", "turismo", "turismo", "turismo", "turismo", "turismo",
        "retail", "retail", "retail", "retail", "retail", "retail",
        "restaurantes", "restaurantes", "restaurantes", "restaurantes", "restaurantes", "restaurantes",
        "transporte", "transporte", "transporte", "transporte", "transporte", "transporte",
        "entretenimiento", "entretenimiento", "entretenimiento", "entretenimiento", "entretenimiento", "entretenimiento",
        "servicios", "servicios", "servicios", "servicios", "servicios", "servicios",
        "eventos", "eventos", "eventos", "eventos", "eventos", "eventos"
    ]
    
    print(f"📊 Testing {len(test_queries)} business sector mentions...")
    print()
    
    # Test each query
    for i, (query, expected_sector) in enumerate(zip(test_queries, expected_sectors), 1):
        print(f"🔍 Test {i}: '{query}' -> Expected: {expected_sector}")
        
        try:
            # Create a simple context
            context = {
                "data_loaded": True,
                "data": {
                    "passengers": pd.DataFrame({
                        'ISO3': ['LVA', 'LVA'],
                        'Year': [2020, 2021],
                        'Month': [1, 1],
                        'Total': [1000, 1200]
                    })
                }
            }
            
            # Analyze the query
            results = simple_business_advisor.analyze_business_query(f"Necesito recomendaciones para mi negocio de {query}", context)
            
            if results.get("error", False):
                print(f"❌ Error: {results.get('message', 'Unknown error')}")
            else:
                detected_sector = results.get('business_sector', '')
                if detected_sector == expected_sector:
                    print(f"✅ Correctly detected: {detected_sector}")
                else:
                    print(f"⚠️ Detected: {detected_sector}, Expected: {expected_sector}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        print()
    
    print("✅ Business sector detection testing completed!")


def test_business_recommendations():
    """Test business recommendations for different sectors."""
    
    print("💡 Testing Business Recommendations...")
    print("=" * 50)
    
    # Test specific business sectors
    business_sectors = [
        'turismo', 'retail', 'restaurantes', 'transporte', 
        'entretenimiento', 'servicios', 'eventos'
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
    
    for i, sector in enumerate(business_sectors, 1):
        print(f"🔍 Test {i}: Business sector '{sector}'")
        print("-" * 40)
        
        try:
            # Get recommendations for the sector
            results = simple_business_advisor.get_business_recommendations(sector, mock_context)
            
            if results.get("error", False):
                print(f"❌ Error: {results.get('message', 'Unknown error')}")
            else:
                print(f"✅ Recommendations generated successfully")
                print(f"📊 Business Sector: {results.get('business_sector', 'Unknown')}")
                
                # Show recommendations summary
                summary = simple_business_advisor.get_business_summary(results)
                print(f"\n📝 **Recommendations Summary:**")
                lines = summary.split('\n')
                for line in lines[:15]:  # Show first 15 lines
                    print(line)
                if len(lines) > 15:
                    print("...")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        print("\n" + "=" * 60 + "\n")
    
    print("✅ Business recommendations testing completed!")


if __name__ == "__main__":
    print("🚀 Starting Business Advisor Tests")
    print("=" * 60)
    
    # Test business advisor
    test_business_advisor()
    
    print("\n" + "=" * 60)
    
    # Test business sector detection
    test_business_sector_detection()
    
    print("\n" + "=" * 60)
    
    # Test business recommendations
    test_business_recommendations()
    
    print("\n🎉 All business advisor tests completed!")
    print("\n📝 The business advisor agent is ready to provide recommendations based on traffic and holiday data.")

