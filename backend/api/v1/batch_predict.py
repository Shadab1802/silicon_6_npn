# backend/api/v1/batch_predict.py
"""
This api route is for batch predictions. Main user is airlines

It accepts input as csv from user, it can be in user_input schema
sub_endcoder converts the user_input schema to machine_input schema that futher get encoded via model self encoder
user get output as json file , which in front end converts to csv table that airlines can download

future aspect we thought to push this output to s3 bucket or sagemaker for future trannig, and we can schedule a api call from backend to Aviationstack
to fetch the actual result, was delay actually present and if error get persistent then devloper team get notification.

"""


from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
import io
from sklearn.preprocessing import RobustScaler, StandardScaler
from app.schemas.input_model import Input 
from app.utils import sub_encoder
from app.utils.model_loader import model,encoders

router = APIRouter()

@router.post("/batch_predict")
async def batch_predict(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    # Read CSV into pandas DataFrame
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))

    # Get feature names from Input model
    feature_columns = list(Input.__fields__.keys())

    # Validate required columns exist
    missing_cols = [col for col in feature_columns if col not in df.columns]
    if missing_cols:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required columns: {missing_cols}"
        )

    # Convert entire CSV to model_input format
    model_input_list = [sub_encoder(row).dict() for _, row in df[feature_columns].iterrows()]
    processed_df = pd.DataFrame(model_input_list)

    # Apply encoders
    for col, le in encoders.items():
        if col in processed_df.columns:
            processed_df[col] = le.transform(processed_df[col])

    # Apply scalers
    robust_cols = ['DEPARTURE_TIME', 'DEPARTURE_DELAY']
    standard_cols = ['MONTH', 'DAY_OF_WEEK', 'ARRIVAL_TIME']
    robust_scaler = RobustScaler()
    standard_scaler = StandardScaler()

    if robust_cols:
        processed_df[robust_cols] = robust_scaler.fit_transform(processed_df[robust_cols])
    if standard_cols:
        processed_df[standard_cols] = standard_scaler.fit_transform(processed_df[standard_cols])

    # Run predictions
    predictions = model.predict(processed_df)

    # Add predictions to original DataFrame
    df["Delayed"] = predictions

    # Return as JSON
    return df.to_dict(orient="records")