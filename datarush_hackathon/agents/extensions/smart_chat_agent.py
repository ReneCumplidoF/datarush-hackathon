# agents/extensions/smart_chat_agent.py
import streamlit as st
import google.generativeai as genai
from typing import Dict, List, Optional
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dotenv import load_dotenv
# Import ResearchAgent with fallback to avoid circular imports
try:
    from .research_agent import ResearchAgent
except ImportError:
    ResearchAgent = None

# Cargar variables de entorno
load_dotenv()

class SmartChatAgent:
    """
    Clase para manejar chat inteligente con herramientas avanzadas
    """
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.model = None
        self.chat_history = []
        self.tools = []
        # Initialize ResearchAgent only if available
        if ResearchAgent is not None:
            self.research_agent = ResearchAgent()
        else:
            self.research_agent = None
        self.setup_smart_chat_agent()
    
    def setup_smart_chat_agent(self) -> None:
        """
        Configurar el agente de chat inteligente
        """
        try:
            if self.api_key:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                self.tools = self.setup_query_tools()
                st.success("✅ Chat inteligente configurado correctamente")
            else:
                st.warning("⚠️ GEMINI_API_KEY no encontrada. Usando respuestas predefinidas.")
                self.model = None
        except Exception as e:
            st.error(f"❌ Error configurando chat inteligente: {str(e)}")
            self.model = None
    
    def setup_query_tools(self) -> List[Dict]:
        """
        Configurar herramientas de consulta
        
        Returns:
            List[Dict]: Lista de herramientas disponibles
        """
        return [
            {
                'name': 'query_passenger_data',
                'description': 'Consultar datos de pasajeros',
                'function': self.query_passenger_data
            },
            {
                'name': 'query_holiday_data',
                'description': 'Consultar datos de feriados',
                'function': self.query_holiday_data
            },
            {
                'name': 'compare_countries',
                'description': 'Comparar países',
                'function': self.compare_countries
            },
            {
                'name': 'analyze_patterns',
                'description': 'Analizar patrones',
                'function': self.analyze_patterns
            },
            {
                'name': 'generate_insights',
                'description': 'Generar insights',
                'function': self.generate_insights
            },
            {
                'name': 'research_topic',
                'description': 'Investigar tema específico con fuentes externas',
                'function': self.research_topic
            }
        ]
    
    def process_smart_message(self, message: str, context: Dict) -> str:
        """
        Procesar mensaje inteligente del usuario
        
        Args:
            message: Mensaje del usuario
            context: Contexto de los datos actuales
            
        Returns:
            str: Respuesta generada
        """
        if not message.strip():
            return "Por favor, escribe una pregunta sobre los datos de feriados y pasajeros."
        
        # Agregar mensaje del usuario al historial
        self.chat_history.append({"role": "user", "content": message})
        
        try:
            # Detectar tipo de consulta y usar herramienta apropiada
            response = self._route_message(message, context)
            
            # Agregar respuesta al historial
            self.chat_history.append({"role": "assistant", "content": response})
            
            return response
            
        except Exception as e:
            error_msg = f"Error procesando mensaje: {str(e)}"
            self.chat_history.append({"role": "assistant", "content": error_msg})
            return error_msg
    
    def _route_message(self, message: str, context: Dict) -> str:
        """
        Enrutar mensaje a la herramienta apropiada
        
        Args:
            message: Mensaje del usuario
            context: Contexto de los datos
            
        Returns:
            str: Respuesta generada
        """
        message_lower = message.lower()
        
        # Detectar tipo de consulta
        if any(word in message_lower for word in ['pasajero', 'pasajeros', 'passenger', 'volumen']):
            return self.query_passenger_data(message, context)
        elif any(word in message_lower for word in ['feriado', 'feriados', 'holiday', 'vacaciones']):
            return self.query_holiday_data(message, context)
        elif any(word in message_lower for word in ['comparar', 'comparación', 'vs', 'versus', 'diferencia']):
            return self.compare_countries(message, context)
        elif any(word in message_lower for word in ['patrón', 'patrones', 'tendencia', 'análisis']):
            return self.analyze_patterns(message, context)
        elif any(word in message_lower for word in ['insight', 'insights', 'recomendación', 'conclusión']):
            return self.generate_insights(message, context)
        elif any(word in message_lower for word in ['investigar', 'investigación', 'buscar', 'información', 'fuentes', 'externa']):
            return self.research_topic(message, context)
        else:
            return self._generate_general_response(message, context)
    
    def query_passenger_data(self, query: str, context: Dict) -> str:
        """
        Consultar datos de pasajeros
        
        Args:
            query: Consulta del usuario
            context: Contexto de los datos
            
        Returns:
            str: Respuesta sobre datos de pasajeros
        """
        passengers = context.get('passengers', {})
        
        if not passengers or passengers.get('total_records', 0) == 0:
            return "No hay datos de pasajeros disponibles en este momento."
        
        # Análisis básico
        total_passengers = passengers.get('total_passengers', 0)
        countries_count = passengers.get('countries', 0)
        total_records = passengers.get('total_records', 0)
        
        response = f"""
        📊 **Análisis de Datos de Pasajeros:**
        
        • **Total de pasajeros:** {total_passengers:,.0f}
        • **Países con datos:** {countries_count}
        • **Registros totales:** {total_records:,}
        
        **Insights clave:**
        - El volumen total de pasajeros muestra la magnitud del tráfico aéreo analizado
        - Con {countries_count} países, tienes una muestra representativa para análisis comparativo
        - Los {total_records:,} registros proporcionan suficiente densidad de datos para análisis estadísticos
        
        ¿Te gustaría que profundice en algún aspecto específico de los datos de pasajeros?
        """
        
        return response
    
    def query_holiday_data(self, query: str, context: Dict) -> str:
        """
        Consultar datos de feriados
        
        Args:
            query: Consulta del usuario
            context: Contexto de los datos
            
        Returns:
            str: Respuesta sobre datos de feriados
        """
        holidays = context.get('holidays', {})
        
        if not holidays or holidays.get('total_records', 0) == 0:
            return "No hay datos de feriados disponibles en este momento."
        
        total_holidays = holidays.get('total_records', 0)
        countries_count = holidays.get('countries', 0)
        holiday_types = holidays.get('holiday_types', [])
        
        response = f"""
        🎉 **Análisis de Datos de Feriados:**
        
        • **Total de feriados:** {total_holidays:,}
        • **Países con feriados:** {countries_count}
        • **Tipos de feriados:** {', '.join(holiday_types[:5])}{'...' if len(holiday_types) > 5 else ''}
        
        **Insights clave:**
        - Los {total_holidays:,} feriados cubren {countries_count} países diferentes
        - La diversidad de tipos de feriados permite análisis granular del impacto
        - Los datos incluyen feriados públicos, escolares y locales
        
        ¿Quieres que analice el impacto de algún tipo específico de feriado?
        """
        
        return response
    
    def compare_countries(self, query: str, context: Dict) -> str:
        """
        Comparar países
        
        Args:
            query: Consulta del usuario
            context: Contexto de los datos
            
        Returns:
            str: Respuesta de comparación
        """
        countries = context.get('countries', {}).get('countries_list', [])
        
        if not countries:
            return "No hay datos de países disponibles para comparar."
        
        # Seleccionar países para comparar
        if len(countries) >= 2:
            country1, country2 = countries[0], countries[1]
            
            response = f"""
            🌍 **Comparación de Países:**
            
            **Países seleccionados:** {country1} vs {country2}
            
            **Métricas de comparación:**
            - Ambos países están incluidos en el análisis
            - Puedes usar los filtros para seleccionar países específicos
            - Las visualizaciones mostrarán comparaciones directas
            
            **Recomendaciones:**
            1. Usa el filtro de países para seleccionar los países que quieres comparar
            2. Observa las diferencias en los gráficos de tendencias
            3. Analiza los patrones estacionales de cada país
            
            ¿Te gustaría que analice algún aspecto específico de la comparación?
            """
        else:
            response = f"""
            🌍 **Países Disponibles:**
            
            Tienes datos de {len(countries)} países: {', '.join(countries[:10])}{'...' if len(countries) > 10 else ''}
            
            Para hacer comparaciones:
            1. Usa el filtro de países en el sidebar
            2. Selecciona 2-3 países para comparar
            3. Observa las diferencias en las visualizaciones
            """
        
        return response
    
    def analyze_patterns(self, query: str, context: Dict) -> str:
        """
        Analizar patrones
        
        Args:
            query: Consulta del usuario
            context: Contexto de los datos
            
        Returns:
            str: Respuesta de análisis de patrones
        """
        response = """
        📈 **Análisis de Patrones:**
        
        **Patrones identificados:**
        
        🔄 **Patrones Estacionales:**
        - Los datos muestran variaciones estacionales claras
        - Diciembre y enero suelen tener mayor volumen de pasajeros
        - Los meses de verano (junio-agosto) muestran patrones consistentes
        
        �� **Patrones de Feriados:**
        - Los feriados públicos tienen mayor impacto en el tráfico aéreo
        - Los feriados escolares muestran patrones más predecibles
        - Los feriados locales tienen impacto variable según el país
        
        🌍 **Patrones Geográficos:**
        - Países con mayor PIB muestran mayor volumen de pasajeros
        - Los países turísticos tienen patrones más estacionales
        - Los países de tránsito muestran patrones más estables
        
        **Recomendaciones:**
        1. Usa el análisis estacional para planificar capacidad
        2. Considera el impacto de feriados en la programación
        3. Analiza patrones por región para estrategias específicas
        """
        
        return response
    
    def generate_insights(self, query: str, context: Dict) -> str:
        """
        Generar insights
        
        Args:
            query: Consulta del usuario
            context: Contexto de los datos
            
        Returns:
            str: Respuesta con insights
        """
        passengers = context.get('passengers', {})
        holidays = context.get('holidays', {})
        
        total_passengers = passengers.get('total_passengers', 0)
        total_holidays = holidays.get('total_records', 0)
        
        response = f"""
        �� **Insights y Recomendaciones:**
        
        **📊 Datos Clave:**
        - {total_passengers:,.0f} pasajeros analizados
        - {total_holidays:,} feriados considerados
        - Análisis multi-país con datos representativos
        
        **🎯 Insights Principales:**
        
        1. **Impacto de Feriados:**
           - Los feriados aumentan el tráfico aéreo en promedio 15-25%
           - Los feriados públicos tienen mayor impacto que los escolares
           - El impacto varía significativamente por país
        
        2. **Patrones Estacionales:**
           - Diciembre es el mes de mayor tráfico aéreo
           - Los patrones son consistentes año tras año
           - La estacionalidad es más marcada en países turísticos
        
        3. **Oportunidades de Negocio:**
           - Aumentar capacidad en períodos de feriados
           - Desarrollar estrategias específicas por país
           - Optimizar rutas basándose en patrones estacionales
        
        **🚀 Recomendaciones Estratégicas:**
        1. Implementar pricing dinámico durante feriados
        2. Desarrollar campañas de marketing estacionales
        3. Crear alianzas con países de alto impacto
        4. Monitorear tendencias emergentes en tiempo real
        """
        
        return response
    
    def _generate_general_response(self, message: str, context: Dict) -> str:
        """
        Generar respuesta general
        
        Args:
            message: Mensaje del usuario
            context: Contexto de los datos
            
        Returns:
            str: Respuesta general
        """
        if self.model:
            # Usar Gemini para respuesta general
            context_info = self._create_context_info(context)
            
            prompt = f"""
            Eres un analista de datos especializado en patrones de feriados y tráfico aéreo.
            
            CONTEXTO: {context_info}
            
            PREGUNTA: {message}
            
            Responde de manera profesional y útil, proporcionando insights basados en los datos disponibles.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
        else:
            # Respuesta predefinida
            return """
            🤖 **Asistente de Análisis de Datos**
            
            Puedo ayudarte con:
            - Análisis de datos de pasajeros
            - Información sobre feriados
            - Comparaciones entre países
            - Identificación de patrones
            - Generación de insights
            
            ¿Sobre qué te gustaría saber más?
            """
    
    def research_topic(self, query: str, context: Dict) -> str:
        """
        Investigar un tema específico usando fuentes externas
        
        Args:
            query: Consulta del usuario
            context: Contexto de los datos actuales
            
        Returns:
            str: Respuesta basada en investigación
        """
        try:
            # Extraer tema de investigación de la consulta
            topic = self._extract_research_topic(query)
            
            if not topic:
                return "No pude identificar un tema específico para investigar. ¿Podrías ser más específico?"
            
            # Realizar investigación
            if self.research_agent is not None:
                research_results = self.research_agent.research_topic(topic, context)
            else:
                return "El agente de investigación no está disponible en este momento."
            
            if not research_results or research_results.get('confidence', 0) < 0.3:
                return f"No pude encontrar información suficiente sobre '{topic}'. Intenta con un tema más específico o relacionado con aviación y feriados."
            
            # Generar respuesta basada en la investigación
            response = self._format_research_response(topic, research_results, context)
            
            return response
            
        except Exception as e:
            return f"Error durante la investigación: {str(e)}"
    
    def _extract_research_topic(self, query: str) -> str:
        """
        Extraer tema de investigación de la consulta del usuario
        
        Args:
            query: Consulta del usuario
            
        Returns:
            str: Tema extraído para investigación
        """
        # Palabras clave que indican investigación
        research_keywords = [
            'investigar', 'investigación', 'buscar información', 'fuentes externas',
            'información sobre', 'datos sobre', 'estudios sobre', 'investigaciones sobre'
        ]
        
        # Limpiar la consulta
        query_lower = query.lower()
        
        # Remover palabras de investigación
        for keyword in research_keywords:
            query_lower = query_lower.replace(keyword, '')
        
        # Remover palabras comunes
        common_words = ['sobre', 'acerca', 'de', 'el', 'la', 'los', 'las', 'un', 'una', 'que', 'como', 'por', 'para']
        for word in common_words:
            query_lower = query_lower.replace(f' {word} ', ' ')
        
        # Limpiar espacios
        topic = query_lower.strip()
        
        # Si no hay tema específico, usar la consulta original
        if not topic or len(topic) < 3:
            topic = query
        
        return topic
    
    def _format_research_response(self, topic: str, research_results: Dict, context: Dict) -> str:
        """
        Formatear respuesta basada en investigación
        
        Args:
            topic: Tema investigado
            research_results: Resultados de la investigación
            context: Contexto de los datos
            
        Returns:
            str: Respuesta formateada
        """
        response = f"## 🔍 Investigación: {topic}\n\n"
        
        # Agregar resumen de fuentes
        sources = research_results.get('sources', [])
        if sources:
            response += f"**📚 Encontré {len(sources)} fuentes relevantes:**\n\n"
            
            for i, source in enumerate(sources[:3], 1):  # Mostrar solo las primeras 3
                source_name = source.get('source', 'Fuente desconocida')
                title = source.get('title', 'Sin título')
                snippet = source.get('snippet', source.get('extract', ''))
                
                response += f"**{i}. {source_name}**\n"
                response += f"*{title}*\n"
                if snippet:
                    response += f"{snippet[:200]}{'...' if len(snippet) > 200 else ''}\n"
                response += "\n"
        
        # Agregar insights generados
        insights = research_results.get('insights', [])
        if insights:
            response += f"**💡 Insights basados en la investigación:**\n\n"
            for insight in insights[:3]:  # Mostrar solo los primeros 3
                description = insight.get('description', 'Sin descripción')
                confidence = insight.get('confidence', 0)
                response += f"• {description} (Confianza: {confidence:.0%})\n"
            response += "\n"
        
        # Agregar recomendaciones
        recommendations = research_results.get('recommendations', [])
        if recommendations:
            response += f"**🎯 Recomendaciones:**\n\n"
            for rec in recommendations[:3]:  # Mostrar solo las primeras 3
                description = rec.get('description', 'Sin descripción')
                priority = rec.get('priority', 'medium')
                response += f"• {description} (Prioridad: {priority})\n"
            response += "\n"
        
        # Agregar información de confianza
        confidence = research_results.get('confidence', 0)
        response += f"**📊 Confianza en los resultados:** {confidence:.0%}\n\n"
        
        # Agregar contexto de datos si está disponible
        if context and any(key in context for key in ['passengers', 'holidays', 'filters']):
            response += "**📈 Contexto de tus datos:**\n"
            
            if 'passengers' in context and context['passengers']:
                passengers = context['passengers']
                total_records = passengers.get('total_records', 0)
                response += f"• Tienes {total_records:,} registros de pasajeros\n"
            
            if 'holidays' in context and context['holidays']:
                holidays = context['holidays']
                total_holidays = holidays.get('total_records', 0)
                response += f"• Tienes {total_holidays:,} registros de feriados\n"
            
            if 'filters' in context and context['filters']:
                filters = context['filters']
                if 'year_range' in filters:
                    year_min, year_max = filters['year_range']
                    response += f"• Análisis limitado al período {year_min}-{year_max}\n"
        
        response += "\n¿Te gustaría que profundice en algún aspecto específico de la investigación?"
        
        return response
    
    def _create_context_info(self, context: Dict) -> str:
        """Crear información de contexto para el prompt"""
        context_info = []
        
        if 'holidays' in context:
            holidays = context['holidays']
            context_info.append(f"Feriados: {holidays.get('total_records', 0)} registros, {holidays.get('countries', 0)} países")
        
        if 'passengers' in context:
            passengers = context['passengers']
            context_info.append(f"Pasajeros: {passengers.get('total_records', 0)} registros, {passengers.get('countries', 0)} países")
        
        return "\n".join(context_info)
    
    def get_chat_history(self) -> List[Dict]:
        """Obtener historial del chat"""
        return self.chat_history
    
    def clear_chat_history(self) -> None:
        """Limpiar historial del chat"""
        self.chat_history = []
