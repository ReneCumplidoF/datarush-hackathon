# 💼 Business Advisor Agent - Guía Completa

## 🎯 Descripción

El **Business Advisor Agent** es un agente especializado que proporciona recomendaciones estratégicas para negocios basadas en patrones de tráfico aéreo y datos de feriados. Analiza el contexto del negocio y ofrece consejos específicos según el giro empresarial.

## 🏗️ Arquitectura del Agente

### **Componentes Principales**

#### 1. **BusinessAdvisorAgent** (`agent.py`)
- **Clase principal** del agente de negocios
- **Análisis de sectores** empresariales
- **Generación de recomendaciones** personalizadas
- **Integración con datos** de tráfico y feriados

#### 2. **SimpleBusinessAdvisorIntegration** (`simple_integration.py`)
- **Interfaz simplificada** para integración
- **Manejo de contexto** del sistema DataRush
- **Procesamiento de consultas** de negocios

## 🎯 Sectores Empresariales Soportados

### **1. Turismo y Hospitalidad** (`turismo`)
- **Keywords**: turismo, hotel, hospedaje, viaje, vacaciones, turista
- **Enfoque**: Servicios para viajeros y turistas
- **Recomendaciones**: Paquetes turísticos, promociones estacionales, alianzas con aerolíneas

### **2. Retail y Comercio** (`retail`)
- **Keywords**: retail, tienda, comercio, venta, productos, shopping
- **Enfoque**: Venta al por menor y comercio
- **Recomendaciones**: Inventario dinámico, productos para viajeros, horarios flexibles

### **3. Restaurantes y Gastronomía** (`restaurantes`)
- **Keywords**: restaurante, comida, gastronomía, cocina, bar, café
- **Enfoque**: Servicios de alimentación y bebidas
- **Recomendaciones**: Menús estacionales, experiencias gastronómicas, reservaciones

### **4. Transporte y Logística** (`transporte`)
- **Keywords**: transporte, taxi, uber, logística, delivery, envío
- **Enfoque**: Servicios de transporte y logística
- **Recomendaciones**: Rutas optimizadas, tarifas dinámicas, servicios premium

### **5. Entretenimiento y Ocio** (`entretenimiento`)
- **Keywords**: entretenimiento, cine, teatro, museo, parque, diversión
- **Enfoque**: Servicios de entretenimiento y ocio
- **Recomendaciones**: Eventos temáticos, experiencias inmersivas, marketing digital

### **6. Servicios Profesionales** (`servicios`)
- **Keywords**: servicio, consultoría, profesional, asesoría, clínica, oficina
- **Enfoque**: Servicios profesionales y de consultoría
- **Recomendaciones**: Horarios extendidos, servicios express, consultoría especializada

### **7. Eventos y Celebraciones** (`eventos`)
- **Keywords**: evento, fiesta, boda, conferencia, celebración, festival
- **Enfoque**: Organización de eventos y celebraciones
- **Recomendaciones**: Temporadas de eventos, paquetes corporativos, espacios versátiles

## 🔍 Análisis de Datos

### **1. Análisis de Tráfico**
- **Nivel de tráfico**: Alto, medio, bajo según pasajeros mensuales
- **Tendencias**: Crecimiento o decrecimiento del tráfico
- **Estacionalidad**: Meses pico y bajos
- **Distribución mensual**: Patrones de tráfico por mes

### **2. Análisis de Feriados**
- **Total de feriados**: Número de eventos especiales
- **Distribución mensual**: Feriados por mes
- **Mes pico de feriados**: Mes con más eventos
- **Impacto en tráfico**: Correlación entre feriados y pasajeros

## 💡 Sistema de Recomendaciones

### **1. Recomendaciones por Nivel de Tráfico**

#### **Alto Tráfico** (>10,000 pasajeros/mes)
- **Turismo**: Aumentar capacidad de atención, promociones especiales
- **Retail**: Incrementar inventario, productos para viajeros
- **Restaurantes**: Menús especiales, horarios ampliados
- **Transporte**: Aumentar flota, tarifas dinámicas
- **Entretenimiento**: Eventos especiales, promociones
- **Servicios**: Horarios ajustados, servicios express
- **Eventos**: Eventos temáticos relacionados con temporada

#### **Tráfico Moderado** (5,000-10,000 pasajeros/mes)
- **Turismo**: Enfoque en turismo local, paquetes promocionales
- **Retail**: Estrategias de retención, promociones de temporada baja
- **Restaurantes**: Menús estacionales, promociones locales
- **Transporte**: Optimización de rutas, servicios especializados
- **Entretenimiento**: Eventos comunitarios, programas de fidelización
- **Servicios**: Servicios de mantenimiento, desarrollo de relaciones
- **Eventos**: Eventos corporativos, celebraciones locales

#### **Bajo Tráfico** (<5,000 pasajeros/mes)
- **Estrategias de eficiencia**: Optimización de recursos
- **Enfoque local**: Desarrollo de mercado local
- **Promociones especiales**: Atraer clientes durante temporada baja

### **2. Recomendaciones por Impacto de Feriados**

#### **Alto Impacto** (>10 feriados)
- **Promociones temáticas**: Eventos especiales para feriados
- **Productos estacionales**: Artículos relacionados con celebraciones
- **Experiencias únicas**: Actividades temáticas
- **Marketing especializado**: Campañas dirigidas a feriados

