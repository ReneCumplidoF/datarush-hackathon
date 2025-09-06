"""
Integrations Agents Package
==========================

Agentes de integración con servicios externos y APIs.

Agentes incluidos:
- SimpleBigQueryIntegration: Integración simplificada para validación de datos (sin BigQuery)
"""

# from .bigquery_integration import BigQueryIntegration  # Disabled - BigQuery removed

# Import simple integration from components
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from components.simple_bigquery_integration import simple_bigquery_integration as SimpleBigQueryIntegration

__all__ = [
    'SimpleBigQueryIntegration'
]
