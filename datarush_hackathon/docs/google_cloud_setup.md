# ☁️ Google Cloud Platform - Configuración Completa

## 📋 **APIs y Servicios Necesarios**

### **1. APIs Habilitadas**
```bash
# Habilitar estas APIs en Google Cloud Console
- BigQuery API
- BigQuery Storage API
- Custom Search API
- Cloud Storage API
- Cloud Storage JSON API
- Cloud Resource Manager API
- Service Usage API
```

### **2. Project ID y Credenciales**
```bash
# Configurar en .env
GOOGLE_CLOUD_PROJECT=tu-proyecto-datarush-2024
GOOGLE_APPLICATION_CREDENTIALS=./bigquery-credentials.json
```

## 🗄️ **Google Cloud Storage Buckets**

### **Estructura de Buckets Recomendada**

```
datarush-raw-data/              # Datos originales
├── holidays/
│   ├── global_holidays.csv
│   └── metadata/
├── passengers/
│   ├── monthly_passengers.csv
│   └── metadata/
└── countries/
    ├── countries.csv
    └── metadata/

datarush-processed-data/        # Datos procesados
├── cleaned/
├── enriched/
└── validated/

datarush-exports/               # Exportaciones
├── csv/
├── json/
├── excel/
└── pdf/

datarush-cache/                 # Cache del sistema
├── research/
├── visualizations/
└── api-responses/
```

### **Configuración de Buckets**

```bash
# Crear buckets (ejecutar en Google Cloud Shell)
gsutil mb gs://datarush-raw-data
gsutil mb gs://datarush-processed-data
gsutil mb gs://datarush-exports
gsutil mb gs://datarush-cache

# Configurar permisos
gsutil iam ch allUsers:objectViewer gs://datarush-exports
gsutil iam ch allUsers:objectViewer gs://datarush-cache
```

## 🔧 **Service Account y Permisos**

### **1. Crear Service Account**
```bash
# Nombre: datarush-service-account
# Roles necesarios:
- BigQuery Data Editor
- BigQuery Job User
- Storage Object Admin
- Storage Object Viewer
- Custom Search API User
```

### **2. Descargar Credenciales**
```bash
# Descargar JSON y guardar como:
./bigquery-credentials.json
```

## 📊 **BigQuery Configuration**

### **1. Dataset Configuration**
```sql
-- Crear dataset
CREATE SCHEMA `tu-proyecto-datarush-2024.passenger_validation`
OPTIONS (
  description="Dataset para validación de datos de pasajeros",
  location="US"
);
```

### **2. Tablas Principales**
```sql
-- Tabla de datos de pasajeros
CREATE TABLE `tu-proyecto-datarush-2024.passenger_validation.passenger_data` (
  ISO3 STRING NOT NULL,
  Year INT64 NOT NULL,
  Month INT64 NOT NULL,
  Total FLOAT64,
  Total_OS FLOAT64,
  Domestic FLOAT64,
  International FLOAT64,
  Date DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Tabla de datos de feriados
CREATE TABLE `tu-proyecto-datarush-2024.passenger_validation.holiday_data` (
  ISO3 STRING NOT NULL,
  Date DATE NOT NULL,
  Type STRING,
  Name STRING,
  Year INT64,
  Month INT64,
  Day INT64,
  Weekday STRING,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Tabla de indicadores económicos
CREATE TABLE `tu-proyecto-datarush-2024.passenger_validation.economic_indicators` (
  ISO3 STRING NOT NULL,
  Year INT64 NOT NULL,
  Indicator STRING NOT NULL,
  Value FLOAT64,
  Source STRING,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);
```

## 🔍 **Custom Search Engine**

### **1. Crear Custom Search Engine**
```bash
# Ir a: https://cse.google.com/
# Configuración:
- Sites to search: Entire web
- Language: Spanish
- Country: All countries
- Safe search: Off
```

### **2. Configurar APIs**
```bash
# En Google Cloud Console:
# 1. Habilitar Custom Search API
# 2. Crear API Key
# 3. Restringir por API (Custom Search API)
```

