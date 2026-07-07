from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
import joblib

app = FastAPI()
try:
    model = joblib.load("loan_model.joblib")
except Exception:
    model=None

#Request schema

class LoanRequest(BaseModel):
    Age:int = Field(...,ge=18,le=60,description="Age between 18 to 60")
    Salary:float = Field(..., gt=10000, description="Salary should be greater than 10000")


# Home endpoint
@app.get("/")
def home():
    return {"message": "Loan Prediction API is Running"}

# Health check Endpoint
@app.get("/health")
def health():
    if model is None :
        return {
            "status":"Unhealthy",
            "model":"Not Loded"
        }
    return{
        "status":"healthy",
        "model":"Loaded"
    }


# prediction endpoint
@app.post("/predict")
def predict(data: LoanRequest):
    """input_data = [[data.Age,data.Salary]]
    prediction = model.predict(input_data)
    
    if prediction[0] == 1:
        result = 'Loan Approved'
    else:
        result = 'Loan Rejected'
    
    return {"prediction": result}"""
    # check model availability
    if model is None:
        raise HTTPException(
            status_code=500,
            detail='Prediction model is not available'
        )
    # Additional Business Validation
    if data.Salary >1000000:
        raise HTTPException(
            status_code=400,
            detail='Salary seems unrealistic.'
        )
    try:

        # Convert input
        input_data = [[data.Age,data.Salary]]
        prediction = model.predict(input_data)
        if prediction[0] == 1:
            result = "Loan Approved"
        else:
            result = "Loan Rejected"
        return {
            "prediction": result
        }
    except Exception:
        raise HTTPException(
            status_code=501,
            detail='Unable to generate prediction'
        )


