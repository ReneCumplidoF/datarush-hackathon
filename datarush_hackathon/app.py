# app.py
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
from agents.extensions.data_analysis_agent.simple_integration import simple_data_analysis_agent
from agents.extensions.business_advisor_agent.simple_integration import simple_business_advisor
from agents.extensions.research_agent.simple_integration import simple_research_agent
from agents.master_agent.simple_integration import simple_master_agent

def main():
    st.set_page_config(
        page_title="AirFlow - Holiday Pattern Analysis",
        page_icon="✈️",
        layout="wide"
    )
    
    # Cargar CSS personalizado para tema AirFlow
    with open('airflow_theme.css', 'r', encoding='utf-8') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    # Inicializar session state
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False
    if 'data' not in st.session_state:
        st.session_state.data = {}
    if 'filters' not in st.session_state:
        st.session_state.filters = {}
    if 'sidebar_expanded' not in st.session_state:
        st.session_state.sidebar_expanded = False
    
    # Inicializar componentes
    data_loader = DataLoader()
    filters = Filters()
    visualizations = Visualizations()
    chat_agent = ChatAgent()
    
    # Header principal con logo AirFlow
    st.markdown("""
    <div class="airflow-title">
        <div class="airflow-logo"></div>
        <h1 class="airflow-title-text">AirFlow - Análisis de Patrones de Feriados</h1>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    # Top Row: Selección de modo y cargar archivos + KPIs
    col_header1, col_header2, col_header3, col_header4, col_header5, col_header6 = st.columns([2, 1, 1, 1, 1, 1])
    
    with col_header1:
        st.subheader("📊 Selección de Modo y Cargar Archivos")
        if st.button("🔄 Cargar Datos", type="primary"):
            with st.spinner("Cargando datos..."):
                try:
                    if data_loader.load_data():
                        if data_loader.clean_data():
                            st.session_state.data = data_loader.get_processed_data()
                            if st.session_state.data:
                                st.session_state.data_loaded = True
                                st.success("✅ Datos cargados correctamente")
                            else:
                                st.error("❌ Error al procesar los datos")
                        else:
                            st.error("❌ Error al limpiar los datos")
                    else:
                        st.error("❌ Error al cargar los archivos")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # KPIs en la parte superior
    if st.session_state.data_loaded and st.session_state.data:
        # Aplicar filtros a los datos para KPIs
        filtered_data = filters.apply_filters(st.session_state.data, st.session_state.filters)
        
        with col_header2:
            if filtered_data.get('passengers') is not None and not filtered_data['passengers'].empty:
                total_passengers = filtered_data['passengers']['Total'].sum()
                st.metric("Total Pasajeros", f"{total_passengers:,.0f}")
            else:
                st.metric("Total Pasajeros", "0")
        
        with col_header3:
            if filtered_data.get('passengers') is not None and not filtered_data['passengers'].empty:
                countries_count = filtered_data['passengers']['ISO3'].nunique()
                st.metric("Países Seleccionados", countries_count)
            else:
                st.metric("Países Seleccionados", "0")
        
        with col_header4:
            if filtered_data.get('holidays') is not None and not filtered_data['holidays'].empty:
                total_holidays = len(filtered_data['holidays'])
                st.metric("Total Feriados", total_holidays)
            else:
                st.metric("Total Feriados", "0")
        
        with col_header5:
            if filtered_data.get('passengers') is not None and not filtered_data['passengers'].empty:
                peak_month = filtered_data['passengers'].groupby('Month')['Total'].sum().idxmax()
                month_names = {1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr', 5: 'May', 6: 'Jun',
                              7: 'Jul', 8: 'Ago', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic'}
                st.metric("Mes Pico", month_names.get(peak_month, peak_month))
            else:
                st.metric("Mes Pico", "N/A")
        
        with col_header6:
            if filtered_data.get('passengers') is not None and not filtered_data['passengers'].empty:
                avg_passengers = filtered_data['passengers']['Total'].mean()
                st.metric("Promedio Pasajeros", f"{avg_passengers:,.0f}")
            else:
                st.metric("Promedio Pasajeros", "0")
    else:
        # Mostrar KPIs vacíos cuando no hay datos
        with col_header2:
            st.metric("Total Pasajeros", "0")
        with col_header3:
            st.metric("Países Seleccionados", "0")
        with col_header4:
            st.metric("Total Feriados", "0")
        with col_header5:
            st.metric("Mes Pico", "N/A")
        with col_header6:
            st.metric("Promedio Pasajeros", "0")
    
    st.markdown("---")
    
    # Layout principal: Sidebar + Contenido + Chat (chat regresado a la derecha)
    if st.session_state.sidebar_expanded:
        # Cuando el menú está abierto, dar más espacio a las gráficas
        col_sidebar, col_main, col_chat = st.columns([0.25, 0.5, 0.25])
    else:
        # Cuando el menú está cerrado, distribución más equilibrada
        col_sidebar, col_main, col_chat = st.columns([0.2, 0.5, 0.3])
    
    # Sidebar deslizable con filtros
    with col_sidebar:
        st.markdown("### 🔧 Filtros")
        
        # Botón hamburger para expandir/colapsar
        if st.button("☰", help="Expandir/Colapsar Filtros"):
            st.session_state.sidebar_expanded = not st.session_state.sidebar_expanded
        
        # Mostrar filtros solo si están expandidos
        if st.session_state.sidebar_expanded and st.session_state.data_loaded and st.session_state.data:
            # Crear filtros
            st.session_state.filters = filters.create_sidebar_filters(st.session_state.data)
        elif not st.session_state.data_loaded:
            st.info("⚠️ Carga datos primero para usar filtros")
    
    # Contenido principal con 4 cuadrantes
    with col_main:
        if st.session_state.data_loaded and st.session_state.data:
            # Validar que los datos sean un diccionario
            if not isinstance(st.session_state.data, dict):
                st.error("❌ Error: Los datos no están en el formato correcto")
                st.stop()
            
            # Aplicar filtros a los datos
            filtered_data = filters.apply_filters(st.session_state.data, st.session_state.filters)
            
            # Validar que filtered_data sea un diccionario
            if not isinstance(filtered_data, dict):
                st.error("❌ Error: Los datos filtrados no están en el formato correcto")
                st.stop()
            
            # 4 Cuadrantes para visualizaciones
            st.markdown("### 📊 Visualizaciones")
            
            # Cuadrante 1 (V1) - Tendencias
            with st.container():
                st.markdown("#### 📈 V1 - Tendencias de Pasajeros")
                trend_fig = visualizations.create_trend_analysis(filtered_data, st.session_state.filters)
                st.plotly_chart(trend_fig, use_container_width=True, key="trend_chart")
            
            # Cuadrante 2 (V2) - Comparación
            with st.container():
                st.markdown("#### 🌍 V2 - Comparación por País")
                comparison_fig = visualizations.create_heatmap_country_month(filtered_data, st.session_state.filters)
                st.plotly_chart(comparison_fig, use_container_width=True, key="comparison_chart")
            
            # Cuadrante 3 (V3) - Impacto
            with st.container():
                st.markdown("#### 📊 V3 - Impacto de Feriados")
                impact_fig = visualizations.create_holiday_impact(filtered_data, st.session_state.filters)
                st.plotly_chart(impact_fig, use_container_width=True, key="impact_chart")
            
            # Cuadrante 4 (V4) - Resumen
            with st.container():
                st.markdown("#### 📋 V4 - Resumen Ejecutivo")
                
                # Métricas detalladas
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if filtered_data.get('passengers') is not None and not filtered_data['passengers'].empty:
                        total_passengers = filtered_data['passengers']['Total'].sum()
                        st.metric("Total Pasajeros", f"{total_passengers:,.0f}")
                    else:
                        st.metric("Total Pasajeros", "0")
                
                with col2:
                    if filtered_data.get('holidays') is not None and not filtered_data['holidays'].empty:
                        total_holidays = len(filtered_data['holidays'])
                        st.metric("Total Feriados", total_holidays)
                    else:
                        st.metric("Total Feriados", "0")
                
                with col3:
                    if filtered_data.get('passengers') is not None and not filtered_data['passengers'].empty:
                        countries_count = filtered_data['passengers']['ISO3'].nunique()
                        st.metric("Países Analizados", countries_count)
                    else:
                        st.metric("Países Analizados", "0")
                
                with col4:
                    if filtered_data.get('passengers') is not None and not filtered_data['passengers'].empty:
                        peak_month = filtered_data['passengers'].groupby('Month')['Total'].sum().idxmax()
                        month_names = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
                                      7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}
                        st.metric("Mes Pico", month_names.get(peak_month, peak_month))
                    else:
                        st.metric("Mes Pico", "N/A")
                
                # KPIs adicionales
                st.markdown("#### 📊 KPIs Principales")
                metrics = visualizations.create_kpi_metrics(filtered_data, st.session_state.filters)
                visualizations._display_kpi_metrics(metrics)
        else:
            st.info(" Usa el botón 'Cargar Datos' para comenzar el análisis")
            
            # Mostrar información sobre la aplicación
            st.markdown("""
            ## 🚀 AirFlow - Análisis de Patrones de Feriados
            
            Esta aplicación te permite analizar el impacto de los feriados en el tráfico aéreo.
            
            ### 📋 Características:
            - **Análisis de tendencias** de pasajeros por mes
            - **Comparación entre países** y regiones
            - **Impacto de feriados** en el tráfico aéreo
            - **Filtros avanzados** para análisis específicos
            - **Visualizaciones interactivas** con Plotly
            
            ### 🎯 Cómo usar:
            1. Haz clic en "Cargar Datos" en la parte superior
            2. Espera a que se procesen los datos
            3. Usa el botón ☰ para expandir los filtros
            4. Explora las diferentes visualizaciones en los 4 cuadrantes
            """)
    
    # Chat en columna derecha (regresado a la derecha)
    with col_chat:
        st.markdown("### 🤖 ChatIA")
        st.markdown("Pregunta sobre los datos de feriados y pasajeros")
        
        # Selector de agente
        agent_type = st.selectbox(
            "Selecciona el tipo de agente:",
            ["Agente Maestro", "Chat General", "Análisis de Datos", "Asesor de Negocios", "Investigador"],
            help="El Agente Maestro coordina múltiples agentes especializados para tareas complejas. Los otros agentes proporcionan capacidades específicas."
        )
        
        # Inicializar historial de chat
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        # Mostrar historial de chat
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Input de chat
        user_input = st.chat_input("Escribe tu pregunta aquí...")
        
        if user_input:
            # Agregar mensaje del usuario al historial
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Mostrar mensaje del usuario
            with st.chat_message("user"):
                st.markdown(user_input)
            
            # Procesar consulta con el agente seleccionado
            with st.spinner("🤖 Pensando..."):
                # Preparar contexto con datos disponibles
                if st.session_state.data_loaded and st.session_state.data:
                    # Validar que los datos sean un diccionario
                    if not isinstance(st.session_state.data, dict):
                        response = f"❌ Error: Los datos no están en el formato correcto. Tipo recibido: {type(st.session_state.data)}"
                    else:
                        # Aplicar filtros a los datos para el contexto
                        context_filtered_data = filters.apply_filters(st.session_state.data, st.session_state.filters)
                        
                        # Validar que filtered_data sea un diccionario
                        if not isinstance(context_filtered_data, dict):
                            response = f"❌ Error: Los datos filtrados no están en el formato correcto. Tipo recibido: {type(context_filtered_data)}"
                        else:
                            context = {
                                "data_loaded": True,
                                "current_filters": st.session_state.filters,
                                "data": context_filtered_data,
                                "filtered_data": context_filtered_data
                            }
                            
                            # Procesar consulta con el agente seleccionado solo si no hay errores
                            if agent_type == "Agente Maestro":
                                # Usar el agente maestro que coordina múltiples agentes
                                try:
                                    master_results = simple_master_agent.process_query(user_input, context)
                                    
                                    # Handle different result types
                                    if isinstance(master_results, dict):
                                        if master_results.get("success", False):
                                            response = simple_master_agent.get_comprehensive_summary(master_results)
                                        else:
                                            response = f"❌ Error: {master_results.get('error', 'Error desconocido')}"
                                    else:
                                        # If master_results is not a dict, treat it as a string response
                                        response = str(master_results)
                                except Exception as e:
                                    response = f"❌ Error en Master Agent: {str(e)}"
                            elif agent_type == "Análisis de Datos":
                                # Usar el agente de análisis de datos
                                analysis_results = simple_data_analysis_agent.analyze_user_query(user_input, context)
                                
                                if analysis_results.get("error", False):
                                    response = f"❌ Error: {analysis_results.get('message', 'Error desconocido')}"
                                else:
                                    response = simple_data_analysis_agent.get_analysis_summary(analysis_results)
                                    
                                    # Mostrar visualizaciones si están disponibles
                                    if 'visualizations' in analysis_results and analysis_results['visualizations']:
                                        for viz in analysis_results['visualizations']:
                                            try:
                                                fig = viz.get('figure')
                                                if fig:
                                                    st.plotly_chart(fig, use_container_width=True)
                                            except ImportError:
                                                st.warning("⚠️ Plotly no está disponible para mostrar visualizaciones")
                                            except Exception as e:
                                                st.warning(f"⚠️ Error mostrando visualización: {str(e)}")
                            elif agent_type == "Asesor de Negocios":
                                # Usar el agente asesor de negocios
                                business_results = simple_business_advisor.analyze_business_query(user_input, context)
                                
                                if business_results.get("error", False):
                                    response = f"❌ Error: {business_results.get('message', 'Error desconocido')}"
                                else:
                                    response = simple_business_advisor.get_business_summary(business_results)
                            elif agent_type == "Investigador":
                                # Usar el agente investigador
                                research_results = simple_research_agent.research_topic(user_input, context)
                                
                                if research_results.get("error", False):
                                    response = f"❌ Error: {research_results.get('message', 'Error desconocido')}"
                                else:
                                    response = simple_research_agent.get_research_summary(research_results)
                            else:
                                # Usar el chat agent original
                                response = chat_agent.process_user_message(user_input, context)
                else:
                    context = {
                        "data_loaded": False,
                        "current_filters": {},
                        "data": {},
                        "filtered_data": {}
                    }
                    
                    # Procesar consulta con el agente seleccionado para datos no cargados
                    if agent_type == "Agente Maestro":
                        # Usar el agente maestro que coordina múltiples agentes
                        master_results = simple_master_agent.process_query(user_input, context)
                        
                        # Handle different result types
                        if isinstance(master_results, dict):
                            if master_results.get("success", False):
                                response = simple_master_agent.get_comprehensive_summary(master_results)
                            else:
                                response = f"❌ Error: {master_results.get('error', 'Error desconocido')}"
                        else:
                            # If master_results is not a dict, treat it as a string response
                            response = str(master_results)
                    elif agent_type == "Análisis de Datos":
                        # Usar el agente de análisis de datos
                        analysis_results = simple_data_analysis_agent.analyze_user_query(user_input, context)
                        
                        if analysis_results.get("error", False):
                            response = f"❌ Error: {analysis_results.get('message', 'Error desconocido')}"
                        else:
                            response = simple_data_analysis_agent.get_analysis_summary(analysis_results)
                    elif agent_type == "Asesor de Negocios":
                        # Usar el agente asesor de negocios
                        business_results = simple_business_advisor.analyze_business_query(user_input, context)
                        
                        if business_results.get("error", False):
                            response = f"❌ Error: {business_results.get('message', 'Error desconocido')}"
                        else:
                            response = simple_business_advisor.get_business_summary(business_results)
                    elif agent_type == "Investigador":
                        # Usar el agente investigador
                        research_results = simple_research_agent.research_topic(user_input, context)
                        
                        if research_results.get("error", False):
                            response = f"❌ Error: {research_results.get('message', 'Error desconocido')}"
                        else:
                            response = simple_research_agent.get_research_summary(research_results)
                    else:
                        # Usar el chat agent original
                        response = chat_agent.process_user_message(user_input, context)
            
            # Agregar respuesta al historial
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            
            # Mostrar respuesta
            with st.chat_message("assistant"):
                st.markdown(response)
        
        # Botón para limpiar chat
        if st.button("🗑️ Limpiar Chat"):
            st.session_state.chat_history = []
            st.rerun()

if __name__ == "__main__":
    main()