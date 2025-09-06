# 🔍 Research Agent - Diagrama de Capacidades

## Arquitectura del Research Agent

```mermaid
graph TD
    A[Usuario hace consulta] --> B[SmartChatAgent detecta investigación]
    B --> C[ResearchAgent.research_topic]
    C --> D[Extraer tema de investigación]
    D --> E[Verificar cache]
    E -->|Cache válido| F[Retornar resultados cached]
    E -->|Cache expirado| G[Iniciar investigación]
    
    G --> H[Wikipedia Search]
    G --> I[Google Search]
    G --> J[News API]
    G --> K[Bing Search - Opcional]
    
    H --> L[Análisis de Contexto]
    I --> L
    J --> L
    K --> L
    
    L --> M[Análisis de Datos de Pasajeros]
    L --> N[Análisis de Datos de Feriados]
    L --> O[Análisis de Filtros Aplicados]
    
    M --> P[Generar Insights]
    N --> P
    O --> P
    
    P --> Q[Generar Recomendaciones]
    Q --> R[Calcular Confianza]
    R --> S[Formatear Respuesta]
    S --> T[Guardar en Cache]
    T --> U[Retornar al Usuario]
```

## Flujo de Investigación Detallado

```mermaid
sequenceDiagram
    participant U as Usuario
    participant SC as SmartChatAgent
    participant R as ResearchAgent
    participant W as Wikipedia
    participant G as Google Search
    participant N as News API
    participant C as Cache
    
    U->>SC: "Investigar impacto COVID-19 en aviación"
    SC->>R: research_topic(topic, context)
    R->>C: Verificar cache
    C->>R: Cache expirado
    
    par Búsqueda Paralela
        R->>W: Buscar en Wikipedia
        W->>R: Información general
    and
        R->>G: Buscar en Google
        G->>R: Resultados web
    and
        R->>N: Buscar noticias
        N->>R: Noticias recientes
    end
    
    R->>R: Analizar contexto de datos
    R->>R: Generar insights
    R->>R: Generar recomendaciones
    R->>R: Calcular confianza
    
    R->>C: Guardar en cache
    R->>SC: Resultados de investigación
    SC->>U: Respuesta formateada
```

## Fuentes de Información

```mermaid
graph LR
    A[Research Agent] --> B[Wikipedia API]
    A --> C[Google Custom Search]
    A --> D[News API]
    A --> E[Bing Search API]
    
    B --> B1[Información General]
    B --> B2[Contexto Histórico]
    B --> B3[Definiciones]
    
    C --> C1[Información Actual]
    C --> C2[Artículos Específicos]
    C --> C3[Estudios Recientes]
    
    D --> D1[Noticias Recientes]
    D --> D2[Tendencias Actuales]
    D --> D3[Eventos Relevantes]
    
    E --> E1[Búsqueda Alternativa]
    E --> E2[Resultados Adicionales]
    E --> E3[Validación Cruzada]
```

## Análisis de Contexto

```mermaid
graph TD
    A[Contexto de Datos] --> B[Datos de Pasajeros]
    A --> C[Datos de Feriados]
    A --> D[Filtros Aplicados]
    
    B --> B1[Patrones Estacionales]
    B --> B2[Tendencias de Crecimiento]
    B --> B3[Impacto de Feriados]
    
    C --> C1[Tipos de Feriados]
    C --> C2[Distribución Geográfica]
    C --> C3[Patrones Temporales]
    
    D --> D1[Período Temporal]
    D --> D2[Países Seleccionados]
    D --> D3[Tipos de Análisis]
    
    B1 --> E[Insights Generados]
    B2 --> E
    B3 --> E
    C1 --> E
    C2 --> E
    C3 --> E
    D1 --> E
    D2 --> E
    D3 --> E
```

## Generación de Respuestas

```mermaid
graph TD
    A[Resultados de Investigación] --> B[Formatear Fuentes]
    A --> C[Formatear Insights]
    A --> D[Formatear Recomendaciones]
    A --> E[Calcular Confianza]
    
    B --> B1[Wikipedia: Título + Extracto]
    B --> B2[Google: Título + Snippet]
    B --> B3[News: Título + Descripción]
    
    C --> C1[Insights de Patrones]
    C --> C2[Insights de Tendencias]
    C --> C3[Insights de Impacto]
    
    D --> D1[Recomendaciones de Análisis]
    D --> D2[Recomendaciones de Predicción]
    D --> D3[Recomendaciones de Comparación]
    
    E --> E1[Score de Fuentes]
    E --> E2[Score de Relevancia]
    E --> E3[Score de Insights]
    
    B1 --> F[Respuesta Final]
    B2 --> F
    B3 --> F
    C1 --> F
    C2 --> F
    C3 --> F
    D1 --> F
    D2 --> F
    D3 --> F
    E1 --> F
    E2 --> F
    E3 --> F
```

## Configuración de APIs

