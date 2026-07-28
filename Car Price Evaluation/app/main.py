from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import pandas as pd
import joblib
from xgboost import XGBRegressor
import traceback

app = FastAPI(title="Car Price Evaluator")

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "model"
APP_DIR = BASE_DIR / "app"

app.mount("/static", StaticFiles(directory=APP_DIR / "static"), name="static")
templates = Jinja2Templates(directory=APP_DIR / "templates")

# Load preprocessor, XGBoost model, and expected features
preprocessor = joblib.load(MODEL_DIR / "preprocessor.joblib")
expected_features = joblib.load(MODEL_DIR / "model_features.joblib")

model = XGBRegressor()
model.load_model(MODEL_DIR / "xgb_model.json")

class CarInput(BaseModel):
    brand: str
    year: int
    mileage: int
    engine_size_l: float
    cylinders: int
    horsepower: int
    transmission: str
    drivetrain: str
    fuel_type: str
    body_style: str
    num_doors: int
    seating_capacity: int
    fuel_economy_mpg: float
    num_owners: int
    accidents_reported: int
    service_history: str
    condition: str
    warranty_months: int
    seller_type: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/predict")
def predict_price(data: CarInput):
    try:
        raw_data = data.model_dump() if hasattr(data, 'model_dump') else data.dict()
        raw_data['brand'] = raw_data['brand'].strip().title()
        
        # Ensure exact feature order and correct data types
        df_input = pd.DataFrame([raw_data])[expected_features]
        
        transformed_input = preprocessor.transform(df_input)
        prediction = model.predict(transformed_input)[0]
        
        return {"predicted_price": round(float(prediction), 2)}
    except Exception as e:
        print("\n--- ERROR DURING PREDICTION ---")
        traceback.print_exc()
        print("-------------------------------\n")
        return {"error": str(e)}