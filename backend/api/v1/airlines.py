from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
import io
# from backend.app.utils.model_fetcher import classifier2
from backend.app.models.input_model import Input  # your Pydantic input model

router = APIRouter()

@router.post("/airlines")
async def batch_predict(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    # Read CSV into pandas DataFrame
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))

    # ✅ Automatically get feature names from Input model
    feature_columns = list(Input.model_fields.keys())

    # Validate required columns exist in uploaded CSV
    missing_cols = [col for col in feature_columns if col not in df.columns]
    if missing_cols:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required columns: {missing_cols}"
        )

    # Select features for prediction
    features = df[feature_columns]

    # Run predictions
    # predictions = classifier2.predict(features)
    predictions=1

    # Add predictions back into DataFrame
    df["delayed"] = predictions

    # Return as JSON
    return df.to_dict(orient="records")