## 📈 **Monitoreo y Logging**

### **1. Cloud Logging**
```bash
# Configurar logs
gcloud logging write datarush-app "DataRush application started" --severity=INFO
```

### **2. Cloud Monitoring**
```bash
# Métricas personalizadas
- API calls per minute
- Data processing time
- Cache hit rate
- Error rate
```

## 💰 **Costos Estimados**

### **BigQuery**
- **Consulta de datos**: $5 por TB procesado
- **Almacenamiento**: $0.02 por GB por mes
- **Estimado mensual**: $10-50

### **Cloud Storage**
- **Almacenamiento**: $0.020 por GB por mes
- **Operaciones**: $0.05 por 10,000 operaciones
- **Estimado mensual**: $5-20

### **Custom Search API**
- **100 consultas gratuitas por día**
- **$5 por 1,000 consultas adicionales**
- **Estimado mensual**: $0-50

### **Total Estimado**: $15-120/mes

## 🚀 **Script de Configuración Automática**

```bash
#!/bin/bash
# setup_google_cloud.sh

# Variables
PROJECT_ID="tu-proyecto-datarush-2024"
SERVICE_ACCOUNT="datarush-service-account"
DATASET_ID="passenger_validation"

# Crear proyecto (si no existe)
gcloud projects create $PROJECT_ID --name="DataRush Project"

# Configurar proyecto
gcloud config set project $PROJECT_ID

# Habilitar APIs
gcloud services enable bigquery.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable customsearch.googleapis.com

# Crear Service Account
gcloud iam service-accounts create $SERVICE_ACCOUNT \
    --display-name="DataRush Service Account"

# Asignar roles
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/bigquery.dataEditor"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/bigquery.jobUser"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.objectAdmin"

# Crear credenciales
gcloud iam service-accounts keys create ./bigquery-credentials.json \
    --iam-account=$SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com

# Crear dataset
bq mk --dataset --location=US $PROJECT_ID:$DATASET_ID

# Crear buckets
gsutil mb gs://$PROJECT_ID-raw-data
gsutil mb gs://$PROJECT_ID-processed-data
gsutil mb gs://$PROJECT_ID-exports
gsutil mb gs://$PROJECT_ID-cache

echo "✅ Configuración completada!"
echo "📁 Credenciales guardadas en: ./bigquery-credentials.json"
echo "🔧 Configura las variables de entorno en .env"
```

## 🔐 **Seguridad y Mejores Prácticas**

### **1. Restricciones de API Key**
```bash
# Restringir por IP
# Restringir por API
# Restringir por referrer
```

### **2. IAM Roles Mínimos**
```bash
# Solo los roles necesarios
# Rotar credenciales regularmente
# Monitorear acceso
```

### **3. Encriptación**
```bash
# Encriptación en tránsito (HTTPS)
# Encriptación en reposo (AES-256)
# Claves de encriptación gestionadas por Google
```

## 📋 **Checklist de Configuración**

- [ ] Proyecto Google Cloud creado
- [ ] APIs habilitadas
- [ ] Service Account creado
- [ ] Credenciales descargadas
- [ ] Buckets de Storage creados
- [ ] Dataset BigQuery creado
- [ ] Custom Search Engine configurado
- [ ] Variables de entorno configuradas
- [ ] Permisos verificados
- [ ] Monitoreo configurado

## 🆘 **Solución de Problemas**

### **Error: "Project not found"**
```bash
# Verificar proyecto
gcloud projects list
gcloud config set project PROJECT_ID
```

### **Error: "Permission denied"**
```bash
# Verificar permisos
gcloud projects get-iam-policy PROJECT_ID
```

### **Error: "API not enabled"**
```bash
# Habilitar API
gcloud services enable API_NAME
```

### **Error: "Bucket not found"**
```bash
# Crear bucket
gsutil mb gs://BUCKET_NAME
```

---

**Configuración completa para DataRush con Google Cloud Platform**

