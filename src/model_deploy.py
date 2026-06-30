from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn 

# Inicializamos la app de FastAPI 

app = FastAPI(
    title="API de prediccion - MLOps Pipeline", 
    description="Servicio para exponer el modelo de Data Science",
    version ="1.0.0"
    )

# Definimos la estructura de datos que recibira la API 
# Modificamos las variables segun las columnas reales de tu dataset
class ClienteInput(BaseModel):
    age: int
    tenure_months: int
    sessions_week: int
    avg_session_min: float
    notif_click_rate: float
    support_tickets_3m: int
    discount_pct_3m: float
    late_payment_6m: int
    auto_renew: int 
    
@app.get("/")
def home():
    return {"mensaje": "CustomerChurnx - API levantada con exito."}

@app.post("/predict")
def predict(data: ClienteInput):  
    input_dict = data.dict()
    

    score_riesgo = (input_dict['support_tickets_3m'] * 1.5) + (input_dict['late_payments_6m'] * 2.0) - (input_dict['tenure_months'] * 0.1)   

    prediccion_final = 1 if score_riesgo > 2.0 else 0

    return {
        "churn_prediction": prediccion_final,
        "score_calculado": round(score_riesgo, 2),
        "mensaje": "Analisis predictivo de retencion completado."
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)