# Diagrama de Flujo de Tareas Multiagente - DataRush

## Flujo de Trabajo Multiagente

```mermaid
graph TD
    A[Usuario inicia aplicación] --> B[DataLoader Agent]
    B --> C{Carga datos exitosa?}
    C -->|No| D[Mostrar error]
    C -->|Sí| E[Filtros Agent]
    E --> F[Visualizations Agent]
    F --> G[Chat Agent]
    G --> H[BigQuery Agent - Opcional]
    
    subgraph "DataLoader Agent"
        B1[Cargar global_holidays.csv]
        B2[Cargar monthly_passengers.csv]
        B3[Cargar countries.csv]
        B4[Procesar y limpiar datos]
        B5[Crear métricas derivadas]
    end
    
    subgraph "Filtros Agent"
        E1[Filtros Temporales]
        E2[Filtros Geográficos]
        E3[Filtros de Feriados]
        E4[Filtros de Pasajeros]
        E5[Filtros de Análisis]
    end
    
    subgraph "Visualizations Agent"
        F1[Mapa de Calor]
        F2[Gráfico de Líneas]
        F3[Gráfico de Barras]
        F4[Métricas KPI]
    end
    
    subgraph "Chat Agent"
        G1[Procesar consulta usuario]
        G2[Detectar tipo de consulta]
        G3[Usar herramienta específica]
        G4[Generar respuesta contextual]
    end
    
    subgraph "BigQuery Agent"
        H1[Validar conexión]
        H2[Obtener datos World Bank]
        H3[Obtener datos OECD]
        H4[Calcular correlaciones]
        H5[Generar métricas validación]
    end
    
    B --> B1
    B1 --> B2
    B2 --> B3
    B3 --> B4
    B4 --> B5
    
    E --> E1
    E1 --> E2
    E2 --> E3
    E3 --> E4
    E4 --> E5
    
    F --> F1
    F1 --> F2
    F2 --> F3
    F3 --> F4
    
    G --> G1
    G1 --> G2
    G2 --> G3
    G3 --> G4
    
    H --> H1
    H1 --> H2
    H2 --> H3
    H3 --> H4
    H4 --> H5
    
    G --> I[Usuario interactúa]
    I --> J{Nueva consulta?}
    J -->|Sí| G
    J -->|No| K[Fin sesión]
    
    H --> L[Mostrar validación]
    L --> M[Actualizar visualizaciones]
```

## Interacciones entre Agentes

```mermaid
sequenceDiagram
    participant U as Usuario
    participant DL as DataLoader
    participant F as Filtros
    participant V as Visualizations
    participant C as Chat Agent
    participant BQ as BigQuery
    
    U->>DL: Cargar datos
    DL->>DL: Procesar CSV
    DL->>F: Datos procesados
    F->>F: Crear filtros
    F->>V: Datos + filtros
    V->>V: Generar gráficos
    V->>C: Contexto visualizaciones
    C->>U: Mostrar interfaz
    
    U->>F: Aplicar filtros
    F->>V: Datos filtrados
    V->>V: Actualizar gráficos
    V->>C: Nuevo contexto
    
    U->>C: Pregunta
    C->>C: Analizar consulta
    C->>F: Obtener datos filtrados
    F->>C: Datos actuales
    C->>U: Respuesta contextual
    
    U->>BQ: Validar datos
    BQ->>BQ: Consultar fuentes externas
    BQ->>V: Métricas validación
    V->>U: Mostrar validación
```

## Arquitectura de Componentes

```mermaid
graph LR
    subgraph "Frontend Layer"
        A[Streamlit App]
        B[Sidebar Filtros]
        C[Visualizaciones]
        D[Chat Interface]
    end
    
    subgraph "Agent Layer"
        E[DataLoader Agent]
        F[Filters Agent]
        G[Visualizations Agent]
        H[Chat Agent]
        I[BigQuery Agent]
    end
    
    subgraph "Data Layer"
        J[CSV Files]
        K[BigQuery]
        L[World Bank API]
    end
    
    subgraph "AI Layer"
        M[Google Gemini]
        N[Smart Chat Tools]
    end
    
    A --> E
    A --> F
    A --> G
    A --> H
    A --> I
    
    E --> J
    F --> E
    G --> F
    H --> M
    H --> N
    I --> K
    I --> L
    
    B --> F
    C --> G
    D --> H
```

## Flujo de Datos

```mermaid
flowchart TD
    A[Archivos CSV] --> B[DataLoader]
    B --> C[Datos Procesados]
    C --> D[Filtros]
    D --> E[Datos Filtrados]
    E --> F[Visualizaciones]
    E --> G[Chat Context]
    F --> H[Interfaz Usuario]
    G --> I[Respuestas IA]
    I --> H
    
    J[BigQuery] --> K[Validación]
    K --> L[Métricas Calidad]
    L --> H
    
    M[Gemini API] --> N[Análisis IA]
    N --> I
```

## Estados del Sistema

```mermaid
stateDiagram-v2
    [*] --> Inicial
    Inicial --> CargandoDatos: Usuario hace clic "Cargar Datos"
    CargandoDatos --> DatosCargados: Datos procesados exitosamente
    CargandoDatos --> ErrorCarga: Error en carga
    ErrorCarga --> Inicial: Reintentar
    
    DatosCargados --> AplicandoFiltros: Usuario modifica filtros
    AplicandoFiltros --> DatosFiltrados: Filtros aplicados
    DatosFiltrados --> AplicandoFiltros: Cambiar filtros
    DatosFiltrados --> ChatActivo: Usuario hace pregunta
    ChatActivo --> DatosFiltrados: Respuesta generada
    ChatActivo --> ValidandoDatos: Usuario solicita validación
    ValidandoDatos --> DatosFiltrados: Validación completada
    
    DatosFiltrados --> [*]: Usuario cierra aplicación
```

## Tareas por Agente

### DataLoader Agent
- Cargar archivos CSV
- Validar integridad de datos
- Limpiar y procesar datos
- Crear métricas derivadas
- Manejar errores de carga

### Filters Agent
- Crear interfaz de filtros
- Aplicar filtros temporales
- Aplicar filtros geográficos
- Aplicar filtros de feriados
- Aplicar filtros de pasajeros
- Validar filtros

### Visualizations Agent
- Generar mapa de calor
- Crear gráficos de líneas
- Crear gráficos de barras
- Calcular métricas KPI
- Actualizar visualizaciones

### Chat Agent
- Procesar consultas del usuario
- Detectar tipo de consulta
- Enrutar a herramienta específica
- Generar respuestas contextuales
- Mantener historial de chat

### BigQuery Agent
- Validar conexión
- Obtener datos externos
- Calcular correlaciones
- Generar métricas de validación
- Manejar errores de conexión
