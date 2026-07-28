import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from xgboost import XGBRegressor

print("Loading dataset...")
df = pd.read_csv("data/data.csv")

X = df.drop(columns=['price'])
y = df['price']

num_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
cat_cols = X.select_dtypes(include=['object']).columns.tolist()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)

num_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

cat_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

preprocessor = ColumnTransformer(transformers=[
    ('num', num_pipeline, num_cols),
    ('cat', cat_pipeline, cat_cols)
])

print("Fitting preprocessor and training XGBoost...")
X_train_prep = preprocessor.fit_transform(X_train)

xgb = XGBRegressor(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42)
xgb.fit(X_train_prep, y_train)

# Save directly to model/
MODEL_DIR = Path("model")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

joblib.dump(preprocessor, MODEL_DIR / "preprocessor.joblib")
xgb.save_model(MODEL_DIR / "xgb_model.json")
joblib.dump(list(X.columns), MODEL_DIR / "model_features.joblib")

print("SUCCESS: Model and Preprocessor trained and saved in .venv!")