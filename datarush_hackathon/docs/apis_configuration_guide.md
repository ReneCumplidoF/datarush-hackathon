# 🔌 APIs Configuration Guide - DataRush

## 📋 **Resumen de APIs Necesarias**

| API | Proveedor | Requerida | Costo | Límite Gratuito |
|-----|-----------|-----------|-------|-----------------|
| **Google Custom Search** | Google | ✅ Sí | $5/1K queries | 100 queries/día |
| **Google Gemini** | Google | ✅ Sí | $0.50/1M tokens | 15 requests/min |
| **BigQuery** | Google | ✅ Sí | $5/TB | 1TB/mes |
| **News API** | NewsAPI | ⚠️ Opcional | $449/mes | 1000 requests/mes |
| **Bing Search** | Microsoft | ⚠️ Opcional | $4/1K queries | 1000 queries/mes |
| **Wikipedia** | Wikimedia | ✅ Gratuita | Gratis | Sin límite |

## 🔑 **1. Google Custom Search API**

### **Configuración Paso a Paso**

#### **Paso 1: Crear Proyecto en Google Cloud**
```bash
# 1. Ir a: https://console.cloud.google.com/
# 2. Crear nuevo proyecto: "datarush-search-api"
# 3. Anotar PROJECT_ID
```

#### **Paso 2: Habilitar API**
```bash
# 1. Ir a: APIs & Services > Library
# 2. Buscar: "Custom Search API"
# 3. Habilitar API
```

#### **Paso 3: Crear API Key**
```bash
# 1. Ir a: APIs & Services > Credentials
# 2. Crear credenciales > API Key
# 3. Restringir por API: Custom Search API
# 4. Copiar API Key
```

#### **Paso 4: Crear Custom Search Engine**
```bash
# 1. Ir a: https://cse.google.com/
# 2. Agregar sitio: "Entire web"
# 3. Idioma: Spanish
# 4. Obtener Search Engine ID
```

#### **Configuración en .env**
```bash
GOOGLE_SEARCH_API_KEY=AIzaSyBxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GOOGLE_SEARCH_ENGINE_ID=012345678901234567890:abcdefghijk
```

## 🤖 **2. Google Gemini API**

### **Configuración Paso a Paso**

#### **Paso 1: Obtener API Key**
```bash
# 1. Ir a: https://makersuite.google.com/app/apikey
# 2. Crear nueva API Key
# 3. Copiar API Key
```

#### **Configuración en .env**
```bash
GEMINI_API_KEY=AIzaSyBxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GEMINI_MODEL=gemini-1.5-flash
GEMINI_TEMPERATURE=0.7
GEMINI_MAX_TOKENS=1000
```

## 📊 **3. BigQuery API**

### **Configuración Paso a Paso**

#### **Paso 1: Crear Proyecto**
```bash
# 1. Ir a: https://console.cloud.google.com/
# 2. Crear proyecto: "datarush-bigquery"
# 3. Anotar PROJECT_ID
```

#### **Paso 2: Habilitar APIs**
```bash
# Habilitar estas APIs:
- BigQuery API
- BigQuery Storage API
- Cloud Resource Manager API
```

#### **Paso 3: Crear Service Account**
```bash
# 1. Ir a: IAM & Admin > Service Accounts
# 2. Crear cuenta: "datarush-bigquery-sa"
# 3. Roles: BigQuery Data Editor, BigQuery Job User
# 4. Crear y descargar JSON
```

#### **Configuración en .env**
```bash
GOOGLE_CLOUD_PROJECT=datarush-bigquery-2024
GOOGLE_APPLICATION_CREDENTIALS=./bigquery-credentials.json
BIGQUERY_DATASET=passenger_validation
BIGQUERY_LOCATION=US
```

## 📰 **4. News API (Opcional)**

### **Configuración Paso a Paso**

#### **Paso 1: Registrarse**
```bash
# 1. Ir a: https://newsapi.org/
# 2. Registrarse (gratuito)
# 3. Verificar email
# 4. Obtener API Key
```

#### **Configuración en .env**
```bash
NEWS_API_KEY=1234567890abcdef1234567890abcdef
```

## 🔍 **5. Bing Search API (Opcional)**

### **Configuración Paso a Paso**

#### **Paso 1: Crear Recurso en Azure**
```bash
# 1. Ir a: https://azure.microsoft.com/
# 2. Crear cuenta gratuita
# 3. Crear recurso: "Cognitive Services"
# 4. Seleccionar: "Bing Search v7"
# 5. Obtener API Key
```

#### **Configuración en .env**
```bash
BING_SEARCH_API_KEY=1234567890abcdef1234567890abcdef
```

## 🗄️ **6. Google Cloud Storage**

### **Configuración de Buckets**

#### **Crear Buckets**
```bash
# Ejecutar en Google Cloud Shell
gsutil mb gs://datarush-raw-data
gsutil mb gs://datarush-processed-data
gsutil mb gs://datarush-exports
gsutil mb gs://datarush-cache
```

