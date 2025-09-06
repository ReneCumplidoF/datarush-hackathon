"""
Research Agent Package

This package contains the Research Agent specialized in searching for external
information to complement insights with web research.
"""

# Import only the simple integration to avoid circular imports
try:
    from .simple_integration import SimpleResearchIntegration, simple_research_agent
    __all__ = [
        'SimpleResearchIntegration',
        'simple_research_agent'
    ]
except ImportError:
    # Fallback if there are import issues
    __all__ = []
