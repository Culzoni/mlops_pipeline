 Proyecto Integrador: Pipeline MLOps - CustomerChurnx

Alumno: Julián Culzoni  
Caso de Negocio: Predicción de abandono de clientes (Churn)  

 Avance 1: Estructura e Ingesta de Datos (v1.0.1)

En esta primera etapa se configuró el entorno de desarrollo y se realizó el primer análisis de los datos del caso CustomerChurnx.

Lo desarrollado:
Estructura MLOps: Creación de la arquitectura del proyecto (`src/`, archivos de configuración y control de versiones).
Gestión de Ramas: Configuración del repositorio con las ramas `master`, `developer` y `certification`.
Ingesta (`Cargar_datos.ipynb`): Conexión y lectura correcta de la base de datos `Base_de_datos.csv` usando Pandas.
Análisis Exploratorio (`comprension_eda.ipynb`): Revisión de tipos de datos, conteo de clientes por tipo de plan y generación del gráfico de distribución de la variable objetivo (`churn`).

----------------------------------------------------------------------------------------------------

Avance 2: Modelado e Ingenieria de Caracteristicas (v1.0.1)

Data Loading o Ingesta de Datos
Utilizamos la libreria 'pandas' para levantar el archivo original 'Base_de_datos.csv desde la raiz mediante la ruta ('../') y convertirlo en un DataFrame 

Aplicamos 'pd.get_dummies()'. Como los algoritmos de ML de 'scikit-learn' solo procesan valores numericos, esta funcion transforma automaticamente todas las variables categoricas (texto) en columnas de valores binarios (0/1 o True/False), expandiendo el dataset para que sea apto para el modelado.

-----------------------------------------------------------------------------------------------------

Avance 3: Puesta en Produccion y Monitoreo (MLOps)

    Caso de Negocio y Objetivos
En esta etapa del proyecto integrador, se dio el salto hacia MLOps (Operaciones de Machine Learning). El objetivo principal es garantizar que el modelo de prediccion de clientes/churn se mantenga estable a lo largo del tiempo bajo un entorno de produccion simulado, previniendo la degradacion de sus metricas de negocio.

    Monitoreo y hallazgos tecnicos (Data Drift)

Para cumplir con los requerimientos de la entrega, se desarrollo un modulo de monitoreo estadistico dentro de 'model_monitoring.py':
- # Metodologia: Implementacion de la prueba de (KS-Test) para evaluar las variables numericas del dataset.
- # Simulacion: Se dividio la base de datos historica ('Base_de_datos.csv') para comparar la distribucion original de entrenamiento (Referencia) contra los datos que ingresan en produccion (Actual).
- # Control automatico: El script evalua el *p-value* con un umbral de 0.05 para alertar de forma automatica si las caracteristicas sufren desviaciones estadísticas significativas.

    Arquitectura de la Aplicacion (Dashboard Web)

Se desarrollo una interfaz interactiva utilizando **Streamlit** ('app.pyy'), organizada de la siguiente manera:
Ventana de monitoreo: Renderiza de forma interactiva el reporte estadistico de Data Drift generado por el pipeline.
Ventana de Predicciones : Un simulador en tiempo real para interactuar con los parametros del modelo.

    Instrucciones para la Ejecucion Local

    Instalaar las dependencias actualizadas del proyecto:
    '''bash
    pip install -r requirements.txt
    '''

    Ejecutar el script para procesar y actualizar las metricas de estabilidad:
    '''bash 
    pyhon model_monitoring.py
    '''

    Lanzar el panel de control interactivo en el navegador ('localhost:8501')
    '''bash
    pyython -m streamlit run app.py
    '''
