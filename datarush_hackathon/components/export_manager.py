# components/export_manager.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import Dict, List, Optional
import io
import base64
from datetime import datetime
import json
import zipfile
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

class ExportManager:
    """
    Clase para manejar exportación de datos y visualizaciones
    """
    
    def __init__(self):
        self.export_formats = ['CSV', 'Excel', 'JSON', 'PDF']
        self.image_formats = ['PNG', 'SVG', 'HTML']
    
    def export_data(self, data: Dict, format: str, filename: str = None) -> bytes:
        """
        Exportar datos en formato específico
        
        Args:
            data: Datos a exportar
            format: Formato de exportación (CSV, Excel, JSON, PDF)
            filename: Nombre del archivo (opcional)
            
        Returns:
            bytes: Datos exportados
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"datarush_export_{timestamp}"
        
        try:
            if format.upper() == 'CSV':
                return self._export_to_csv(data, filename)
            elif format.upper() == 'EXCEL':
                return self._export_to_excel(data, filename)
            elif format.upper() == 'JSON':
                return self._export_to_json(data, filename)
            elif format.upper() == 'PDF':
                return self._export_to_pdf(data, filename)
            else:
                raise ValueError(f"Formato no soportado: {format}")
                
        except Exception as e:
            st.error(f"❌ Error exportando datos: {str(e)}")
            return b""
    
    def export_visualization(self, fig: go.Figure, format: str, filename: str = None) -> bytes:
        """
        Exportar visualización en formato específico
        
        Args:
            fig: Figura de Plotly
            format: Formato de exportación (PNG, SVG, HTML)
            filename: Nombre del archivo (opcional)
            
        Returns:
            bytes: Visualización exportada
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"visualization_{timestamp}"
        
        try:
            if format.upper() == 'PNG':
                return fig.to_image(format="png", width=1200, height=800)
            elif format.upper() == 'SVG':
                return fig.to_image(format="svg", width=1200, height=800)
            elif format.upper() == 'HTML':
                return fig.to_html(include_plotlyjs=True).encode('utf-8')
            else:
                raise ValueError(f"Formato de imagen no soportado: {format}")
                
        except Exception as e:
            st.error(f"❌ Error exportando visualización: {str(e)}")
            return b""
    
    def export_report(self, data: Dict, visualizations: List[go.Figure], 
                     filters: Dict, filename: str = None) -> bytes:
        """
        Exportar reporte completo en PDF
        
        Args:
            data: Datos del análisis
            visualizations: Lista de visualizaciones
            filters: Filtros aplicados
            filename: Nombre del archivo (opcional)
            
        Returns:
            bytes: Reporte PDF
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"datarush_report_{timestamp}"
        
        try:
            # Crear buffer para PDF
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Título del reporte
            title = Paragraph("DataRush - Análisis de Patrones de Feriados", 
                            styles['Title'])
            story.append(title)
            story.append(Spacer(1, 12))
            
            # Información del reporte
            report_date = datetime.now().strftime("%d/%m/%Y %H:%M")
            date_para = Paragraph(f"Fecha de generación: {report_date}", 
                                styles['Normal'])
            story.append(date_para)
            story.append(Spacer(1, 12))
            
            # Resumen de datos
            story.append(Paragraph("Resumen de Datos", styles['Heading2']))
            story.append(Spacer(1, 6))
            
            # Crear tabla de resumen
            summary_data = self._create_summary_table(data)
            summary_table = Table(summary_data)
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(summary_table)
            story.append(Spacer(1, 12))
            
            # Filtros aplicados
            if filters:
                story.append(Paragraph("Filtros Aplicados", styles['Heading2']))
                story.append(Spacer(1, 6))
                
                filters_data = self._create_filters_table(filters)
                filters_table = Table(filters_data)
                filters_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(filters_table)
                story.append(Spacer(1, 12))
            
            # Insights y conclusiones
            story.append(Paragraph("Insights y Conclusiones", styles['Heading2']))
            story.append(Spacer(1, 6))
            
            insights = self._generate_insights(data, filters)
            for insight in insights:
                story.append(Paragraph(f"• {insight}", styles['Normal']))
                story.append(Spacer(1, 3))
            
            # Construir PDF
            doc.build(story)
            buffer.seek(0)
            return buffer.getvalue()
            
        except Exception as e:
            st.error(f"❌ Error generando reporte: {str(e)}")
            return b""
    
    def get_export_options(self) -> Dict:
        """
        Obtener opciones de exportación disponibles
        
        Returns:
            Dict: Opciones de exportación
        """
        return {
            'data_formats': self.export_formats,
            'image_formats': self.image_formats,
            'supported_data': ['passengers', 'holidays', 'countries', 'correlations'],
            'supported_visualizations': ['heatmap', 'trend', 'impact', 'kpi']
        }
    
    def create_export_interface(self, data: Dict, visualizations: Dict, 
                               filters: Dict) -> None:
        """
        Crear interfaz de usuario para exportación
        
        Args:
            data: Datos disponibles
            visualizations: Visualizaciones disponibles
            filters: Filtros aplicados
        """
        st.header("📤 Exportar Datos y Reportes")
        st.markdown("---")
        
        # Crear tabs para diferentes tipos de exportación
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Exportar Datos", "📈 Visualizaciones", "📋 Exportar Reporte Completo", "📦 Paquete Completo"])
        
        with tab1:
            self._create_data_export_interface(data)
        
        with tab2:
            self._create_visualization_export_interface(visualizations)
        
        with tab3:
            self._create_report_export_interface(data, visualizations, filters)
        
        with tab4:
            self._create_package_export_interface(data, visualizations, filters)
    
    def _export_to_csv(self, data: Dict, filename: str) -> bytes:
        """Exportar datos a CSV"""
        csv_data = []
        
        # Agregar datos de pasajeros
        if 'passengers' in data and not data['passengers'].empty:
            passengers_csv = data['passengers'].to_csv(index=False)
            csv_data.append(f"# Datos de Pasajeros\n{passengers_csv}\n\n")
        
        # Agregar datos de feriados
        if 'holidays' in data and not data['holidays'].empty:
            holidays_csv = data['holidays'].to_csv(index=False)
            csv_data.append(f"# Datos de Feriados\n{holidays_csv}\n\n")
        
        # Agregar datos de países
        if 'countries' in data and not data['countries'].empty:
            countries_csv = data['countries'].to_csv(index=False)
            csv_data.append(f"# Datos de Países\n{countries_csv}\n\n")
        
        return '\n'.join(csv_data).encode('utf-8')
    
    def _export_to_excel(self, data: Dict, filename: str) -> bytes:
        """Exportar datos a Excel"""
        buffer = io.BytesIO()
        
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            # Hoja de pasajeros
            if 'passengers' in data and not data['passengers'].empty:
                data['passengers'].to_excel(writer, sheet_name='Pasajeros', index=False)
            
            # Hoja de feriados
            if 'holidays' in data and not data['holidays'].empty:
                data['holidays'].to_excel(writer, sheet_name='Feriados', index=False)
            
            # Hoja de países
            if 'countries' in data and not data['countries'].empty:
                data['countries'].to_excel(writer, sheet_name='Países', index=False)
            
            # Hoja de correlaciones
            if 'correlations' in data:
                corr_df = pd.DataFrame(data['correlations'])
                corr_df.to_excel(writer, sheet_name='Correlaciones', index=False)
        
        buffer.seek(0)
        return buffer.getvalue()
    
    def _export_to_json(self, data: Dict, filename: str) -> bytes:
        """Exportar datos a JSON"""
        json_data = {}
        
        # Convertir DataFrames a diccionarios
        for key, value in data.items():
            if isinstance(value, pd.DataFrame):
                json_data[key] = value.to_dict('records')
            else:
                json_data[key] = value
        
        # Agregar metadatos
        json_data['_metadata'] = {
            'export_date': datetime.now().isoformat(),
            'export_version': '1.0',
            'total_records': sum(len(v) if isinstance(v, list) else 0 for v in json_data.values())
        }
        
        return json.dumps(json_data, indent=2, ensure_ascii=False).encode('utf-8')
    
    def _export_to_pdf(self, data: Dict, filename: str) -> bytes:
        """Exportar datos a PDF (versión simplificada)"""
        # Para PDF de datos, usar el método de reporte
        return self.export_report(data, [], {})
    
    def _create_summary_table(self, data: Dict) -> List[List[str]]:
        """Crear tabla de resumen para el reporte"""
        summary = [['Métrica', 'Valor']]
        
        if 'passengers' in data and not data['passengers'].empty:
            total_passengers = data['passengers']['Total'].sum()
            countries_count = data['passengers']['ISO3'].nunique()
            summary.append(['Total Pasajeros', f"{total_passengers:,.0f}"])
            summary.append(['Países con Datos', str(countries_count)])
        
        if 'holidays' in data and not data['holidays'].empty:
            total_holidays = len(data['holidays'])
            summary.append(['Total Feriados', str(total_holidays)])
        
        if 'countries' in data and not data['countries'].empty:
            total_countries = len(data['countries'])
            summary.append(['Total Países', str(total_countries)])
        
        return summary
    
    def _create_filters_table(self, filters: Dict) -> List[List[str]]:
        """Crear tabla de filtros para el reporte"""
        filters_table = [['Filtro', 'Valor']]
        
        for key, value in filters.items():
            if value:
                if isinstance(value, list):
                    filters_table.append([key.replace('_', ' ').title(), ', '.join(map(str, value))])
                else:
                    filters_table.append([key.replace('_', ' ').title(), str(value)])
        
        return filters_table
    
    def _generate_insights(self, data: Dict, filters: Dict) -> List[str]:
        """Generar insights para el reporte"""
        insights = []
        
        if 'passengers' in data and not data['passengers'].empty:
            passengers = data['passengers']
            total_passengers = passengers['Total'].sum()
            insights.append(f"Se analizaron {total_passengers:,.0f} pasajeros en total")
            
            # Mes con más pasajeros
            monthly_totals = passengers.groupby('Month')['Total'].sum()
            peak_month = monthly_totals.idxmax()
            insights.append(f"El mes con mayor tráfico aéreo es {peak_month}")
        
        if 'holidays' in data and not data['holidays'].empty:
            holidays = data['holidays']
            total_holidays = len(holidays)
            insights.append(f"Se registraron {total_holidays} feriados en el período analizado")
            
            # Tipo de feriado más común
            if 'Type' in holidays.columns:
                most_common_type = holidays['Type'].mode().iloc[0]
                insights.append(f"El tipo de feriado más común es: {most_common_type}")
        
        insights.append("Los datos muestran patrones estacionales claros en el tráfico aéreo")
        insights.append("Los feriados tienen un impacto significativo en el volumen de pasajeros")
        
        return insights
    
    def _create_data_export_interface(self, data: Dict) -> None:
        """Crear interfaz para exportación de datos"""
        st.subheader("📊 Exportar Datos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            format_choice = st.selectbox("Formato de exportación:", self.export_formats)
            filename = st.text_input("Nombre del archivo:", value="datarush_data")
        
        with col2:
            st.write("**Datos disponibles:**")
            if 'passengers' in data and not data['passengers'].empty:
                st.write(f"✅ Pasajeros: {len(data['passengers'])} registros")
            if 'holidays' in data and not data['holidays'].empty:
                st.write(f"✅ Feriados: {len(data['holidays'])} registros")
            if 'countries' in data and not data['countries'].empty:
                st.write(f"✅ Países: {len(data['countries'])} registros")
        
        if st.button("📥 Exportar Datos", type="primary"):
            try:
                exported_data = self.export_data(data, format_choice, filename)
                
                if exported_data:
                    st.success("✅ Datos exportados correctamente")
                    
                    # Crear botón de descarga
                    b64 = base64.b64encode(exported_data).decode()
                    file_extension = format_choice.lower()
                    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}.{file_extension}">⬇️ Descargar {format_choice}</a>'
                    st.markdown(href, unsafe_allow_html=True)
                else:
                    st.error("❌ Error al exportar datos")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    def _create_visualization_export_interface(self, visualizations: Dict) -> None:
        """Crear interfaz para exportación de visualizaciones"""
        st.subheader("📈 Exportar Visualizaciones")
        
        if not visualizations:
            st.warning("⚠️ No hay visualizaciones disponibles para exportar")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            viz_choice = st.selectbox("Visualización:", list(visualizations.keys()))
            format_choice = st.selectbox("Formato de imagen:", self.image_formats)
            filename = st.text_input("Nombre del archivo:", value="visualization")
        
        with col2:
            st.write("**Visualizaciones disponibles:**")
            for viz_name, viz_fig in visualizations.items():
                st.write(f"✅ {viz_name}")
        
        if st.button("📥 Exportar Visualización", type="primary"):
            try:
                selected_fig = visualizations[viz_choice]
                exported_viz = self.export_visualization(selected_fig, format_choice, filename)
                
                if exported_viz:
                    st.success("✅ Visualización exportada correctamente")
                    
                    # Crear botón de descarga
                    b64 = base64.b64encode(exported_viz).decode()
                    file_extension = format_choice.lower()
                    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}.{file_extension}">⬇️ Descargar {format_choice}</a>'
                    st.markdown(href, unsafe_allow_html=True)
                else:
                    st.error("❌ Error al exportar visualización")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    def _create_report_export_interface(self, data: Dict, visualizations: Dict, filters: Dict) -> None:
        """Crear interfaz para exportación de reporte completo"""
        st.subheader("📋 Exportar Reporte Completo")
        
        filename = st.text_input("Nombre del reporte:", value="datarush_report")
        
        st.write("**El reporte incluirá:**")
        st.write("• Resumen de datos y métricas")
        st.write("• Filtros aplicados")
        st.write("• Insights y conclusiones")
        st.write("• Análisis de patrones")
        
        if st.button("📥 Generar Reporte PDF", type="primary"):
            try:
                # Convertir visualizaciones a lista
                viz_list = list(visualizations.values()) if visualizations else []
                
                exported_report = self.export_report(data, viz_list, filters, filename)
                
                if exported_report:
                    st.success("✅ Reporte generado correctamente")
                    
                    # Crear botón de descarga
                    b64 = base64.b64encode(exported_report).decode()
                    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}.pdf">⬇️ Descargar PDF</a>'
                    st.markdown(href, unsafe_allow_html=True)
                else:
                    st.error("❌ Error al generar reporte")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    def _create_package_export_interface(self, data: Dict, visualizations: Dict, filters: Dict) -> None:
        """Crear interfaz para exportación de paquete completo"""
        st.subheader("📦 Exportar Paquete Completo")
        
        filename = st.text_input("Nombre del paquete:", value="datarush_complete")
        
        st.write("**El paquete incluirá:**")
        st.write("• Todos los datos en formato Excel")
        st.write("• Todas las visualizaciones en PNG")
        st.write("• Reporte completo en PDF")
        st.write("• Metadatos y configuración")
        
        if st.button("📥 Generar Paquete ZIP", type="primary"):
            try:
                # Crear archivo ZIP
                zip_buffer = io.BytesIO()
                
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    # Agregar datos en Excel
                    excel_data = self._export_to_excel(data, "data")
                    zip_file.writestr("datos.xlsx", excel_data)
                    
                    # Agregar visualizaciones
                    for viz_name, viz_fig in visualizations.items():
                        png_data = self.export_visualization(viz_fig, "PNG", viz_name)
                        zip_file.writestr(f"visualizaciones/{viz_name}.png", png_data)
                    
                    # Agregar reporte PDF
                    viz_list = list(visualizations.values()) if visualizations else []
                    pdf_data = self.export_report(data, viz_list, filters, "reporte")
                    zip_file.writestr("reporte.pdf", pdf_data)
                    
                    # Agregar metadatos
                    metadata = {
                        'export_date': datetime.now().isoformat(),
                        'data_summary': self._create_summary_table(data),
                        'filters_applied': filters,
                        'visualizations_included': list(visualizations.keys())
                    }
                    zip_file.writestr("metadata.json", json.dumps(metadata, indent=2))
                
                zip_buffer.seek(0)
                zip_data = zip_buffer.getvalue()
                
                st.success("✅ Paquete generado correctamente")
                
                # Crear botón de descarga
                b64 = base64.b64encode(zip_data).decode()
                href = f'<a href="data:application/zip;base64,{b64}" download="{filename}.zip">⬇️ Descargar ZIP</a>'
                st.markdown(href, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")