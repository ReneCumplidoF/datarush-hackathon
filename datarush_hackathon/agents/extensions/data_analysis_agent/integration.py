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

"""Integration module for the Data Analysis Agent with DataRush system.

This module provides integration functions to connect the data analysis agent
with the existing DataRush system components.
"""

import os
import sys
from typing import Dict, Any, Optional, List
import streamlit as st

# Add the parent directory to the path for importing components
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

# from .agent import data_analysis_agent

# Import with fallback
try:
    from .agent import data_analysis_agent
except ImportError as e:
    print(f"Warning: Could not import data_analysis_agent: {e}")
    # Create a mock agent
    class MockAgent:
        def run(self, query, context=None):
            return f"Mock analysis for: {query}"
    data_analysis_agent = MockAgent()
from components.data_loader import DataLoader
from components.filters import Filters
from components.visualizations import Visualizations


class DataAnalysisAgentIntegration:
    """
    Integration class for the Data Analysis Agent with DataRush system.
    """
    
    def __init__(self):
        self.agent = data_analysis_agent
        self.data_loader = DataLoader()
        self.filters = Filters()
        self.visualizations = Visualizations()
        self.analysis_cache = {}
    
    def analyze_user_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyze a user query using the data analysis agent.
        
        Args:
            query: User query to analyze
            context: Optional context from the DataRush system
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            # Prepare context for the agent
            agent_context = self._prepare_agent_context(context)
            
            # Use the agent to analyze the query
            response = self.agent.run(query, context=agent_context)
            
            # Process the response
            analysis_results = self._process_agent_response(response)
            
            return analysis_results
            
        except Exception as e:
            st.error(f"❌ Error in data analysis: {str(e)}")
            return {
                "error": True,
                "message": f"Error in data analysis: {str(e)}",
                "analysis_type": "error"
            }
    
    def _prepare_agent_context(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Prepare context for the data analysis agent.
        
        Args:
            context: Context from the DataRush system
            
        Returns:
            Dictionary containing prepared context
        """
        agent_context = {
            "data_loaded": False,
            "data": {},
            "current_filters": {},
            "analysis_timestamp": None
        }
        
        # Load data if available
        try:
            if self.data_loader.load_data() and self.data_loader.clean_data():
                agent_context["data"] = self.data_loader.get_processed_data()
                agent_context["data_loaded"] = True
        except Exception as e:
            st.warning(f"⚠️ Error loading data: {str(e)}")
        
        # Apply current filters if available
        if context and "filters" in context:
            agent_context["current_filters"] = context["filters"]
        
        # Add any additional context
        if context:
            agent_context.update(context)
        
        return agent_context
    
    def _process_agent_response(self, response: Any) -> Dict[str, Any]:
        """
        Process the response from the data analysis agent.
        
        Args:
            response: Response from the agent
            
        Returns:
            Dictionary containing processed analysis results
        """
        try:
            # Extract analysis results from the response
            if hasattr(response, 'content'):
                content = response.content
            elif isinstance(response, str):
                content = response
            else:
                content = str(response)
            
            # Parse the response to extract structured data
            analysis_results = {
                "content": content,
                "analysis_type": "general",
                "insights": [],
                "visualization": None,
                "metrics": {},
                "success": True
            }
            
            # Try to extract structured information from the response
            if "trend" in content.lower():
                analysis_results["analysis_type"] = "trend_analysis"
            elif "holiday" in content.lower() or "feriado" in content.lower():
                analysis_results["analysis_type"] = "holiday_impact_analysis"
            elif "country" in content.lower() or "país" in content.lower():
                analysis_results["analysis_type"] = "geographic_analysis"
            elif "seasonal" in content.lower() or "estacional" in content.lower():
                analysis_results["analysis_type"] = "seasonal_analysis"
            elif "statistical" in content.lower() or "estadístico" in content.lower():
                analysis_results["analysis_type"] = "statistical_analysis"
            elif "comparison" in content.lower() or "comparación" in content.lower():
                analysis_results["analysis_type"] = "comparison_analysis"
            
            return analysis_results
            
        except Exception as e:
            return {
                "error": True,
                "message": f"Error processing agent response: {str(e)}",
                "analysis_type": "error"
            }
    
    def get_available_analyses(self) -> List[Dict[str, str]]:
        """
        Get list of available analysis types.
        
        Returns:
            List of dictionaries containing analysis information
        """
        return [
            {
                "type": "trend_analysis",
                "name": "Análisis de Tendencias",
                "description": "Analiza patrones temporales y tasas de crecimiento en los datos de pasajeros"
            },
            {
                "type": "holiday_impact_analysis",
                "name": "Análisis de Impacto de Feriados",
                "description": "Estudia la correlación entre feriados y tráfico de pasajeros"
            },
            {
                "type": "geographic_analysis",
                "name": "Análisis Geográfico",
                "description": "Analiza la distribución de datos entre diferentes países"
            },
            {
                "type": "seasonal_analysis",
                "name": "Análisis Estacional",
                "description": "Identifica patrones estacionales en los datos"
            },
            {
                "type": "statistical_analysis",
                "name": "Análisis Estadístico",
                "description": "Realiza estadísticas descriptivas y correlaciones"
            },
            {
                "type": "comparison_analysis",
                "name": "Análisis de Comparación",
                "description": "Compara datos entre países, meses o períodos"
            }
        ]
    
    def get_analysis_summary(self, analysis_results: Dict[str, Any]) -> str:
        """
        Get a summary of the analysis results.
        
        Args:
            analysis_results: Results from the analysis
            
        Returns:
            String containing the summary
        """
        if analysis_results.get("error", False):
            return f"❌ Error: {analysis_results.get('message', 'Unknown error')}"
        
        summary = f"## 📊 Análisis: {analysis_results.get('analysis_type', 'General')}\n\n"
        
        # Add content
        if analysis_results.get("content"):
            summary += f"**Resultados:**\n{analysis_results['content']}\n\n"
        
        # Add insights
        insights = analysis_results.get("insights", [])
        if insights:
            summary += "**💡 Insights:**\n"
            for insight in insights:
                summary += f"- {insight}\n"
            summary += "\n"
        
        # Add metrics
        metrics = analysis_results.get("metrics", {})
        if metrics:
            summary += "**📈 Métricas:**\n"
            for key, value in metrics.items():
                summary += f"- {key}: {value}\n"
        
        return summary


# Create a global instance for easy access
data_analysis_integration = DataAnalysisAgentIntegration()
