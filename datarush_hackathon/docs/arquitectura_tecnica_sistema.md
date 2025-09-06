# Arquitectura Técnica del Sistema DataRush

## Diagrama de Arquitectura General

```mermaid
graph TB
    subgraph "Frontend Layer"
        A[Streamlit Web App]
        B[Sidebar Controls]
        C[Main Content Area]
        D[Chat Interface]
    end
    
    subgraph "Agent Layer"
        E[DataLoader Agent]
        F[Filters Agent]
        G[Visualizations Agent]
        H[Chat Agent]
        I[BigQuery Agent]
    end
    
    subgraph "Data Processing Layer"
        J[Pandas DataFrames]
        K[Data Validation]
        L[Metrics Calculation]
    end
    
    subgraph "External Services"
        M[Google Gemini API]
        N[BigQuery]
        O[World Bank API]
        P[OECD Data]
    end
    
    subgraph "Data Storage"
        Q[CSV Files]
        R[Session State]
        S[Cache Memory]
    end
    
    A --> E
    A --> F
    A --> G
    A --> H
    A --> I
    
    E --> J
    F --> J
    G --> J
    H --> M
    I --> N
    I --> O
    I --> P
    
    J --> K
    K --> L
    L --> G
    
    E --> Q
    A --> R
    G --> S
    
    B --> F
    C --> G
    D --> H
```

## Arquitectura de Componentes Detallada

```mermaid
classDiagram
    class StreamlitApp {
        +main()
        +setup_page_config()
        +initialize_session_state()
        +create_layout()
    }
    
    class DataLoader {
        +load_data()
        +clean_data()
        +get_processed_data()
        +get_data_summary()
        +get_filter_options()
    }
    
    class Filters {
        +create_sidebar_filters()
        +apply_filters()
        +get_active_filters_summary()
        +validate_filters()
        +_create_country_mapping()
        +_get_filter_options()
    }
    
    class Visualizations {
        +create_heatmap_country_month()
        +create_trend_analysis()
        +create_holiday_impact()
        +create_kpi_metrics()
        +_display_kpi_metrics()
    }
    
    class ChatAgent {
        +process_user_message()
        +setup_gemini_agent()
        +_generate_gemini_response()
        +_generate_predefined_response()
        +_create_context_info()
        +get_chat_history()
        +clear_chat_history()
    }
    
    class SmartChatAgent {
        +process_smart_message()
        +setup_smart_chat_agent()
        +setup_query_tools()
        +query_passenger_data()
        +query_holiday_data()
        +compare_countries()
        +analyze_patterns()
        +generate_insights()
    }
    
    class BigQueryIntegration {
        +test_connection()
        +get_world_bank_data()
        +get_oecd_data()
        +get_economic_indicators()
        +create_validation_table()
        +run_validation_analysis()
        +_calculate_data_quality_score()
    }
    
    StreamlitApp --> DataLoader
    StreamlitApp --> Filters
    StreamlitApp --> Visualizations
    StreamlitApp --> ChatAgent
    StreamlitApp --> BigQueryIntegration
    
    DataLoader --> Filters
    Filters --> Visualizations
    ChatAgent --> SmartChatAgent
    BigQueryIntegration --> Visualizations
```

## Flujo de Datos Técnico

```mermaid
flowchart TD
    A[CSV Files] --> B[DataLoader.load_data]
    B --> C[DataLoader.clean_data]
    C --> D[DataLoader.get_processed_data]
    D --> E[Filters.create_sidebar_filters]
    E --> F[Filters.apply_filters]
    F --> G[Visualizations.create_*]
    G --> H[Streamlit Display]
    
    I[User Input] --> J[ChatAgent.process_user_message]
    J --> K[Gemini API]
    K --> L[Response Generation]
    L --> H
    
    M[BigQuery] --> N[BigQueryIntegration.get_*_data]
    N --> O[Validation Analysis]
    O --> P[Metrics Calculation]
    P --> H
    
    Q[Session State] --> R[Data Persistence]
    R --> S[State Management]
    S --> H
```

## Patrones de Diseño Implementados

### 1. Agent Pattern
```mermaid
graph LR
    A[Agent Interface] --> B[DataLoader Agent]
    A --> C[Filters Agent]
    A --> D[Visualizations Agent]
    A --> E[Chat Agent]
    A --> F[BigQuery Agent]
    
    B --> B1[Specific Implementation]
    C --> C1[Specific Implementation]
    D --> D1[Specific Implementation]
    E --> E1[Specific Implementation]
    F --> F1[Specific Implementation]
```

### 2. Strategy Pattern (Chat Responses)
```mermaid
graph TD
    A[ChatAgent] --> B[Response Strategy]
    B --> C[Gemini Strategy]
    B --> D[Predefined Strategy]
    
    C --> C1[AI Generated Response]
    D --> D1[Rule Based Response]
    
    E[Query Type Detection] --> F[Strategy Selection]
    F --> C
    F --> D
```

### 3. Observer Pattern (Filter Updates)
```mermaid
graph TD
    A[Filter Change] --> B[Notify Observers]
    B --> C[Visualizations Update]
    B --> D[Chat Context Update]
    B --> E[Metrics Update]
    
    F[Filter State] --> G[Observer List]
    G --> C
    G --> D
    G --> E
```

## Arquitectura de Datos

