"""
Integración con BigQuery para Validación Cruzada de Datos
========================================================

Este módulo proporciona funcionalidades para conectar con BigQuery
y obtener datos económicos adicionales para validar la confiabilidad
de los datos de pasajeros.

Requisitos:
- google-cloud-bigquery
- python-dotenv
- Archivo de credenciales JSON
"""

import os
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from google.cloud import bigquery
from google.cloud.exceptions import NotFound, BadRequest
import logging
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BigQueryIntegration:
    """Clase para integración con BigQuery"""
    
    def __init__(self, project_id: Optional[str] = None, credentials_path: Optional[str] = None):
        """
        Inicializa la conexión con BigQuery
        
        Args:
            project_id: ID del proyecto de Google Cloud
            credentials_path: Ruta al archivo de credenciales JSON
        """
        self.project_id = project_id or os.getenv('GOOGLE_CLOUD_PROJECT')
        self.credentials_path = credentials_path or os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        self.dataset_id = os.getenv('BIGQUERY_DATASET', 'passenger_validation')
        self.client = None
        self.dataset = None
        
        if not self.project_id:
            raise ValueError("PROJECT_ID es requerido. Configurar GOOGLE_CLOUD_PROJECT en .env")
        
        self._setup_client()
        self._setup_dataset()
    
    def _setup_client(self):
        """Configura el cliente de BigQuery con autenticación alternativa"""
        try:
            # Intentar con credenciales JSON primero
            if self.credentials_path and os.path.exists(self.credentials_path):
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.credentials_path
                logger.info(f"Usando credenciales desde: {self.credentials_path}")
                self.client = bigquery.Client(project=self.project_id)
                logger.info(f"Cliente BigQuery configurado para proyecto: {self.project_id}")
                return
            
            # Si no hay credenciales JSON, usar autenticación alternativa
            logger.info("No se encontraron credenciales JSON, usando autenticación alternativa...")
            
            # Intentar con Application Default Credentials
            try:
                self.client = bigquery.Client(project=self.project_id)
                logger.info(f"Cliente BigQuery configurado con ADC para proyecto: {self.project_id}")
                return
            except Exception as e:
                logger.warning(f"Error con ADC: {str(e)}")
            
            # Intentar con gcloud auth
            try:
                import subprocess
                result = subprocess.run(['gcloud', 'auth', 'list'], 
                                      capture_output=True, text=True)
                if result.returncode == 0 and "No credentialed accounts" not in result.stdout:
                    self.client = bigquery.Client(project=self.project_id)
                    logger.info(f"Cliente BigQuery configurado con gcloud auth para proyecto: {self.project_id}")
                    return
            except Exception as e:
                logger.warning(f"Error con gcloud auth: {str(e)}")
            
            # Si todo falla, crear cliente sin autenticación (solo para datasets públicos)
            logger.warning("Usando cliente sin autenticación (solo datasets públicos)")
            self.client = bigquery.Client(project=self.project_id)
            
        except Exception as e:
            logger.error(f"Error configurando cliente BigQuery: {str(e)}")
            raise
    
    def _setup_dataset(self):
        """Configura el dataset de BigQuery"""
        try:
            dataset_ref = self.client.dataset(self.dataset_id)
            self.dataset = self.client.get_dataset(dataset_ref)
            logger.info(f"Dataset encontrado: {self.dataset_id}")
            
        except NotFound:
            logger.info(f"Dataset {self.dataset_id} no encontrado. Creando...")
            self._create_dataset()
    
    def _create_dataset(self):
        """Crea el dataset si no existe"""
        try:
            dataset_ref = bigquery.Dataset(f"{self.project_id}.{self.dataset_id}")
            dataset_ref.location = "US"  # Configurar región
            self.dataset = self.client.create_dataset(dataset_ref, timeout=30)
            logger.info(f"Dataset creado: {self.dataset_id}")
            
        except Exception as e:
            logger.error(f"Error creando dataset: {str(e)}")
            raise
    
    def test_connection(self) -> bool:
        """Prueba la conexión con BigQuery"""
        try:
            # Consulta simple para probar conexión
            query = "SELECT 1 as test_value"
            result = self.client.query(query).result()
            
            for row in result:
                if row.test_value == 1:
                    logger.info("✅ Conexión con BigQuery exitosa")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Error en conexión BigQuery: {str(e)}")
            return False
    
    def get_world_bank_data(self, country_codes: List[str], 
                           indicators: List[str], 
                           start_year: int = 2010, 
                           end_year: int = 2019) -> pd.DataFrame:
        """
        Obtiene datos del World Bank desde BigQuery
        
        Args:
            country_codes: Lista de códigos ISO3 de países
            indicators: Lista de indicadores del World Bank
            start_year: Año de inicio
            end_year: Año de fin
            
        Returns:
            DataFrame con datos del World Bank
        """
        try:
            # Construir consulta SQL
            country_list = "', '".join(country_codes)
            indicator_list = "', '".join(indicators)
            
            query = f"""
            SELECT 
                country_code as ISO3,
                year as Year,
                indicator_code as Indicator,
                value as Value,
                'World Bank BigQuery' as Source
            FROM `bigquery-public-data.world_bank_intl_education.international_education`
            WHERE country_code IN ('{country_list}')
            AND indicator_code IN ('{indicator_list}')
            AND year BETWEEN {start_year} AND {end_year}
            AND value IS NOT NULL
            ORDER BY country_code, year, indicator_code
            """
            
            logger.info(f"Ejecutando consulta World Bank para {len(country_codes)} países")
            query_job = self.client.query(query)
            results = query_job.result()
            
            # Convertir a DataFrame
            data = []
            for row in results:
                data.append({
                    'ISO3': row.ISO3,
                    'Year': row.Year,
                    'Indicator': row.Indicator,
                    'Value': row.Value,
                    'Source': row.Source
                })
            
            df = pd.DataFrame(data)
            logger.info(f"✅ Datos World Bank obtenidos: {len(df)} registros")
            return df
            
        except Exception as e:
            logger.error(f"Error obteniendo datos World Bank: {str(e)}")
            return pd.DataFrame()
    
    def get_oecd_data(self, country_codes: List[str], 
                      indicators: List[str], 
                      start_year: int = 2010, 
                      end_year: int = 2019) -> pd.DataFrame:
        """
        Obtiene datos de la OECD desde BigQuery
        
        Args:
            country_codes: Lista de códigos ISO3 de países
            indicators: Lista de indicadores de la OECD
            start_year: Año de inicio
            end_year: Año de fin
            
        Returns:
            DataFrame con datos de la OECD
        """
        try:
            # Construir consulta SQL
            country_list = "', '".join(country_codes)
            indicator_list = "', '".join(indicators)
            
            query = f"""
            SELECT 
                country as ISO3,
                year as Year,
                indicator as Indicator,
                value as Value,
                'OECD BigQuery' as Source
            FROM `bigquery-public-data.oecd_economic_indicators.economic_indicators`
            WHERE country IN ('{country_list}')
            AND indicator IN ('{indicator_list}')
            AND year BETWEEN {start_year} AND {end_year}
            AND value IS NOT NULL
            ORDER BY country, year, indicator
            """
            
            logger.info(f"Ejecutando consulta OECD para {len(country_codes)} países")
            query_job = self.client.query(query)
            results = query_job.result()
            
            # Convertir a DataFrame
            data = []
            for row in results:
                data.append({
                    'ISO3': row.ISO3,
                    'Year': row.Year,
                    'Indicator': row.Indicator,
                    'Value': row.Value,
                    'Source': row.Source
                })
            
            df = pd.DataFrame(data)
            logger.info(f"✅ Datos OECD obtenidos: {len(df)} registros")
            return df
            
        except Exception as e:
            logger.error(f"Error obteniendo datos OECD: {str(e)}")
            return pd.DataFrame()
    
    def get_economic_indicators(self, country_codes: List[str], 
                               start_year: int = 2010, 
                               end_year: int = 2019) -> pd.DataFrame:
        """
        Obtiene indicadores económicos combinados
        
        Args:
            country_codes: Lista de códigos ISO3 de países
            start_year: Año de inicio
            end_year: Año de fin
            
        Returns:
            DataFrame con indicadores económicos combinados
        """
        logger.info("Obteniendo indicadores económicos combinados...")
        
        # Indicadores del World Bank
        wb_indicators = [
            'NY.GDP.MKTP.CD',  # PIB
            'SP.POP.TOTL',     # Población
            'ST.INT.ARVL',     # Llegadas de turistas
            'NY.GDP.PCAP.CD',  # PIB per cápita
            'FP.CPI.TOTL.ZG'   # Inflación
        ]
        
        # Obtener datos del World Bank
        df_wb = self.get_world_bank_data(country_codes, wb_indicators, start_year, end_year)
        
        # Indicadores de la OECD
        oecd_indicators = [
            'GDP',
            'POPULATION',
            'TOURISM_ARRIVALS',
            'GDP_PER_CAPITA',
            'INFLATION'
        ]
        
        # Obtener datos de la OECD
        df_oecd = self.get_oecd_data(country_codes, oecd_indicators, start_year, end_year)
        
        # Combinar datos
        df_combined = pd.concat([df_wb, df_oecd], ignore_index=True)
        
        logger.info(f"✅ Indicadores económicos combinados: {len(df_combined)} registros")
        return df_combined
    
    def create_validation_table(self, df_passengers: pd.DataFrame) -> bool:
        """
        Crea tabla de validación con datos de pasajeros
        
        Args:
            df_passengers: DataFrame con datos de pasajeros
            
        Returns:
            True si la tabla se creó exitosamente
        """
        try:
            table_id = f"{self.project_id}.{self.dataset_id}.passenger_data"
            
            # Configurar esquema
            schema = [
                bigquery.SchemaField("ISO3", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("Year", "INTEGER", mode="REQUIRED"),
                bigquery.SchemaField("Month", "INTEGER", mode="REQUIRED"),
                bigquery.SchemaField("Total", "FLOAT", mode="NULLABLE"),
                bigquery.SchemaField("Total_OS", "FLOAT", mode="NULLABLE"),
                bigquery.SchemaField("Domestic", "FLOAT", mode="NULLABLE"),
                bigquery.SchemaField("International", "FLOAT", mode="NULLABLE"),
            ]
            
            # Crear tabla
            table = bigquery.Table(table_id, schema=schema)
            table = self.client.create_table(table)
            
            logger.info(f"Tabla creada: {table_id}")
            
            # Cargar datos
            job_config = bigquery.LoadJobConfig(
                schema=schema,
                write_disposition="WRITE_TRUNCATE"
            )
            
            job = self.client.load_table_from_dataframe(
                df_passengers, table_id, job_config=job_config
            )
            job.result()
            
            logger.info(f"✅ Datos cargados en tabla: {len(df_passengers)} registros")
            return True
            
        except Exception as e:
            logger.error(f"Error creando tabla de validación: {str(e)}")
            return False
    
    def run_validation_analysis(self, country_codes: List[str]) -> Dict:
        """
        Ejecuta análisis de validación completo
        
        Args:
            country_codes: Lista de códigos ISO3 de países
            
        Returns:
            Diccionario con resultados del análisis
        """
        try:
            logger.info("Iniciando análisis de validación con BigQuery...")
            
            # Obtener indicadores económicos
            df_economic = self.get_economic_indicators(country_codes)
            
            # Consulta de análisis de correlación
            query = f"""
            WITH passenger_stats AS (
                SELECT 
                    ISO3,
                    Year,
                    AVG(Total) as avg_total,
                    AVG(Total_OS) as avg_total_os,
                    STDDEV(Total) as std_total,
                    STDDEV(Total_OS) as std_total_os
                FROM `{self.project_id}.{self.dataset_id}.passenger_data`
                WHERE ISO3 IN ('{"', '".join(country_codes)}')
                GROUP BY ISO3, Year
            ),
            economic_stats AS (
                SELECT 
                    ISO3,
                    Year,
                    AVG(CASE WHEN Indicator = 'NY.GDP.MKTP.CD' THEN Value END) as gdp,
                    AVG(CASE WHEN Indicator = 'SP.POP.TOTL' THEN Value END) as population,
                    AVG(CASE WHEN Indicator = 'ST.INT.ARVL' THEN Value END) as tourism
                FROM `{self.project_id}.{self.dataset_id}.economic_indicators`
                WHERE ISO3 IN ('{"', '".join(country_codes)}')
                GROUP BY ISO3, Year
            )
            SELECT 
                p.ISO3,
                p.Year,
                p.avg_total,
                p.avg_total_os,
                p.std_total,
                p.std_total_os,
                e.gdp,
                e.population,
                e.tourism,
                CORR(p.avg_total, p.avg_total_os) as correlation_official_os,
                CORR(p.avg_total, e.gdp) as correlation_official_gdp,
                CORR(p.avg_total_os, e.gdp) as correlation_os_gdp
            FROM passenger_stats p
            LEFT JOIN economic_stats e ON p.ISO3 = e.ISO3 AND p.Year = e.Year
            ORDER BY p.ISO3, p.Year
            """
            
            query_job = self.client.query(query)
            results = query_job.result()
            
            # Convertir resultados a DataFrame
            data = []
            for row in results:
                data.append({
                    'ISO3': row.ISO3,
                    'Year': row.Year,
                    'avg_total': row.avg_total,
                    'avg_total_os': row.avg_total_os,
                    'std_total': row.std_total,
                    'std_total_os': row.std_total_os,
                    'gdp': row.gdp,
                    'population': row.population,
                    'tourism': row.tourism,
                    'correlation_official_os': row.correlation_official_os,
                    'correlation_official_gdp': row.correlation_official_gdp,
                    'correlation_os_gdp': row.correlation_os_gdp
                })
            
            df_analysis = pd.DataFrame(data)
            
            # Calcular métricas de validación
            validation_metrics = {
                'total_records': len(df_analysis),
                'countries_analyzed': df_analysis['ISO3'].nunique(),
                'avg_correlation_official_os': df_analysis['correlation_official_os'].mean(),
                'avg_correlation_official_gdp': df_analysis['correlation_official_gdp'].mean(),
                'avg_correlation_os_gdp': df_analysis['correlation_os_gdp'].mean(),
                'data_quality_score': self._calculate_data_quality_score(df_analysis)
            }
            
            logger.info("✅ Análisis de validación completado")
            return {
                'analysis_data': df_analysis,
                'economic_data': df_economic,
                'validation_metrics': validation_metrics
            }
            
        except Exception as e:
            logger.error(f"Error en análisis de validación: {str(e)}")
            return {}
    
    def _calculate_data_quality_score(self, df: pd.DataFrame) -> float:
        """Calcula un score de calidad de datos"""
        try:
            # Factores de calidad
            completeness = df.notna().sum().sum() / (len(df) * len(df.columns))
            consistency = 1 - abs(df['correlation_official_os']).mean()
            reliability = df['correlation_official_gdp'].mean()
            
            # Score ponderado
            quality_score = (completeness * 0.4 + consistency * 0.3 + reliability * 0.3)
            return min(max(quality_score, 0), 1)  # Entre 0 y 1
            
        except Exception:
            return 0.0
    
    def get_query_cost_estimate(self, query: str) -> Dict:
        """
        Estima el costo de una consulta
        
        Args:
            query: Consulta SQL
            
        Returns:
            Diccionario con estimación de costo
        """
        try:
            job_config = bigquery.QueryJobConfig(dry_run=True)
            query_job = self.client.query(query, job_config=job_config)
            
            # Obtener bytes procesados
            bytes_processed = query_job.total_bytes_processed
            cost_usd = (bytes_processed / (1024**4)) * 5  # $5 por TB
            
            return {
                'bytes_processed': bytes_processed,
                'cost_usd': cost_usd,
                'cost_formatted': f"${cost_usd:.4f}"
            }
            
        except Exception as e:
            logger.error(f"Error estimando costo: {str(e)}")
            return {'bytes_processed': 0, 'cost_usd': 0, 'cost_formatted': '$0.0000'}

def main():
    """Función principal para testing"""
    try:
        # Inicializar BigQuery
        bq = BigQueryIntegration()
        
        # Probar conexión
        if bq.test_connection():
            print("✅ Conexión con BigQuery exitosa")
            
            # Probar consulta simple
            country_codes = ['USA', 'CAN', 'MEX']
            df = bq.get_economic_indicators(country_codes)
            print(f"✅ Datos obtenidos: {len(df)} registros")
            
        else:
            print("❌ Error en conexión con BigQuery")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
