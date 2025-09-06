# Configuración de BigQuery para Validación Cruzada

## 🎯 Objetivo
Implementar BigQuery para obtener datos económicos adicionales que permitan validar la confiabilidad de los datos de pasajeros.

## 📋 Requisitos Previos

### 1. Cuenta de Google Cloud Platform
- [ ] Crear cuenta en [Google Cloud Console](https://console.cloud.google.com/)
- [ ] Activar facturación (requerido para BigQuery)
- [ ] Crear un proyecto nuevo o usar uno existente

### 2. APIs Necesarias
- [ ] BigQuery API
- [ ] BigQuery Data Transfer API (opcional)
- [ ] Cloud Resource Manager API

### 3. Credenciales de Servicio
- [ ] Crear cuenta de servicio
- [ ] Descargar archivo JSON de credenciales
- [ ] Configurar variables de entorno

## 🚀 Pasos de Configuración

### Paso 1: Crear Proyecto en Google Cloud
```bash
# 1. Ir a Google Cloud Console
# 2. Crear nuevo proyecto o seleccionar existente
# 3. Anotar el PROJECT_ID
```

### Paso 2: Activar APIs
```bash
# En Google Cloud Console:
# 1. Ir a "APIs & Services" > "Library"
# 2. Buscar y activar:
#    - BigQuery API
#    - BigQuery Data Transfer API
#    - Cloud Resource Manager API
```

### Paso 3: Crear Cuenta de Servicio
```bash
# En Google Cloud Console:
# 1. Ir a "IAM & Admin" > "Service Accounts"
# 2. Crear cuenta de servicio:
#    - Nombre: "bigquery-data-validator"
#    - Descripción: "Servicio para validación de datos de pasajeros"
#    - Roles necesarios:
#      - BigQuery Data Viewer
#      - BigQuery Job User
#      - BigQuery Data Editor (opcional)
```

### Paso 4: Descargar Credenciales
```bash
# 1. Hacer clic en la cuenta de servicio creada
# 2. Ir a "Keys" > "Add Key" > "Create new key"
# 3. Seleccionar "JSON"
# 4. Descargar el archivo JSON
# 5. Guardar como "bigquery-credentials.json" en el directorio del proyecto
```

### Paso 5: Configurar Variables de Entorno
```bash
# Crear archivo .env en el directorio del proyecto
GOOGLE_CLOUD_PROJECT=tu-proyecto-id
GOOGLE_APPLICATION_CREDENTIALS=./bigquery-credentials.json
BIGQUERY_DATASET=passenger_validation
BIGQUERY_TABLE=economic_indicators
```

## 📦 Instalación de Dependencias

### 1. Instalar Librerías de Google Cloud
```bash
pip install google-cloud-bigquery
pip install google-cloud-bigquery-storage
pip install python-dotenv
```

### 2. Actualizar requirements.txt
```txt
google-cloud-bigquery>=3.11.0
google-cloud-bigquery-storage>=2.19.0
python-dotenv>=1.0.0
```

## 🔧 Implementación del Código

### 1. Crear Módulo de BigQuery
```python
# components/bigquery_integration.py
```

### 2. Configurar Conexión
```python
# Configuración de autenticación
# Consultas a datasets públicos
# Creación de tablas personalizadas
```

### 3. Integrar con Validación Cruzada
```python
# Modificar validacion_cruzada_datos.py
# Agregar métodos de BigQuery
# Integrar con análisis existente
```

## 📊 Datasets Recomendados

### 1. Datasets Públicos de BigQuery
- **World Bank Data**: `bigquery-public-data.world_bank_intl_education`
- **OECD Data**: `bigquery-public-data.oecd_economic_indicators`
- **UN Data**: `bigquery-public-data.united_nations_international_energy_agency`

### 2. Datasets Personalizados
- Crear dataset para datos de pasajeros
- Crear tablas de validación
- Implementar vistas materializadas

## 🧪 Testing y Validación

### 1. Test de Conexión
```python
def test_bigquery_connection():
    # Verificar conexión
    # Probar consulta simple
    # Validar credenciales
```

### 2. Test de Consultas
```python
def test_bigquery_queries():
    # Probar consultas a datasets públicos
    # Validar resultados
    # Verificar rendimiento
```

### 3. Test de Integración
```python
def test_bigquery_integration():
    # Integrar con validación cruzada
    # Probar análisis completo
    # Validar resultados finales
```

## 💰 Consideraciones de Costos

### 1. BigQuery Pricing
- **Consulta**: $5 por TB procesado
- **Almacenamiento**: $0.02 por GB por mes
- **Streaming**: $0.01 por 200MB

### 2. Optimizaciones de Costo
- Usar datasets públicos cuando sea posible
- Implementar cache de resultados
- Optimizar consultas con WHERE clauses
- Usar particionado de tablas

### 3. Límites de Cuota
- **Consultas por día**: 1,000 (gratis)
- **Consultas concurrentes**: 100
- **Tamaño de consulta**: 1TB

## 🔒 Seguridad y Mejores Prácticas

### 1. Seguridad
- Nunca commitear credenciales
- Usar variables de entorno
- Implementar rotación de claves
- Configurar IAM apropiadamente

### 2. Mejores Prácticas
- Usar conexiones persistentes
- Implementar retry logic
- Logging de consultas
- Monitoreo de costos

### 3. Manejo de Errores
- Timeout de consultas
- Fallback a datos locales
- Mensajes de error informativos
- Logging detallado

## 📈 Monitoreo y Alertas

### 1. Métricas a Monitorear
- Costo de consultas
- Tiempo de respuesta
- Errores de conexión
- Uso de cuota

### 2. Alertas Recomendadas
- Costo diario > $10
- Tiempo de respuesta > 30s
- Errores > 5% de consultas
- Cuota utilizada > 80%

## 🚀 Próximos Pasos

1. **Configurar Google Cloud** (30 min)
2. **Instalar dependencias** (10 min)
3. **Implementar código** (1 hora)
4. **Testing** (30 min)
5. **Integración** (30 min)

## 📞 Soporte

- [Documentación BigQuery](https://cloud.google.com/bigquery/docs)
- [Python Client Library](https://googleapis.dev/python/bigquery/latest/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/google-bigquery)
- [Google Cloud Support](https://cloud.google.com/support)

---

*Guía generada para DataRush Hackathon*
