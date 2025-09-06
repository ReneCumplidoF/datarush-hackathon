"""
Master Agent Package

This package contains the Master Agent that coordinates and manages
all specialized agents to enable collaboration on complex tasks.
"""

from .agent import MasterAgent, master_agent

__all__ = [
    'MasterAgent',
    'master_agent'
]

