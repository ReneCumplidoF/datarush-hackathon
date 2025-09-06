 .
 # ✈️ AirFlow - Análisis de Patrones de Feriados

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**AirFlow** es una aplicación web avanzada de análisis de datos que estudia el **impacto de los feriados en el tráfico aéreo mundial**. Combina visualizaciones interactivas, inteligencia artificial multiagente y validación cruzada de datos con un diseño visual moderno inspirado en la identidad de AirFlow.

## 🚀 Características Principales

### 🤖 Sistema Multiagente Especializado
- **🎯 Master Agent**: Coordina múltiples agentes para tareas complejas
- **📊 Data Analysis Agent**: Análisis estadístico y visualizaciones avanzadas
- **💼 Business Advisor Agent**: Insights estratégicos y recomendaciones de negocio
- **🔍 Research Agent**: Investigación profunda y validación de datos
- **💬 Smart Chat Agent**: Conversación general y asistencia básica

### 📊 Análisis de Datos Avanzado
- **44,393 feriados** de múltiples países (2010-2019)
- **7,242 registros de pasajeros** de 90 países
- **249 países** con información geográfica
- **Validación cruzada** con World Bank API y BigQuery

### 📈 Visualizaciones Interactivas
- **Mapa de Calor**: Países vs Meses para patrones estacionales
- **Gráfico de Líneas**: Tendencias temporales del tráfico aéreo
- **Gráfico de Barras**: Impacto de feriados en pasajeros
- **Métricas KPI**: Resumen ejecutivo de datos clave

## 🛠️ Tecnologías Utilizadas

- **Frontend**: Streamlit (Python web framework)
- **Visualizaciones**: Plotly (gráficos interactivos)
- **IA Multiagente**: Google Gemini API + Sistema de agentes especializados
- **Datos**: Pandas, NumPy (procesamiento)
- **Validación**: BigQuery, World Bank API
- **Tema Visual**: CSS personalizado con efectos AirFlow
- **Testing**: Pytest (tests unitarios)

## 🚀 Instalación Rápida

### 1. Clonar el Repositorio
```bash
git clone https://github.com/ReneCumplidoF/datarush-hackathon.git
cd datarush-hackathon/datarush_hackathon
```

### 2. Configurar Entorno Virtual
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
```bash
# Crear archivo .env
GEMINI_API_KEY=tu_api_key_aqui
GOOGLE_CLOUD_PROJECT=tu_proyecto_id
GOOGLE_APPLICATION_CREDENTIALS=./bigquery-credentials.json
```

### 5. Ejecutar la Aplicación
```bash
streamlit run app.py
```

### 6. Acceder a la Aplicación
- Abrir navegador en: `http://localhost:8501`
- Hacer clic en "Cargar Datos" en el sidebar
- Explorar visualizaciones y usar el chat con IA

## 📁 Estructura del Proyecto

```
datarush_hackathon/
├── components/                    # Componentes del sistema
│   ├── data_loader.py            # Cargador y procesador de datos
│   ├── filters.py                # Sistema de filtros avanzados
│   ├── visualizations.py         # Visualizaciones interactivas
│   ├── chat_agent.py             # Chat inteligente con IA
│   └── bigquery_integration.py   # Validación cruzada con BigQuery
├── agents/                       # Sistema multiagente
│   ├── core/                     # Componentes base
│   ├── extensions/               # Agentes especializados
│   │   ├── data_analysis_agent/  # Agente de análisis de datos
│   │   ├── business_advisor_agent/ # Agente asesor de negocios
│   │   └── research_agent/       # Agente investigador
│   ├── master_agent/             # Agente maestro coordinador
│   ├── integrations/             # Integraciones externas
│   └── tools/                    # Herramientas auxiliares
├── tests/                        # Tests unitarios
├── datos/                        # Archivos de datos
│   ├── global_holidays.csv       # 44,393 feriados
│   ├── monthly_passengers.csv    # 7,242 registros de pasajeros
│   └── countries.csv             # 249 países
├── app.py                        # Aplicación principal Streamlit
├── airflow_theme.css             # Tema visual AirFlow
└── requirements.txt              # Dependencias Python
```

## 🎯 Casos de Uso

### Para Aerolíneas
- **Planificación de capacidad** basada en patrones de feriados
- **Optimización de precios** en períodos de alta demanda
- **Estrategias de marketing** dirigidas a períodos específicos

### Para Organizaciones de Turismo
- **Predicción de demanda** en diferentes destinos
- **Análisis de competencia** entre países
- **Identificación de oportunidades** de mercado

### Para Investigadores
- **Datos validados** de múltiples fuentes
- **Herramientas de análisis** avanzadas
- **Insights automáticos** mediante IA

## 🧪 Testing

### Tests Unitarios
```bash
# Ejecutar todos los tests
python -m pytest tests/ -v

# Ejecutar test específico
python -m pytest tests/test_data_loader.py -v
```

### Testing Manual
```bash
# Ejecutar script de testing manual
python testing_manual.py
```

## 📊 Métricas de Rendimiento

| Operación | Tiempo | Estado |
|-----------|--------|--------|
| Carga de datos | 0.03s | ✅ Excelente |
| Limpieza de datos | 0.02s | ✅ Excelente |
| Creación de filtros | 0.17s | ✅ Excelente |
| Visualizaciones | <0.02s | ✅ Excelente |
| Testing completo | 1.34s | ✅ Excelente |

## 🔍 Insights Generados

### Patrones Identificados
- **Estacionalidad**: Picos en diciembre y agosto
- **Diferencias culturales**: Feriados religiosos vs nacionales
- **Crecimiento**: 15% anual en viajes durante feriados
- **Correlaciones**: Alta correlación con datos económicos (0.976)

### Recomendaciones Automáticas
- Países con mayor potencial de crecimiento
- Períodos óptimos para campañas de marketing
- Estrategias de precios basadas en patrones
- Identificación de datos inconsistentes

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👥 Desarrolladores

- **René Cumplido** - *Desarrollo principal* - [@ReneCumplidoF](https://github.com/ReneCumplidoF)
- **Fernanda Ojeda** - *Desarrollo principal* - [@Fer-Ojeda](https://github.com/Fer-Ojeda)

## 🙏 Agradecimientos

- **DataRush Hackathon** por la oportunidad de participar
- **Google Cloud** por las APIs de BigQuery y Gemini
- **Streamlit** por el framework web
- **Plotly** por las visualizaciones interactivas

---

**Desarrollado para DataRush Hackathon - Diciembre 2024**

*Sistema multiagente con tema AirFlow - Análisis avanzado de patrones de feriados en tráfico aéreo*
