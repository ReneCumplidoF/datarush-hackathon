"""
Formatters Module
================

Módulo de formateadores para los agentes del sistema DataRush.

Clases incluidas:
- DataFormatter: Formateo de datos
- ResponseFormatter: Formateo de respuestas
- ExportFormatter: Formateo para exportación
"""

import pandas as pd
from typing import Dict, List, Any, Optional
import streamlit as st
from datetime import datetime

class DataFormatter:
    """Formateador de datos para el sistema DataRush"""
    
    @staticmethod
    def format_number(value: float, decimals: int = 0) -> str:
        """
        Formatear número con separadores de miles
        
        Args:
            value: Valor numérico
            decimals: Número de decimales
            
        Returns:
            str: Número formateado
        """
        if pd.isna(value) or value is None:
            return "N/A"
        
        return f"{value:,.{decimals}f}"
    
    @staticmethod
    def format_percentage(value: float, decimals: int = 1) -> str:
        """
        Formatear porcentaje
        
        Args:
            value: Valor numérico (0-1 o 0-100)
            decimals: Número de decimales
            
        Returns:
            str: Porcentaje formateado
        """
        if pd.isna(value) or value is None:
            return "N/A"
        
        # Si el valor está entre 0 y 1, convertirlo a porcentaje
        if 0 <= value <= 1:
            value = value * 100
        
        return f"{value:.{decimals}f}%"
    
    @staticmethod
    def format_date(date, format_str: str = "%Y-%m-%d") -> str:
        """
        Formatear fecha
        
        Args:
            date: Fecha a formatear
            format_str: Formato de salida
            
        Returns:
            str: Fecha formateada
        """
        if pd.isna(date) or date is None:
            return "N/A"
        
        if isinstance(date, str):
            date = pd.to_datetime(date)
        
        return date.strftime(format_str)
    
    @staticmethod
    def format_dataframe_summary(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Formatear resumen de DataFrame
        
        Args:
            df: DataFrame a resumir
            
        Returns:
            Dict: Resumen formateado
        """
        if df is None or df.empty:
            return {"error": "No hay datos disponibles"}
        
        summary = {
            "total_records": len(df),
            "columns": len(df.columns),
            "memory_usage": f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB",
            "null_values": df.isnull().sum().sum(),
            "duplicate_rows": df.duplicated().sum()
        }
        
        return summary

class ResponseFormatter:
    """Formateador de respuestas para el sistema DataRush"""
    
    @staticmethod
    def format_chat_response(response: str, response_type: str = "general") -> str:
        """
        Formatear respuesta del chat
        
        Args:
            response: Respuesta a formatear
            response_type: Tipo de respuesta (general, data, error)
            
        Returns:
            str: Respuesta formateada
        """
        if not response:
            return "No hay respuesta disponible."
        
        # Formatear según el tipo de respuesta
        if response_type == "data":
            return f"📊 **Datos:**\n\n{response}"
        elif response_type == "error":
            return f"❌ **Error:**\n\n{response}"
        elif response_type == "success":
            return f"✅ **Éxito:**\n\n{response}"
        else:
            return response
    
    @staticmethod
    def format_metric_card(title: str, value: Any, delta: Optional[Any] = None) -> str:
        """
        Formatear tarjeta de métrica
        
        Args:
            title: Título de la métrica
            value: Valor de la métrica
            delta: Cambio respecto al período anterior
            
        Returns:
            str: Tarjeta formateada
        """
        if delta is not None:
            delta_str = f" ({delta:+.1f}%)" if isinstance(delta, (int, float)) else f" ({delta})"
        else:
            delta_str = ""
        
        return f"**{title}:** {value}{delta_str}"
    
    @staticmethod
    def format_insight_bullet(insight: str, category: str = "general") -> str:
        """
        Formatear insight como viñeta
        
        Args:
            insight: Insight a formatear
            category: Categoría del insight
            
        Returns:
            str: Insight formateado
        """
        icons = {
            "trend": "📈",
            "pattern": "🔍",
            "recommendation": "💡",
            "warning": "⚠️",
            "success": "✅",
            "general": "•"
        }
        
        icon = icons.get(category, "•")
        return f"{icon} {insight}"

class ExportFormatter:
    """Formateador para exportación de datos"""
    
    @staticmethod
    def format_csv_export(df: pd.DataFrame, filename: str = None) -> str:
        """
        Formatear DataFrame para exportación CSV
        
        Args:
            df: DataFrame a exportar
            filename: Nombre del archivo
            
        Returns:
            str: Ruta del archivo exportado
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"datarush_export_{timestamp}.csv"
        
        # Limpiar datos para exportación
        df_clean = df.copy()
        
        # Convertir fechas a string
        date_columns = df_clean.select_dtypes(include=['datetime64']).columns
        for col in date_columns:
            df_clean[col] = df_clean[col].dt.strftime('%Y-%m-%d')
        
        # Guardar archivo
        df_clean.to_csv(filename, index=False, encoding='utf-8')
        return filename
    
    @staticmethod
    def format_excel_export(data_dict: Dict[str, pd.DataFrame], filename: str = None) -> str:
        """
        Formatear múltiples DataFrames para exportación Excel
        
        Args:
            data_dict: Diccionario con nombre de hoja y DataFrame
            filename: Nombre del archivo
            
        Returns:
            str: Ruta del archivo exportado
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"datarush_export_{timestamp}.xlsx"
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            for sheet_name, df in data_dict.items():
                # Limpiar datos para exportación
                df_clean = df.copy()
                
                # Convertir fechas a string
                date_columns = df_clean.select_dtypes(include=['datetime64']).columns
                for col in date_columns:
                    df_clean[col] = df_clean[col].dt.strftime('%Y-%m-%d')
                
                df_clean.to_excel(writer, sheet_name=sheet_name, index=False)
        
        return filename
    
    @staticmethod
    def format_json_export(data: Dict[str, Any], filename: str = None) -> str:
        """
        Formatear datos para exportación JSON
        
        Args:
            data: Datos a exportar
            filename: Nombre del archivo
            
        Returns:
            str: Ruta del archivo exportado
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"datarush_export_{timestamp}.json"
        
        import json
        
        # Convertir DataFrames a diccionarios
        def convert_dataframes(obj):
            if isinstance(obj, pd.DataFrame):
                return obj.to_dict('records')
            elif isinstance(obj, dict):
                return {k: convert_dataframes(v) for k, v in obj.items()}
            else:
                return obj
        
        data_clean = convert_dataframes(data)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data_clean, f, indent=2, ensure_ascii=False, default=str)
        
        return filename