#### **Configurar Permisos**
```bash
# Hacer buckets públicos para exports
gsutil iam ch allUsers:objectViewer gs://datarush-exports
gsutil iam ch allUsers:objectViewer gs://datarush-cache
```

#### **Configuración en .env**
```bash
GCS_BUCKET_RAW_DATA=datarush-raw-data
GCS_BUCKET_PROCESSED_DATA=datarush-processed-data
GCS_BUCKET_EXPORTS=datarush-exports
GCS_BUCKET_CACHE=datarush-cache
```

## 🔧 **Script de Configuración Automática**

### **setup_apis.sh**
```bash
#!/bin/bash

echo "🚀 Configurando APIs para DataRush..."

# Verificar si gcloud está instalado
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI no está instalado"
    echo "Instalar desde: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Variables
PROJECT_ID="datarush-apis-$(date +%s)"
SERVICE_ACCOUNT="datarush-service-account"

echo "📋 Creando proyecto: $PROJECT_ID"
gcloud projects create $PROJECT_ID

echo "🔧 Configurando proyecto"
gcloud config set project $PROJECT_ID

echo "🔌 Habilitando APIs"
gcloud services enable bigquery.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable customsearch.googleapis.com

echo "👤 Creando Service Account"
gcloud iam service-accounts create $SERVICE_ACCOUNT \
    --display-name="DataRush Service Account"

echo "🔑 Asignando roles"
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/bigquery.dataEditor"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/bigquery.jobUser"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.objectAdmin"

echo "📄 Creando credenciales"
gcloud iam service-accounts keys create ./bigquery-credentials.json \
    --iam-account=$SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com

echo "🗄️ Creando buckets"
gsutil mb gs://$PROJECT_ID-raw-data
gsutil mb gs://$PROJECT_ID-processed-data
gsutil mb gs://$PROJECT_ID-exports
gsutil mb gs://$PROJECT_ID-cache

echo "📊 Creando dataset BigQuery"
bq mk --dataset --location=US $PROJECT_ID:passenger_validation

echo "✅ Configuración completada!"
echo "📁 Credenciales: ./bigquery-credentials.json"
echo "🔧 PROJECT_ID: $PROJECT_ID"
echo "📋 Configura las variables en .env"
```

## 💰 **Estimación de Costos**

### **Costo Mensual Estimado**

| Servicio | Uso Estimado | Costo |
|----------|--------------|-------|
| **Google Custom Search** | 1,000 queries | $5 |
| **Google Gemini** | 100K tokens | $0.05 |
| **BigQuery** | 10GB procesados | $0.05 |
| **Cloud Storage** | 1GB almacenado | $0.02 |
| **News API** | 1,000 requests | $0 |
| **Bing Search** | 1,000 queries | $4 |
| **Total** | | **$9.12/mes** |

### **Límites Gratuitos**

| Servicio | Límite Gratuito | Duración |
|----------|----------------|----------|
| **Google Custom Search** | 100 queries/día | Permanente |
| **Google Gemini** | 15 requests/min | Permanente |
| **BigQuery** | 1TB/mes | Permanente |
| **Cloud Storage** | 5GB | Permanente |
| **News API** | 1,000 requests/mes | Permanente |
| **Bing Search** | 1,000 queries/mes | 3 meses |

## 🔐 **Seguridad y Mejores Prácticas**

### **1. Restricciones de API Key**
```bash
# Restringir por IP
# Restringir por API específica
# Rotar keys regularmente
```

### **2. Monitoreo de Uso**
```bash
# Configurar alertas de límites
# Monitorear costos
# Revisar logs de acceso
```

### **3. Backup de Configuración**
```bash
# Guardar archivo .env en lugar seguro
# Backup de credenciales JSON
# Documentar configuración
```

## 🚨 **Solución de Problemas**

### **Error: "API key not valid"**
```bash
# Verificar API key
# Verificar restricciones
# Verificar facturación habilitada
```

### **Error: "Quota exceeded"**
```bash
# Verificar límites
# Esperar reset de cuota
# Considerar upgrade de plan
```

### **Error: "Permission denied"**
```bash
# Verificar roles de Service Account
# Verificar permisos de bucket
# Verificar configuración de IAM
```

## 📋 **Checklist de Configuración**

- [ ] Google Cloud Project creado
- [ ] Custom Search API habilitada
- [ ] Custom Search Engine creado
- [ ] Gemini API key obtenida
- [ ] BigQuery configurado
- [ ] Service Account creado
- [ ] Credenciales descargadas
- [ ] Buckets de Storage creados
- [ ] Variables de entorno configuradas
- [ ] APIs opcionales configuradas
- [ ] Permisos verificados
- [ ] Monitoreo configurado
- [ ] Backup de configuración

---

**Configuración completa de todas las APIs necesarias para DataRush**

