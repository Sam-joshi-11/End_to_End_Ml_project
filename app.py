from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI()

model = joblib.load("loan_model.joblib")

#Request schema

class LoanRequest(BaseModel):
    Age:int
    Salary:float

# Home endpoint
@app.get("/")
def home():
    return {"message": "Loan Prediction API is Running"}

# prediction endpoint
@app.post("/predict")
def predict(data: LoanRequest):
    input_data = [[data.Age,data.Salary]]
    prediction = model.predict(input_data)
    
    if prediction[0] == 1:
        result = 'Loan Approved'
    else:
        result = 'Loan Rejected'
    
    return {"prediction": result}

