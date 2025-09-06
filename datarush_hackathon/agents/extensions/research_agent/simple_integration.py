#!/usr/bin/env python3
"""
Simple integration for Research Agent.

This module provides a simplified interface for the Research Agent
that works without external API dependencies.
"""

import sys
import os
from typing import Dict, Any, List
import pandas as pd
from datetime import datetime

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

# Import ResearchAgent directly to avoid circular imports
try:
    from .research_agent import ResearchAgent
except ImportError:
    # Fallback if import fails
    ResearchAgent = None


class SimpleResearchIntegration:
    """
    Simple integration class for Research Agent.
    """
    
    def __init__(self):
        """Initialize the simple integration."""
        # Initialize agent only if ResearchAgent is available
        if ResearchAgent is not None:
            self.agent = ResearchAgent()
        else:
            self.agent = None
        self.knowledge_base = self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Initialize a knowledge base with aviation-related information.
        
        Returns:
            Dictionary containing knowledge base entries
        """
        return {
            "patrones_estacionales": [
                {
                    "title": "Patrones Estacionales en Aviación",
                    "content": "Los patrones estacionales en la aviación muestran picos durante los meses de verano (junio-agosto) y feriados importantes como Navidad y Año Nuevo. Los meses de invierno suelen tener menor tráfico, excepto en destinos de esquí.",
                    "source": "Conocimiento Base",
                    "relevance_score": 0.9
                }
            ],
            "impacto_feriados": [
                {
                    "title": "Impacto de Feriados en Tráfico Aéreo",
                    "content": "Los feriados tienen un impacto significativo en el tráfico aéreo, con aumentos del 20-40% durante períodos festivos. Los feriados más impactantes incluyen Navidad, Año Nuevo, Semana Santa y feriados nacionales importantes.",
                    "source": "Conocimiento Base",
                    "relevance_score": 0.95
                }
            ],
            "crecimiento_aviacion": [
                {
                    "title": "Crecimiento de la Industria Aérea",
                    "content": "La industria aérea ha mostrado un crecimiento promedio del 4-5% anual antes de la pandemia. La recuperación post-COVID-19 ha sido gradual, con patrones de crecimiento variables por región.",
                    "source": "Conocimiento Base",
                    "relevance_score": 0.85
                }
            ],
            "tecnologia_aviacion": [
                {
                    "title": "Tecnología en Aviación",
                    "content": "Las nuevas tecnologías en aviación incluyen aviones más eficientes, sistemas de navegación avanzados, y mejoras en la experiencia del pasajero. La sostenibilidad es un foco importante con el desarrollo de combustibles alternativos.",
                    "source": "Conocimiento Base",
                    "relevance_score": 0.8
                }
            ],
            "regulaciones_aereas": [
                {
                    "title": "Regulaciones Aéreas Internacionales",
                    "content": "Las regulaciones aéreas internacionales están coordinadas por la OACI (Organización de Aviación Civil Internacional) y incluyen estándares de seguridad, emisiones, y operaciones. Cada país tiene sus propias regulaciones adicionales.",
                    "source": "Conocimiento Base",
                    "relevance_score": 0.75
                }
            ]
        }
    
    def research_topic(self, topic: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Research a topic using the knowledge base and external sources.
        
        Args:
            topic: Topic to research
            context: Optional context from the DataRush system
            
        Returns:
            Dictionary containing research results
        """
        try:
            # First, try to get information from knowledge base
            knowledge_results = self._search_knowledge_base(topic)
            
            # Then, try external research if available
            external_results = self._try_external_research(topic, context)
            
            # Combine results
            combined_results = {
                'topic': topic,
                'timestamp': datetime.now().isoformat(),
                'sources': knowledge_results + external_results.get('sources', []),
                'insights': self._generate_insights_from_knowledge(topic, knowledge_results),
                'recommendations': self._generate_recommendations_from_topic(topic),
                'confidence': self._calculate_combined_confidence(knowledge_results, external_results)
            }
            
            return combined_results
            
        except Exception as e:
            return {
                "error": True,
                "message": f"Error in research: {str(e)}",
                "analysis_type": "research_error"
            }
    
    def _search_knowledge_base(self, topic: str) -> List[Dict[str, Any]]:
        """
        Search the knowledge base for relevant information.
        
        Args:
            topic: Topic to search for
            
        Returns:
            List of relevant knowledge base entries
        """
        results = []
        topic_lower = topic.lower()
        
        # Search through knowledge base categories
        for category, entries in self.knowledge_base.items():
            for entry in entries:
                # Check if topic keywords match entry content
                if self._is_relevant(topic_lower, entry['content'].lower()):
                    results.append(entry)
        
        return results
    
    def _is_relevant(self, topic: str, content: str) -> bool:
        """
        Check if content is relevant to the topic.
        
        Args:
            topic: Search topic
            content: Content to check
            
        Returns:
            True if relevant, False otherwise
        """
        # Extract keywords from topic
        topic_words = set(topic.split())
        content_words = set(content.split())
        
        # Check for common words
        common_words = topic_words.intersection(content_words)
        
        # Check for aviation-related keywords
        aviation_keywords = ['aviación', 'aéreo', 'aerolíneas', 'pasajeros', 'tráfico', 'feriado', 'estacional', 'crecimiento', 'tendencia']
        topic_has_aviation = any(keyword in topic for keyword in aviation_keywords)
        content_has_aviation = any(keyword in content for keyword in aviation_keywords)
        
        # Relevance if there are common words or both have aviation keywords
        return len(common_words) > 0 or (topic_has_aviation and content_has_aviation)
    
    def _try_external_research(self, topic: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Try to perform external research using the full ResearchAgent.
        
        Args:
            topic: Topic to research
            context: Optional context
            
        Returns:
            Dictionary with external research results
        """
        try:
            # Check if ResearchAgent is available
            if ResearchAgent is None:
                return {
                    'sources': [],
                    'insights': [],
                    'recommendations': [],
                    'confidence': 0.0
                }
            
            # Try to use the full research agent
            external_results = self.agent.research_topic(topic, context)
            return external_results
        except Exception as e:
            # If external research fails, return empty results
            return {
                'sources': [],
                'insights': [],
                'recommendations': [],
                'confidence': 0.0
            }
    
    def _generate_insights_from_knowledge(self, topic: str, knowledge_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate insights from knowledge base results.
        
        Args:
            topic: Research topic
            knowledge_results: Results from knowledge base
            
        Returns:
            List of insights
        """
        insights = []
        
        for result in knowledge_results:
            insight = {
                'type': 'knowledge_insight',
                'description': f"Basado en {result['source']}: {result['content'][:100]}...",
                'confidence': result.get('relevance_score', 0.5),
                'source': result['source']
            }
            insights.append(insight)
        
        # Add topic-specific insights
        if 'patrón' in topic.lower() or 'estacional' in topic.lower():
            insights.append({
                'type': 'pattern_insight',
                'description': 'Los patrones estacionales en aviación son consistentes y predecibles, lo que permite planificación estratégica.',
                'confidence': 0.8,
                'source': 'análisis_interno'
            })
        
        if 'feriado' in topic.lower() or 'vacaciones' in topic.lower():
            insights.append({
                'type': 'holiday_insight',
                'description': 'Los feriados crean oportunidades de negocio significativas en el sector aéreo.',
                'confidence': 0.9,
                'source': 'análisis_interno'
            })
        
        if 'crecimiento' in topic.lower() or 'tendencia' in topic.lower():
            insights.append({
                'type': 'growth_insight',
                'description': 'El crecimiento en aviación está influenciado por factores económicos, tecnológicos y sociales.',
                'confidence': 0.7,
                'source': 'análisis_interno'
            })
        
        return insights
    
    def _generate_recommendations_from_topic(self, topic: str) -> List[Dict[str, Any]]:
        """
        Generate recommendations based on the research topic.
        
        Args:
            topic: Research topic
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        if 'análisis' in topic.lower():
            recommendations.append({
                'type': 'analysis_recommendation',
                'description': 'Considere aplicar filtros específicos para un análisis más detallado de los datos.',
                'priority': 'medium'
            })
        
        if 'predicción' in topic.lower() or 'pronóstico' in topic.lower():
            recommendations.append({
                'type': 'prediction_recommendation',
                'description': 'Use datos históricos para generar proyecciones futuras más precisas.',
                'priority': 'high'
            })
        
        if 'comparación' in topic.lower():
            recommendations.append({
                'type': 'comparison_recommendation',
                'description': 'Compare diferentes países o períodos para identificar diferencias significativas.',
                'priority': 'medium'
            })
        
        if 'feriado' in topic.lower():
            recommendations.append({
                'type': 'holiday_recommendation',
                'description': 'Analice el impacto específico de cada tipo de feriado en el tráfico aéreo.',
                'priority': 'high'
            })
        
        return recommendations
    
    def _calculate_combined_confidence(self, knowledge_results: List[Dict[str, Any]], external_results: Dict[str, Any]) -> float:
        """
        Calculate combined confidence score.
        
        Args:
            knowledge_results: Results from knowledge base
            external_results: Results from external research
            
        Returns:
            Combined confidence score (0-1)
        """
        confidence = 0.0
        
        # Base confidence from knowledge results
        if knowledge_results:
            avg_knowledge_confidence = sum(result.get('relevance_score', 0.5) for result in knowledge_results) / len(knowledge_results)
            confidence += avg_knowledge_confidence * 0.6
        
        # Add external research confidence
        external_confidence = external_results.get('confidence', 0.0)
        confidence += external_confidence * 0.4
        
        return min(confidence, 1.0)
    
    def get_research_summary(self, research_results: Dict[str, Any]) -> str:
        """
        Get a formatted summary of the research results.
        
        Args:
            research_results: Results from the research
            
        Returns:
            Formatted summary string
        """
        # Handle case where research_results might be a string
        if isinstance(research_results, str):
            return research_results
        
        # Handle case where research_results is not a dict
        if not isinstance(research_results, dict):
            return f"❌ Error: Resultado de investigación en formato inesperado: {type(research_results)}"
        
        if research_results.get("error", False):
            return f"❌ Error: {research_results.get('message', 'Error desconocido')}"
        
        topic = research_results.get('topic', 'Tema desconocido')
        sources = research_results.get('sources', [])
        insights = research_results.get('insights', [])
        recommendations = research_results.get('recommendations', [])
        confidence = research_results.get('confidence', 0.0)
        
        # Create narrative summary
        summary = f"## 🔍 Investigación: {topic}\n\n"
        
        # Add sources summary
        if sources:
            summary += f"**📚 Fuentes encontradas:** {len(sources)}\n\n"
            for source in sources[:3]:  # Show first 3 sources
                summary += f"• **{source.get('source', 'Fuente desconocida')}**: {source.get('title', 'Sin título')}\n"
                if source.get('content'):
                    content_preview = source['content'][:150] + "..." if len(source['content']) > 150 else source['content']
                    summary += f"  {content_preview}\n"
                summary += "\n"
        
        # Add insights summary
        if insights:
            summary += f"**💡 Insights generados:** {len(insights)}\n\n"
            for insight in insights[:3]:  # Show first 3 insights
                summary += f"• {insight.get('description', 'Sin descripción')}\n"
                summary += f"  *Confianza: {insight.get('confidence', 0):.1%}*\n\n"
        
        # Add recommendations summary
        if recommendations:
            summary += f"**🎯 Recomendaciones:** {len(recommendations)}\n\n"
            for rec in recommendations[:3]:  # Show first 3 recommendations
                priority = rec.get('priority', 'medium')
                priority_emoji = "🔴" if priority == 'high' else "🟡" if priority == 'medium' else "🟢"
                summary += f"• {priority_emoji} {rec.get('description', 'Sin descripción')}\n"
            summary += "\n"
        
        # Add confidence
        confidence_emoji = "🟢" if confidence > 0.7 else "🟡" if confidence > 0.4 else "🔴"
        summary += f"**📊 Confianza general:** {confidence_emoji} {confidence:.1%}\n"
        
        return summary


# Create a global instance for easy access
simple_research_agent = SimpleResearchIntegration()
