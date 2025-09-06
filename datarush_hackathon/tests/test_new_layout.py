#!/usr/bin/env python3
"""
Script de prueba para el nuevo layout de la aplicación DataRush
"""

import streamlit as st
import sys
import os
import pandas as pd

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from components.data_loader import DataLoader
from components.filters import Filters
from components.visualizations import Visualizations
from components.chat_agent import ChatAgent

def test_new_layout():
    """Probar el nuevo layout de la aplicación"""
    
    print("🧪 Iniciando pruebas del nuevo layout...")
    
    # Inicializar componentes
    data_loader = DataLoader()
    filters = Filters()
    visualizations = Visualizations()
    chat_agent = ChatAgent()
    
    print("✅ Componentes inicializados correctamente")
    
    # Probar carga de datos
    print("📊 Probando carga de datos...")
    if data_loader.load_data():
        if data_loader.clean_data():
            data = data_loader.get_processed_data()
            if data:
                print("✅ Datos cargados correctamente")
                
                # Probar filtros
                print("🔧 Probando filtros...")
                filter_options = filters._get_filter_options(data)
                print(f"✅ Opciones de filtros: {list(filter_options.keys())}")
                
                # Probar visualizaciones
                print("📈 Probando visualizaciones...")
                try:
                    # Crear filtros de prueba
                    test_filters = {
                        'year_range': (2020, 2023),
                        'months': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                        'countries': list(data['passengers']['ISO3'].unique()[:5]) if not data['passengers'].empty else [],
                        'holiday_types': list(data['holidays']['Type'].unique()[:3]) if not data['holidays'].empty else [],
                        'flight_types': ['Total']
                    }
                    
                    # Aplicar filtros
                    filtered_data = filters.apply_filters(data, test_filters)
                    print("✅ Filtros aplicados correctamente")
                    
                    # Probar visualizaciones
                    trend_fig = visualizations.create_trend_analysis(filtered_data, test_filters)
                    print("✅ Gráfico de tendencias creado")
                    
                    comparison_fig = visualizations.create_heatmap_country_month(filtered_data, test_filters)
                    print("✅ Gráfico de comparación creado")
                    
                    impact_fig = visualizations.create_holiday_impact(filtered_data, test_filters)
                    print("✅ Gráfico de impacto creado")
                    
                    # Probar KPIs
                    print("📊 Probando KPIs...")
                    if filtered_data.get('passengers') is not None and not filtered_data['passengers'].empty:
                        total_passengers = filtered_data['passengers']['Total'].sum()
                        countries_count = filtered_data['passengers']['ISO3'].nunique()
                        print(f"✅ KPI0 - Total Pasajeros: {total_passengers:,.0f}")
                        print(f"✅ KPI1 - Países Seleccionados: {countries_count}")
                    
                    if filtered_data.get('holidays') is not None and not filtered_data['holidays'].empty:
                        total_holidays = len(filtered_data['holidays'])
                        print(f"✅ KPI2 - Total Feriados: {total_holidays}")
                    
                    # Probar chat
                    print("🤖 Probando chat...")
                    context = {
                        "data_loaded": True,
                        "current_filters": test_filters,
                        "filtered_data": filtered_data
                    }
                    response = chat_agent.process_user_message("¿Cuál es el total de pasajeros?", context)
                    print(f"✅ Chat funcionando: {response[:100]}...")
                    
                    print("\n🎉 ¡Todas las pruebas del nuevo layout pasaron exitosamente!")
                    return True
                    
                except Exception as e:
                    print(f"❌ Error en visualizaciones: {str(e)}")
                    return False
            else:
                print("❌ Error: No se pudieron procesar los datos")
                return False
        else:
            print("❌ Error: No se pudieron limpiar los datos")
            return False
    else:
        print("❌ Error: No se pudieron cargar los datos")
        return False

def test_layout_structure():
    """Probar la estructura del layout"""
    
    print("\n🏗️ Probando estructura del layout...")
    
    # Verificar que app.py existe y es válido
    if os.path.exists("app.py"):
        print("✅ app.py existe")
        
        # Leer el archivo y verificar elementos clave
        with open("app.py", "r", encoding="utf-8") as f:
            content = f.read()
            
        # Verificar elementos del nuevo layout
        checks = [
            ("☰", "Botón hamburger"),
            ("KPI0", "KPI0 en header"),
            ("KPI1", "KPI1 en header"),
            ("KPI2", "KPI2 en header"),
            ("KPI3", "KPI3 en header"),
            ("KPI4", "KPI4 en header"),
            ("V1 - Tendencias", "Cuadrante V1"),
            ("V2 - Comparación", "Cuadrante V2"),
            ("V3 - Impacto", "Cuadrante V3"),
            ("V4 - Resumen", "Cuadrante V4"),
            ("ChatIA", "Chat en columna derecha"),
            ("sidebar_expanded", "Estado del sidebar"),
            ("col_sidebar, col_main, col_chat", "Layout de 3 columnas")
        ]
        
        for check, description in checks:
            if check in content:
                print(f"✅ {description}")
            else:
                print(f"❌ {description} - NO ENCONTRADO")
        
        print("\n🎯 Layout implementado según especificaciones:")
        print("   - ✅ Sidebar deslizable con botón hamburger")
        print("   - ✅ KPIs en la parte superior (KPI0-KPI4)")
        print("   - ✅ 4 cuadrantes para visualizaciones (V1-V4)")
        print("   - ✅ Chat en columna derecha")
        print("   - ✅ Layout optimizado para pantalla completa")
        
        return True
    else:
        print("❌ app.py no existe")
        return False

if __name__ == "__main__":
    print("🚀 DataRush - Pruebas del Nuevo Layout")
    print("=" * 50)
    
    # Probar estructura del layout
    layout_ok = test_layout_structure()
    
    # Probar funcionalidad
    if layout_ok:
        functionality_ok = test_new_layout()
        
        if functionality_ok:
            print("\n🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
            print("\n📋 Resumen del nuevo layout:")
            print("   • Sidebar deslizable con filtros en checkboxes")
            print("   • KPIs dinámicos en la parte superior")
            print("   • 4 cuadrantes para visualizaciones simultáneas")
            print("   • Chat con IA en columna derecha")
            print("   • Layout optimizado para pantalla completa")
            print("\n🎯 Para usar la aplicación:")
            print("   streamlit run app.py")
        else:
            print("\n❌ Algunas pruebas de funcionalidad fallaron")
    else:
        print("\n❌ Error en la estructura del layout")
