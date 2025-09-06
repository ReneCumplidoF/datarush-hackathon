#!/usr/bin/env python3
"""
Simple integration for Business Advisor Agent.

This module provides a simplified interface for the Business Advisor Agent
that works without external dependencies.
"""

import sys
import os
from typing import Dict, Any
import pandas as pd

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from agents.extensions.business_advisor_agent.agent import business_advisor_agent


class SimpleBusinessAdvisorIntegration:
    """
    Simple integration class for Business Advisor Agent.
    """
    
    def __init__(self):
        """Initialize the simple integration."""
        self.agent = business_advisor_agent
    
    def analyze_business_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyze a business query and provide recommendations.
        
        Args:
            query: User query about business recommendations
            context: Optional context from the DataRush system
            
        Returns:
            Dictionary containing business analysis results
        """
        try:
            # Prepare context for the analysis
            agent_context = self._prepare_agent_context(context)
            
            # Analyze the query
            analysis_results = self.agent.analyze_business_query(query, agent_context)
            
            return analysis_results
            
        except Exception as e:
            return {
                "error": True,
                "message": f"Error in business analysis: {str(e)}",
                "analysis_type": "business_analysis_error"
            }
    
    def _prepare_agent_context(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Prepare context for the business analysis.
        
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
        
        # Use data from context if available (from DataRush system)
        if context and context.get("data_loaded", False):
            agent_context["data"] = context.get("data", {})
            agent_context["data_loaded"] = True
            agent_context["current_filters"] = context.get("current_filters", {})
            agent_context["analysis_timestamp"] = pd.Timestamp.now().isoformat()
        else:
            # Fallback: No data available
            agent_context["data_loaded"] = False
        
        # Add any additional context
        if context:
            agent_context.update(context)
        
        return agent_context
    
    def get_business_summary(self, analysis_results: Dict[str, Any]) -> str:
        """
        Get a formatted summary of the business analysis.
        
        Args:
            analysis_results: Results from the business analysis
            
        Returns:
            Formatted summary string
        """
        # Handle case where analysis_results might be a string
        if isinstance(analysis_results, str):
            return analysis_results
        
        # Handle case where analysis_results is not a dict
        if not isinstance(analysis_results, dict):
            return f"❌ Error: Resultado de análisis de negocio en formato inesperado: {type(analysis_results)}"
        
        return self.agent.get_business_summary(analysis_results)
    
    def get_available_business_sectors(self) -> Dict[str, Dict[str, str]]:
        """
        Get list of available business sectors.
        
        Returns:
            Dictionary of business sectors with their information
        """
        return self.agent.business_sectors
    
    def get_business_recommendations(self, business_sector: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Get recommendations for a specific business sector.
        
        Args:
            business_sector: Business sector to analyze
            context: Optional context from the DataRush system
            
        Returns:
            Dictionary containing recommendations
        """
        try:
            # Create a query for the specific business sector
            query = f"Necesito recomendaciones para mi negocio de {business_sector}"
            
            # Analyze the query
            analysis_results = self.analyze_business_query(query, context)
            
            return analysis_results
            
        except Exception as e:
            return {
                "error": True,
                "message": f"Error getting recommendations for {business_sector}: {str(e)}",
                "analysis_type": "business_analysis_error"
            }


# Create a global instance for easy access
simple_business_advisor = SimpleBusinessAdvisorIntegration()
