import streamlit as st
import streamlit.components.v1 as components
import requests
import os


st.set_page_config(page_title="CustomerChurnx - Dashboard Real", layout="wide")

st.title("Panel de Control Comercial - CustomerChurnx")
st.write("Interfaz gráfica conectada al modelo real de Machine Learning mediante FastAPI.")


tab1, tab2 = st.tabs(["🔮 Simulador de Predicciones Reales", "Monitoreo de Data Drift"])

with tab1:
    st.header("Simulador de Predicción de Churn en Production")
    st.write("Mueva los parámetros del cliente para evaluar su riesgo de abandono real.")
    
    with st.form("form_churn_real"):
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.slider("Edad del Cliente (age):", 18, 100, 35)
            tenure_months = st.slider("Antigüedad en Meses (tenure_months):", 0, 72, 12)
            sessions_week = st.number_input("Sesiones por Semana (sessions_week):", min_value=0, value=5)
            avg_session_min = st.number_input("Minutos Promedio por Sesión (avg_session_min):", min_value=0.0, value=25.5)
        
        with col2:
            notif_click_rate = st.slider("Tasa de Click en Notificaciones (notif_click_rate):", 0.0, 1.0, 0.25, step=0.01)
            support_tickets_3m = st.number_input("Tickets de Soporte (Últimos 3 meses):", min_value=0, value=1)
            late_payments_6m = st.number_input("Pagos Atrasados (Últimos 6 meses):", min_value=0, value=0)
            discount_pct_3m = st.slider("Porcentaje de Descuento Recibido:", 0.0, 1.0, 0.0, step=0.05)
            auto_renew = st.selectbox("¿Tiene Renovación Automática? (auto_renew):", [0, 1], format_func=lambda x: "Sí (1)" if x == 1 else "No (0)")
        
        enviar_datos = st.form_submit_button("Consultar Predicción de Inteligencia Artificial")
        
        if enviar_datos:
            diccionario_cliente = {
                "age": int(age),
                "tenure_months": int(tenure_months),
                "sessions_week": int(sessions_week),
                "avg_session_min": float(avg_session_min),
                "notif_click_rate": float(notif_click_rate),
                "support_tickets_3m": int(support_tickets_3m),
                "discount_pct_3m": float(discount_pct_3m),
                "late_payments_6m": int(late_payments_6m),
                "auto_renew": int(auto_renew)
            }
            
            
            payload = {
                "datos_cliente": diccionario_cliente
            }
            
            url_api = "http://localhost:8000/predict"
            
            try:
                respuesta = requests.post(url_api, json=payload)
                
                if respuesta.status_code == 200:
                    resultado = respuesta.json()
                    
                    if "error" in resultado:
                        st.error(f"Error del servidor: {resultado['error']}")
                    else:
                        prediction = resultado["churn_prediction"]
                        score = resultado["score_calculado"]
                        
                        # Renderizamos los carteles según la IA real de tu Regresión Logística
                        if prediction == 1:
                            st.error(f" **ALERTA DE CHURN**: El modelo real predice que el cliente **ABANDONARÁ** el servicio (Riesgo Calculado: {score}%).")
                        else:
                            st.success(f" **CLIENTE FIEL**: El modelo real predice que el cliente **SE QUEDARÁ** en la empresa (Confianza: {score}%).")
                        
                        # Mostramos el JSON de respuesta para auditoría de los profesores
                        st.json(resultado)
                else:
                    st.error(f"Error en la API: Código de estado {respuesta.status_code}")
            except requests.exceptions.ConnectionError:
                st.error(" Error de Conexión: No se pudo conectar con el servidor backend de FastAPI.")
                st.info("Asegúrese de mantener encendida su API en la otra terminal corriendo: python src/model_deploy.py")

with tab2:
    st.header("Análisis Estadístico de Estabilidad (Data Drift)")
    st.write("Reporte automático del pipeline mediante la prueba Kolmogorov-Smirnov:")
    
    ruta_reporte = "src/reporte_data_drift.html"
    if os.path.exists(ruta_reporte):
        with open(ruta_reporte, "r", encoding="utf-8") as f:
            html_content = f.read()
        components.html(html_content, height=750, scrolling=True)
    else:
        st.warning("No se encontró el archivo de reporte en 'src/reporte_data_drift.html'. Corra primero 'python model_monitoring.py'.")
