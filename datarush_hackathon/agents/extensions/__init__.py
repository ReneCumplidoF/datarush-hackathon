"""
Extensions Agents Package
========================

Agentes de extensión que proporcionan funcionalidades avanzadas y especializadas.

Agentes incluidos:
- SmartChatAgent: Chat inteligente con herramientas especializadas
- ResearchAgent: Agente de investigación con capacidades de búsqueda externa
- DataAnalysisAgent: Agente especializado en análisis de datos del tablero
"""

from .smart_chat_agent import SmartChatAgent
from .data_analysis_agent import data_analysis_agent
from .business_advisor_agent.simple_integration import simple_business_advisor

# Import ResearchAgent with fallback to avoid circular imports
try:
    from .research_agent import ResearchAgent
    __all__ = [
        'SmartChatAgent',
        'ResearchAgent',
        'data_analysis_agent',
        'simple_business_advisor'
    ]
except ImportError:
    __all__ = [
        'SmartChatAgent',
        'data_analysis_agent',
        'simple_business_advisor'
    ]
