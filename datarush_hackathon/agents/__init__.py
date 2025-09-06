"""
DataRush Agents Package
======================

Este paquete contiene todos los agentes del sistema DataRush organizados por categorías:

- core: Agentes principales del sistema
- extensions: Agentes de extensión y funcionalidades avanzadas
- integrations: Agentes de integración con servicios externos
- tools: Herramientas y utilidades para los agentes

Estructura:
----------
agents/
├── __init__.py
├── core/                    # Agentes principales
│   ├── __init__.py
│   ├── data_loader.py       # DataLoader Agent
│   ├── filters.py           # Filters Agent
│   ├── visualizations.py    # Visualizations Agent
│   └── chat_agent.py        # Chat Agent
├── extensions/              # Agentes de extensión
│   ├── __init__.py
│   ├── smart_chat_agent.py  # Smart Chat Agent
│   ├── advanced_filters.py  # Advanced Filters
│   ├── advanced_visualizations.py  # Advanced Visualizations
│   ├── data_enricher.py     # Data Enricher
│   └── export_manager.py    # Export Manager
├── integrations/            # Agentes de integración
│   ├── __init__.py
│   └── bigquery_integration.py  # BigQuery Integration
└── tools/                   # Herramientas y utilidades
    ├── __init__.py
    ├── validators.py        # Validadores de datos
    ├── formatters.py        # Formateadores
    └── metrics.py           # Calculadoras de métricas
"""

from .core import *
from .extensions import *
# from .integrations import *  # Disabled - BigQuery integration removed
from .tools import *

__version__ = "1.0.0"
__author__ = "DataRush Team"
__description__ = "Sistema de agentes multiagente para análisis de patrones de feriados"
