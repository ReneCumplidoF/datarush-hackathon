"""
Research Agent Module
====================

Agente de investigación que puede buscar información externa cuando no tiene
respuestas específicas sobre los datos del sistema DataRush.

Capacidades:
- Búsqueda web inteligente
- Análisis de contexto de datos
- Generación de insights basados en investigación
- Integración con múltiples fuentes de información
"""

import streamlit as st
import requests
import json
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
import time
import re
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class ResearchAgent:
    """
    Agente de investigación para buscar información externa y generar insights
    """
    
    def __init__(self):
        self.api_keys = {
            'google': os.getenv('GOOGLE_SEARCH_API_KEY'),
            'bing': os.getenv('BING_SEARCH_API_KEY'),
            'wikipedia': None,  # Wikipedia no requiere API key
            'news': os.getenv('NEWS_API_KEY')
        }
        
        self.search_engines = ['wikipedia', 'google', 'bing', 'news']
        self.research_cache = {}
        self.max_cache_age = 3600  # 1 hora en segundos
        
    def research_topic(self, topic: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Investigar un tema específico relacionado con los datos
        
        Args:
            topic: Tema a investigar
            context: Contexto de los datos actuales
            
        Returns:
            Dict: Resultados de la investigación
        """
        # Verificar cache primero
        cache_key = f"{topic}_{hash(str(context))}"
        if self._is_cached(cache_key):
            return self.research_cache[cache_key]
        
        st.info(f"🔍 Investigando: {topic}")
        
        research_results = {
            'topic': topic,
            'timestamp': datetime.now().isoformat(),
            'sources': [],
            'insights': [],
            'recommendations': [],
            'confidence': 0.0
        }
        
        try:
            # 1. Búsqueda en Wikipedia para contexto general
            wikipedia_info = self._search_wikipedia(topic)
            if wikipedia_info:
                research_results['sources'].append(wikipedia_info)
            
            # 2. Búsqueda web para información actual
            web_results = self._search_web(topic, context)
            if web_results:
                research_results['sources'].extend(web_results)
            
            # 3. Búsqueda de noticias para información reciente
            news_results = self._search_news(topic)
            if news_results:
                research_results['sources'].extend(news_results)
            
            # 4. Analizar contexto de datos si está disponible
            if context:
                data_insights = self._analyze_data_context(topic, context)
                if data_insights:
                    research_results['insights'].extend(data_insights)
            
            # 5. Generar insights basados en la investigación
            insights = self._generate_insights(topic, research_results['sources'])
            research_results['insights'].extend(insights)
            
            # 6. Generar recomendaciones
            recommendations = self._generate_recommendations(topic, research_results)
            research_results['recommendations'].extend(recommendations)
            
            # 7. Calcular confianza en los resultados
            research_results['confidence'] = self._calculate_confidence(research_results)
            
            # Guardar en cache
            self.research_cache[cache_key] = research_results
            
            return research_results
            
        except Exception as e:
            st.error(f"❌ Error en investigación: {str(e)}")
            return research_results
    
    def _search_wikipedia(self, topic: str) -> Optional[Dict[str, Any]]:
        """
        Buscar información en Wikipedia
        
        Args:
            topic: Tema a buscar
            
        Returns:
            Dict: Información de Wikipedia
        """
        try:
            # Buscar página de Wikipedia
            search_url = "https://es.wikipedia.org/api/rest_v1/page/summary/" + topic.replace(" ", "_")
            response = requests.get(search_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'source': 'Wikipedia',
                    'title': data.get('title', ''),
                    'extract': data.get('extract', ''),
                    'url': data.get('content_urls', {}).get('desktop', {}).get('page', ''),
                    'relevance_score': self._calculate_relevance_score(topic, data.get('extract', ''))
                }
        except Exception as e:
            st.warning(f"⚠️ Error buscando en Wikipedia: {str(e)}")
        
        return None
    
    def _search_web(self, topic: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Buscar información en la web usando Google Custom Search
        
        Args:
            topic: Tema a buscar
            context: Contexto de los datos
            
        Returns:
            List[Dict]: Resultados de búsqueda web
        """
        results = []
        
        if not self.api_keys['google']:
            st.warning("⚠️ Google Search API key no configurada")
            return results
        
        try:
            # Construir query de búsqueda
            query = self._build_search_query(topic, context)
            
            # Buscar en Google
            search_url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'key': self.api_keys['google'],
                'cx': os.getenv('GOOGLE_SEARCH_ENGINE_ID', ''),
                'q': query,
                'num': 5,
                'lr': 'lang_es'  # Búsqueda en español
            }
            
            response = requests.get(search_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                for item in data.get('items', []):
                    results.append({
                        'source': 'Google Search',
                        'title': item.get('title', ''),
                        'snippet': item.get('snippet', ''),
                        'url': item.get('link', ''),
                        'relevance_score': self._calculate_relevance_score(topic, item.get('snippet', ''))
                    })
        
        except Exception as e:
            st.warning(f"⚠️ Error en búsqueda web: {str(e)}")
        
        return results
    
    def _search_news(self, topic: str) -> List[Dict[str, Any]]:
        """
        Buscar noticias recientes sobre el tema
        
        Args:
            topic: Tema a buscar
            
        Returns:
            List[Dict]: Resultados de noticias
        """
        results = []
        
        if not self.api_keys['news']:
            return results
        
        try:
            # Buscar noticias de los últimos 30 días
            from_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            
            news_url = "https://newsapi.org/v2/everything"
            params = {
                'apiKey': self.api_keys['news'],
                'q': topic,
                'from': from_date,
                'language': 'es',
                'sortBy': 'relevancy',
                'pageSize': 5
            }
            
            response = requests.get(news_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                for article in data.get('articles', []):
                    results.append({
                        'source': 'News API',
                        'title': article.get('title', ''),
                        'description': article.get('description', ''),
                        'url': article.get('url', ''),
                        'published_at': article.get('publishedAt', ''),
                        'relevance_score': self._calculate_relevance_score(topic, article.get('description', ''))
                    })
        
        except Exception as e:
            st.warning(f"⚠️ Error buscando noticias: {str(e)}")
        
        return results
    
    def _analyze_data_context(self, topic: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analizar el contexto de los datos para generar insights
        
        Args:
            topic: Tema a analizar
            context: Contexto de los datos
            
        Returns:
            List[Dict]: Insights basados en datos
        """
        insights = []
        
        try:
            # Analizar datos de pasajeros
            if 'passengers' in context and context['passengers']:
                passenger_insights = self._analyze_passenger_context(topic, context['passengers'])
                insights.extend(passenger_insights)
            
            # Analizar datos de feriados
            if 'holidays' in context and context['holidays']:
                holiday_insights = self._analyze_holiday_context(topic, context['holidays'])
                insights.extend(holiday_insights)
            
            # Analizar filtros aplicados
            if 'filters' in context and context['filters']:
                filter_insights = self._analyze_filter_context(topic, context['filters'])
                insights.extend(filter_insights)
        
        except Exception as e:
            st.warning(f"⚠️ Error analizando contexto: {str(e)}")
        
        return insights
    
    def _analyze_passenger_context(self, topic: str, passenger_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analizar contexto de datos de pasajeros
        
        Args:
            topic: Tema a analizar
            passenger_data: Datos de pasajeros
            
        Returns:
            List[Dict]: Insights de pasajeros
        """
        insights = []
        
        try:
            # Extraer palabras clave del tema
            topic_keywords = self._extract_keywords(topic)
            
            # Analizar patrones estacionales
            if any(keyword in topic_keywords for keyword in ['estacional', 'temporada', 'mes', 'año']):
                insights.append({
                    'type': 'seasonal_analysis',
                    'description': 'Análisis de patrones estacionales en datos de pasajeros',
                    'confidence': 0.8,
                    'data_points': passenger_data.get('total_records', 0)
                })
            
            # Analizar crecimiento
            if any(keyword in topic_keywords for keyword in ['crecimiento', 'tendencia', 'evolución']):
                insights.append({
                    'type': 'growth_analysis',
                    'description': 'Análisis de tendencias de crecimiento en tráfico aéreo',
                    'confidence': 0.7,
                    'data_points': passenger_data.get('total_records', 0)
                })
            
            # Analizar impacto de feriados
            if any(keyword in topic_keywords for keyword in ['feriado', 'vacaciones', 'impacto']):
                insights.append({
                    'type': 'holiday_impact',
                    'description': 'Análisis del impacto de feriados en el tráfico aéreo',
                    'confidence': 0.9,
                    'data_points': passenger_data.get('total_records', 0)
                })
        
        except Exception as e:
            st.warning(f"⚠️ Error analizando contexto de pasajeros: {str(e)}")
        
        return insights
    
    def _analyze_holiday_context(self, topic: str, holiday_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analizar contexto de datos de feriados
        
        Args:
            topic: Tema a analizar
            holiday_data: Datos de feriados
            
        Returns:
            List[Dict]: Insights de feriados
        """
        insights = []
        
        try:
            topic_keywords = self._extract_keywords(topic)
            
            # Analizar tipos de feriados
            if any(keyword in topic_keywords for keyword in ['tipo', 'categoría', 'público', 'religioso']):
                insights.append({
                    'type': 'holiday_type_analysis',
                    'description': 'Análisis de tipos y categorías de feriados',
                    'confidence': 0.8,
                    'data_points': holiday_data.get('total_records', 0)
                })
            
            # Analizar distribución geográfica
            if any(keyword in topic_keywords for keyword in ['país', 'región', 'geográfico']):
                insights.append({
                    'type': 'geographic_analysis',
                    'description': 'Análisis de distribución geográfica de feriados',
                    'confidence': 0.7,
                    'data_points': holiday_data.get('countries', 0)
                })
        
        except Exception as e:
            st.warning(f"⚠️ Error analizando contexto de feriados: {str(e)}")
        
        return insights
    
    def _analyze_filter_context(self, topic: str, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analizar contexto de filtros aplicados
        
        Args:
            topic: Tema a analizar
            filters: Filtros aplicados
            
        Returns:
            List[Dict]: Insights de filtros
        """
        insights = []
        
        try:
            # Analizar filtros temporales
            if 'year_range' in filters:
                year_min, year_max = filters['year_range']
                insights.append({
                    'type': 'temporal_filter',
                    'description': f'Análisis limitado al período {year_min}-{year_max}',
                    'confidence': 0.9,
                    'data_points': f"{year_max - year_min + 1} años"
                })
            
            # Analizar filtros geográficos
            if 'countries' in filters and filters['countries']:
                country_count = len(filters['countries'])
                insights.append({
                    'type': 'geographic_filter',
                    'description': f'Análisis limitado a {country_count} países específicos',
                    'confidence': 0.9,
                    'data_points': country_count
                })
        
        except Exception as e:
            st.warning(f"⚠️ Error analizando contexto de filtros: {str(e)}")
        
        return insights
    
    def _generate_insights(self, topic: str, sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generar insights basados en la investigación
        
        Args:
            topic: Tema investigado
            sources: Fuentes de información
            
        Returns:
            List[Dict]: Insights generados
        """
        insights = []
        
        try:
            # Combinar información de todas las fuentes
            combined_text = ""
            for source in sources:
                combined_text += f"{source.get('title', '')} {source.get('snippet', '')} {source.get('extract', '')} "
            
            # Generar insights basados en el contenido
            if 'patrón' in topic.lower() or 'tendencia' in topic.lower():
                insights.append({
                    'type': 'pattern_insight',
                    'description': 'Identificación de patrones en datos de tráfico aéreo',
                    'confidence': 0.8,
                    'source': 'research_analysis'
                })
            
            if 'feriado' in topic.lower() or 'vacaciones' in topic.lower():
                insights.append({
                    'type': 'holiday_insight',
                    'description': 'Impacto de feriados en el comportamiento de viajes',
                    'confidence': 0.9,
                    'source': 'research_analysis'
                })
            
            if 'crecimiento' in topic.lower() or 'evolución' in topic.lower():
                insights.append({
                    'type': 'growth_insight',
                    'description': 'Tendencias de crecimiento en el sector aéreo',
                    'confidence': 0.7,
                    'source': 'research_analysis'
                })
        
        except Exception as e:
            st.warning(f"⚠️ Error generando insights: {str(e)}")
        
        return insights
    
    def _generate_recommendations(self, topic: str, research_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generar recomendaciones basadas en la investigación
        
        Args:
            topic: Tema investigado
            research_results: Resultados de la investigación
            
        Returns:
            List[Dict]: Recomendaciones generadas
        """
        recommendations = []
        
        try:
            # Recomendaciones basadas en el tema
            if 'análisis' in topic.lower():
                recommendations.append({
                    'type': 'analysis_recommendation',
                    'description': 'Considerar aplicar filtros específicos para un análisis más detallado',
                    'priority': 'medium'
                })
            
            if 'predicción' in topic.lower() or 'pronóstico' in topic.lower():
                recommendations.append({
                    'type': 'prediction_recommendation',
                    'description': 'Usar datos históricos para generar proyecciones futuras',
                    'priority': 'high'
                })
            
            if 'comparación' in topic.lower():
                recommendations.append({
                    'type': 'comparison_recommendation',
                    'description': 'Comparar diferentes países o períodos para identificar diferencias',
                    'priority': 'medium'
                })
            
            # Recomendaciones basadas en la confianza
            if research_results['confidence'] < 0.5:
                recommendations.append({
                    'type': 'data_quality_recommendation',
                    'description': 'Considerar validar los datos con fuentes adicionales',
                    'priority': 'high'
                })
        
        except Exception as e:
            st.warning(f"⚠️ Error generando recomendaciones: {str(e)}")
        
        return recommendations
    
    def _build_search_query(self, topic: str, context: Dict[str, Any] = None) -> str:
        """
        Construir query de búsqueda optimizada
        
        Args:
            topic: Tema a buscar
            context: Contexto de los datos
            
        Returns:
            str: Query de búsqueda optimizada
        """
        query = topic
        
        # Agregar términos relacionados con aviación si no están presentes
        aviation_terms = ['aviación', 'aéreo', 'aerolíneas', 'pasajeros', 'tráfico aéreo']
        if not any(term in topic.lower() for term in aviation_terms):
            query += " aviación tráfico aéreo"
        
        # Agregar contexto temporal si está disponible
        if context and 'filters' in context:
            filters = context['filters']
            if 'year_range' in filters:
                year_min, year_max = filters['year_range']
                query += f" {year_min}-{year_max}"
        
        return query
    
    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extraer palabras clave de un texto
        
        Args:
            text: Texto a procesar
            
        Returns:
            List[str]: Palabras clave extraídas
        """
        # Palabras clave relevantes para el análisis de datos
        keywords = []
        
        # Términos temporales
        temporal_terms = ['estacional', 'temporada', 'mes', 'año', 'crecimiento', 'tendencia', 'evolución']
        for term in temporal_terms:
            if term in text.lower():
                keywords.append(term)
        
        # Términos de análisis
        analysis_terms = ['patrón', 'análisis', 'comparación', 'predicción', 'pronóstico']
        for term in analysis_terms:
            if term in text.lower():
                keywords.append(term)
        
        # Términos de feriados
        holiday_terms = ['feriado', 'vacaciones', 'impacto', 'público', 'religioso']
        for term in holiday_terms:
            if term in text.lower():
                keywords.append(term)
        
        return keywords
    
    def _calculate_relevance_score(self, topic: str, content: str) -> float:
        """
        Calcular score de relevancia entre un tema y contenido
        
        Args:
            topic: Tema de búsqueda
            content: Contenido a evaluar
            
        Returns:
            float: Score de relevancia (0-1)
        """
        if not content:
            return 0.0
        
        topic_words = set(topic.lower().split())
        content_words = set(content.lower().split())
        
        # Calcular intersección de palabras
        common_words = topic_words.intersection(content_words)
        
        if not topic_words:
            return 0.0
        
        # Score basado en la proporción de palabras comunes
        relevance_score = len(common_words) / len(topic_words)
        
        # Bonus por palabras clave importantes
        important_words = ['aviación', 'aéreo', 'pasajeros', 'feriado', 'tráfico']
        for word in important_words:
            if word in content.lower():
                relevance_score += 0.1
        
        return min(relevance_score, 1.0)
    
    def _calculate_confidence(self, research_results: Dict[str, Any]) -> float:
        """
        Calcular confianza en los resultados de investigación
        
        Args:
            research_results: Resultados de la investigación
            
        Returns:
            float: Score de confianza (0-1)
        """
        confidence = 0.0
        
        # Confianza basada en número de fuentes
        source_count = len(research_results.get('sources', []))
        if source_count > 0:
            confidence += min(source_count * 0.2, 0.6)
        
        # Confianza basada en relevancia de fuentes
        sources = research_results.get('sources', [])
        if sources:
            avg_relevance = sum(source.get('relevance_score', 0) for source in sources) / len(sources)
            confidence += avg_relevance * 0.3
        
        # Confianza basada en insights generados
        insights_count = len(research_results.get('insights', []))
        if insights_count > 0:
            confidence += min(insights_count * 0.1, 0.2)
        
        return min(confidence, 1.0)
    
    def _is_cached(self, cache_key: str) -> bool:
        """
        Verificar si un resultado está en cache
        
        Args:
            cache_key: Clave del cache
            
        Returns:
            bool: True si está en cache y es válido
        """
        if cache_key not in self.research_cache:
            return False
        
        cached_result = self.research_cache[cache_key]
        timestamp = datetime.fromisoformat(cached_result['timestamp'])
        
        # Verificar si el cache no ha expirado
        return (datetime.now() - timestamp).seconds < self.max_cache_age
    
    def get_research_summary(self, research_results: Dict[str, Any]) -> str:
        """
        Generar resumen de la investigación
        
        Args:
            research_results: Resultados de la investigación
            
        Returns:
            str: Resumen formateado
        """
        if not research_results:
            return "No hay resultados de investigación disponibles."
        
        summary = f"## 🔍 Investigación: {research_results['topic']}\n\n"
        
        # Resumen de fuentes
        sources = research_results.get('sources', [])
        if sources:
            summary += f"**📚 Fuentes encontradas:** {len(sources)}\n"
            for source in sources[:3]:  # Mostrar solo las primeras 3
                summary += f"- {source.get('source', 'Fuente desconocida')}: {source.get('title', 'Sin título')}\n"
            summary += "\n"
        
        # Resumen de insights
        insights = research_results.get('insights', [])
        if insights:
            summary += f"**💡 Insights generados:** {len(insights)}\n"
            for insight in insights[:3]:  # Mostrar solo los primeros 3
                summary += f"- {insight.get('description', 'Sin descripción')}\n"
            summary += "\n"
        
        # Resumen de recomendaciones
        recommendations = research_results.get('recommendations', [])
        if recommendations:
            summary += f"**🎯 Recomendaciones:** {len(recommendations)}\n"
            for rec in recommendations[:3]:  # Mostrar solo las primeras 3
                summary += f"- {rec.get('description', 'Sin descripción')}\n"
            summary += "\n"
        
        # Confianza
        confidence = research_results.get('confidence', 0)
        summary += f"**📊 Confianza:** {confidence:.1%}\n"
        
        return summary

