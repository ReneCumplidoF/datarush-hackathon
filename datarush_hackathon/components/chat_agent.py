# components/chat_agent.py
import streamlit as st
import google.generativeai as genai
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class ChatAgent:
    """
    Clase para manejar el chat con IA usando Google Gemini
    """
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.model = None
        self.chat_history = []
        self.setup_gemini_agent()
    
    def setup_gemini_agent(self) -> None:
        """
        Configurar el agente de Gemini
        """
        try:
            if self.api_key:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                st.success("✅ Gemini API configurado correctamente")
            else:
                st.warning("⚠️ GEMINI_API_KEY no encontrada. Usando respuestas predefinidas.")
                self.model = None
        except Exception as e:
            st.error(f"❌ Error configurando Gemini: {str(e)}")
            self.model = None
    
    def process_user_message(self, message: str, context: Dict) -> str:
        """
        Procesar mensaje del usuario y generar respuesta
        
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
            if self.model:
                # Usar Gemini API
                response = self._generate_gemini_response(message, context)
            else:
                # Usar respuestas predefinidas
                response = self._generate_predefined_response(message, context)
            
            # Agregar respuesta al historial
            self.chat_history.append({"role": "assistant", "content": response})
            
            return response
            
        except Exception as e:
            error_msg = f"Error procesando mensaje: {str(e)}"
            self.chat_history.append({"role": "assistant", "content": error_msg})
            return error_msg
    
    def _generate_gemini_response(self, message: str, context: Dict) -> str:
        """
        Generar respuesta usando Gemini API
        
        Args:
            message: Mensaje del usuario
            context: Contexto de los datos
            
        Returns:
            str: Respuesta generada
        """
        # Crear prompt con contexto
        context_info = self._create_context_info(context)
        
        prompt = f"""
        Eres un analista de datos especializado en patrones de feriados y tráfico aéreo.
        
        CONTEXTO DE LOS DATOS:
        {context_info}
        
        PREGUNTA DEL USUARIO: {message}
        
        INSTRUCCIONES:
        1. Responde de manera clara y profesional
        2. Usa los datos del contexto para dar respuestas específicas
        3. Si no tienes información suficiente, indícalo claramente
        4. Incluye insights y recomendaciones cuando sea apropiado
        5. Responde en español
        
        RESPUESTA:
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def _generate_predefined_response(self, message: str, context: Dict) -> str:
        """
        Generar respuesta predefinida cuando Gemini no está disponible
        
        Args:
            message: Mensaje del usuario
            context: Contexto de los datos
            
        Returns:
            str: Respuesta predefinida
        """
        message_lower = message.lower()
        
        # Respuestas predefinidas basadas en palabras clave
        if any(word in message_lower for word in ['país', 'países', 'country']):
            countries = context.get('countries', [])
            if countries:
                return f"Actualmente tienes datos de {len(countries)} países. Los países con más datos son: {', '.join(countries[:5])}."
            else:
                return "No hay información de países disponible en este momento."
        
        elif any(word in message_lower for word in ['feriado', 'feriados', 'holiday']):
            holidays = context.get('holidays', {})
            if holidays:
                return f"Tienes {holidays.get('total_records', 0)} registros de feriados. Los tipos más comunes son: {', '.join(holidays.get('holiday_types', [])[:3])}."
            else:
                return "No hay información de feriados disponible en este momento."
        
        elif any(word in message_lower for word in ['pasajero', 'pasajeros', 'passenger']):
            passengers = context.get('passengers', {})
            if passengers:
                return f"Tienes {passengers.get('total_records', 0)} registros de pasajeros. El total de pasajeros es: {passengers.get('total_passengers', 0):,.0f}."
            else:
                return "No hay información de pasajeros disponible en este momento."
        
        elif any(word in message_lower for word in ['tendencia', 'tendencias', 'trend']):
            return "Para analizar tendencias, puedes usar el gráfico de líneas en la sección de visualizaciones. Muestra la evolución del tráfico aéreo a lo largo del tiempo."
        
        elif any(word in message_lower for word in ['patrón', 'patrones', 'pattern']):
            return "Los patrones estacionales se pueden observar en el mapa de calor. Muestra cómo varía el tráfico aéreo por país y mes."
        
        elif any(word in message_lower for word in ['ayuda', 'help', 'comando']):
            return """
            Puedo ayudarte con:
            - Información sobre países y datos disponibles
            - Análisis de feriados y su impacto
            - Tendencias de pasajeros aéreos
            - Patrones estacionales
            - Interpretación de visualizaciones
            
            ¿Sobre qué te gustaría saber más?
            """
        
        else:
            return "Interesante pregunta. Para obtener información más específica, puedes usar los filtros en el sidebar para explorar los datos o preguntarme sobre países, feriados, pasajeros o tendencias."
    
    def _create_context_info(self, context: Dict) -> str:
        """
        Crear información de contexto para el prompt
        
        Args:
            context: Contexto de los datos
            
        Returns:
            str: Información de contexto formateada
        """
        context_info = []
        
        # Información de feriados
        if 'holidays' in context:
            holidays = context['holidays']
            context_info.append(f"Feriados: {holidays.get('total_records', 0)} registros, {holidays.get('countries', 0)} países")
            if 'holiday_types' in holidays:
                context_info.append(f"Tipos de feriados: {', '.join(holidays['holiday_types'][:5])}")
        
        # Información de pasajeros
        if 'passengers' in context:
            passengers = context['passengers']
            context_info.append(f"Pasajeros: {passengers.get('total_records', 0)} registros, {passengers.get('countries', 0)} países")
            context_info.append(f"Total pasajeros: {passengers.get('total_passengers', 0):,.0f}")
        
        # Información de países
        if 'countries' in context:
            countries = context['countries']
            context_info.append(f"Países disponibles: {len(countries.get('countries_list', []))}")
        
        return "\n".join(context_info)
    
    def get_chat_history(self) -> List[Dict]:
        """
        Obtener historial del chat
        
        Returns:
            List[Dict]: Historial del chat
        """
        return self.chat_history
    
    def clear_chat_history(self) -> None:
        """
        Limpiar historial del chat
        """
        self.chat_history = []
    
    def format_response(self, response: str) -> str:
        """
        Formatear respuesta para mostrar en Streamlit
        
        Args:
            response: Respuesta a formatear
            
        Returns:
            str: Respuesta formateada
        """
        # Formatear markdown básico
        formatted = response.replace('\n', '\n\n')
        return formatted
