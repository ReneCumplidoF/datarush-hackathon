# ✈️ AirFlow - Análisis de Patrones de Feriados

Una aplicación de análisis de datos que utiliza múltiples agentes de IA para analizar el impacto de los feriados en el tráfico aéreo.

## 🚀 Características

- **Análisis de tendencias** de pasajeros por mes
- **Comparación entre países** y regiones  
- **Impacto de feriados** en el tráfico aéreo
- **Filtros avanzados** para análisis específicos
- **Visualizaciones interactivas** con Plotly
- **Chat IA** con múltiples agentes especializados

## 🏗️ Arquitectura

El sistema utiliza una arquitectura multi-agente con los siguientes componentes:

- **Master Agent**: Coordina múltiples agentes especializados
- **Data Analysis Agent**: Análisis estadístico y visualizaciones
- **Business Advisor Agent**: Recomendaciones de negocio
- **Research Agent**: Investigación y contexto adicional
- **Chat Agent**: Interfaz conversacional

## 📦 Instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd datarush_hackathon
```

2. **Crear entorno virtual**
```bash
python -m venv venv
```

3. **Activar entorno virtual**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

5. **Configurar variables de entorno**
```bash
# Copiar archivo de ejemplo
copy env_example.txt .env

# Editar .env con tus API keys
```

6. **Ejecutar aplicación**
```bash
streamlit run app.py
```

## 🔧 Configuración

### Variables de Entorno Requeridas

```env
GEMINI_API_KEY=tu_api_key_aqui
GOOGLE_SEARCH_API_KEY=tu_api_key_aqui
```

### Archivos de Datos

La aplicación utiliza los siguientes archivos de datos en la carpeta `datos/`:

- `countries.csv`: Información de países
- `global_holidays.csv`: Datos de feriados globales
- `monthly_passengers.csv`: Datos de pasajeros mensuales

## 📊 Uso

1. **Cargar Datos**: Haz clic en "Cargar Datos" para procesar los archivos
2. **Aplicar Filtros**: Usa el botón ☰ para expandir los filtros
3. **Explorar Visualizaciones**: Analiza los 4 cuadrantes de visualizaciones
4. **Chat IA**: Interactúa con los diferentes agentes especializados

## 🧪 Testing

```bash
# Ejecutar todos los tests
python -m pytest tests/

# Ejecutar test específico
python tests/test_data_loader.py
```

## 📁 Estructura del Proyecto

```
datarush_hackathon/
├── agents/                 # Agentes de IA especializados
├── components/            # Componentes de la aplicación
├── docs/                  # Documentación
├── tests/                 # Archivos de prueba
├── datos/                 # Datos de entrada
├── app.py                 # Aplicación principal
└── requirements.txt       # Dependencias
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 📞 Contacto

Para preguntas o soporte, contacta al equipo de desarrollo.
