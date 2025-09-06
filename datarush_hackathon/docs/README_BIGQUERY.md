# 🚀 Configuración de BigQuery para Validación Cruzada

## 📋 Resumen de lo que necesitas

### 1. **Cuenta de Google Cloud Platform** ⭐⭐⭐⭐⭐
- [ ] Crear cuenta en [Google Cloud Console](https://console.cloud.google.com/)
- [ ] Activar facturación (requerido para BigQuery)
- [ ] Crear un proyecto nuevo o usar uno existente

### 2. **APIs Necesarias** ⭐⭐⭐⭐⭐
- [ ] BigQuery API
- [ ] BigQuery Data Transfer API (opcional)
- [ ] Cloud Resource Manager API

### 3. **Credenciales de Servicio** ⭐⭐⭐⭐⭐
- [ ] Crear cuenta de servicio
- [ ] Descargar archivo JSON de credenciales
- [ ] Configurar variables de entorno

## 🔧 Pasos de Configuración

### Paso 1: Crear Proyecto en Google Cloud
1. Ir a [Google Cloud Console](https://console.cloud.google.com/)
2. Crear nuevo proyecto o seleccionar existente
3. Anotar el **PROJECT_ID**

### Paso 2: Activar APIs
1. Ir a "APIs & Services" > "Library"
2. Buscar y activar:
   - BigQuery API
   - BigQuery Data Transfer API
   - Cloud Resource Manager API

### Paso 3: Crear Cuenta de Servicio
1. Ir a "IAM & Admin" > "Service Accounts"
2. Crear cuenta de servicio:
   - **Nombre**: `bigquery-data-validator`
   - **Descripción**: `bigquery-data-validator`
   - **Roles necesarios**:
     - BigQuery Data Viewer
     - BigQuery Job User
     
     - BigQuery Data Editor (opcional)

### Paso 4: Descargar Credenciales
1. Hacer clic en la cuenta de servicio creada
2. Ir a "Keys" > "Add Key" > "Create new key"
3. Seleccionar "JSON"
4. Descargar el archivo JSON
5. Guardar como `bigquery-credentials.json` en el directorio del proyecto

### Paso 5: Configurar Variables de Entorno
1. Copiar `env_example.txt` a `.env`
2. Configurar las siguientes variables:
   ```env
   GOOGLE_CLOUD_PROJECT=tu-proyecto-id
   GOOGLE_APPLICATION_CREDENTIALS=./bigquery-credentials.json
   BIGQUERY_DATASET=passenger_validation
   BIGQUERY_TABLE=economic_indicators
   ```

## 📦 Instalación de Dependencias

### Opción 1: Instalación Automática
```bash
python setup_bigquery.py
```

### Opción 2: Instalación Manual
```bash
pip install google-cloud-bigquery
pip install google-cloud-bigquery-storage
pip install python-dotenv
```

## 🧪 Verificación de Configuración

### Ejecutar Script de Configuración
```bash
python setup_bigquery.py
```

### Probar Conexión
```bash
python -c "from components.bigquery_integration import BigQueryIntegration; bq = BigQueryIntegration(); print('✅ Conexión exitosa' if bq.test_connection() else '❌ Error de conexión')"
```

## 🚀 Uso de BigQuery

### Ejecutar Validación Cruzada
```bash
python validacion_cruzada_datos.py
```

### Usar BigQuery Independientemente
```python
from components.bigquery_integration import BigQueryIntegration

# Inicializar
bq = BigQueryIntegration()

# Obtener datos económicos
df = bq.get_economic_indicators(['USA', 'CAN', 'MEX'])

# Ejecutar análisis completo
resultados = bq.run_validation_analysis(['USA', 'CAN', 'MEX'])
```

## 💰 Consideraciones de Costos

### BigQuery Pricing
- **Consulta**: $5 por TB procesado
- **Almacenamiento**: $0.02 por GB por mes
- **Streaming**: $0.01 por 200MB

### Optimizaciones de Costo
- Usar datasets públicos cuando sea posible
- Implementar cache de resultados
- Optimizar consultas con WHERE clauses
- Usar particionado de tablas

### Límites de Cuota
- **Consultas por día**: 1,000 (gratis)
- **Consultas concurrentes**: 100
- **Tamaño de consulta**: 1TB

## 🔒 Seguridad y Mejores Prácticas

### Seguridad
- ✅ Nunca commitear credenciales
- ✅ Usar variables de entorno
- ✅ Implementar rotación de claves
- ✅ Configurar IAM apropiadamente

### Mejores Prácticas
- ✅ Usar conexiones persistentes
- ✅ Implementar retry logic
- ✅ Logging de consultas
- ✅ Monitoreo de costos

## 📊 Datasets Disponibles

### Datasets Públicos de BigQuery
- **World Bank Data**: `bigquery-public-data.world_bank_intl_education`
- **OECD Data**: `bigquery-public-data.oecd_economic_indicators`
- **UN Data**: `bigquery-public-data.united_nations_international_energy_agency`

### Datasets Personalizados
- Crear dataset para datos de pasajeros
- Crear tablas de validación
- Implementar vistas materializadas

## 🎯 Valor Agregado de BigQuery

### Ventajas
- ✅ **Datos oficiales**: Fuente confiable y actualizada
- ✅ **Escalabilidad**: Maneja grandes volúmenes de datos
- ✅ **Integración**: Se conecta fácilmente con otros servicios de Google
- ✅ **Análisis avanzado**: SQL potente para análisis complejos

### Casos de Uso
- ✅ **Validación cruzada**: Comparar con datos económicos oficiales
- ✅ **Análisis de correlación**: Encontrar relaciones entre variables
- ✅ **Predicciones**: Usar datos históricos para proyecciones
- ✅ **Reportes**: Generar análisis automáticos

## 🆘 Solución de Problemas

### Error: "Credentials not found"
- Verificar que `GOOGLE_APPLICATION_CREDENTIALS` esté configurado
- Verificar que el archivo JSON existe y es válido

### Error: "Project not found"
- Verificar que `GOOGLE_CLOUD_PROJECT` esté configurado correctamente
- Verificar que el proyecto existe en Google Cloud

### Error: "API not enabled"
- Activar BigQuery API en Google Cloud Console
- Esperar unos minutos para que se propague

### Error: "Permission denied"
- Verificar que la cuenta de servicio tenga los permisos necesarios
- Verificar que el proyecto tenga facturación activada

## 📞 Soporte

- [Documentación BigQuery](https://cloud.google.com/bigquery/docs)
- [Python Client Library](https://googleapis.dev/python/bigquery/latest/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/google-bigquery)
- [Google Cloud Support](https://cloud.google.com/support)

---

*Configuración completada para DataRush Hackathon*
