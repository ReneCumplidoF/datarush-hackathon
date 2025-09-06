#!/usr/bin/env python3
"""
Business Advisor Agent

This agent provides business recommendations based on air traffic patterns and holidays.
It analyzes data to give specific advice for different business sectors.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import streamlit as st


class BusinessAdvisorAgent:
    """
    Agent specialized in providing business recommendations based on air traffic and holiday data.
    """
    
    def __init__(self):
        """Initialize the Business Advisor Agent."""
        self.business_sectors = {
            'turismo': {
                'name': 'Turismo y Hospitalidad',
                'keywords': ['turismo', 'hotel', 'hospedaje', 'viaje', 'vacaciones', 'turista'],
                'description': 'Negocios relacionados con turismo, hoteles, restaurantes y servicios de viaje'
            },
            'retail': {
                'name': 'Retail y Comercio',
                'keywords': ['retail', 'tienda', 'comercio', 'venta', 'productos', 'shopping'],
                'description': 'Negocios de venta al por menor, tiendas y comercio'
            },
            'restaurantes': {
                'name': 'Restaurantes y Gastronomía',
                'keywords': ['restaurante', 'comida', 'gastronomía', 'cocina', 'bar', 'café'],
                'description': 'Negocios de alimentación y bebidas'
            },
            'transporte': {
                'name': 'Transporte y Logística',
                'keywords': ['transporte', 'taxi', 'uber', 'logística', 'delivery', 'envío'],
                'description': 'Servicios de transporte y logística'
            },
            'entretenimiento': {
                'name': 'Entretenimiento y Ocio',
                'keywords': ['entretenimiento', 'cine', 'teatro', 'museo', 'parque', 'diversión'],
                'description': 'Negocios de entretenimiento, cultura y ocio'
            },
            'servicios': {
                'name': 'Servicios Profesionales',
                'keywords': ['servicio', 'consultoría', 'profesional', 'asesoría', 'clínica', 'oficina'],
                'description': 'Servicios profesionales y de consultoría'
            },
            'eventos': {
                'name': 'Eventos y Celebraciones',
                'keywords': ['evento', 'fiesta', 'boda', 'conferencia', 'celebración', 'festival'],
                'description': 'Negocios de eventos, celebraciones y conferencias'
            }
        }
        
        self.recommendation_templates = {
            'high_traffic': {
                'turismo': "Con el alto tráfico aéreo esperado, es recomendable aumentar la capacidad de atención y preparar promociones especiales para turistas.",
                'retail': "El aumento de pasajeros representa una oportunidad para incrementar el inventario y ofrecer productos dirigidos a viajeros.",
                'restaurantes': "Prepare menús especiales y considere ampliar horarios de atención para aprovechar el mayor flujo de personas.",
                'transporte': "Aumente la flota de vehículos y considere tarifas dinámicas para maximizar ingresos durante picos de demanda.",
                'entretenimiento': "Organice eventos especiales y promociones para atraer a los visitantes adicionales.",
                'servicios': "Ajuste horarios de atención y considere servicios express para viajeros con tiempo limitado.",
                'eventos': "Planifique eventos temáticos relacionados con la temporada de mayor tráfico."
            },
            'low_traffic': {
                'turismo': "Durante períodos de menor tráfico, enfoque en turismo local y ofrezca paquetes promocionales.",
                'retail': "Implemente estrategias de retención de clientes locales y promociones de temporada baja.",
                'restaurantes': "Desarrolle menús estacionales y promociones para atraer clientes locales.",
                'transporte': "Optimice rutas y considere servicios especializados para clientes locales.",
                'entretenimiento': "Organice eventos comunitarios y programas de fidelización para residentes locales.",
                'servicios': "Enfoque en servicios de mantenimiento y desarrollo de relaciones con clientes existentes.",
                'eventos': "Planifique eventos corporativos y celebraciones locales durante la temporada baja."
            },
            'holiday_impact': {
                'turismo': "Los feriados son oportunidades perfectas para paquetes turísticos especiales y eventos temáticos.",
                'retail': "Prepare promociones especiales para feriados y considere productos estacionales.",
                'restaurantes': "Desarrolle menús festivos y ofrezca experiencias culinarias temáticas.",
                'transporte': "Ajuste horarios y tarifas para acomodar el aumento de viajes durante feriados.",
                'entretenimiento': "Organice eventos especiales y actividades temáticas para feriados.",
                'servicios': "Ajuste horarios de atención y ofrezca servicios especiales para feriados.",
                'eventos': "Los feriados son ideales para eventos corporativos y celebraciones especiales."
            }
        }
    
    def analyze_business_query(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a business query and provide recommendations.
        
        Args:
            query: User query about business recommendations
            context: Data context from DataRush system
            
        Returns:
            Dictionary containing business analysis and recommendations
        """
        try:
            # Extract business sector from query
            business_sector = self._identify_business_sector(query)
            
            if not business_sector:
                return {
                    "error": True,
                    "message": "No se pudo identificar el giro del negocio. Por favor, mencione el tipo de negocio (turismo, retail, restaurantes, etc.)",
                    "analysis_type": "business_analysis_error"
                }
            
            # Analyze traffic patterns
            traffic_analysis = self._analyze_traffic_patterns(context)
            
            # Analyze holiday impact
            holiday_analysis = self._analyze_holiday_impact(context)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                business_sector, traffic_analysis, holiday_analysis, context
            )
            
            return {
                "analysis_type": "business_analysis",
                "business_sector": business_sector,
                "traffic_analysis": traffic_analysis,
                "holiday_analysis": holiday_analysis,
                "recommendations": recommendations,
                "success": True
            }
            
        except Exception as e:
            return {
                "error": True,
                "message": f"Error en análisis de negocios: {str(e)}",
                "analysis_type": "business_analysis_error"
            }
    
    def _identify_business_sector(self, query: str) -> Optional[str]:
        """
        Identify the business sector from the query.
        
        Args:
            query: User query
            
        Returns:
            Business sector key or None if not identified
        """
        query_lower = query.lower()
        
        for sector_key, sector_info in self.business_sectors.items():
            for keyword in sector_info['keywords']:
                if keyword in query_lower:
                    return sector_key
        
        return None
    
    def _analyze_traffic_patterns(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze traffic patterns from the data.
        
        Args:
            context: Data context
            
        Returns:
            Dictionary with traffic analysis
        """
        try:
            data = context.get('data', {})
            passengers_df = data.get('passengers')
            
            if passengers_df is None or passengers_df.empty:
                return {
                    "status": "no_data",
                    "message": "No hay datos de tráfico disponibles"
                }
            
            # Calculate traffic metrics
            total_passengers = passengers_df['Total'].sum()
            avg_monthly = passengers_df.groupby('Month')['Total'].mean().mean()
            
            # Find peak and low months
            monthly_traffic = passengers_df.groupby('Month')['Total'].sum()
            peak_month = monthly_traffic.idxmax()
            low_month = monthly_traffic.idxmin()
            
            # Calculate growth rate
            yearly_traffic = passengers_df.groupby('Year')['Total'].sum()
            if len(yearly_traffic) > 1:
                growth_rate = (yearly_traffic.iloc[-1] - yearly_traffic.iloc[0]) / yearly_traffic.iloc[0]
            else:
                growth_rate = 0
            
            # Determine traffic level
            if avg_monthly > 10000:
                traffic_level = "high"
            elif avg_monthly > 5000:
                traffic_level = "medium"
            else:
                traffic_level = "low"
            
            return {
                "status": "success",
                "total_passengers": total_passengers,
                "avg_monthly": avg_monthly,
                "peak_month": peak_month,
                "low_month": low_month,
                "growth_rate": growth_rate,
                "traffic_level": traffic_level,
                "monthly_distribution": monthly_traffic.to_dict()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error analizando patrones de tráfico: {str(e)}"
            }
    
    def _analyze_holiday_impact(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze holiday impact on traffic.
        
        Args:
            context: Data context
            
        Returns:
            Dictionary with holiday analysis
        """
        try:
            data = context.get('data', {})
            holidays_df = data.get('holidays')
            passengers_df = data.get('passengers')
            
            if holidays_df is None or holidays_df.empty:
                return {
                    "status": "no_data",
                    "message": "No hay datos de feriados disponibles"
                }
            
            # Count holidays by month
            holidays_df['Month'] = pd.to_datetime(holidays_df['Date']).dt.month
            monthly_holidays = holidays_df.groupby('Month').size()
            
            # Find months with most holidays
            peak_holiday_month = monthly_holidays.idxmax() if not monthly_holidays.empty else None
            
            # Analyze holiday impact on traffic
            holiday_impact = {}
            if passengers_df is not None and not passengers_df.empty:
                for month in range(1, 13):
                    month_holidays = monthly_holidays.get(month, 0)
                    month_traffic = passengers_df[passengers_df['Month'] == month]['Total'].sum()
                    holiday_impact[month] = {
                        'holidays': month_holidays,
                        'traffic': month_traffic
                    }
            
            return {
                "status": "success",
                "total_holidays": len(holidays_df),
                "monthly_holidays": monthly_holidays.to_dict(),
                "peak_holiday_month": peak_holiday_month,
                "holiday_impact": holiday_impact
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error analizando impacto de feriados: {str(e)}"
            }
    
    def _generate_recommendations(self, business_sector: str, traffic_analysis: Dict[str, Any], 
                                holiday_analysis: Dict[str, Any], context: Dict[str, Any]) -> List[str]:
        """
        Generate business recommendations based on analysis.
        
        Args:
            business_sector: Identified business sector
            traffic_analysis: Traffic pattern analysis
            holiday_analysis: Holiday impact analysis
            context: Data context
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Get business sector info
        sector_info = self.business_sectors.get(business_sector, {})
        sector_name = sector_info.get('name', business_sector)
        
        # Add sector-specific introduction
        recommendations.append(f"**Recomendaciones para {sector_name}:**")
        recommendations.append("")
        
        # Traffic-based recommendations
        if traffic_analysis.get('status') == 'success':
            traffic_level = traffic_analysis.get('traffic_level', 'medium')
            avg_monthly = traffic_analysis.get('avg_monthly', 0)
            growth_rate = traffic_analysis.get('growth_rate', 0)
            peak_month = traffic_analysis.get('peak_month', 0)
            low_month = traffic_analysis.get('low_month', 0)
            
            # Traffic level recommendations
            if traffic_level == 'high':
                recommendations.append(f"• **Alto tráfico detectado** ({avg_monthly:,.0f} pasajeros/mes):")
                recommendations.append(f"  {self.recommendation_templates['high_traffic'].get(business_sector, 'Aproveche el alto tráfico con estrategias específicas.')}")
            elif traffic_level == 'low':
                recommendations.append(f"• **Tráfico moderado** ({avg_monthly:,.0f} pasajeros/mes):")
                recommendations.append(f"  {self.recommendation_templates['low_traffic'].get(business_sector, 'Enfoque en estrategias para tráfico moderado.')}")
            
            # Growth rate recommendations
            if growth_rate > 0.1:
                recommendations.append(f"• **Crecimiento positivo** ({growth_rate:.1%}): El mercado está en expansión, considere inversiones en capacidad.")
            elif growth_rate < -0.1:
                recommendations.append(f"• **Tendencia a la baja** ({growth_rate:.1%}): Enfoque en eficiencia y retención de clientes.")
            
            # Seasonal recommendations
            if peak_month and low_month:
                month_names = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
                              7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}
                recommendations.append(f"• **Estacionalidad**: Mayor actividad en {month_names.get(peak_month, peak_month)}, menor en {month_names.get(low_month, low_month)}")
                recommendations.append(f"  Planifique estrategias diferenciadas para cada temporada.")
        
        # Holiday-based recommendations
        if holiday_analysis.get('status') == 'success':
            total_holidays = holiday_analysis.get('total_holidays', 0)
            peak_holiday_month = holiday_analysis.get('peak_holiday_month')
            
            if total_holidays > 0:
                recommendations.append(f"• **Impacto de feriados** ({total_holidays} feriados identificados):")
                recommendations.append(f"  {self.recommendation_templates['holiday_impact'].get(business_sector, 'Aproveche los feriados con promociones especiales.')}")
                
                if peak_holiday_month:
                    month_names = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
                                  7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}
                    recommendations.append(f"  Concentre esfuerzos en {month_names.get(peak_holiday_month, peak_holiday_month)} (mes con más feriados).")
        
        # Additional sector-specific recommendations
        recommendations.extend(self._get_sector_specific_recommendations(business_sector, traffic_analysis, holiday_analysis))
        
        return recommendations
    
    def _get_sector_specific_recommendations(self, business_sector: str, traffic_analysis: Dict[str, Any], 
                                           holiday_analysis: Dict[str, Any]) -> List[str]:
        """
        Get additional sector-specific recommendations.
        
        Args:
            business_sector: Business sector
            traffic_analysis: Traffic analysis
            holiday_analysis: Holiday analysis
            
        Returns:
            List of additional recommendations
        """
        recommendations = []
        
        if business_sector == 'turismo':
            recommendations.extend([
                "• **Estrategias de marketing**: Desarrolle campañas dirigidas a viajeros internacionales.",
                "• **Servicios adicionales**: Considere ofrecer tours guiados y experiencias locales auténticas.",
                "• **Partnerships**: Establezca alianzas con aerolíneas y agencias de viaje."
            ])
        elif business_sector == 'retail':
            recommendations.extend([
                "• **Inventario dinámico**: Ajuste el inventario según patrones de tráfico estacional.",
                "• **Productos para viajeros**: Incluya artículos de viaje y souvenirs locales.",
                "• **Horarios flexibles**: Ajuste horarios de apertura según flujos de tráfico."
            ])
        elif business_sector == 'restaurantes':
            recommendations.extend([
                "• **Menús estacionales**: Desarrolle menús que reflejen la temporada y eventos locales.",
                "• **Experiencias gastronómicas**: Ofrezca degustaciones y experiencias culinarias únicas.",
                "• **Reservaciones**: Implemente sistema de reservaciones para gestionar la demanda."
            ])
        elif business_sector == 'transporte':
            recommendations.extend([
                "• **Rutas optimizadas**: Desarrolle rutas que conecten con puntos de mayor tráfico.",
                "• **Tarifas dinámicas**: Implemente precios variables según demanda y temporada.",
                "• **Servicios premium**: Ofrezca opciones de transporte de lujo para viajeros de negocios."
            ])
        elif business_sector == 'entretenimiento':
            recommendations.extend([
                "• **Eventos temáticos**: Organice eventos que coincidan con feriados y temporadas altas.",
                "• **Experiencias inmersivas**: Desarrolle actividades que atraigan tanto locales como visitantes.",
                "• **Marketing digital**: Utilice redes sociales para promocionar eventos a viajeros."
            ])
        elif business_sector == 'servicios':
            recommendations.extend([
                "• **Horarios extendidos**: Considere horarios de atención que acomoden a viajeros.",
                "• **Servicios express**: Ofrezca opciones rápidas para clientes con tiempo limitado.",
                "• **Consultoría especializada**: Desarrolle servicios específicos para empresas del sector turístico."
            ])
        elif business_sector == 'eventos':
            recommendations.extend([
                "• **Temporadas de eventos**: Planifique eventos durante meses de mayor tráfico.",
                "• **Paquetes corporativos**: Desarrolle ofertas para grupos de viajeros de negocios.",
                "• **Espacios versátiles**: Diseñe espacios que puedan adaptarse a diferentes tipos de eventos."
            ])
        
        return recommendations
    
    def get_business_summary(self, analysis_results: Dict[str, Any]) -> str:
        """
        Get a formatted summary of the business analysis.
        
        Args:
            analysis_results: Results from the business analysis
            
        Returns:
            Formatted summary string
        """
        if analysis_results.get("error", False):
            return f"❌ Error: {analysis_results.get('message', 'Error desconocido')}"
        
        business_sector = analysis_results.get("business_sector", "negocio")
        recommendations = analysis_results.get("recommendations", [])
        traffic_analysis = analysis_results.get("traffic_analysis", {})
        holiday_analysis = analysis_results.get("holiday_analysis", {})
        
        # Create narrative summary
        summary = f"## 💼 Análisis de Negocios - {business_sector.title()}\n\n"
        
        # Add traffic insights
        if traffic_analysis.get('status') == 'success':
            avg_monthly = traffic_analysis.get('avg_monthly', 0)
            traffic_level = traffic_analysis.get('traffic_level', 'medium')
            growth_rate = traffic_analysis.get('growth_rate', 0)
            
            summary += f"**📊 Análisis de Tráfico:**\n\n"
            summary += f"• **Nivel de tráfico**: {traffic_level.title()} ({avg_monthly:,.0f} pasajeros/mes)\n"
            summary += f"• **Tendencia**: {'Crecimiento' if growth_rate > 0 else 'Decrecimiento'} del {abs(growth_rate):.1%}\n"
            summary += f"• **Oportunidad**: {'Alto potencial' if traffic_level == 'high' else 'Potencial moderado'} para el sector\n\n"
        
        # Add holiday insights
        if holiday_analysis.get('status') == 'success':
            total_holidays = holiday_analysis.get('total_holidays', 0)
            summary += f"**🎉 Impacto de Feriados:**\n\n"
            summary += f"• **Feriados identificados**: {total_holidays} eventos especiales\n"
            summary += f"• **Oportunidad**: {'Excelente' if total_holidays > 10 else 'Moderada'} para promociones temáticas\n\n"
        
        # Add recommendations
        if recommendations:
            summary += "**💡 Recomendaciones Estratégicas:**\n\n"
            for recommendation in recommendations:
                summary += f"{recommendation}\n"
        
        return summary


# Create a global instance for easy access
business_advisor_agent = BusinessAdvisorAgent()

