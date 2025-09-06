# 🔐 Solución: Políticas de Organización que Bloquean BigQuery

## 🚨 Problema Identificado

Tu organización tiene la política `iam.disableServiceAccountKeyCreation` activada, que impide la creación de claves de cuentas de servicio por razones de seguridad.

## ✅ Soluciones Alternativas (Sin Credenciales JSON)

### **Opción 1: Autenticación con gcloud CLI (Recomendada)**

#### Paso 1: Instalar gcloud CLI
```bash
# Windows (PowerShell)
Invoke-WebRequest -Uri "https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe" -OutFile "GoogleCloudSDKInstaller.exe"
.\GoogleCloudSDKInstaller.exe

# macOS
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Linux
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

#### Paso 2: Autenticarse
```bash
# Autenticación de usuario
gcloud auth login

# Configurar proyecto
gcloud config set project TU-PROJECT-ID

# Autenticación para aplicaciones
gcloud auth application-default login
```

#### Paso 3: Verificar configuración
```bash
# Ver cuentas autenticadas
gcloud auth list

# Ver proyecto actual
gcloud config get-value project

# Probar BigQuery
gcloud auth application-default print-access-token
```

### **Opción 2: Usar Solo Datasets Públicos (Sin Autenticación)**

#### Ventajas:
- ✅ No requiere credenciales
- ✅ Acceso a datasets públicos de Google
- ✅ Ideal para desarrollo y pruebas

#### Limitaciones:
- ❌ Solo datasets públicos
- ❌ No puede crear tablas personalizadas
- ❌ Límites de cuota más estrictos

### **Opción 3: Solicitar Permisos al Administrador**

#### Contactar al Administrador de Políticas:
1. **Rol requerido**: `roles/orgpolicy.policyAdmin`
2. **Política a deshabilitar**: `iam.disableServiceAccountKeyCreation`
3. **Justificación**: Desarrollo de validación de datos para hackathon

#### Mensaje para el Administrador:
```
Hola [Nombre del Administrador],

Necesito acceso a BigQuery para un proyecto de hackathon de validación de datos. 
La política iam.disableServiceAccountKeyCreation está bloqueando la creación de 
credenciales de cuenta de servicio.

¿Podrías temporalmente deshabilitar esta política para mi proyecto 
[TU-PROJECT-ID] o sugerir una alternativa segura?

Gracias,
[Tu nombre]
```

## 🚀 Implementación Inmediata

### **Usar la Solución sin Credenciales JSON**

He actualizado el código para que funcione automáticamente sin credenciales JSON:

```python
# El código ahora intenta múltiples métodos de autenticación
from components.bigquery_integration import BigQueryIntegration

# Esto funcionará automáticamente con gcloud auth
bq = BigQueryIntegration()
```

### **Probar la Configuración**

```bash
# Ejecutar script de autenticación alternativa
python autenticacion_alternativa.py

# O ejecutar validación cruzada directamente
python validacion_cruzada_datos.py
```

## 📋 Pasos Recomendados

### **Para Desarrollo Inmediato:**
1. ✅ Instalar gcloud CLI
2. ✅ Ejecutar `gcloud auth login`
3. ✅ Ejecutar `gcloud auth application-default login`
4. ✅ Probar con `python autenticacion_alternativa.py`

### **Para Producción:**
1. 📞 Contactar administrador de políticas
2. 🔐 Solicitar deshabilitación temporal de política
3. 📝 Documentar justificación de negocio
4. 🔄 Implementar rotación de credenciales

## 🎯 Alternativas de Datos

### **Si BigQuery no es posible:**

#### 1. **Usar solo World Bank API**
```python
# Ya implementado en validacion_cruzada_datos.py
df_worldbank = self.obtener_datos_worldbank(paises_unicos, indicadores)
```

#### 2. **Usar OpenFlights API**
```python
# Ya implementado
datos_openflights = self.obtener_datos_openflights()
```

#### 3. **Usar datos locales**
```python
# Crear datasets de ejemplo
# Implementar validación con datos simulados
```

## 🔧 Configuración Rápida

### **Archivo .env simplificado:**
```env
# Solo configurar el proyecto
GOOGLE_CLOUD_PROJECT=tu-proyecto-id

# No necesitas credenciales JSON
# GOOGLE_APPLICATION_CREDENTIALS=./bigquery-credentials.json

# Configuración de BigQuery
BIGQUERY_DATASET=passenger_validation
BIGQUERY_TABLE=economic_indicators
```

### **Verificar configuración:**
```bash
# Verificar gcloud
gcloud auth list

# Verificar proyecto
gcloud config get-value project

# Probar BigQuery
python -c "from components.bigquery_integration import BigQueryIntegration; bq = BigQueryIntegration(); print('✅ OK' if bq.test_connection() else '❌ Error')"
```

## 🆘 Solución de Problemas

### **Error: "No authenticated accounts"**
```bash
gcloud auth login
gcloud auth application-default login
```

### **Error: "Project not found"**
```bash
gcloud config set project TU-PROJECT-ID
```

### **Error: "API not enabled"**
```bash
gcloud services enable bigquery.googleapis.com
```

### **Error: "Permission denied"**
- Verificar que el proyecto tenga facturación activada
- Verificar que tu cuenta tenga permisos de BigQuery

## 📞 Contacto de Soporte

### **Para problemas de políticas:**
- **Google Cloud Support**: https://cloud.google.com/support
- **Documentación de políticas**: https://cloud.google.com/resource-manager/docs/organization-policy

### **Para problemas técnicos:**
- **Stack Overflow**: https://stackoverflow.com/questions/tagged/google-bigquery
- **GitHub Issues**: Crear issue en el repositorio del proyecto

---

*Solución implementada para DataRush Hackathon*
