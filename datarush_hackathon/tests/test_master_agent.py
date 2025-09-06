#!/usr/bin/env python3
"""
Test script for Master Agent.

This script tests the master agent's ability to coordinate multiple
specialized agents for complex tasks.
"""

import os
import sys
import pandas as pd
from datetime import datetime

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.master_agent.simple_integration import simple_master_agent


def test_master_agent():
    """Test the master agent functionality."""
    
    print("🎯 Testing Master Agent...")
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
    
    # Test queries for different complexity levels
    test_queries = [
        # High complexity - comprehensive analysis
        "Necesito un análisis completo del tráfico aéreo en Europa con recomendaciones estratégicas para mi negocio de turismo",
        
        # Medium complexity - business strategy
        "¿Qué estrategias me recomiendas para mi restaurante basándote en los datos de tráfico?",
        
        # Medium complexity - research validation
        "Investiga los patrones de tráfico aéreo en España y valida los hallazgos con información externa",
        
        # Low complexity - quick analysis
        "¿Cuántos pasajeros hay en total?",
        
        # Business-focused query
        "Tengo un negocio de transporte, ¿cómo puedo aprovechar los datos de feriados?",
        
        # Research-focused query
        "Busca información sobre las tendencias futuras en aviación",
        
        # General query
        "¿Puedes ayudarme a entender los datos?"
    ]
    
    print(f"📊 Testing with {len(test_queries)} queries of different complexity...")
    print()
    
    # Test each query
    for i, query in enumerate(test_queries, 1):
        print(f"🔍 Test {i}: {query}")
        print("-" * 40)
        
        try:
            # Process query with master agent
            results = simple_master_agent.process_query(query, mock_context)
            
            if results.get("success", False):
                print(f"✅ Master agent processing successful")
                print(f"📊 Workflow used: {results.get('workflow_used', 'Unknown')}")
                print(f"🤖 Agents involved: {', '.join(results.get('agents_involved', []))}")
                
                # Show comprehensive summary
                summary = simple_master_agent.get_comprehensive_summary(results)
                print(f"\n📝 **Comprehensive Summary:**")
                lines = summary.split('\n')
                for line in lines[:15]:  # Show first 15 lines
                    print(line)
                if len(lines) > 15:
                    print("...")
                
            else:
                print(f"❌ Error: {results.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        print("\n" + "=" * 60 + "\n")
    
    print("✅ Master agent testing completed!")


def test_workflow_selection():
    """Test workflow selection for different queries."""
    
    print("🔄 Testing Workflow Selection...")
    print("=" * 50)
    
    test_queries = [
        "análisis completo del tráfico aéreo",
        "recomendaciones para mi negocio de turismo",
        "investigar patrones de tráfico",
        "¿cuántos pasajeros hay?",
        "estrategias para mi restaurante",
        "buscar información sobre aviación"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"🔍 Test {i}: {query}")
        print("-" * 40)
        
        try:
            # Get workflow suggestions
            suggestions = simple_master_agent.get_workflow_suggestions(query)
            
            if suggestions:
                print(f"✅ Found {len(suggestions)} workflow suggestions:")
                for j, suggestion in enumerate(suggestions[:3], 1):  # Show top 3
                    print(f"   {j}. {suggestion['name']} (Confidence: {suggestion['confidence']:.1%})")
                    print(f"      Agents: {', '.join(suggestion['agents'])}")
            else:
                print("⚠️ No workflow suggestions found")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        print()
    
    print("✅ Workflow selection testing completed!")


def test_agent_coordination():
    """Test agent coordination capabilities."""
    
    print("🤝 Testing Agent Coordination...")
    print("=" * 50)
    
    # Test comprehensive analysis workflow
    query = "Necesito un análisis integral del tráfico aéreo con recomendaciones de negocio"
    
    print(f"🔍 Testing comprehensive analysis: {query}")
    print("-" * 40)
    
    try:
        # Analyze query complexity
        analysis = simple_master_agent.analyze_query_complexity(query)
        
        if analysis.get('success', False):
            analysis_result = analysis['analysis']
            print(f"✅ Query analysis successful")
            print(f"   Complexity: {analysis_result.get('complexity', 'Unknown')}")
            print(f"   Query type: {analysis_result.get('query_type', 'Unknown')}")
            print(f"   Required capabilities: {analysis_result.get('required_capabilities', [])}")
            print(f"   Has data context: {analysis_result.get('has_data_context', False)}")
        else:
            print(f"❌ Analysis error: {analysis.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    print()
    
    # Test agent status
    print("📊 Testing agent status...")
    try:
        status = simple_master_agent.get_agent_status()
        print(f"✅ Agent status retrieved")
        print(f"   Total agents: {status.get('total_agents', 0)}")
        print(f"   Available agents: {', '.join(status.get('available_agents', []))}")
        
        # Show agent capabilities
        capabilities = status.get('agent_capabilities', {})
        print(f"   Agent capabilities:")
        for agent_id, caps in capabilities.items():
            print(f"     - {caps['name']}: {caps['description']}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    print("\n✅ Agent coordination testing completed!")


def test_workflow_templates():
    """Test available workflow templates."""
    
    print("📋 Testing Workflow Templates...")
    print("=" * 50)
    
    try:
        # Get available workflows
        workflows = simple_master_agent.get_available_workflows()
        
        print(f"✅ Found {len(workflows)} workflow templates:")
        print()
        
        for workflow_id, workflow in workflows.items():
            print(f"🔧 {workflow['name']}")
            print(f"   ID: {workflow_id}")
            print(f"   Description: {workflow['description']}")
            print(f"   Agents: {', '.join(workflow['agents'])}")
            print(f"   Workflow: {' → '.join(workflow['workflow'])}")
            print()
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    print("✅ Workflow templates testing completed!")


if __name__ == "__main__":
    print("🚀 Starting Master Agent Tests")
    print("=" * 60)
    
    # Test master agent
    test_master_agent()
    
    print("\n" + "=" * 60)
    
    # Test workflow selection
    test_workflow_selection()
    
    print("\n" + "=" * 60)
    
    # Test agent coordination
    test_agent_coordination()
    
    print("\n" + "=" * 60)
    
    # Test workflow templates
    test_workflow_templates()
    
    print("\n🎉 All master agent tests completed!")
    print("\n📝 The master agent is ready to coordinate multiple specialized agents for complex tasks.")

