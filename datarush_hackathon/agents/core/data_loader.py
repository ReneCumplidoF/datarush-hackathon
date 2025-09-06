# components/data_loader.py
import pandas as pd
import streamlit as st
from typing import Dict, Optional, Tuple
import os

class DataLoader:
    """
    Clase para cargar y procesar datos de feriados y pasajeros aéreos
    """
    
    def __init__(self, data_path: str = "datos/"):
        self.data_path = data_path
        self.holidays_data = None
        self.passengers_data = None
        self.countries_data = None
        self.processed_data = None
        
    def load_data(self) -> bool:
        """
        Cargar datos desde archivos CSV
        
        Returns:
            bool: True si se cargaron correctamente, False en caso contrario
        """
        try:
            # Cargar datos de feriados
            holidays_path = os.path.join(self.data_path, "global_holidays.csv")
            if os.path.exists(holidays_path):
                self.holidays_data = pd.read_csv(holidays_path)
                print(f"✅ Datos de feriados cargados: {len(self.holidays_data)} registros")
            else:
                print(f"❌ No se encontró el archivo: {holidays_path}")
                return False
            
            # Cargar datos de pasajeros
            passengers_path = os.path.join(self.data_path, "monthly_passengers.csv")
            if os.path.exists(passengers_path):
                self.passengers_data = pd.read_csv(passengers_path)
                print(f"✅ Datos de pasajeros cargados: {len(self.passengers_data)} registros")
            else:
                print(f"❌ No se encontró el archivo: {passengers_path}")
                return False
            
            # Cargar datos de países
            countries_path = os.path.join(self.data_path, "countries.csv")
            if os.path.exists(countries_path):
                self.countries_data = pd.read_csv(countries_path)
                print(f"✅ Datos de países cargados: {len(self.countries_data)} registros")
            else:
                print(f"❌ No se encontró el archivo: {countries_path}")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Error cargando datos: {str(e)}")
            return False
    
    def clean_data(self) -> bool:
        """
        Limpiar y procesar datos cargados
        
        Returns:
            bool: True si se procesaron correctamente, False en caso contrario
        """
        try:
            if self.holidays_data is None or self.passengers_data is None or self.countries_data is None:
                print("❌ Primero debe cargar los datos")
                return False
            
            # Limpiar datos de feriados
            self.holidays_data['Date'] = pd.to_datetime(self.holidays_data['Date'])
            self.holidays_data['Year'] = self.holidays_data['Date'].dt.year
            self.holidays_data['Month'] = self.holidays_data['Date'].dt.month
            self.holidays_data['Day'] = self.holidays_data['Date'].dt.day
            self.holidays_data['Weekday'] = self.holidays_data['Date'].dt.day_name()
            
            # Limpiar datos de pasajeros
            self.passengers_data['Date'] = pd.to_datetime(
                self.passengers_data[['Year', 'Month']].assign(Day=1)
            )
            
            # Procesar datos de pasajeros - manejar valores vacíos
            print(f"🔍 Debug: Columnas disponibles en pasajeros: {self.passengers_data.columns.tolist()}")
            print(f"🔍 Debug: Valores únicos en Total: {self.passengers_data['Total'].nunique()}")
            print(f"🔍 Debug: Valores únicos en Total_OS: {self.passengers_data['Total_OS'].nunique()}")
            
            # Usar Total_OS como columna principal si Total está vacía
            if 'Total_OS' in self.passengers_data.columns:
                # Llenar Total con Total_OS donde Total esté vacío
                self.passengers_data['Total'] = self.passengers_data['Total'].fillna(self.passengers_data['Total_OS'])
                print(f"🔍 Debug: Después de llenar con Total_OS: {self.passengers_data['Total'].nunique()} valores únicos")
                
                # Si Total sigue vacío, usar la suma de Domestic + International
                mask_total_empty = self.passengers_data['Total'].isna()
                if 'Domestic' in self.passengers_data.columns and 'International' in self.passengers_data.columns:
                    domestic_filled = self.passengers_data['Domestic'].fillna(0)
                    international_filled = self.passengers_data['International'].fillna(0)
                    self.passengers_data.loc[mask_total_empty, 'Total'] = domestic_filled + international_filled
                    print(f"🔍 Debug: Después de llenar con Domestic+International: {self.passengers_data['Total'].nunique()} valores únicos")
            
            # Convertir Total a numérico, manejando errores
            self.passengers_data['Total'] = pd.to_numeric(self.passengers_data['Total'], errors='coerce')
            
            # Mostrar estadísticas antes de filtrar
            print(f"🔍 Debug: Total de registros antes de filtrar: {len(self.passengers_data)}")
            print(f"🔍 Debug: Registros con Total válido: {self.passengers_data['Total'].notna().sum()}")
            print(f"🔍 Debug: Registros con Total > 0: {(self.passengers_data['Total'] > 0).sum()}")
            print(f"🔍 Debug: Países únicos antes de filtrar: {self.passengers_data['ISO3'].nunique()}")
            
            # NO eliminar filas - mantener todos los datos
            # self.passengers_data = self.passengers_data.dropna(subset=['Total'])  # ELIMINADO
            # self.passengers_data = self.passengers_data[self.passengers_data['Total'] > 0]  # ELIMINADO
            
            # Solo eliminar filas donde Total es completamente inválido
            self.passengers_data = self.passengers_data[self.passengers_data['Total'].notna()]
            
            print(f"✅ Datos de pasajeros procesados: {len(self.passengers_data)} registros válidos")
            print(f"✅ Países únicos después de procesar: {self.passengers_data['ISO3'].nunique()}")
            print(f"✅ Rango de pasajeros: {self.passengers_data['Total'].min():.0f} - {self.passengers_data['Total'].max():.0f}")
            
            # Crear datos procesados
            self.processed_data = {
                'holidays': self.holidays_data,
                'passengers': self.passengers_data,
                'countries': self.countries_data
            }
            
            print("✅ Datos procesados correctamente")
            return True
            
        except Exception as e:
            print(f"❌ Error procesando datos: {str(e)}")
            return False
    
    def get_processed_data(self) -> Optional[Dict]:
        """
        Obtener datos procesados
        
        Returns:
            Dict: Diccionario con datos procesados o None si no están disponibles
        """
        return self.processed_data
    
    def get_data_summary(self) -> Dict:
        """
        Obtener resumen de los datos cargados
        
        Returns:
            Dict: Resumen de los datos
        """
        if self.processed_data is None:
            return {"error": "No hay datos procesados"}
        
        holidays = self.processed_data['holidays']
        passengers = self.processed_data['passengers']
        countries = self.processed_data['countries']
        
        return {
            "holidays": {
                "total_records": len(holidays),
                "countries": holidays['ISO3'].nunique(),
                "date_range": f"{holidays['Date'].min().strftime('%Y-%m-%d')} a {holidays['Date'].max().strftime('%Y-%m-%d')}",
                "holiday_types": holidays['Type'].unique().tolist()
            },
            "passengers": {
                "total_records": len(passengers),
                "countries": passengers['ISO3'].nunique(),
                "date_range": f"{passengers['Year'].min()} a {passengers['Year'].max()}",
                "total_passengers": passengers['Total'].sum()
            },
            "countries": {
                "total_countries": len(countries),
                "countries_list": countries['name'].tolist()
            }
        }
    
    def get_filter_options(self) -> Dict:
        """
        Obtener opciones para filtros
        
        Returns:
            Dict: Opciones para cada filtro
        """
        if self.processed_data is None:
            return {}
        
        holidays = self.processed_data['holidays']
        passengers = self.processed_data['passengers']
        countries = self.processed_data['countries']
        
        return {
            "years": sorted(passengers['Year'].unique().tolist()),
            "months": sorted(passengers['Month'].unique().tolist()),
            "countries": sorted(passengers['ISO3'].unique().tolist()),
            "holiday_types": sorted(holidays['Type'].unique().tolist()),
            "continents": sorted(countries['name'].unique().tolist()) if 'continent' in countries.columns else []
        }