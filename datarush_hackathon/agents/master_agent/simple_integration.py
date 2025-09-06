#!/usr/bin/env python3
"""
Simple integration for Master Agent.

This module provides a simplified interface for the Master Agent
that coordinates all specialized agents.
"""

import sys
import os
from typing import Dict, Any, List

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from agents.master_agent.agent import master_agent


class SimpleMasterAgentIntegration:
    """
    Simple integration class for Master Agent.
    """
    
    def __init__(self):
        """Initialize the simple integration."""
        try:
            self.agent = master_agent
            if self.agent is None:
                print("Warning: master_agent is None")
        except Exception as e:
            print(f"Error initializing master agent: {e}")
            self.agent = None
    
    def process_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process a query using the Master Agent.
        
        Args:
            query: User query
            context: Optional context from the DataRush system
            
        Returns:
            Dictionary containing comprehensive results
        """
        try:
            # Debug: Print agent status
            print(f"🔍 Debug - Master Agent Status: {self.agent is not None}")
            print(f"🔍 Debug - Agent Type: {type(self.agent)}")
            print(f"🔍 Debug - Query: {query[:50]}...")
            print(f"🔍 Debug - Context keys: {list(context.keys()) if isinstance(context, dict) else 'Not a dict'}")
            
            # Check if agent is available
            if self.agent is None:
                print("🔍 Debug - Master agent is None, returning error")
                return {
                    "success": False,
                    "error": "Master agent is not available",
                    "query": query,
                    "timestamp": None
                }
            
            # Process query with master agent
            print("🔍 Debug - Calling master agent process_query...")
            results = self.agent.process_query(query, context)
            print(f"🔍 Debug - Master agent returned type: {type(results)}")
            print(f"🔍 Debug - Master agent returned keys: {list(results.keys()) if isinstance(results, dict) else 'Not a dict'}")
            
            return results
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error in master agent processing: {str(e)}",
                "query": query,
                "timestamp": None
            }
    
    def get_comprehensive_summary(self, results: Dict[str, Any]) -> str:
        """
        Get a comprehensive summary of the master agent results.
        
        Args:
            results: Results from the master agent
            
        Returns:
            Formatted summary string
        """
        # Handle case where results might be a string
        if isinstance(results, str):
            return results
        
        # Handle case where results is a dict
        if isinstance(results, dict):
            if not results.get('success', False):
                return f"❌ Error: {results.get('error', 'Error desconocido')}"
            
            # Return the synthesis directly as it's already formatted
            return results.get('synthesis', 'No hay síntesis disponible')
        
        # Fallback for other types
        return str(results)
    
    def get_agent_status(self) -> Dict[str, Any]:
        """
        Get status of all agents.
        
        Returns:
            Dictionary with status of all agents
        """
        return self.agent.get_agent_status()
    
    def get_workflow_suggestions(self, query: str) -> List[Dict[str, Any]]:
        """
        Get suggested workflows for a query.
        
        Args:
            query: User query
            
        Returns:
            List of suggested workflows
        """
        return self.agent.get_workflow_suggestions(query)
    
    def analyze_query_complexity(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyze query complexity and requirements.
        
        Args:
            query: User query
            context: Optional context
            
        Returns:
            Analysis result
        """
        try:
            analysis = self.agent._analyze_query(query, context)
            return {
                'success': True,
                'analysis': analysis,
                'query': query
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Error analyzing query: {str(e)}",
                'query': query
            }
    
    def get_available_workflows(self) -> Dict[str, Any]:
        """
        Get all available workflow templates.
        
        Returns:
            Dictionary with all workflow templates
        """
        return self.agent.workflow_templates
    
    def get_agent_capabilities(self) -> Dict[str, Any]:
        """
        Get capabilities of all agents.
        
        Returns:
            Dictionary with agent capabilities
        """
        return self.agent.agent_capabilities


# Create a global instance for easy access
simple_master_agent = SimpleMasterAgentIntegration()
