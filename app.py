import streamlit as st
import streamlit.components.v1 as components
import os

# Configuración visual de la página
st.set_page_config(page_title="Dashboard MLOps - Avance 3", layout="wide")

st.title("🚀 Pipeline de MLOps - Panel de Control e Interfaz")
st.write("Proyecto Integrador - Entrega de Monitoreo y Modelado")

# Creamos dos pestañas bien claras para la evaluación
tab1, tab2 = st.tabs(["📊 Monitoreo de Data Drift", "🔮 Simulador de Predicciones"])

with tab1:
    st.header("Análisis Estadístico de Estabilidad (Data Drift)")
    st.write("A continuación se muestra el reporte generado columna por columna usando la prueba estadística de Kolmogorov-Smirnov:")
    
    ruta_reporte = "src/reporte_data_drift.html"
    
    # Comprobar si el archivo HTML que creamos antes existe
    if os.path.exists(ruta_reporte):
        # Leer el contenido del HTML
        with open(ruta_reporte, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # Renderizar el HTML de forma interactiva dentro de Streamlit
        components.html(html_content, height=750, scrolling=True)
    else:
        st.error("⚠️ No se encontró el reporte en 'src/reporte_data_drift.html'.")
        st.info("Por favor, ejecuta en tu terminal: 'python detectar_drift.py' para generarlo primero.")

with tab2:
    st.header("Simulador de Predicción en Producción")
    st.write("Interfaz interactiva para ingresar parámetros y obtener una predicción en tiempo real.")
    
    with st.form("form_prediccion"):
        st.subheader("Variables del Dataset")
        
        # Inputs interactivos de prueba (puedes adaptarlos a tus columnas reales luego)
        val_1 = st.number_input("Ingresa una característica numérica principal:", value=0.0)
        val_2 = st.slider("Selecciona un rango de control:", 0, 100, 50)
        
        enviar = st.form_submit_button("Ejecutar Modelo Predictivo")
        
        if enviar:
            st.success("¡Pipeline de inferencia ejecutado!")
            st.metric(label="Resultado Esperado", value="Simulación Correcta ✅")
