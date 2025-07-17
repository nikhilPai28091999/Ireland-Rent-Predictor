from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
import os
import requests
from app.chat import chatFunction
from fastapi import Request
import httpx

# Load model and features
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, '..', 'model', 'rental_price_model.pkl')
features_path = os.path.join(BASE_DIR, '..', 'model', 'model_features.pkl')

model = joblib.load(model_path)
features = joblib.load(features_path)


# nlp = spacy.load("en_core_web_sm")
user_sessions = {}

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

class QueryInput(BaseModel):
    text: str

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
    print("test")
    return df.to_dict(orient="records")


# @app.post("/parse-query")
# def parse_query(data: QueryInput, request: Request):

#     user_id = "default_user"  # Or use something like `request.client.host`

#     # Initialize memory if not already
#     if user_id not in user_sessions:
#         user_sessions[user_id] = {
#             "bed": None,
#             "bath": None,
#             "location": None,
#             "utilities": [],
#         }

#     # Load current session
#     session = user_sessions[user_id]


#     doc = nlp(data.text.lower())
#     parsed = chatFunction(doc, {}, data, expected_utilities)

#     for key in ["bed", "bath", "location"]:
#         if parsed.get(key):
#             session[key] = parsed[key]

#     if "utilities" in parsed:
#         for u in parsed["utilities"]:
#             if u not in session["utilities"]:
#                 session["utilities"].append(u) 
    
#     missing_fields = []
#     if not session["bed"]:
#         missing_fields.append("missingBed")
#     if not session["bath"]:
#         missing_fields.append("missingBath")
#     if not session["location"]:
#         missing_fields.append("missingLocation")

#     if missing_fields:
#         messages = [botMessages[field] for field in missing_fields if field in botMessages]
#         messages = " ".join(messages)
#         return messages
    

#     response = requests.post("http://127.0.0.1:8000/predict", json=session, verify=False)
#     prediction = response.json()["predicted_rent"]
#     return "The predicted rent for {} Bed and {} Bath in {} will be approximately €{}. Would you like to see the properties associated with this?".format(session["bed"],session["bath"],session["location"],prediction)

greeting_responses = {
    "greet": "Hello! How can I help you today?",
    "mood_unhappy": "Why? What happened?"
}

class Message(BaseModel):
    text: str

@app.post("/analyze-message")
async def analyze_message(message: Message):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:5005/model/parse",
                json={"text": message.text}
            )
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Rasa NLU connection error: {str(e)}")

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Rasa NLU request failed")

    rasa_result = response.json()
    intent = rasa_result.get("intent", {}).get("name", "unknown")
    entities = {
        e["entity"]: e["value"]
        for e in rasa_result.get("entities", [])
    }

    # Custom replies based on known intents
    reply = greeting_responses.get(intent, f"Intent detected: {intent}, entities: {entities}")

    return {
        "reply": reply,
        "intent": intent,
        "entities": entities
    }
