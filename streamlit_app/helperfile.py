import os
from io import BytesIO
import boto3
import pandas as pd
import streamlit as st
import logging


# create MinIO connection
def create_minio_connection() -> tuple:
    # MinIO Configuration
    MINIO_ENDPOINT = os.environ.get("MINIO_ENDPOINT")
    MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY")
    BUCKET_NAME_WEATHER = os.environ.get("BUCKET_NAME_WEATHER")
    BUCKET_NAME_RETAIL = os.environ.get("BUCKET_NAME_RETAIL")

    # Initialize MinIO Client
    s3 = boto3.client(
        "s3", endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY
    )
    logging.info("Finished initialising Minio connection for loading!")
    return s3, BUCKET_NAME_WEATHER, BUCKET_NAME_RETAIL


# Load Data from MinIO
@st.cache_data
def load_data(file_name: str, type: str = "retail"):
    s3, BUCKET_WEATHER, BUCKET_RETAIL = create_minio_connection()
    logging.info(f"{BUCKET_RETAIL=}; {BUCKET_WEATHER=}")
    if type == "weather":
        bucket = BUCKET_WEATHER
    elif type == "retail":
        bucket = BUCKET_RETAIL
    else:
        raise ValueError("Choose valid data bucket choice!")

    file_name = f"gold/{file_name}.parquet"
    gold_obj = s3.get_object(Bucket=bucket, Key=file_name)
    df = pd.read_parquet(BytesIO(gold_obj["Body"].read()))
    logging.info(f"read file: {file_name}")
    return df
