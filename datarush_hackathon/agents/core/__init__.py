"""
Core Agents Package
==================

Agentes principales del sistema DataRush que forman la funcionalidad base.

Agentes incluidos:
- DataLoader: Carga y procesamiento de datos
- Filters: Sistema de filtros avanzados
- Visualizations: Generación de visualizaciones
- ChatAgent: Chat básico con IA
"""

from .data_loader import DataLoader
from .filters import Filters
from .visualizations import Visualizations
from .chat_agent import ChatAgent

__all__ = [
    'DataLoader',
    'Filters', 
    'Visualizations',
    'ChatAgent'
]

