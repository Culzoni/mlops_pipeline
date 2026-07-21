from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import joblib
import pandas as pd
import os

app = FastAPI(
    title="CustomerChurnx - API de Producción Real",
    description="Servidor backend oficial conectado al modelo entrenado de Regresión Logística",
    version="2.0.0"
)

RUTA_MODELO = "src/src/modelo_churn.pkl"
RUTA_COLUMNAS = "src/src/columnas_modelo.pkl"

if os.path.exists(RUTA_MODELO) and os.path.exists(RUTA_COLUMNAS):
    modelo = joblib.load(RUTA_MODELO)
    columnas_entrenamiento = joblib.load(RUTA_COLUMNAS)
    print(" ¡Éxito! Modelo y columnas de entrenamiento cargados correctamente desde el disco.")
else:
    modelo = None
    columnas_entrenamiento = []
    print(" Alerta: No se encontraron los archivos .pkl en la ruta 'src/'. Ejecute su notebook primero.")
class ClienteData(BaseModel):
    datos_cliente: dict

@app.get("/")
def home():
    status = "Online" if modelo is not  None else "Falta Cargar Modelo"
    return {
        "status": status, 
        "proyecto": "CustomerChurnx - Producción", 
        "modelo_detectado": str(type(modelo))
    }

@app.post("/predict")
def predict(payload: ClienteData):
    if modelo is None:
        return {"error": "El servidor no tiene un modelo entrenado cargado en memoria."}
        
   
    input_dict = payload.datos_cliente
    
    
    df_usuario = pd.DataFrame([input_dict])
    
    
    df_usuario_dummies = pd.get_dummies(df_usuario)
    
    df_final = pd.DataFrame(columns=columnas_entrenamiento)
    df_final = pd.concat([df_final, df_usuario_dummies], ignore_index=True)
    df_final = df_final.fillna(0)
    
    df_final = df_final[columnas_entrenamiento]
    
    
    prediccion = modelo.predict(df_final)[0]
    
    try:
        probabilidades = modelo.predict_proba(df_final)[0]
        score_riesgo = probabilidades[1]  
    except:
        score_riesgo = 0.50

    return {
        "churn_prediction": int(prediccion),
        "score_calculado": round(float(score_riesgo * 100), 2),
        "mensaje": "Inferencia de Machine Learning ejecutada con éxito en el backend real."
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)