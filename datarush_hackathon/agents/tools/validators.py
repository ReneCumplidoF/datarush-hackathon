"""
Validators Module
================

Módulo de validadores para los agentes del sistema DataRush.

Clases incluidas:
- DataValidator: Validación de datos
- FilterValidator: Validación de filtros
- InputValidator: Validación de entrada del usuario
"""

import pandas as pd
from typing import Dict, List, Any, Optional
import streamlit as st

class DataValidator:
    """Validador de datos para el sistema DataRush"""
    
    @staticmethod
    def validate_dataframe(df: pd.DataFrame, required_columns: List[str]) -> bool:
        """
        Validar que un DataFrame tenga las columnas requeridas
        
        Args:
            df: DataFrame a validar
            required_columns: Lista de columnas requeridas
            
        Returns:
            bool: True si es válido, False en caso contrario
        """
        if df is None or df.empty:
            return False
        
        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            st.error(f"❌ Columnas faltantes: {', '.join(missing_columns)}")
            return False
        
        return True
    
    @staticmethod
    def validate_data_types(df: pd.DataFrame, column_types: Dict[str, str]) -> bool:
        """
        Validar tipos de datos de un DataFrame
        
        Args:
            df: DataFrame a validar
            column_types: Diccionario con columnas y tipos esperados
            
        Returns:
            bool: True si es válido, False en caso contrario
        """
        for column, expected_type in column_types.items():
            if column in df.columns:
                actual_type = str(df[column].dtype)
                if expected_type not in actual_type:
                    st.warning(f"⚠️ Columna {column}: esperado {expected_type}, encontrado {actual_type}")
                    return False
        
        return True
    
    @staticmethod
    def validate_date_range(df: pd.DataFrame, date_column: str, min_year: int, max_year: int) -> bool:
        """
        Validar rango de fechas en un DataFrame
        
        Args:
            df: DataFrame a validar
            date_column: Nombre de la columna de fecha
            min_year: Año mínimo
            max_year: Año máximo
            
        Returns:
            bool: True si es válido, False en caso contrario
        """
        if date_column not in df.columns:
            return False
        
        df[date_column] = pd.to_datetime(df[date_column])
        min_date = df[date_column].min()
        max_date = df[date_column].max()
        
        if min_date.year < min_year or max_date.year > max_year:
            st.warning(f"⚠️ Rango de fechas fuera de límites: {min_date.year}-{max_date.year}")
            return False
        
        return True

class FilterValidator:
    """Validador de filtros para el sistema DataRush"""
    
    @staticmethod
    def validate_year_range(year_range: tuple) -> bool:
        """
        Validar rango de años
        
        Args:
            year_range: Tupla con (año_min, año_max)
            
        Returns:
            bool: True si es válido, False en caso contrario
        """
        if not year_range or len(year_range) != 2:
            return False
        
        year_min, year_max = year_range
        if year_min > year_max:
            st.error("❌ El año mínimo no puede ser mayor al máximo")
            return False
        
        if year_min < 2010 or year_max > 2030:
            st.warning("⚠️ Rango de años fuera de límites recomendados")
            return False
        
        return True
    
    @staticmethod
    def validate_country_selection(countries: List[str], available_countries: List[str]) -> bool:
        """
        Validar selección de países
        
        Args:
            countries: Lista de países seleccionados
            available_countries: Lista de países disponibles
            
        Returns:
            bool: True si es válido, False en caso contrario
        """
        if not countries:
            return True
        
        invalid_countries = set(countries) - set(available_countries)
        if invalid_countries:
            st.error(f"❌ Países no válidos: {', '.join(invalid_countries)}")
            return False
        
        return True
    
    @staticmethod
    def validate_passenger_range(passenger_range: tuple, max_passengers: float) -> bool:
        """
        Validar rango de pasajeros
        
        Args:
            passenger_range: Tupla con (min_pass, max_pass)
            max_passengers: Máximo de pasajeros disponible
            
        Returns:
            bool: True si es válido, False en caso contrario
        """
        if not passenger_range or len(passenger_range) != 2:
            return False
        
        min_pass, max_pass = passenger_range
        if min_pass > max_pass:
            st.error("❌ El volumen mínimo no puede ser mayor al máximo")
            return False
        
        if max_pass > max_passengers:
            st.warning(f"⚠️ Volumen máximo excede datos disponibles: {max_passengers:,.0f}")
            return False
        
        return True

class InputValidator:
    """Validador de entrada del usuario para el sistema DataRush"""
    
    @staticmethod
    def validate_chat_input(message: str) -> bool:
        """
        Validar entrada del chat
        
        Args:
            message: Mensaje del usuario
            
        Returns:
            bool: True si es válido, False en caso contrario
        """
        if not message or not message.strip():
            return False
        
        if len(message.strip()) < 2:
            st.warning("⚠️ El mensaje es muy corto")
            return False
        
        if len(message) > 1000:
            st.warning("⚠️ El mensaje es muy largo")
            return False
        
        return True
    
    @staticmethod
    def validate_file_upload(file) -> bool:
        """
        Validar archivo subido
        
        Args:
            file: Archivo subido
            
        Returns:
            bool: True si es válido, False en caso contrario
        """
        if file is None:
            return False
        
        allowed_extensions = ['.csv', '.xlsx', '.json']
        file_extension = file.name.lower().split('.')[-1]
        
        if f'.{file_extension}' not in allowed_extensions:
            st.error(f"❌ Tipo de archivo no soportado: {file_extension}")
            return False
        
        if file.size > 50 * 1024 * 1024:  # 50MB
            st.error("❌ Archivo demasiado grande (máximo 50MB)")
            return False
        
        return True
    
    @staticmethod
    def validate_api_key(api_key: str, service: str) -> bool:
        """
        Validar clave de API
        
        Args:
            api_key: Clave de API
            service: Servicio (gemini, etc.)
            
        Returns:
            bool: True si es válido, False en caso contrario
        """
        if not api_key or not api_key.strip():
            st.warning(f"⚠️ Clave de API para {service} no encontrada")
            return False
        
        if len(api_key) < 10:
            st.error(f"❌ Clave de API para {service} inválida")
            return False
        
        return True
