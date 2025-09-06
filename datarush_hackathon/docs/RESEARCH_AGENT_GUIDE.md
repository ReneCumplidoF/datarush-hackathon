# 🔍 Research Agent - Guía Completa

## 🎯 Descripción

El **Research Agent** es un agente especializado en búsqueda de información externa que complementa los insights del sistema DataRush con investigación web, noticias y fuentes de conocimiento para proporcionar análisis más completos y contextualizados.

## 🏗️ Arquitectura del Agente

### **Componentes Principales**

#### 1. **ResearchAgent** (`research_agent.py`)
- **Clase principal** del agente de investigación
- **Búsqueda web** usando Google Custom Search API
- **Búsqueda de noticias** usando News API
- **Búsqueda en Wikipedia** para contexto general
- **Análisis de contexto** de datos del sistema

#### 2. **SimpleResearchIntegration** (`simple_integration.py`)
- **Interfaz simplificada** para integración
- **Base de conocimiento** integrada
- **Funcionamiento sin dependencias** externas
- **Fallback inteligente** cuando las APIs no están disponibles

## 🔍 Fuentes de Información

### **1. Base de Conocimiento Integrada**
- **Patrones estacionales**: Información sobre estacionalidad en aviación
- **Impacto de feriados**: Efectos de feriados en tráfico aéreo
- **Crecimiento de aviación**: Tendencias de crecimiento de la industria
- **Tecnología aérea**: Nuevas tecnologías en aviación
- **Regulaciones aéreas**: Normativas internacionales

### **2. Fuentes Externas (Opcionales)**
- **Wikipedia**: Contexto general y definiciones
- **Google Search**: Información actualizada de la web
- **News API**: Noticias recientes sobre el tema
- **Bing Search**: Búsqueda alternativa

## 🧠 Sistema de Investigación

### **1. Proceso de Investigación**

#### **Paso 1: Búsqueda en Base de Conocimiento**
- **Búsqueda local**: Información pre-cargada y relevante
- **Matching inteligente**: Detección de relevancia por palabras clave
- **Categorización**: Organización por temas específicos

#### **Paso 2: Investigación Externa (Opcional)**
- **Wikipedia**: Contexto general y definiciones
- **Búsqueda web**: Información actualizada
- **Noticias**: Información reciente y relevante

#### **Paso 3: Análisis de Contexto**
- **Datos de pasajeros**: Análisis de patrones en datos locales
- **Datos de feriados**: Impacto de eventos especiales
- **Filtros aplicados**: Consideración de restricciones del usuario

#### **Paso 4: Generación de Insights**
- **Insights de conocimiento**: Basados en información encontrada
- **Insights de análisis**: Basados en datos del sistema
- **Insights contextuales**: Relacionados con el tema específico

#### **Paso 5: Recomendaciones**
- **Recomendaciones de análisis**: Sugerencias para análisis más detallado
- **Recomendaciones de predicción**: Consejos para proyecciones futuras
- **Recomendaciones de comparación**: Sugerencias para análisis comparativos

### **2. Cálculo de Confianza**

#### **Factores de Confianza**
- **Número de fuentes**: Más fuentes = mayor confianza
- **Relevancia de fuentes**: Score de relevancia de cada fuente
- **Calidad de insights**: Número y calidad de insights generados
- **Consistencia**: Coherencia entre diferentes fuentes

#### **Niveles de Confianza**
- **🟢 Alta (>70%)**: Múltiples fuentes consistentes y relevantes
- **🟡 Media (40-70%)**: Fuentes limitadas pero relevantes
- **🔴 Baja (<40%)**: Pocas fuentes o información inconsistente

## 🚀 Uso del Agente

### **1. Integración en la Aplicación**
```python
from agents.extensions.research_agent.simple_integration import simple_research_agent

# Investigar un tema
results = simple_research_agent.research_topic(topic, context)

# Obtener resumen de investigación
summary = simple_research_agent.get_research_summary(results)
```

### **2. Consultas de Ejemplo**

#### **Patrones y Tendencias**
- "patrones de tráfico aéreo en Europa"
- "tendencias de crecimiento en aviación"
- "análisis estacional del tráfico aéreo"

#### **Impacto de Feriados**
- "impacto de feriados en el turismo"
- "efectos de vacaciones en tráfico aéreo"
- "influencia de eventos especiales"

