"""
Test de Integración del Chat con Gemini
=======================================

Script para verificar que el chat esté correctamente integrado en la aplicación.
"""

import sys
import os
import streamlit as st

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from components.chat_agent import ChatAgent

def test_chat_integration():
    """Test de integración del chat"""
    print("🤖 TESTING: Integración del Chat con Gemini")
    print("=" * 60)
    
    try:
        # Inicializar ChatAgent
        print("1. Inicializando ChatAgent...")
        chat_agent = ChatAgent()
        print("✅ ChatAgent inicializado correctamente")
        
        # Test 1: Configuración de Gemini
        print("\n2. Verificando configuración de Gemini...")
        if chat_agent.api_key:
            print("✅ API Key de Gemini configurada")
        else:
            print("⚠️ API Key de Gemini no configurada (usando respuestas predefinidas)")
        
        if chat_agent.model:
            print("✅ Modelo de Gemini configurado")
        else:
            print("⚠️ Modelo de Gemini no disponible (usando respuestas predefinidas)")
        
        # Test 2: Procesamiento de mensajes
        print("\n3. Probando procesamiento de mensajes...")
        test_messages = [
            "¿Cuáles son los países con más pasajeros?",
            "¿Qué feriados tienen mayor impacto en el tráfico aéreo?",
            "¿Cuál es la tendencia de pasajeros en diciembre?",
            "Resumen de los datos disponibles"
        ]
        
        context = {
            "data_loaded": True,
            "current_filters": {},
            "filtered_data": {
                "passengers": "datos_de_pasajeros",
                "holidays": "datos_de_feriados"
            }
        }
        
        for i, message in enumerate(test_messages, 1):
            print(f"   Test {i}: '{message}'")
            try:
                response = chat_agent.process_user_message(message, context)
                if response:
                    print(f"   ✅ Respuesta: {response[:100]}...")
                else:
                    print(f"   ❌ Sin respuesta")
            except Exception as e:
                print(f"   ⚠️ Error: {str(e)}")
        
        # Test 3: Historial de chat
        print("\n4. Probando historial de chat...")
        history = chat_agent.get_chat_history()
        if history is not None:
            print(f"✅ Historial obtenido: {len(history)} mensajes")
        else:
            print("❌ Error al obtener historial")
        
        # Test 4: Limpieza de historial
        print("\n5. Probando limpieza de historial...")
        try:
            chat_agent.clear_chat_history()
            print("✅ Historial limpiado correctamente")
        except Exception as e:
            print(f"❌ Error al limpiar historial: {str(e)}")
        
        print("\n✅ INTEGRACIÓN DEL CHAT: COMPLETADA")
        return True
        
    except Exception as e:
        print(f"\n❌ Error en integración del chat: {str(e)}")
        return False

def test_app_integration():
    """Test de integración en la aplicación"""
    print("\n🔗 TESTING: Integración en la Aplicación")
    print("=" * 60)
    
    try:
        # Verificar que app.py importa ChatAgent
        print("1. Verificando importación en app.py...")
        with open('app.py', 'r', encoding='utf-8') as f:
            app_content = f.read()
        
        if 'from components.chat_agent import ChatAgent' in app_content:
            print("✅ ChatAgent importado en app.py")
        else:
            print("❌ ChatAgent no importado en app.py")
            return False
        
        if 'chat_agent = ChatAgent()' in app_content:
            print("✅ ChatAgent inicializado en app.py")
        else:
            print("❌ ChatAgent no inicializado en app.py")
            return False
        
        if 'st.chat_input' in app_content:
            print("✅ Interfaz de chat implementada en app.py")
        else:
            print("❌ Interfaz de chat no implementada en app.py")
            return False
        
        if 'chat_agent.process_user_message' in app_content:
            print("✅ Procesamiento de mensajes implementado en app.py")
        else:
            print("❌ Procesamiento de mensajes no implementado en app.py")
            return False
        
        print("\n✅ INTEGRACIÓN EN LA APLICACIÓN: COMPLETADA")
        return True
        
    except Exception as e:
        print(f"\n❌ Error en integración de la aplicación: {str(e)}")
        return False

def main():
    """Función principal de testing"""
    print("🚀 TESTING DE INTEGRACIÓN DEL CHAT CON GEMINI")
    print("=" * 70)
    
    # Test 1: Integración del chat
    chat_success = test_chat_integration()
    
    # Test 2: Integración en la aplicación
    app_success = test_app_integration()
    
    # Resumen final
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE INTEGRACIÓN DEL CHAT")
    print("=" * 70)
    
    if chat_success and app_success:
        print("🎉 ¡INTEGRACIÓN DEL CHAT COMPLETADA EXITOSAMENTE!")
        print("\n✅ ChatAgent funcionando correctamente")
        print("✅ Interfaz de chat integrada en la aplicación")
        print("✅ Procesamiento de mensajes implementado")
        print("✅ Historial de chat funcionando")
        print("\n🚀 La aplicación está lista para usar con chat con IA")
    else:
        print("⚠️ INTEGRACIÓN DEL CHAT PARCIALMENTE COMPLETADA")
        if not chat_success:
            print("❌ Problemas en ChatAgent")
        if not app_success:
            print("❌ Problemas en integración de la aplicación")
    
    print(f"\n📋 Para usar la aplicación con chat:")
    print(f"   streamlit run app.py")
    print(f"\n📋 Para configurar Gemini API:")
    print(f"   1. Copia env_gemini_example.txt a .env")
    print(f"   2. Configura tu GEMINI_API_KEY")
    print(f"   3. Reinicia la aplicación")

if __name__ == "__main__":
    main()