```mermaid
erDiagram
    HOLIDAYS {
        string ISO3
        date Date
        string Type
        string Name
        int Year
        int Month
        int Day
        string Weekday
    }
    
    PASSENGERS {
        string ISO3
        int Year
        int Month
        float Total
        float Total_OS
        float Domestic
        float International
        date Date
    }
    
    COUNTRIES {
        string alpha_3
        string name
        string continent
        string region
    }
    
    FILTERS {
        string filter_type
        string filter_value
        boolean is_active
    }
    
    CHAT_HISTORY {
        string role
        string content
        timestamp created_at
    }
    
    VALIDATION_METRICS {
        string metric_name
        float value
        string source
        timestamp calculated_at
    }
    
    HOLIDAYS ||--o{ PASSENGERS : "ISO3"
    COUNTRIES ||--o{ HOLIDAYS : "alpha_3"
    COUNTRIES ||--o{ PASSENGERS : "alpha_3"
    FILTERS ||--o{ PASSENGERS : "applies_to"
    CHAT_HISTORY ||--o{ VALIDATION_METRICS : "references"
```

## Configuración de Servicios

```mermaid
graph TD
    A[Environment Variables] --> B[GEMINI_API_KEY]
    A --> C[GOOGLE_CLOUD_PROJECT]
    A --> D[GOOGLE_APPLICATION_CREDENTIALS]
    A --> E[BIGQUERY_DATASET]
    
    B --> F[Chat Agent]
    C --> G[BigQuery Integration]
    D --> G
    E --> G
    
    H[Configuration Files] --> I[requirements.txt]
    H --> J[.env]
    H --> K[bigquery-credentials.json]
    
    I --> L[Python Dependencies]
    J --> M[Environment Setup]
    K --> N[BigQuery Authentication]
```

## Flujo de Autenticación

```mermaid
sequenceDiagram
    participant U as Usuario
    participant A as App
    participant G as Gemini API
    participant B as BigQuery
    participant W as World Bank
    
    U->>A: Iniciar aplicación
    A->>A: Cargar variables entorno
    A->>G: Verificar API key
    G->>A: Autenticación exitosa
    A->>B: Verificar credenciales
    B->>A: Conexión exitosa
    A->>W: Verificar acceso
    W->>A: Acceso confirmado
    A->>U: Aplicación lista
```

## Manejo de Errores

```mermaid
graph TD
    A[Error Detection] --> B{Error Type}
    B -->|Data Loading| C[DataLoader Error Handler]
    B -->|API Error| D[API Error Handler]
    B -->|Validation Error| E[Validation Error Handler]
    B -->|UI Error| F[UI Error Handler]
    
    C --> C1[Log Error]
    C --> C2[Show User Message]
    C --> C3[Retry Option]
    
    D --> D1[Check API Key]
    D --> D2[Fallback Response]
    D --> D3[User Notification]
    
    E --> E1[Validate Input]
    E --> E2[Show Validation Message]
    E --> E3[Reset to Default]
    
    F --> F1[Log UI Error]
    F --> F2[Show Error Message]
    F --> F3[Reload Component]
```

## Métricas de Rendimiento

```mermaid
graph LR
    A[Performance Metrics] --> B[Response Time]
    A --> C[Memory Usage]
    A --> D[CPU Usage]
    A --> E[Error Rate]
    
    B --> B1[Data Loading: 0.03s]
    B --> B2[Filtering: 0.17s]
    B --> B3[Visualization: <0.02s]
    B --> B4[Chat Response: 0.5-2s]
    
    C --> C1[DataFrames: ~50MB]
    C --> C2[Session State: ~10MB]
    C --> C3[Cache: ~5MB]
    
    D --> D1[Data Processing: Low]
    D --> D2[Visualization: Medium]
    D --> D3[API Calls: High]
    
    E --> E1[Data Loading: 0%]
    E --> E2[API Calls: 5%]
    E --> E3[Validation: 2%]
```

## Escalabilidad y Optimización

```mermaid
graph TD
    A[Scalability Considerations] --> B[Data Volume]
    A --> C[User Concurrency]
    A --> D[API Rate Limits]
    A --> E[Memory Management]
    
    B --> B1[Lazy Loading]
    B --> B2[Data Pagination]
    B --> B3[Incremental Processing]
    
    C --> C1[Session Isolation]
    C --> C2[State Management]
    C --> C3[Resource Pooling]
    
    D --> D1[Request Queuing]
    D --> D2[Response Caching]
    D --> D3[Fallback Mechanisms]
    
    E --> E1[DataFrame Optimization]
    E --> E2[Memory Cleanup]
    E --> E3[Garbage Collection]
```

## Seguridad y Privacidad

```mermaid
graph TD
    A[Security Measures] --> B[API Key Protection]
    A --> C[Data Privacy]
    A --> D[Input Validation]
    A --> E[Error Handling]
    
    B --> B1[Environment Variables]
    B --> B2[No Hardcoded Keys]
    B --> B3[Secure Storage]
    
    C --> C1[No Personal Data]
    C --> C2[Aggregated Statistics]
    C --> C3[Data Anonymization]
    
    D --> D1[Input Sanitization]
    D --> D2[Type Validation]
    D --> D3[Range Checking]
    
    E --> E1[No Sensitive Info in Logs]
    E --> E2[Generic Error Messages]
    E --> E3[Graceful Degradation]
```

