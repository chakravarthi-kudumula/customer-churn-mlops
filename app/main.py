from fastapi import FastAPI
from pydantic import BaseModel
from src.serving.inference import predict

# Initialize FastAPI app
app = FastAPI(
    title="Telco Customer Churn Prediction API",
    description="ML API for predicting customer churn",
    version="1.0.0"
)

# Health check (important for AWS)
@app.get("/")
def root():
    return {"status": "ok"}

# Request schema
class CustomerData(BaseModel):
    gender: str
    Partner: str
    Dependents: str
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    tenure: int
    MonthlyCharges: float
    TotalCharges: float

# Prediction endpoint
@app.post("/predict")
def get_prediction(data: CustomerData):
    try:
        result = predict(data.dict())
        return {"prediction": result}
    except Exception as e:
        return {"error": str(e)}