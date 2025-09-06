#!/usr/bin/env python3
"""
Test script for Research Agent.

This script tests the research agent's ability to search for external information
and complement insights with web research.
"""

import os
import sys
import pandas as pd
from datetime import datetime

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.extensions.research_agent import ResearchAgent


def test_research_agent():
    """Test the research agent functionality."""
    
    print("🔍 Testing Research Agent...")
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
    
    # Test queries for different research topics
    test_queries = [
        "patrones de tráfico aéreo en Europa",
        "impacto de feriados en el turismo",
        "tendencias de crecimiento en aviación",
        "análisis estacional del tráfico aéreo",
        "comparación de países en tráfico aéreo",
        "predicción de tráfico aéreo futuro",
        "efectos de la pandemia en la aviación",
        "nuevas tecnologías en aerolíneas",
        "sostenibilidad en la aviación",
        "regulaciones aéreas internacionales"
    ]
    
    print(f"📊 Testing with {len(test_queries)} research queries...")
    print()
    
    # Initialize research agent
    research_agent = ResearchAgent()
    
    # Test each query
    for i, query in enumerate(test_queries, 1):
        print(f"🔍 Test {i}: {query}")
        print("-" * 40)
        
        try:
            # Research the topic
            results = research_agent.research_topic(query, mock_context)
            
            if results.get('sources') or results.get('insights'):
                print(f"✅ Research successful")
                print(f"📊 Sources found: {len(results.get('sources', []))}")
                print(f"💡 Insights generated: {len(results.get('insights', []))}")
                print(f"🎯 Recommendations: {len(results.get('recommendations', []))}")
                print(f"📈 Confidence: {results.get('confidence', 0):.1%}")
                
                # Show research summary
                summary = research_agent.get_research_summary(results)
                print(f"\n📝 **Research Summary:**")
                lines = summary.split('\n')
                for line in lines[:10]:  # Show first 10 lines
                    print(line)
                if len(lines) > 10:
                    print("...")
                
            else:
                print(f"⚠️ No sources or insights found")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        print("\n" + "=" * 60 + "\n")
    
    print("✅ Research agent testing completed!")


def test_research_sources():
    """Test different research sources."""
    
    print("🔍 Testing Research Sources...")
    print("=" * 50)
    
    research_agent = ResearchAgent()
    
    # Test Wikipedia search
    print("📚 Testing Wikipedia search...")
    try:
        wikipedia_result = research_agent._search_wikipedia("aviación")
        if wikipedia_result:
            print(f"✅ Wikipedia: {wikipedia_result.get('title', 'No title')}")
            print(f"   Relevance: {wikipedia_result.get('relevance_score', 0):.2f}")
        else:
            print("⚠️ No Wikipedia results")
    except Exception as e:
        print(f"❌ Wikipedia error: {str(e)}")
    
    print()
    
    # Test web search (if API key available)
    print("🌐 Testing web search...")
    try:
        web_results = research_agent._search_web("tráfico aéreo", {})
        if web_results:
            print(f"✅ Web search: {len(web_results)} results")
            for result in web_results[:2]:  # Show first 2 results
                print(f"   - {result.get('title', 'No title')}")
        else:
            print("⚠️ No web results (API key may not be configured)")
    except Exception as e:
        print(f"❌ Web search error: {str(e)}")
    
    print()
    
    # Test news search (if API key available)
    print("📰 Testing news search...")
    try:
        news_results = research_agent._search_news("aviación")
        if news_results:
            print(f"✅ News search: {len(news_results)} results")
            for result in news_results[:2]:  # Show first 2 results
                print(f"   - {result.get('title', 'No title')}")
        else:
            print("⚠️ No news results (API key may not be configured)")
    except Exception as e:
        print(f"❌ News search error: {str(e)}")
    
    print("\n✅ Research sources testing completed!")


def test_research_insights():
    """Test research insights generation."""
    
    print("💡 Testing Research Insights...")
    print("=" * 50)
    
    research_agent = ResearchAgent()
    
    # Test insight generation
    test_topics = [
        "patrones estacionales en aviación",
        "crecimiento del tráfico aéreo",
        "impacto de feriados en viajes",
        "tendencias de la industria aérea",
        "análisis comparativo de países"
    ]
    
    mock_sources = [
        {
            'source': 'Wikipedia',
            'title': 'Aviación comercial',
            'extract': 'La aviación comercial ha experimentado un crecimiento constante en las últimas décadas, con patrones estacionales marcados y un impacto significativo de feriados en el tráfico de pasajeros.',
            'relevance_score': 0.8
        },
        {
            'source': 'Google Search',
            'title': 'Tendencias en tráfico aéreo 2024',
            'snippet': 'El tráfico aéreo mundial muestra una recuperación post-pandemia con patrones estacionales claros y un aumento en viajes durante feriados.',
            'relevance_score': 0.9
        }
    ]
    
    for i, topic in enumerate(test_topics, 1):
        print(f"🔍 Test {i}: {topic}")
        print("-" * 40)
        
        try:
            # Generate insights
            insights = research_agent._generate_insights(topic, mock_sources)
            
            if insights:
                print(f"✅ Generated {len(insights)} insights:")
                for insight in insights:
                    print(f"   - {insight.get('description', 'No description')}")
                    print(f"     Type: {insight.get('type', 'Unknown')}")
                    print(f"     Confidence: {insight.get('confidence', 0):.1%}")
            else:
                print("⚠️ No insights generated")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
        
        print()
    
    print("✅ Research insights testing completed!")


if __name__ == "__main__":
    print("🚀 Starting Research Agent Tests")
    print("=" * 60)
    
    # Test research agent
    test_research_agent()
    
    print("\n" + "=" * 60)
    
    # Test research sources
    test_research_sources()
    
    print("\n" + "=" * 60)
    
    # Test research insights
    test_research_insights()
    
    print("\n🎉 All research agent tests completed!")
    print("\n📝 The research agent is ready to complement insights with external information.")
    print("\n⚠️ Note: Some features may require API keys for Google Search, News API, etc.")

