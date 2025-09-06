"""
Metrics Module
==============

Módulo de calculadoras de métricas para los agentes del sistema DataRush.

Clases incluidas:
- MetricsCalculator: Calculadora de métricas generales
- CorrelationCalculator: Calculadora de correlaciones
- QualityCalculator: Calculadora de calidad de datos
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import streamlit as st

class MetricsCalculator:
    """Calculadora de métricas para el sistema DataRush"""
    
    @staticmethod
    def calculate_basic_metrics(df: pd.DataFrame, value_column: str) -> Dict[str, float]:
        """
        Calcular métricas básicas de un DataFrame
        
        Args:
            df: DataFrame con datos
            value_column: Columna con valores numéricos
            
        Returns:
            Dict: Métricas básicas
        """
        if df.empty or value_column not in df.columns:
            return {}
        
        values = df[value_column].dropna()
        
        if values.empty:
            return {}
        
        metrics = {
            'count': len(values),
            'sum': values.sum(),
            'mean': values.mean(),
            'median': values.median(),
            'std': values.std(),
            'min': values.min(),
            'max': values.max(),
            'q25': values.quantile(0.25),
            'q75': values.quantile(0.75)
        }
        
        return metrics
    
    @staticmethod
    def calculate_growth_rate(df: pd.DataFrame, value_column: str, time_column: str) -> float:
        """
        Calcular tasa de crecimiento
        
        Args:
            df: DataFrame con datos
            value_column: Columna con valores
            time_column: Columna con tiempo
            
        Returns:
            float: Tasa de crecimiento
        """
        if df.empty or value_column not in df.columns or time_column not in df.columns:
            return 0.0
        
        df_sorted = df.sort_values(time_column)
        values = df_sorted[value_column].dropna()
        
        if len(values) < 2:
            return 0.0
        
        first_value = values.iloc[0]
        last_value = values.iloc[-1]
        
        if first_value == 0:
            return 0.0
        
        growth_rate = ((last_value - first_value) / first_value) * 100
        return growth_rate
    
    @staticmethod
    def calculate_seasonality(df: pd.DataFrame, value_column: str, time_column: str) -> Dict[str, float]:
        """
        Calcular métricas de estacionalidad
        
        Args:
            df: DataFrame con datos
            value_column: Columna con valores
            time_column: Columna con tiempo
            
        Returns:
            Dict: Métricas de estacionalidad
        """
        if df.empty or value_column not in df.columns or time_column not in df.columns:
            return {}
        
        df[time_column] = pd.to_datetime(df[time_column])
        df['month'] = df[time_column].dt.month
        df['year'] = df[time_column].dt.year
        
        monthly_avg = df.groupby('month')[value_column].mean()
        
        seasonality = {
            'peak_month': monthly_avg.idxmax(),
            'low_month': monthly_avg.idxmin(),
            'peak_value': monthly_avg.max(),
            'low_value': monthly_avg.min(),
            'seasonality_index': (monthly_avg.max() - monthly_avg.min()) / monthly_avg.mean()
        }
        
        return seasonality
    
    @staticmethod
    def calculate_holiday_impact(df: pd.DataFrame, value_column: str, holiday_column: str) -> Dict[str, float]:
        """
        Calcular impacto de feriados
        
        Args:
            df: DataFrame con datos
            value_column: Columna con valores
            holiday_column: Columna con indicador de feriado
            
        Returns:
            Dict: Métricas de impacto de feriados
        """
        if df.empty or value_column not in df.columns or holiday_column not in df.columns:
            return {}
        
        holiday_data = df[df[holiday_column] == True][value_column].dropna()
        non_holiday_data = df[df[holiday_column] == False][value_column].dropna()
        
        if holiday_data.empty or non_holiday_data.empty:
            return {}
        
        impact = {
            'holiday_avg': holiday_data.mean(),
            'non_holiday_avg': non_holiday_data.mean(),
            'impact_percentage': ((holiday_data.mean() - non_holiday_data.mean()) / non_holiday_data.mean()) * 100,
            'holiday_std': holiday_data.std(),
            'non_holiday_std': non_holiday_data.std()
        }
        
        return impact

class CorrelationCalculator:
    """Calculadora de correlaciones para el sistema DataRush"""
    
    @staticmethod
    def calculate_correlation_matrix(df: pd.DataFrame, numeric_columns: List[str]) -> pd.DataFrame:
        """
        Calcular matriz de correlación
        
        Args:
            df: DataFrame con datos
            numeric_columns: Lista de columnas numéricas
            
        Returns:
            pd.DataFrame: Matriz de correlación
        """
        if df.empty or not numeric_columns:
            return pd.DataFrame()
        
        available_columns = [col for col in numeric_columns if col in df.columns]
        if not available_columns:
            return pd.DataFrame()
        
        correlation_matrix = df[available_columns].corr()
        return correlation_matrix
    
    @staticmethod
    def calculate_correlation_with_target(df: pd.DataFrame, target_column: str, feature_columns: List[str]) -> Dict[str, float]:
        """
        Calcular correlación con variable objetivo
        
        Args:
            df: DataFrame con datos
            target_column: Columna objetivo
            feature_columns: Lista de columnas de características
            
        Returns:
            Dict: Correlaciones con la variable objetivo
        """
        if df.empty or target_column not in df.columns:
            return {}
        
        correlations = {}
        for feature in feature_columns:
            if feature in df.columns:
                corr = df[target_column].corr(df[feature])
                if not pd.isna(corr):
                    correlations[feature] = corr
        
        return correlations
    
    @staticmethod
    def calculate_partial_correlation(df: pd.DataFrame, x: str, y: str, control_vars: List[str]) -> float:
        """
        Calcular correlación parcial
        
        Args:
            df: DataFrame con datos
            x: Variable X
            y: Variable Y
            control_vars: Variables de control
            
        Returns:
            float: Correlación parcial
        """
        if df.empty or x not in df.columns or y not in df.columns:
            return 0.0
        
        # Filtrar datos válidos
        valid_data = df[[x, y] + control_vars].dropna()
        
        if len(valid_data) < 3:
            return 0.0
        
        try:
            from scipy.stats import pearsonr
            from sklearn.linear_model import LinearRegression
            
            # Calcular residuos de X controlando por control_vars
            X_control = valid_data[control_vars].values
            y_x = valid_data[x].values
            y_y = valid_data[y].values
            
            model_x = LinearRegression().fit(X_control, y_x)
            residuals_x = y_x - model_x.predict(X_control)
            
            model_y = LinearRegression().fit(X_control, y_y)
            residuals_y = y_y - model_y.predict(X_control)
            
            # Correlación entre residuos
            partial_corr, _ = pearsonr(residuals_x, residuals_y)
            return partial_corr
            
        except ImportError:
            st.warning("⚠️ scikit-learn no disponible para correlación parcial")
            return 0.0
        except Exception as e:
            st.warning(f"⚠️ Error calculando correlación parcial: {str(e)}")
            return 0.0

class QualityCalculator:
    """Calculadora de calidad de datos para el sistema DataRush"""
    
    @staticmethod
    def calculate_completeness_score(df: pd.DataFrame) -> float:
        """
        Calcular score de completitud
        
        Args:
            df: DataFrame a evaluar
            
        Returns:
            float: Score de completitud (0-1)
        """
        if df.empty:
            return 0.0
        
        total_cells = df.shape[0] * df.shape[1]
        non_null_cells = df.notna().sum().sum()
        
        completeness = non_null_cells / total_cells
        return completeness
    
    @staticmethod
    def calculate_consistency_score(df: pd.DataFrame, key_columns: List[str]) -> float:
        """
        Calcular score de consistencia
        
        Args:
            df: DataFrame a evaluar
            key_columns: Columnas clave para consistencia
            
        Returns:
            float: Score de consistencia (0-1)
        """
        if df.empty or not key_columns:
            return 0.0
        
        available_columns = [col for col in key_columns if col in df.columns]
        if not available_columns:
            return 0.0
        
        consistency_scores = []
        
        for col in available_columns:
            if df[col].dtype in ['object', 'string']:
                # Para columnas categóricas, verificar consistencia de formato
                unique_values = df[col].dropna().unique()
                if len(unique_values) > 0:
                    # Verificar si todos los valores siguen el mismo patrón
                    sample_value = str(unique_values[0])
                    pattern_consistency = sum(1 for val in unique_values if str(val).startswith(sample_value[:2])) / len(unique_values)
                    consistency_scores.append(pattern_consistency)
            else:
                # Para columnas numéricas, verificar rango razonable
                values = df[col].dropna()
                if len(values) > 0:
                    q1, q3 = values.quantile([0.25, 0.75])
                    iqr = q3 - q1
                    lower_bound = q1 - 1.5 * iqr
                    upper_bound = q3 + 1.5 * iqr
                    
                    outliers = ((values < lower_bound) | (values > upper_bound)).sum()
                    consistency = 1 - (outliers / len(values))
                    consistency_scores.append(max(0, consistency))
        
        return np.mean(consistency_scores) if consistency_scores else 0.0
    
    @staticmethod
    def calculate_accuracy_score(df: pd.DataFrame, reference_data: pd.DataFrame, key_columns: List[str]) -> float:
        """
        Calcular score de precisión comparando con datos de referencia
        
        Args:
            df: DataFrame a evaluar
            reference_data: DataFrame de referencia
            key_columns: Columnas clave para comparación
            
        Returns:
            float: Score de precisión (0-1)
        """
        if df.empty or reference_data.empty or not key_columns:
            return 0.0
        
        available_columns = [col for col in key_columns if col in df.columns and col in reference_data.columns]
        if not available_columns:
            return 0.0
        
        accuracy_scores = []
        
        for col in available_columns:
            df_values = df[col].dropna()
            ref_values = reference_data[col].dropna()
            
            if len(df_values) == 0 or len(ref_values) == 0:
                continue
            
            # Calcular correlación entre los valores
            try:
                correlation = df_values.corr(ref_values)
                if not pd.isna(correlation):
                    accuracy_scores.append(abs(correlation))
            except:
                # Si no se puede calcular correlación, usar diferencia porcentual
                mean_df = df_values.mean()
                mean_ref = ref_values.mean()
                
                if mean_ref != 0:
                    accuracy = 1 - abs(mean_df - mean_ref) / abs(mean_ref)
                    accuracy_scores.append(max(0, accuracy))
        
        return np.mean(accuracy_scores) if accuracy_scores else 0.0
    
    @staticmethod
    def calculate_overall_quality_score(df: pd.DataFrame, reference_data: pd.DataFrame = None, key_columns: List[str] = None) -> Dict[str, float]:
        """
        Calcular score general de calidad de datos
        
        Args:
            df: DataFrame a evaluar
            reference_data: DataFrame de referencia (opcional)
            key_columns: Columnas clave (opcional)
            
        Returns:
            Dict: Scores de calidad
        """
        scores = {
            'completeness': QualityCalculator.calculate_completeness_score(df),
            'consistency': 0.0,
            'accuracy': 0.0,
            'overall': 0.0
        }
        
        if key_columns:
            scores['consistency'] = QualityCalculator.calculate_consistency_score(df, key_columns)
        
        if reference_data is not None and key_columns:
            scores['accuracy'] = QualityCalculator.calculate_accuracy_score(df, reference_data, key_columns)
        
        # Calcular score general ponderado
        weights = {'completeness': 0.4, 'consistency': 0.3, 'accuracy': 0.3}
        scores['overall'] = sum(scores[key] * weights[key] for key in weights.keys())
        
        return scores