```mermaid
graph TD
    A[Variables de Entorno] --> B[Google Search API]
    A --> C[News API]
    A --> D[Bing Search API]
    A --> E[Configuración Cache]
    
    B --> B1[GOOGLE_SEARCH_API_KEY]
    B --> B2[GOOGLE_SEARCH_ENGINE_ID]
    B --> B3[Límite: 100 queries/día]
    
    C --> C1[NEWS_API_KEY]
    C --> C2[Límite: 1000 requests/mes]
    C --> C3[Noticias últimos 30 días]
    
    D --> D1[BING_SEARCH_API_KEY]
    D --> D2[Límite: 1000 requests/mes]
    D --> D3[Búsqueda alternativa]
    
    E --> E1[RESEARCH_CACHE_TIME=3600]
    E --> E2[MAX_SOURCES_PER_QUERY=5]
    E --> E3[MIN_RELEVANCE_SCORE=0.3]
```

## Métricas de Rendimiento

```mermaid
graph LR
    A[Métricas de Research Agent] --> B[Tiempo de Respuesta]
    A --> C[Calidad de Fuentes]
    A --> D[Confianza en Resultados]
    A --> E[Uso de Cache]
    
    B --> B1[< 10 segundos objetivo]
    B --> B2[Wikipedia: ~2s]
    B --> B3[Google: ~3s]
    B --> B4[News: ~2s]
    
    C --> C1[Score de Relevancia > 0.5]
    C --> C2[Fuentes Diversas]
    C --> C3[Información Actualizada]
    
    D --> D1[Confianza > 0.7]
    D --> D2[Múltiples Fuentes]
    D --> D3[Insights Coherentes]
    
    E --> E1[Cache Hit Rate > 60%]
    E --> E2[Reducción de APIs calls]
    E --> E3[Mejora de Rendimiento]
```

## Casos de Uso del Research Agent

```mermaid
graph TD
    A[Consultas de Usuario] --> B[Análisis de Tendencias]
    A --> C[Validación de Datos]
    A --> D[Contexto de Mercado]
    A --> E[Investigación Académica]
    
    B --> B1["¿Cómo afecta el COVID-19 a la aviación?"]
    B --> B2["Tendencias de viajes en 2024"]
    B --> B3["Impacto de feriados en turismo"]
    
    C --> C1["Verificar datos con fuentes externas"]
    C --> C2["Identificar anomalías"]
    C --> C3["Sugerir mejoras"]
    
    D --> D1["Eventos que afectan la aviación"]
    D --> D2["Análisis de competencia"]
    D --> D3["Tendencias económicas"]
    
    E --> E1["Estudios científicos relevantes"]
    E --> E2["Metodologías de análisis"]
    E --> E3["Mejores prácticas"]
```

## Integración con SmartChatAgent

```mermaid
graph TD
    A[SmartChatAgent] --> B[Detectar Palabras Clave]
    B --> C{¿Es consulta de investigación?}
    C -->|Sí| D[Activar ResearchAgent]
    C -->|No| E[Usar herramientas normales]
    
    D --> F[research_topic()]
    F --> G[Procesar múltiples fuentes]
    G --> H[Generar respuesta contextual]
    H --> I[Formatear para chat]
    I --> J[Retornar al usuario]
    
    E --> K[query_passenger_data]
    E --> L[query_holiday_data]
    E --> M[compare_countries]
    E --> N[analyze_patterns]
    E --> O[generate_insights]
```

## Palabras Clave de Activación

```mermaid
graph LR
    A[Palabras Clave] --> B[investigar]
    A --> C[investigación]
    A --> D[buscar información]
    A --> E[fuentes externas]
    A --> F[información sobre]
    A --> G[datos sobre]
    A --> H[estudios sobre]
    A --> I[investigaciones sobre]
    
    B --> J[Activar ResearchAgent]
    C --> J
    D --> J
    E --> J
    F --> J
    G --> J
    H --> J
    I --> J
```

## Flujo de Cache

```mermaid
graph TD
    A[Consulta de Investigación] --> B[Generar Cache Key]
    B --> C{¿Existe en Cache?}
    C -->|Sí| D{¿Cache válido?}
    C -->|No| E[Realizar Investigación]
    
    D -->|Sí| F[Retornar Cache]
    D -->|No| E
    
    E --> G[Buscar en Fuentes]
    G --> H[Procesar Resultados]
    H --> I[Generar Respuesta]
    I --> J[Guardar en Cache]
    J --> K[Retornar Resultado]
    
    F --> L[Actualizar Timestamp]
    K --> L
```

## Configuración de Relevancia

```mermaid
graph TD
    A[Calcular Relevancia] --> B[Extraer Palabras Clave]
    B --> C[Comparar con Contenido]
    C --> D[Calcular Intersección]
    D --> E[Bonus por Palabras Importantes]
    E --> F[Score Final de Relevancia]
    
    G[Palabras Importantes] --> H[aviación]
    G --> I[aéreo]
    G --> J[pasajeros]
    G --> K[feriado]
    G --> L[tráfico]
    
    H --> E
    I --> E
    J --> E
    K --> E
    L --> E
```

Este Research Agent convierte al sistema DataRush en una herramienta mucho más inteligente y completa, capaz de proporcionar información contextual y actualizada cuando los datos internos no son suficientes para responder las consultas del usuario.

