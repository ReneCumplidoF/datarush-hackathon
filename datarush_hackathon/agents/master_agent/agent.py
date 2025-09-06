#!/usr/bin/env python3
"""
Master Agent for DataRush System

This agent coordinates and manages all specialized agents to enable collaboration
on complex tasks that require multiple perspectives and capabilities.
"""

import streamlit as st
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import json
import pandas as pd

# Import specialized agents
from ..extensions.data_analysis_agent.simple_integration import simple_data_analysis_agent
from ..extensions.business_advisor_agent.simple_integration import simple_business_advisor
from ..extensions.research_agent.simple_integration import simple_research_agent
from ..core.chat_agent import ChatAgent
from .enhanced_workflows import enhanced_workflows


class MasterAgent:
    """
    Master Agent that coordinates and manages all specialized agents.
    
    This agent acts as a central coordinator that can:
    - Analyze complex queries and determine which agents to involve
    - Orchestrate multi-agent workflows
    - Combine results from multiple agents
    - Provide comprehensive responses that leverage all available capabilities
    """
    
    def __init__(self):
        """Initialize the Master Agent with all specialized agents."""
        self.agents = {
            'data_analysis': simple_data_analysis_agent,
            'business_advisor': simple_business_advisor,
            'research': simple_research_agent,
            'chat': ChatAgent()
        }
        
        self.agent_capabilities = {
            'data_analysis': {
                'name': 'Análisis de Datos',
                'description': 'Análisis específico de datos del tablero DataRush',
                'keywords': ['análisis', 'datos', 'tendencia', 'patrón', 'estadística', 'métrica', 'gráfico', 'visualización'],
                'strengths': ['análisis cuantitativo', 'visualizaciones', 'métricas específicas', 'patrones de datos']
            },
            'business_advisor': {
                'name': 'Asesor de Negocios',
                'description': 'Recomendaciones estratégicas basadas en tráfico y feriados',
                'keywords': ['negocio', 'recomendación', 'estrategia', 'turismo', 'retail', 'restaurante', 'transporte', 'servicio'],
                'strengths': ['recomendaciones estratégicas', 'análisis de mercado', 'insights de negocio', 'planificación']
            },
            'research': {
                'name': 'Investigador',
                'description': 'Búsqueda de información externa para complementar insights',
                'keywords': ['investigar', 'buscar', 'información', 'contexto', 'fuente', 'estudio', 'investigación'],
                'strengths': ['investigación externa', 'contexto amplio', 'fuentes múltiples', 'validación']
            },
            'chat': {
                'name': 'Chat General',
                'description': 'Conversación general y respuestas básicas',
                'keywords': ['pregunta', 'ayuda', 'información', 'general', 'básico'],
                'strengths': ['conversación natural', 'respuestas generales', 'orientación']
            }
        }
        
        self.workflow_templates = {
            'comprehensive_analysis': {
                'name': 'Análisis Integral',
                'description': 'Análisis completo que combina datos, investigación y recomendaciones',
                'agents': ['data_analysis', 'research', 'business_advisor'],
                'workflow': [
                    'data_analysis',  # Análisis de datos
                    'research',       # Investigación externa
                    'business_advisor' # Recomendaciones de negocio
                ]
            },
            'business_strategy': {
                'name': 'Estrategia de Negocio',
                'description': 'Desarrollo de estrategia de negocio con análisis de datos',
                'agents': ['business_advisor', 'data_analysis'],
                'workflow': [
                    'data_analysis',    # Análisis de datos de soporte
                    'business_advisor'  # Recomendaciones estratégicas
                ]
            },
            'research_validation': {
                'name': 'Validación de Investigación',
                'description': 'Validar hallazgos con investigación externa',
                'agents': ['data_analysis', 'research'],
                'workflow': [
                    'data_analysis',  # Análisis inicial
                    'research'        # Validación externa
                ]
            },
            'quick_analysis': {
                'name': 'Análisis Rápido',
                'description': 'Análisis rápido de datos sin investigación externa',
                'agents': ['data_analysis'],
                'workflow': [
                    'data_analysis'  # Solo análisis de datos
                ]
            }
        }
    
    def process_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process a query using the most appropriate agents and workflow.
        
        Args:
            query: User query
            context: Optional context from DataRush system
            
        Returns:
            Dictionary containing comprehensive results from multiple agents
        """
        try:
            print(f"🔍 Debug - Master Agent process_query started")
            print(f"🔍 Debug - Query: {query[:50]}...")
            print(f"🔍 Debug - Context type: {type(context)}")
            print(f"🔍 Debug - Context keys: {list(context.keys()) if isinstance(context, dict) else 'Not a dict'}")
            
            # Step 1: Analyze query to determine best approach
            print("🔍 Debug - Step 1: Analyzing query...")
            analysis_result = self._analyze_query(query, context)
            print(f"🔍 Debug - Analysis result type: {type(analysis_result)}")
            print(f"🔍 Debug - Analysis result keys: {list(analysis_result.keys()) if isinstance(analysis_result, dict) else 'Not a dict'}")
            
            # Step 2: Select appropriate workflow
            print("🔍 Debug - Step 2: Selecting workflow...")
            workflow = self._select_workflow(analysis_result)
            print(f"🔍 Debug - Workflow type: {type(workflow)}")
            print(f"🔍 Debug - Workflow keys: {list(workflow.keys()) if isinstance(workflow, dict) else 'Not a dict'}")
            
            # Step 3: Execute workflow with selected agents
            print("🔍 Debug - Step 3: Executing workflow...")
            results = self._execute_workflow(workflow, query, context)
            print(f"🔍 Debug - Workflow results type: {type(results)}")
            print(f"🔍 Debug - Workflow results keys: {list(results.keys()) if isinstance(results, dict) else 'Not a dict'}")
            
            # Step 4: Synthesize results from all agents
            print("🔍 Debug - Step 4: Synthesizing results...")
            synthesis = self._synthesize_results(results, query, context)
            print(f"🔍 Debug - Synthesis type: {type(synthesis)}")
            print(f"🔍 Debug - Synthesis length: {len(synthesis) if isinstance(synthesis, str) else 'Not a string'}")
            
            final_result = {
                'success': True,
                'query': query,
                'workflow_used': workflow['name'],
                'agents_involved': workflow['agents'],
                'individual_results': results,
                'synthesis': synthesis,
                'timestamp': datetime.now().isoformat()
            }
            print(f"🔍 Debug - Final result type: {type(final_result)}")
            print(f"🔍 Debug - Final result keys: {list(final_result.keys())}")
            
            return final_result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'query': query,
                'timestamp': datetime.now().isoformat()
            }
    
    def _analyze_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyze the query to determine complexity and required capabilities.
        
        Args:
            query: User query
            context: Optional context
            
        Returns:
            Analysis result with complexity and required capabilities
        """
        query_lower = query.lower()
        
        # Determine complexity level
        complexity_indicators = {
            'high': ['completo', 'integral', 'estratégico', 'análisis profundo', 'investigación', 'recomendación'],
            'medium': ['análisis', 'comparar', 'evaluar', 'estudiar', 'examinar'],
            'low': ['pregunta', 'información', 'ayuda', 'básico']
        }
        
        complexity = 'low'
        for level, indicators in complexity_indicators.items():
            if any(indicator in query_lower for indicator in indicators):
                complexity = level
                break
        
        # Identify required capabilities
        required_capabilities = []
        for agent_id, capabilities in self.agent_capabilities.items():
            if any(keyword in query_lower for keyword in capabilities['keywords']):
                required_capabilities.append(agent_id)
        
        # If no specific capabilities identified, use chat
        if not required_capabilities:
            required_capabilities = ['chat']
        
        # Determine if data context is available
        has_data_context = context and context.get('data_loaded', False)
        
        return {
            'complexity': complexity,
            'required_capabilities': required_capabilities,
            'has_data_context': has_data_context,
            'query_type': self._classify_query_type(query_lower)
        }
    
    def _classify_query_type(self, query_lower: str) -> str:
        """Classify the type of query."""
        if any(word in query_lower for word in ['negocio', 'recomendación', 'estrategia', 'turismo', 'retail']):
            return 'business'
        elif any(word in query_lower for word in ['análisis', 'datos', 'tendencia', 'patrón', 'métrica']):
            return 'analysis'
        elif any(word in query_lower for word in ['investigar', 'buscar', 'información', 'contexto']):
            return 'research'
        elif any(word in query_lower for word in ['completo', 'integral', 'todo', 'todos']):
            return 'comprehensive'
        else:
            return 'general'
    
    def _select_workflow(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Select the most appropriate workflow based on analysis.
        
        Args:
            analysis_result: Result from query analysis
            
        Returns:
            Selected workflow configuration
        """
        # Use enhanced workflows for better analysis
        query = analysis_result.get('query', '')
        return enhanced_workflows.get_workflow_for_query(query, analysis_result)
    
    def _execute_workflow(self, workflow: Dict[str, Any], query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the selected workflow with the specified agents.
        
        Args:
            workflow: Workflow configuration
            query: User query
            context: Optional context
            
        Returns:
            Results from all agents in the workflow
        """
        print(f"🔍 Debug - _execute_workflow called")
        print(f"🔍 Debug - Workflow type: {type(workflow)}")
        print(f"🔍 Debug - Workflow keys: {list(workflow.keys()) if isinstance(workflow, dict) else 'Not a dict'}")
        print(f"🔍 Debug - Query: {query[:50]}...")
        print(f"🔍 Debug - Context type: {type(context)}")
        print(f"🔍 Debug - Self.agents type: {type(self.agents)}")
        print(f"🔍 Debug - Self.agents keys: {list(self.agents.keys()) if isinstance(self.agents, dict) else 'Not a dict'}")
        
        try:
            # Use enhanced workflow execution for better integration
            print("🔍 Debug - Calling enhanced_workflows.execute_enhanced_workflow...")
            result = enhanced_workflows.execute_enhanced_workflow(workflow, query, context, self.agents)
            print(f"🔍 Debug - Enhanced workflow returned type: {type(result)}")
            print(f"🔍 Debug - Enhanced workflow returned keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
            return result
        except Exception as e:
            print(f"🔍 Debug - Error in enhanced workflow execution: {str(e)}")
            print(f"🔍 Debug - Error type: {type(e)}")
            import traceback
            print(f"🔍 Debug - Traceback: {traceback.format_exc()}")
            raise e
    
    def _synthesize_results(self, results: Dict[str, Any], query: str, context: Dict[str, Any]) -> str:
        """
        Synthesize results from multiple agents into a comprehensive response.
        
        Args:
            results: Results from all agents
            query: Original query
            context: Optional context
            
        Returns:
            Synthesized comprehensive response
        """
        # Check if this is an enhanced workflow result
        if 'synthesis' in results and 'stages' in results:
            # Use enhanced synthesis
            return results['synthesis']
        
        # Fallback to basic synthesis for backward compatibility
        synthesis_parts = []
        
        # Header
        synthesis_parts.append("## 🎯 Análisis Integral - Respuesta del Agente Maestro")
        synthesis_parts.append("")
        synthesis_parts.append(f"**Consulta:** {query}")
        synthesis_parts.append("")
        
        # Successful agents
        successful_agents = [agent_id for agent_id, result in results.items() if isinstance(result, dict) and result.get('success', False)]
        failed_agents = [agent_id for agent_id, result in results.items() if not (isinstance(result, dict) and result.get('success', False))]
        
        if successful_agents:
            synthesis_parts.append(f"**Agentes involucrados:** {', '.join([self.agent_capabilities[aid]['name'] for aid in successful_agents])}")
            synthesis_parts.append("")
        
        # Individual agent results
        for agent_id, result in results.items():
            if isinstance(result, dict) and result.get('success', False):
                agent_name = self.agent_capabilities[agent_id]['name']
                synthesis_parts.append(f"### 🤖 {agent_name}")
                synthesis_parts.append("")
                synthesis_parts.append(result.get('summary', 'No hay resumen disponible'))
                synthesis_parts.append("")
        
        # Failed agents (if any)
        if failed_agents:
            synthesis_parts.append("### ⚠️ Agentes con Problemas")
            synthesis_parts.append("")
            for agent_id in failed_agents:
                agent_name = self.agent_capabilities[agent_id]['name']
                result = results[agent_id]
                if isinstance(result, dict):
                    error = result.get('error', 'Error desconocido')
                else:
                    error = f"Resultado inesperado: {type(result)}"
                synthesis_parts.append(f"• **{agent_name}**: {error}")
            synthesis_parts.append("")
        
        # Synthesis summary
        synthesis_parts.append("### 🔗 Síntesis Integral")
        synthesis_parts.append("")
        synthesis_parts.append("El Agente Maestro ha coordinado múltiples agentes especializados para proporcionar una respuesta integral que combina:")
        synthesis_parts.append("")
        
        if 'data_analysis' in successful_agents:
            synthesis_parts.append("• **Análisis de datos** específicos del tablero DataRush")
        if 'research' in successful_agents:
            synthesis_parts.append("• **Investigación externa** para contexto adicional")
        if 'business_advisor' in successful_agents:
            synthesis_parts.append("• **Recomendaciones estratégicas** basadas en datos y contexto")
        if 'chat' in successful_agents:
            synthesis_parts.append("• **Orientación general** y respuestas contextuales")
        
        synthesis_parts.append("")
        synthesis_parts.append("Esta respuesta integral proporciona una perspectiva completa que combina datos internos, investigación externa y recomendaciones estratégicas.")
        
        return "\n".join(synthesis_parts)
    
    def get_agent_status(self) -> Dict[str, Any]:
        """
        Get status of all agents.
        
        Returns:
            Dictionary with status of all agents
        """
        status = {
            'total_agents': len(self.agents),
            'available_agents': list(self.agents.keys()),
            'agent_capabilities': self.agent_capabilities,
            'workflow_templates': self.workflow_templates,
            'timestamp': datetime.now().isoformat()
        }
        
        return status
    
    def get_workflow_suggestions(self, query: str) -> List[Dict[str, Any]]:
        """
        Get suggested workflows for a query.
        
        Args:
            query: User query
            
        Returns:
            List of suggested workflows
        """
        analysis = self._analyze_query(query)
        suggestions = []
        
        for workflow_id, workflow in self.workflow_templates.items():
            # Check if workflow is appropriate for this query
            if self._is_workflow_appropriate(workflow, analysis):
                suggestions.append({
                    'id': workflow_id,
                    'name': workflow['name'],
                    'description': workflow['description'],
                    'agents': [self.agent_capabilities[aid]['name'] for aid in workflow['agents']],
                    'confidence': self._calculate_workflow_confidence(workflow, analysis)
                })
        
        # Sort by confidence
        suggestions.sort(key=lambda x: x['confidence'], reverse=True)
        
        return suggestions
    
    def _is_workflow_appropriate(self, workflow: Dict[str, Any], analysis: Dict[str, Any]) -> bool:
        """Check if a workflow is appropriate for the analysis."""
        required_capabilities = analysis['required_capabilities']
        workflow_agents = workflow['agents']
        
        # Check if workflow agents match required capabilities
        return any(agent in workflow_agents for agent in required_capabilities)
    
    def _calculate_workflow_confidence(self, workflow: Dict[str, Any], analysis: Dict[str, Any]) -> float:
        """Calculate confidence score for a workflow."""
        required_capabilities = analysis['required_capabilities']
        workflow_agents = workflow['agents']
        
        # Calculate overlap
        overlap = len(set(required_capabilities) & set(workflow_agents))
        total_required = len(required_capabilities)
        
        if total_required == 0:
            return 0.5  # Default confidence
        
        return overlap / total_required


# Create a global instance for easy access
master_agent = MasterAgent()