#### **Análisis Comparativo**
- "comparación de países en tráfico aéreo"
- "diferencias regionales en aviación"
- "análisis de mercados aéreos"

#### **Predicciones y Futuro**
- "predicción de tráfico aéreo futuro"
- "tendencias futuras en aviación"
- "impacto de nuevas tecnologías"

### **3. Respuesta del Agente**

#### **Formato de Respuesta**
```
## 🔍 Investigación: [Tema]

**📚 Fuentes encontradas:** [Número]

• **Wikipedia**: [Título]
  [Contenido resumido...]

• **Google Search**: [Título]
  [Snippet...]

**💡 Insights generados:** [Número]

• [Descripción del insight]
  *Confianza: [X]%*

**🎯 Recomendaciones:** [Número]

• 🔴 [Recomendación de alta prioridad]
• 🟡 [Recomendación de media prioridad]

**📊 Confianza general:** 🟢 [X]%
```

## 🧪 Pruebas

### **Script de Prueba**: `test_research_agent.py`
- **Pruebas de funcionalidad**: 10 consultas de diferentes temas
- **Pruebas de fuentes**: Verificación de diferentes fuentes de información
- **Pruebas de insights**: Generación de insights y recomendaciones

### **Ejecutar Pruebas**
```bash
python test_research_agent.py
```

## 📊 Base de Conocimiento

### **1. Patrones Estacionales**
- **Contenido**: Información sobre estacionalidad en aviación
- **Keywords**: estacional, temporada, mes, año, patrón
- **Relevancia**: 0.9

### **2. Impacto de Feriados**
- **Contenido**: Efectos de feriados en tráfico aéreo
- **Keywords**: feriado, vacaciones, impacto, evento especial
- **Relevancia**: 0.95

### **3. Crecimiento de Aviación**
- **Contenido**: Tendencias de crecimiento de la industria
- **Keywords**: crecimiento, tendencia, evolución, desarrollo
- **Relevancia**: 0.85

### **4. Tecnología Aérea**
- **Contenido**: Nuevas tecnologías en aviación
- **Keywords**: tecnología, innovación, eficiencia, sostenibilidad
- **Relevancia**: 0.8

### **5. Regulaciones Aéreas**
- **Contenido**: Normativas internacionales de aviación
- **Keywords**: regulación, normativa, estándar, seguridad
- **Relevancia**: 0.75

## 🎯 Beneficios del Agente

### **1. Complemento de Insights**
- **Información externa**: Contexto adicional para análisis
- **Perspectiva amplia**: Visión más completa del tema
- **Validación**: Confirmación de hallazgos con fuentes externas

### **2. Investigación Inteligente**
- **Búsqueda contextual**: Queries optimizadas para aviación
- **Múltiples fuentes**: Diversidad de información
- **Relevancia**: Filtrado de información relevante

### **3. Análisis Integrado**
- **Datos locales + externos**: Combinación de información
- **Contexto del sistema**: Consideración de filtros y datos actuales
- **Insights personalizados**: Análisis específico para el contexto

## 🔧 Configuración

### **1. Funcionamiento Básico**
- **Sin configuración**: Funciona con base de conocimiento integrada
- **Sin APIs externas**: No requiere claves de API
- **Funcionamiento local**: Toda la funcionalidad básica disponible

### **2. Funcionamiento Avanzado (Opcional)**
- **Google Search API**: Para búsqueda web actualizada
- **News API**: Para noticias recientes
- **Bing Search API**: Para búsqueda alternativa

### **3. Variables de Entorno (Opcionales)**
```env
GOOGLE_SEARCH_API_KEY=your_google_api_key
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id
NEWS_API_KEY=your_news_api_key
BING_SEARCH_API_KEY=your_bing_api_key
```

## 🎉 Resultado Final

El **Research Agent** proporciona:

✅ **Investigación externa** para complementar insights
✅ **Base de conocimiento** integrada y especializada
✅ **Múltiples fuentes** de información
✅ **Análisis contextual** basado en datos del sistema
✅ **Insights personalizados** según el tema de investigación
✅ **Recomendaciones específicas** para análisis más detallado
✅ **Funcionamiento sin dependencias** externas
✅ **Integración completa** con el sistema DataRush

**El agente investigador está listo para complementar los insights con información externa relevante y contextualizada.**