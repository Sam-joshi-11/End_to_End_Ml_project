import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

#load dataset
df = pd.read_csv("dataset.csv")
# Features
X = df[['Age','Salary']]
#Target
y = df["Approved"]

# Train model
model = RandomForestClassifier()
model.fit(X,y)

#save model
joblib.dump(model,"loan_model.joblib")
print("Model saved successfully")


