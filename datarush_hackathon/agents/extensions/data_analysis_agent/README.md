# Data Analysis Agent

A specialized agent for analyzing data from the DataRush Hackathon system. This agent can access information from the dashboard and local databases to generate insights and answer user questions about holiday patterns and passenger data.

## Features

- **Data Access**: Direct access to DataRush dashboard data
- **Database Analysis**: Query and filter local CSV databases
- **Trend Analysis**: Identify patterns and trends in passenger data
- **Holiday Impact**: Analyze the impact of holidays on passenger traffic
- **Geographic Analysis**: Compare data across different countries
- **Statistical Analysis**: Perform statistical calculations and correlations
- **Visualization**: Generate charts and graphs for data visualization

## Available Analysis Types

1. **Trend Analysis**: Analyze temporal patterns and growth rates
2. **Comparison Analysis**: Compare data across countries, months, or periods
3. **Holiday Impact Analysis**: Study the correlation between holidays and passenger traffic
4. **Seasonal Analysis**: Identify seasonal patterns in the data
5. **Geographic Analysis**: Analyze data distribution across countries
6. **Statistical Analysis**: Perform descriptive statistics and correlations

## Tools

- `analyze_trends`: Analyze trends in passenger data over time
- `analyze_holiday_impact`: Analyze the impact of holidays on passenger traffic
- `analyze_geographic_distribution`: Analyze geographic distribution of passenger data
- `analyze_seasonal_patterns`: Analyze seasonal patterns in passenger data
- `perform_statistical_analysis`: Perform statistical analysis on passenger data
- `compare_countries`: Compare passenger data across countries

## Usage

The agent is designed to work within the DataRush multi-agent system. It automatically loads data from the DataRush dashboard and provides analysis capabilities based on user queries.

## Dependencies

- google-adk
- pandas
- numpy
- plotly
- streamlit
- python-dotenv

## Installation

```bash
pip install -e .
```

## Development

```bash
pip install -e ".[dev]"
```

