"""
Integración Simplificada para Validación Cruzada de Datos (Sin BigQuery)
========================================================================

Este módulo proporciona funcionalidades simplificadas para validación
de datos sin depender de BigQuery. Utiliza solo datos locales.

Funcionalidades:
- Validación de datos locales
- Análisis de consistencia
- Generación de reportes de validación
"""

import os
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimpleBigQueryIntegration:
    """
    Integración simplificada para validación de datos sin BigQuery.
    """
    
    def __init__(self):
        self.data_loaded = False
        self.validation_results = {}
        self.data_quality_metrics = {}
    
    def validate_data_quality(self, data: Dict[str, pd.DataFrame]) -> Dict[str, any]:
        """
        Validar la calidad de los datos locales.
        
        Args:
            data: Diccionario con los DataFrames de datos
            
        Returns:
            Dict: Resultados de la validación
        """
        try:
            validation_results = {
                "timestamp": pd.Timestamp.now().isoformat(),
                "data_sources": {},
                "quality_metrics": {},
                "recommendations": [],
                "overall_score": 0.0
            }
            
            # Validar datos de pasajeros
            if 'passengers' in data:
                passenger_validation = self._validate_passenger_data(data['passengers'])
                validation_results["data_sources"]["passengers"] = passenger_validation
            
            # Validar datos de feriados
            if 'holidays' in data:
                holiday_validation = self._validate_holiday_data(data['holidays'])
                validation_results["data_sources"]["holidays"] = holiday_validation
            
            # Validar datos de países
            if 'countries' in data:
                country_validation = self._validate_country_data(data['countries'])
                validation_results["data_sources"]["countries"] = country_validation
            
            # Calcular métricas de calidad general
            validation_results["quality_metrics"] = self._calculate_quality_metrics(validation_results["data_sources"])
            
            # Generar recomendaciones
            validation_results["recommendations"] = self._generate_recommendations(validation_results["data_sources"])
            
            # Calcular score general
            validation_results["overall_score"] = self._calculate_overall_score(validation_results["quality_metrics"])
            
            self.validation_results = validation_results
            return validation_results
            
        except Exception as e:
            logger.error(f"Error en validación de datos: {str(e)}")
            return {
                "error": True,
                "message": f"Error en validación: {str(e)}",
                "timestamp": pd.Timestamp.now().isoformat()
            }
    
    def _validate_passenger_data(self, df: pd.DataFrame) -> Dict[str, any]:
        """Validar datos de pasajeros."""
        validation = {
            "source": "passengers",
            "total_records": len(df),
            "completeness": 0.0,
            "consistency": 0.0,
            "accuracy": 0.0,
            "issues": [],
            "recommendations": []
        }
        
        try:
            # Verificar completitud
            total_cells = df.size
            null_cells = df.isnull().sum().sum()
            validation["completeness"] = 1.0 - (null_cells / total_cells) if total_cells > 0 else 0.0
            
            # Verificar consistencia
            if 'Total' in df.columns:
                negative_values = (df['Total'] < 0).sum()
                validation["consistency"] = 1.0 - (negative_values / len(df)) if len(df) > 0 else 0.0
                
                if negative_values > 0:
                    validation["issues"].append(f"Se encontraron {negative_values} valores negativos en Total")
            
            # Verificar precisión
            if 'Year' in df.columns:
                current_year = pd.Timestamp.now().year
                invalid_years = ((df['Year'] < 2000) | (df['Year'] > current_year)).sum()
                validation["accuracy"] = 1.0 - (invalid_years / len(df)) if len(df) > 0 else 0.0
                
                if invalid_years > 0:
                    validation["issues"].append(f"Se encontraron {invalid_years} años inválidos")
            
            # Generar recomendaciones
            if validation["completeness"] < 0.9:
                validation["recommendations"].append("Considerar limpiar datos faltantes")
            
            if validation["consistency"] < 0.95:
                validation["recommendations"].append("Revisar valores negativos o inconsistentes")
            
            if validation["accuracy"] < 0.95:
                validation["recommendations"].append("Verificar fechas y valores de año")
            
        except Exception as e:
            validation["issues"].append(f"Error en validación: {str(e)}")
        
        return validation
    
    def _validate_holiday_data(self, df: pd.DataFrame) -> Dict[str, any]:
        """Validar datos de feriados."""
        validation = {
            "source": "holidays",
            "total_records": len(df),
            "completeness": 0.0,
            "consistency": 0.0,
            "accuracy": 0.0,
            "issues": [],
            "recommendations": []
        }
        
        try:
            # Verificar completitud
            total_cells = df.size
            null_cells = df.isnull().sum().sum()
            validation["completeness"] = 1.0 - (null_cells / total_cells) if total_cells > 0 else 0.0
            
            # Verificar consistencia de fechas
            if 'Date' in df.columns:
                try:
                    df['Date'] = pd.to_datetime(df['Date'])
                    validation["consistency"] = 1.0
                except:
                    validation["consistency"] = 0.0
                    validation["issues"].append("Formato de fecha inválido")
            
            # Verificar precisión de códigos ISO
            if 'ISO3' in df.columns:
                valid_iso3 = df['ISO3'].str.len() == 3
                invalid_iso3 = (~valid_iso3).sum()
                validation["accuracy"] = 1.0 - (invalid_iso3 / len(df)) if len(df) > 0 else 0.0
                
                if invalid_iso3 > 0:
                    validation["issues"].append(f"Se encontraron {invalid_iso3} códigos ISO3 inválidos")
            
            # Generar recomendaciones
            if validation["completeness"] < 0.9:
                validation["recommendations"].append("Completar datos de feriados faltantes")
            
            if validation["consistency"] < 0.95:
                validation["recommendations"].append("Corregir formato de fechas")
            
            if validation["accuracy"] < 0.95:
                validation["recommendations"].append("Verificar códigos de país")
            
        except Exception as e:
            validation["issues"].append(f"Error en validación: {str(e)}")
        
        return validation
    
    def _validate_country_data(self, df: pd.DataFrame) -> Dict[str, any]:
        """Validar datos de países."""
        validation = {
            "source": "countries",
            "total_records": len(df),
            "completeness": 0.0,
            "consistency": 0.0,
            "accuracy": 0.0,
            "issues": [],
            "recommendations": []
        }
        
        try:
            # Verificar completitud
            total_cells = df.size
            null_cells = df.isnull().sum().sum()
            validation["completeness"] = 1.0 - (null_cells / total_cells) if total_cells > 0 else 0.0
            
            # Verificar consistencia de códigos
            if 'alpha_3' in df.columns:
                valid_alpha3 = df['alpha_3'].str.len() == 3
                invalid_alpha3 = (~valid_alpha3).sum()
                validation["consistency"] = 1.0 - (invalid_alpha3 / len(df)) if len(df) > 0 else 0.0
                
                if invalid_alpha3 > 0:
                    validation["issues"].append(f"Se encontraron {invalid_alpha3} códigos alpha_3 inválidos")
            
            # Verificar precisión de nombres
            if 'name' in df.columns:
                empty_names = df['name'].isnull().sum()
                validation["accuracy"] = 1.0 - (empty_names / len(df)) if len(df) > 0 else 0.0
                
                if empty_names > 0:
                    validation["issues"].append(f"Se encontraron {empty_names} nombres de país vacíos")
            
            # Generar recomendaciones
            if validation["completeness"] < 0.9:
                validation["recommendations"].append("Completar información de países faltante")
            
            if validation["consistency"] < 0.95:
                validation["recommendations"].append("Corregir códigos de país")
            
            if validation["accuracy"] < 0.95:
                validation["recommendations"].append("Verificar nombres de países")
            
        except Exception as e:
            validation["issues"].append(f"Error en validación: {str(e)}")
        
        return validation
    
    def _calculate_quality_metrics(self, data_sources: Dict[str, Dict]) -> Dict[str, float]:
        """Calcular métricas de calidad general."""
        metrics = {
            "overall_completeness": 0.0,
            "overall_consistency": 0.0,
            "overall_accuracy": 0.0,
            "total_issues": 0,
            "data_sources_count": len(data_sources)
        }
        
        if not data_sources:
            return metrics
        
        # Calcular promedios
        completeness_scores = [source.get("completeness", 0.0) for source in data_sources.values()]
        consistency_scores = [source.get("consistency", 0.0) for source in data_sources.values()]
        accuracy_scores = [source.get("accuracy", 0.0) for source in data_sources.values()]
        
        metrics["overall_completeness"] = np.mean(completeness_scores) if completeness_scores else 0.0
        metrics["overall_consistency"] = np.mean(consistency_scores) if consistency_scores else 0.0
        metrics["overall_accuracy"] = np.mean(accuracy_scores) if accuracy_scores else 0.0
        
        # Contar issues totales
        total_issues = sum(len(source.get("issues", [])) for source in data_sources.values())
        metrics["total_issues"] = total_issues
        
        return metrics
    
    def _generate_recommendations(self, data_sources: Dict[str, Dict]) -> List[str]:
        """Generar recomendaciones basadas en la validación."""
        recommendations = []
        
        # Recomendaciones generales
        if len(data_sources) < 3:
            recommendations.append("Considerar agregar más fuentes de datos para validación cruzada")
        
        # Recomendaciones específicas por fuente
        for source_name, source_data in data_sources.items():
            if source_data.get("completeness", 0.0) < 0.8:
                recommendations.append(f"Mejorar completitud de datos en {source_name}")
            
            if source_data.get("consistency", 0.0) < 0.8:
                recommendations.append(f"Revisar consistencia de datos en {source_name}")
            
            if source_data.get("accuracy", 0.0) < 0.8:
                recommendations.append(f"Verificar precisión de datos en {source_name}")
        
        return recommendations
    
    def _calculate_overall_score(self, quality_metrics: Dict[str, float]) -> float:
        """Calcular score general de calidad."""
        if not quality_metrics:
            return 0.0
        
        # Ponderar las métricas
        completeness = quality_metrics.get("overall_completeness", 0.0)
        consistency = quality_metrics.get("overall_consistency", 0.0)
        accuracy = quality_metrics.get("overall_accuracy", 0.0)
        
        # Score ponderado (completitud 40%, consistencia 30%, precisión 30%)
        overall_score = (completeness * 0.4) + (consistency * 0.3) + (accuracy * 0.3)
        
        return round(overall_score, 3)
    
    def get_validation_report(self) -> str:
        """Generar reporte de validación en formato texto."""
        if not self.validation_results:
            return "No hay resultados de validación disponibles."
        
        report = f"# Reporte de Validación de Datos\n\n"
        report += f"**Timestamp:** {self.validation_results.get('timestamp', 'N/A')}\n\n"
        
        # Score general
        overall_score = self.validation_results.get('overall_score', 0.0)
        report += f"## Score General de Calidad: {overall_score:.1%}\n\n"
        
        # Métricas de calidad
        quality_metrics = self.validation_results.get('quality_metrics', {})
        if quality_metrics:
            report += f"## Métricas de Calidad\n\n"
            report += f"- **Completitud:** {quality_metrics.get('overall_completeness', 0.0):.1%}\n"
            report += f"- **Consistencia:** {quality_metrics.get('overall_consistency', 0.0):.1%}\n"
            report += f"- **Precisión:** {quality_metrics.get('overall_accuracy', 0.0):.1%}\n"
            report += f"- **Total de Issues:** {quality_metrics.get('total_issues', 0)}\n"
            report += f"- **Fuentes de Datos:** {quality_metrics.get('data_sources_count', 0)}\n\n"
        
        # Fuentes de datos
        data_sources = self.validation_results.get('data_sources', {})
        if data_sources:
            report += f"## Fuentes de Datos\n\n"
            for source_name, source_data in data_sources.items():
                report += f"### {source_name.title()}\n"
                report += f"- **Registros:** {source_data.get('total_records', 0):,}\n"
                report += f"- **Completitud:** {source_data.get('completeness', 0.0):.1%}\n"
                report += f"- **Consistencia:** {source_data.get('consistency', 0.0):.1%}\n"
                report += f"- **Precisión:** {source_data.get('accuracy', 0.0):.1%}\n"
                
                issues = source_data.get('issues', [])
                if issues:
                    report += f"- **Issues:**\n"
                    for issue in issues:
                        report += f"  - {issue}\n"
                
                recommendations = source_data.get('recommendations', [])
                if recommendations:
                    report += f"- **Recomendaciones:**\n"
                    for rec in recommendations:
                        report += f"  - {rec}\n"
                
                report += "\n"
        
        # Recomendaciones generales
        recommendations = self.validation_results.get('recommendations', [])
        if recommendations:
            report += f"## Recomendaciones Generales\n\n"
            for i, rec in enumerate(recommendations, 1):
                report += f"{i}. {rec}\n"
        
        return report
    
    def export_validation_results(self, filename: str = None) -> str:
        """Exportar resultados de validación a archivo."""
        if not self.validation_results:
            return "No hay resultados para exportar."
        
        if filename is None:
            timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
            filename = f"validation_report_{timestamp}.txt"
        
        try:
            report = self.get_validation_report()
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
            
            return f"Reporte exportado a: {filename}"
            
        except Exception as e:
            return f"Error exportando reporte: {str(e)}"


# Crear instancia global
simple_bigquery_integration = SimpleBigQueryIntegration()

