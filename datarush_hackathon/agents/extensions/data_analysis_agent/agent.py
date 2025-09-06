# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Data Analysis Agent for DataRush Hackathon.

This agent specializes in analyzing data from the DataRush dashboard and
local databases to generate insights and answer user questions.
"""

import os
import sys
from datetime import date
from typing import Dict, Any

# Add the parent directory to the path for importing components
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

# from google.adk.agents import Agent
# from google.adk.agents.callback_context import CallbackContext
# from google.adk.tools import load_artifacts

# Fallback imports for when google.adk is not available
try:
    from google.adk.agents import Agent
    from google.adk.agents.callback_context import CallbackContext
    from google.adk.tools import load_artifacts
    ADK_AVAILABLE = True
except ImportError:
    ADK_AVAILABLE = False
    # Create mock classes for when ADK is not available
    class Agent:
        def __init__(self, *args, **kwargs):
            self.model = kwargs.get('model', 'gemini-2.0-flash-exp')
            self.name = kwargs.get('name', 'data_analysis_agent')
            self.instruction = kwargs.get('instruction', '')
            self.global_instruction = kwargs.get('global_instruction', '')
            self.tools = kwargs.get('tools', [])
            self.before_agent_callback = kwargs.get('before_agent_callback', None)
        
        def run(self, query, context=None):
            return f"Análisis de datos para: {query}\n\nContexto: {context}"
    
    class CallbackContext:
        def __init__(self):
            self.state = {}
    
    def load_artifacts():
        return []

from .prompts import return_instructions_root, return_global_instruction
from .tools import (
    analyze_trends_tool,
    analyze_holiday_impact_tool,
    analyze_geographic_distribution_tool,
    analyze_seasonal_patterns_tool,
    perform_statistical_analysis_tool,
    compare_countries_tool
)

# Import DataRush components
from components.data_loader import DataLoader
from components.filters import Filters
from components.visualizations import Visualizations

date_today = date.today()


def setup_before_agent_call(callback_context: CallbackContext):
    """Setup the data analysis agent with DataRush context."""
    
    # Initialize DataRush components if not already done
    if "data_loader" not in callback_context.state:
        callback_context.state["data_loader"] = DataLoader()
    
    if "filters" not in callback_context.state:
        callback_context.state["filters"] = Filters()
    
    if "visualizations" not in callback_context.state:
        callback_context.state["visualizations"] = Visualizations()
    
    # Load data if available
    if "data_loaded" not in callback_context.state:
        try:
            data_loader = callback_context.state["data_loader"]
            if data_loader.load_data() and data_loader.clean_data():
                callback_context.state["data"] = data_loader.get_processed_data()
                callback_context.state["data_loaded"] = True
            else:
                callback_context.state["data"] = {}
                callback_context.state["data_loaded"] = False
        except Exception as e:
            callback_context.state["data"] = {}
            callback_context.state["data_loaded"] = False
            callback_context.state["data_error"] = str(e)
    
    # Set up current filters
    if "current_filters" not in callback_context.state:
        callback_context.state["current_filters"] = {}
    
    # Update agent instruction with current context (only if ADK is available)
    if ADK_AVAILABLE and hasattr(callback_context, '_invocation_context'):
        if callback_context.state.get("data_loaded", False):
            data = callback_context.state.get("data", {})
            data_summary = _create_data_summary(data)
            
            callback_context._invocation_context.agent.instruction = (
                return_instructions_root() + f"""

## Current Data Context:
{data_summary}

## Available Data:
- Passenger Data: {'Available' if data.get('passengers') is not None else 'Not Available'}
- Holiday Data: {'Available' if data.get('holidays') is not None else 'Not Available'}
- Country Data: {'Available' if data.get('countries') is not None else 'Not Available'}

## Current Filters Applied:
{callback_context.state.get('current_filters', {})}

"""
            )
        else:
            callback_context._invocation_context.agent.instruction = (
                return_instructions_root() + """

## Current Data Context:
No data is currently loaded. Please use the data loading tools to access data first.

"""
            )


def _create_data_summary(data: Dict[str, Any]) -> str:
    """Create a summary of the current data context."""
    summary = []
    
    if data.get('passengers') is not None:
        passengers_df = data['passengers']
        summary.append(f"- Passenger Data: {len(passengers_df)} records")
        summary.append(f"  - Countries: {passengers_df['ISO3'].nunique()}")
        summary.append(f"  - Years: {passengers_df['Year'].min()}-{passengers_df['Year'].max()}")
        summary.append(f"  - Total Passengers: {passengers_df['Total'].sum():,.0f}")
    
    if data.get('holidays') is not None:
        holidays_df = data['holidays']
        summary.append(f"- Holiday Data: {len(holidays_df)} records")
        summary.append(f"  - Countries: {holidays_df['ISO3'].nunique()}")
        summary.append(f"  - Holiday Types: {holidays_df['Type'].nunique()}")
    
    if data.get('countries') is not None:
        countries_df = data['countries']
        summary.append(f"- Country Data: {len(countries_df)} records")
    
    return "\n".join(summary) if summary else "No data available"


# Create the data analysis agent
if ADK_AVAILABLE:
    data_analysis_agent = Agent(
        model=os.getenv("DATA_ANALYSIS_AGENT_MODEL", "gemini-2.0-flash-exp"),
        name="data_analysis_agent",
        instruction=return_instructions_root(),
        global_instruction=return_global_instruction(),
        tools=[
            analyze_trends_tool,
            analyze_holiday_impact_tool,
            analyze_geographic_distribution_tool,
            analyze_seasonal_patterns_tool,
            perform_statistical_analysis_tool,
            compare_countries_tool,
            load_artifacts,
        ],
        before_agent_callback=setup_before_agent_call,
    )
else:
    # Create a simplified agent when ADK is not available
    data_analysis_agent = Agent(
        model=os.getenv("DATA_ANALYSIS_AGENT_MODEL", "gemini-2.0-flash-exp"),
        name="data_analysis_agent",
        instruction=return_instructions_root(),
        global_instruction=return_global_instruction(),
        tools=[
            analyze_trends_tool,
            analyze_holiday_impact_tool,
            analyze_geographic_distribution_tool,
            analyze_seasonal_patterns_tool,
            perform_statistical_analysis_tool,
            compare_countries_tool,
        ],
        before_agent_callback=setup_before_agent_call,
    )
