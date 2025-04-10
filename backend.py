from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKeyHeader
import pandas as pd
import uuid
import os
import json
from typing import List

app = FastAPI(title="Diabetes Data API", version="1.0")

DATA_STORE = "./user_data"
API_KEYS = {}  # In-memory key store
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

# Ensure data directory exists
os.makedirs(DATA_STORE, exist_ok=True)


def clean_and_structure(file: UploadFile) -> List[dict]:
    try:
        if file.filename.endswith(".xlsx"):
            df = pd.read_excel(file.file)
        else:
            df = pd.read_csv(file.file)

        # Standardize column names
        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

        # Replace missing values
        df.replace({"missing": None, "N/A": None, "n/a": None}, inplace=True)

        # Rename specific known columns
        renamed_cols = {
            "glucose_(mg/dl)": "glucose_mg_dl",
            "insulin_(uu/ml)": "insulin_uu_ml",
            "a1c_(%)": "a1c_percent"
        }
        df.rename(columns=renamed_cols, inplace=True)

        return df.to_dict(orient="records")

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Data cleaning failed: {e}")


def validate_api_key(api_key: str = Depends(api_key_header)) -> str:
    if not api_key or api_key not in API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid or missing API key.")
    return api_key


@app.post("/upload", summary="Upload a patient data file")
def upload_file(file: UploadFile = File(...)):
    try:
        # Clean and structure data
        structured_data = clean_and_structure(file)

        # Generate and store API key
        user_key = str(uuid.uuid4())
        API_KEYS[user_key] = user_key

        # Save structured data as JSON
        with open(os.path.join(DATA_STORE, f"{user_key}.json"), "w") as f:
            json.dump(structured_data, f)

        return {
            "message": "File processed successfully.",
            "api_key": user_key,
            "endpoint": "/api/v1/data"
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@app.get("/api/v1/data", summary="Access your uploaded patient data")
def get_data(api_key: str = Depends(validate_api_key)):
    try:
        data_path = os.path.join(DATA_STORE, f"{api_key}.json")
        if not os.path.exists(data_path):
            raise HTTPException(status_code=404, detail="Data not found for this API key.")

        with open(data_path, "r") as f:
            data = json.load(f)

        return JSONResponse(content=data)

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not retrieve data: {e}")
