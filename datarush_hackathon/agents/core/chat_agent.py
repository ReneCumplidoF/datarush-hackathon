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
        
        # Obtener datos del contexto
        data = context.get('data', {}) or context.get('filtered_data', {})
        
        # Respuestas predefinidas basadas en palabras clave
        if any(word in message_lower for word in ['país', 'países', 'country']):
            if 'countries' in data and hasattr(data['countries'], 'shape'):
                countries_df = data['countries']
                countries_count = countries_df.shape[0]
                if 'Country' in countries_df.columns:
                    countries_list = countries_df['Country'].head(5).tolist()
                    return f"Actualmente tienes datos de {countries_count} países. Algunos países disponibles son: {', '.join(countries_list)}."
                else:
                    return f"Tienes datos de {countries_count} países disponibles."
            else:
                return "No hay información de países disponible en este momento."
        
        elif any(word in message_lower for word in ['feriado', 'feriados', 'holiday']):
            if 'holidays' in data and hasattr(data['holidays'], 'shape'):
                holidays_df = data['holidays']
                records_count = holidays_df.shape[0]
                if 'Holiday_Type' in holidays_df.columns:
                    holiday_types = holidays_df['Holiday_Type'].value_counts().head(3)
                    return f"Tienes {records_count} registros de feriados. Los tipos más comunes son: {', '.join(holiday_types.index.tolist())}."
                else:
                    return f"Tienes {records_count} registros de feriados disponibles."
            else:
                return "No hay información de feriados disponible en este momento."
        
        elif any(word in message_lower for word in ['pasajero', 'pasajeros', 'passenger']):
            if 'passengers' in data and hasattr(data['passengers'], 'shape'):
                passengers_df = data['passengers']
                records_count = passengers_df.shape[0]
                if 'Total' in passengers_df.columns:
                    total_passengers = passengers_df['Total'].sum()
                    return f"Tienes {records_count} registros de pasajeros. El total de pasajeros es: {total_passengers:,.0f}."
                else:
                    return f"Tienes {records_count} registros de pasajeros disponibles."
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
        
        # Verificar si hay datos cargados
        if not context.get('data_loaded', False):
            return "No hay datos cargados en el sistema. Por favor, carga los datos primero usando el botón 'Cargar Datos'."
        
        # Obtener datos filtrados
        data = context.get('data', {}) or context.get('filtered_data', {})
        
        if not data:
            return "Los datos están cargados pero no están disponibles en el contexto actual."
        
        # Información de feriados
        if 'holidays' in data and hasattr(data['holidays'], 'shape'):
            holidays_df = data['holidays']
            context_info.append(f"📅 Feriados: {holidays_df.shape[0]} registros con {holidays_df.shape[1]} columnas")
            if 'Country' in holidays_df.columns:
                countries_count = holidays_df['Country'].nunique()
                context_info.append(f"   - Países con feriados: {countries_count}")
            if 'Holiday_Type' in holidays_df.columns:
                holiday_types = holidays_df['Holiday_Type'].value_counts().head(3)
                context_info.append(f"   - Tipos más comunes: {', '.join(holiday_types.index.tolist())}")
        
        # Información de pasajeros
        if 'passengers' in data and hasattr(data['passengers'], 'shape'):
            passengers_df = data['passengers']
            context_info.append(f"✈️ Pasajeros: {passengers_df.shape[0]} registros con {passengers_df.shape[1]} columnas")
            if 'Total' in passengers_df.columns:
                total_passengers = passengers_df['Total'].sum()
                context_info.append(f"   - Total de pasajeros: {total_passengers:,.0f}")
            if 'Country' in passengers_df.columns:
                countries_count = passengers_df['Country'].nunique()
                context_info.append(f"   - Países con datos de pasajeros: {countries_count}")
        
        # Información de países
        if 'countries' in data and hasattr(data['countries'], 'shape'):
            countries_df = data['countries']
            context_info.append(f"🌍 Países: {countries_df.shape[0]} países disponibles")
            if 'Country' in countries_df.columns:
                context_info.append(f"   - Nombres de países: {', '.join(countries_df['Country'].head(5).tolist())}...")
        
        # Información de filtros
        current_filters = context.get('current_filters', {})
        if current_filters:
            context_info.append(f"🔧 Filtros aplicados: {len(current_filters)} filtros activos")
            if 'year_range' in current_filters:
                year_min, year_max = current_filters['year_range']
                context_info.append(f"   - Rango de años: {year_min}-{year_max}")
            if 'countries' in current_filters and current_filters['countries']:
                context_info.append(f"   - Países filtrados: {len(current_filters['countries'])} países")
        
        return "\n".join(context_info) if context_info else "Los datos están cargados pero no se pudo extraer información específica."
    
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
