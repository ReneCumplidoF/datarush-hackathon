# Guía del Agente de Análisis de Datos

## Descripción

El Agente de Análisis de Datos es un agente especializado que puede acceder directamente a la información del tablero DataRush y las bases de datos locales para generar insights específicos sobre patrones de feriados y datos de pasajeros.

## Características Principales

### 🔍 Capacidades de Análisis
- **Análisis de Tendencias**: Identifica patrones temporales y tasas de crecimiento
- **Análisis de Impacto de Feriados**: Estudia la correlación entre feriados y tráfico aéreo
- **Análisis Geográfico**: Compara datos entre diferentes países
- **Análisis Estacional**: Identifica patrones estacionales en los datos
- **Análisis Estadístico**: Realiza estadísticas descriptivas y correlaciones
- **Análisis de Comparación**: Compara datos entre países, meses o períodos

### 🛠️ Herramientas Disponibles
- `analyze_trends`: Analiza tendencias en datos de pasajeros a lo largo del tiempo
- `analyze_holiday_impact`: Analiza el impacto de feriados en el tráfico de pasajeros
- `analyze_geographic_distribution`: Analiza la distribución geográfica de datos de pasajeros
- `analyze_seasonal_patterns`: Analiza patrones estacionales en datos de pasajeros
- `perform_statistical_analysis`: Realiza análisis estadístico en datos de pasajeros
- `compare_countries`: Compara datos de pasajeros entre países

## Cómo Usar

### 1. Acceso desde la Interfaz
1. Abre la aplicación DataRush
2. Carga los datos usando el botón "Cargar Datos"
3. En la sección de chat, selecciona "Análisis de Datos" en el selector de agente
4. Escribe tu pregunta sobre los datos

### 2. Ejemplos de Preguntas

#### Análisis de Tendencias
- "¿Cuáles son las tendencias de pasajeros en los últimos años?"
- "¿Cómo ha evolucionado el tráfico aéreo desde 2020?"
- "¿Qué tasa de crecimiento tienen los pasajeros?"

#### Análisis de Feriados
- "¿Cómo afectan los feriados al tráfico aéreo?"
- "¿Hay correlación entre feriados y pasajeros?"
- "¿Qué feriados tienen mayor impacto en el tráfico?"

#### Análisis Geográfico
- "¿Qué países tienen más pasajeros?"
- "¿Cómo se distribuyen los pasajeros por región?"
- "¿Cuáles son los top 10 países con más tráfico?"

#### Análisis Estacional
- "¿Hay patrones estacionales en los datos?"
- "¿Cuál es el mes con más pasajeros?"
- "¿Cómo varía el tráfico por temporada?"

#### Análisis Estadístico
- "¿Cuál es el promedio de pasajeros por país?"
- "¿Qué tan dispersos están los datos?"
- "¿Hay correlaciones significativas en los datos?"

### 3. Interpretación de Resultados

El agente proporciona:
- **Tipo de Análisis**: Identifica qué tipo de análisis se realizó
- **Insights**: Conclusiones clave basadas en los datos
- **Métricas**: Estadísticas relevantes y números importantes
- **Visualizaciones**: Gráficos y图表 para mejor comprensión
- **Resumen de Datos**: Información sobre los datos analizados

## Arquitectura Técnica

### Estructura de Archivos
```
agents/extensions/data_analysis_agent/
├── __init__.py              # Inicialización del módulo
├── agent.py                 # Agente principal
├── prompts.py               # Instrucciones y prompts
├── tools.py                 # Herramientas de análisis
├── integration.py           # Integración con DataRush
├── pyproject.toml           # Configuración del proyecto
└── README.md                # Documentación del agente
```

### Integración con DataRush
- Se integra con el sistema existente a través de `integration.py`
- Accede a los componentes de DataRush: `DataLoader`, `Filters`, `Visualizations`
- Utiliza el contexto del sistema para análisis contextuales

### Dependencias
- `google-adk`: Framework de agentes de Google
- `pandas`: Manipulación de datos
- `numpy`: Cálculos numéricos
- `plotly`: Visualizaciones interactivas
- `streamlit`: Interfaz de usuario

## Configuración

### Variables de Entorno
```bash
# Modelo del agente (opcional)
DATA_ANALYSIS_AGENT_MODEL=gemini-2.0-flash-exp

# API Keys (si se usan servicios externos)
GEMINI_API_KEY=your_gemini_api_key
```

### Instalación
```bash
# Instalar dependencias
pip install -e agents/extensions/data_analysis_agent/

# O instalar desde el directorio raíz
pip install -e .
```

## Pruebas

### Ejecutar Pruebas
```bash
python test_data_analysis_agent.py
```

### Pruebas Incluidas
- Pruebas de integración con el sistema DataRush
- Pruebas de herramientas individuales
- Pruebas con datos simulados
- Validación de respuestas y visualizaciones

## Limitaciones y Consideraciones

### Limitaciones Actuales
- Requiere que los datos estén cargados en el sistema DataRush
- Las visualizaciones se muestran en formato JSON (requiere conversión)
- Algunas herramientas pueden requerir datos específicos

### Mejoras Futuras
- Integración más profunda con visualizaciones de Streamlit
- Caché de análisis para mejorar rendimiento
- Análisis predictivos y de machine learning
- Exportación de resultados a diferentes formatos

## Soporte y Contribución

### Reportar Problemas
- Crear un issue en el repositorio
- Incluir logs de error y contexto
- Describir pasos para reproducir el problema

### Contribuir
- Seguir las convenciones de código existentes
- Añadir pruebas para nuevas funcionalidades
- Actualizar documentación según sea necesario

## Ejemplos de Uso Avanzado

### Análisis Personalizado
```python
from agents.extensions.data_analysis_agent.integration import data_analysis_integration

# Crear contexto personalizado
context = {
    "data_loaded": True,
    "current_filters": {"countries": ["USA", "MEX"]},
    "filtered_data": {...}
}

# Realizar análisis
results = data_analysis_integration.analyze_user_query(
    "¿Cómo se comparan USA y México en tráfico aéreo?",
    context
)
```

### Acceso Directo a Herramientas
```python
from agents.extensions.data_analysis_agent.tools import analyze_trends

# Usar herramienta directamente
results = analyze_trends(data, filters, time_period="yearly")
```

---

**Nota**: Este agente está diseñado para trabajar dentro del ecosistema DataRush y aprovecha las capacidades existentes del sistema para proporcionar análisis avanzados y insights específicos sobre los datos de feriados y pasajeros.