#### **Impacto Moderado** (5-10 feriados)
- **Estrategias balanceadas**: Combinación de enfoques
- **Promociones selectivas**: Eventos especiales clave
- **Desarrollo de mercado**: Crecimiento sostenible

### **3. Recomendaciones por Tendencia**

#### **Crecimiento Positivo** (>10%)
- **Inversión en capacidad**: Expansión de servicios
- **Desarrollo de mercado**: Nuevas oportunidades
- **Estrategias de crecimiento**: Aprovechamiento de tendencias

#### **Tendencia a la Baja** (<-10%)
- **Eficiencia operativa**: Optimización de costos
- **Retención de clientes**: Programas de fidelización
- **Diversificación**: Nuevos mercados y servicios

## 🚀 Uso del Agente

### **1. Integración en la Aplicación**
```python
from agents.extensions.business_advisor_agent.simple_integration import simple_business_advisor

# Analizar consulta de negocios
results = simple_business_advisor.analyze_business_query(query, context)

# Obtener resumen de recomendaciones
summary = simple_business_advisor.get_business_summary(results)
```

### **2. Consultas de Ejemplo**

#### **Turismo**
- "Necesito recomendaciones para mi negocio de turismo"
- "¿Qué me recomiendas para mi hotel?"
- "Tengo una agencia de viajes, ¿qué estrategias me sugieres?"

#### **Retail**
- "¿Qué me recomiendas para mi tienda de retail?"
- "Tengo una tienda de productos, ¿cómo puedo aprovechar el tráfico?"
- "Mi negocio es de comercio, ¿qué estrategias me sugieres?"

#### **Restaurantes**
- "¿Qué me recomiendas para mi restaurante?"
- "Tengo un café, ¿cómo puedo aprovechar los feriados?"
- "Mi negocio es de gastronomía, ¿qué estrategias me sugieres?"

### **3. Respuesta del Agente**

#### **Formato de Respuesta**
```
## 💼 Análisis de Negocios - [Sector]

**📊 Análisis de Tráfico:**
• Nivel de tráfico: [Alto/Medio/Bajo] ([X] pasajeros/mes)
• Tendencia: [Crecimiento/Decrecimiento] del [X]%
• Oportunidad: [Alto/Moderado] potencial para el sector

**🎉 Impacto de Feriados:**
• Feriados identificados: [X] eventos especiales
• Oportunidad: [Excelente/Moderada] para promociones temáticas

**💡 Recomendaciones Estratégicas:**
• [Recomendación específica 1]
• [Recomendación específica 2]
• [Recomendación específica 3]
```

## 🧪 Pruebas

### **Script de Prueba**: `test_business_advisor.py`
- **Pruebas de funcionalidad**: 10 consultas de diferentes sectores
- **Pruebas de detección**: 42 variaciones de sectores empresariales
- **Pruebas de recomendaciones**: 7 sectores específicos

### **Ejecutar Pruebas**
```bash
python test_business_advisor.py
```

## 📊 Métricas de Análisis

### **1. Métricas de Tráfico**
- **Total de pasajeros**: Suma total de pasajeros
- **Promedio mensual**: Promedio de pasajeros por mes
- **Mes pico**: Mes con mayor tráfico
- **Mes bajo**: Mes con menor tráfico
- **Tasa de crecimiento**: Crecimiento anual del tráfico
- **Nivel de tráfico**: Clasificación del tráfico

### **2. Métricas de Feriados**
- **Total de feriados**: Número total de eventos
- **Distribución mensual**: Feriados por mes
- **Mes pico de feriados**: Mes con más eventos
- **Impacto en tráfico**: Correlación feriados-tráfico

## 🎯 Beneficios del Agente

### **1. Recomendaciones Personalizadas**
- **Específicas por sector**: Consejos adaptados al giro del negocio
- **Basadas en datos**: Análisis real de tráfico y feriados
- **Contextualizadas**: Consideración del entorno local

### **2. Análisis Estratégico**
- **Patrones de tráfico**: Identificación de tendencias
- **Impacto de feriados**: Oportunidades estacionales
- **Recomendaciones accionables**: Consejos específicos y prácticos

### **3. Integración Completa**
- **Datos en tiempo real**: Información actualizada del tablero
- **Filtros aplicados**: Consideración de filtros del usuario
- **Contexto local**: Análisis específico de la región

## 🔧 Configuración

### **1. Requisitos**
- **Datos de tráfico**: Información de pasajeros por país/mes
- **Datos de feriados**: Eventos especiales por país/fecha
- **Contexto del sistema**: Estado actual del tablero DataRush

### **2. Integración**
- **Importación**: `from agents.extensions.business_advisor_agent.simple_integration import simple_business_advisor`
- **Uso**: `simple_business_advisor.analyze_business_query(query, context)`
- **Resumen**: `simple_business_advisor.get_business_summary(results)`

## 🎉 Resultado Final

El **Business Advisor Agent** proporciona:

✅ **Recomendaciones específicas** por sector empresarial
✅ **Análisis basado en datos** reales de tráfico y feriados
✅ **Consejos accionables** para optimizar negocios
✅ **Integración completa** con el sistema DataRush
✅ **Detección automática** del giro del negocio
✅ **Recomendaciones contextualizadas** según el entorno local

**El agente está listo para proporcionar recomendaciones estratégicas basadas en datos reales de tráfico aéreo y feriados.**

