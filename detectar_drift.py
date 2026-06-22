import os
import pandas as pd
from scipy.stats import ks_2samp

def generar_reporte_drift():
    print("Iniciando análisis estadístico de Data Drift...")
    ruta_datos = "Base_de_datos.csv"
    
    if not os.path.exists(ruta_datos):
        print(f"Error: No se encontró el archivo {ruta_datos}")
        return

    # 1. Cargar el dataset completo
    df = pd.read_csv(ruta_datos)
    
    # Seleccionar solo columnas numéricas para el análisis estadístico
    columnas_numericas = df.select_dtypes(include=['int64', 'float64']).columns
    
    # 2. Dividir a la mitad para simular (Entrenamiento vs Producción)
    mitad = len(df) // 2
    df_referencia = df.iloc[:mitad]
    df_actual = df.iloc[mitad:]

    columnas_con_drift = 0
    filas_html_columnas = ""

    # 3. Calcular el Drift feature por feature usando Kolmogorov-Smirnov
    for col in columnas_numericas:
        # Extraer distribuciones
        dist_ref = df_referencia[col].dropna()
        dist_act = df_actual[col].dropna()
        
        if len(dist_ref) > 0 and len(dist_act) > 0:
            # Ejecutar prueba estadística de dos muestras
            stat, p_value = ks_2samp(dist_ref, dist_act)
            
            # Si el p-value es menor a 0.05, la distribución cambió significativamente (Drift)
            tiene_drift = p_value < 0.05
            status_text = "⚠️ Drift Detectado" if tiene_drift else "✅ Estable"
            status_class = "drift" if tiene_drift else "no-drift"
            
            if tiene_drift:
                columnas_con_drift += 1
                
            filas_html_columnas += f"""
            <tr>
                <td><strong>{col}</strong></td>
                <td>{p_value:.4f}</td>
                <td><span class="status {status_class}">{status_text}</span></td>
            </tr>
            """

    # 4. Determinar estado global del dataset (si más del 20% de las columnas cambiaron)
    total_columnas = len(columnas_numericas)
    porcentaje_drift = (columnas_con_drift / total_columnas) if total_columnas > 0 else 0
    dataset_drift = porcentaje_drift > 0.20

    # 5. Armar el diseño HTML interactivo para tu aplicación
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Reporte MLOps - Data Drift</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f4f6f9; color: #333; }}
            .card {{ background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-width: 800px; margin: 0 auto; }}
            h2 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; margin-top: 0; }}
            .grid {{ display: flex; gap: 20px; margin-bottom: 20px; }}
            .metric {{ flex: 1; background: #edf2f7; padding: 15px; border-radius: 6px; text-align: center; font-size: 16px; }}
            .metric-val {{ font-size: 24px; font-weight: bold; color: #2b6cb0; margin-top: 5px; }}
            .status {{ font-weight: bold; padding: 4px 8px; border-radius: 4px; display: inline-block; font-size: 14px; }}
            .drift {{ background-color: #fed7d7; color: #9b2c2c; }}
            .no-drift {{ background-color: #c6f6d5; color: #22543d; }}
            .global-status {{ padding: 15px; border-radius: 6px; text-align: center; font-weight: bold; font-size: 18px; margin-bottom: 25px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
            th, td {{ padding: 10px; border-bottom: 1px solid #e2e8f0; text-align: left; }}
            th {{ background-color: #f7fafc; color: #4a5568; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>📊 Reporte de Monitoreo - Data Drift</h2>
            
            <div class="global-status {'drift' if dataset_drift else 'no-drift'}">
                { "⚠️ ALERTA: EL DATASET GLOBAL TIENE DRIFT (MÁS DEL 20% DE COLUMNAS ALTERADAS)" if dataset_drift else "✅ PIPELINE ESTABLE: DATASET DENTRO DE LOS PARÁMETROS NORMALES" }
            </div>

            <div class="grid">
                <div class="metric">Variables Analizadas<div class="metric-val">{total_columnas}</div></div>
                <div class="metric">Variables con Drift<div class="metric-val">{columnas_con_drift}</div></div>
                <div class="metric">Porcentaje de Cambio<div class="metric-val">{porcentaje_drift * 100:.1f}%</div></div>
            </div>

            <h3>Detalle por Característica (Métricas p-value)</h3>
            <table>
                <thead>
                    <tr>
                        <th>Columna Numérica</th>
                        <th>p-value (KS Test)</th>
                        <th>Estado de Estabilidad</th>
                    </tr>
                </thead>
                <tbody>
                    {filas_html_columnas}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """

    # 6. Crear la carpeta src y guardar el archivo HTML nativamente
    if not os.path.exists("src"):
        os.makedirs("src")
        
    ruta_reporte = "src/reporte_data_drift.html"
    with open(ruta_reporte, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ ¡ÉXITO TOTAL! Reporte generado en: {ruta_reporte}")

if __name__ == "__main__":
    generar_reporte_drift()
