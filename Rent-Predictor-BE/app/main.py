from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware


# Load model and features
model = joblib.load("../model/rental_price_model.pkl")
features = joblib.load("../model/model_features.pkl")



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # your Vite frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the input schema
class RentalInput(BaseModel):
    bed: float
    bath: float
    location: str
    utilities: list[str] = []

expected_utilities = [
    "Parking",
    "Central Heating",
    "Washing Machine",
    "Dryer",
    "Dishwasher",
    "Internet",
    "Garden / Patio / Balcony",
    "Microwave",
    "Gym",
    "Pets Allowed"
]


@app.get("/")
def home():
    return {"message": "Rental Market API is working!"}

@app.post("/predict")
def predict_rent(data: RentalInput):

    # Create input DataFrame with 1 row
    input_dict = {
        "Bed": [data.bed],
        "Bath": [data.bath]
    }

    # Add location one-hot encoding
    for col in features:
        if col.startswith("Location_"):
            input_dict[col] = [1 if col == f"Location_{data.location}" else 0]

    for util in expected_utilities:
        input_dict[util] = [1 if util in data.utilities else 0]
        

    # Create DataFrame in model's expected order
    X_input = pd.DataFrame(input_dict)[features]

    # Predict
    prediction = model.predict(X_input)[0]
    return {"predicted_rent": round(prediction, 2)}

@app.get("/feature-importance")
def get_feature_importance():
    df = pd.read_csv("../data/feature_importances.csv")
    return df.to_dict(orient="records")
