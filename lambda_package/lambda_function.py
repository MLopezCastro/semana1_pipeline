import os
import boto3
import pandas as pd
from io import StringIO
from urllib.parse import unquote_plus
from pipeline.transform import clean_column_names, drop_nulls, filter_positive_values
from utils.logger import get_logger

logger = get_logger()
s3 = boto3.client('s3')

# Variables de entorno que vas a configurar en la consola de Lambda
OUTPUT_BUCKET = os.environ.get("OUTPUT_BUCKET", "marcelo-ventas-pipeline-output")
OUTPUT_PREFIX = os.environ.get("OUTPUT_PREFIX", "processed/")  # termina en "/"

def _build_output_key(input_key: str) -> str:
    """
    Si el input viene bajo 'raw/', lo reemplaza por 'processed/'.
    Si viene en la raíz u otra carpeta, antepone 'processed/'.
    """
    key = input_key.lstrip("/")  # limpio por si viene con / al inicio
    if key.startswith("raw/"):
        return key.replace("raw/", OUTPUT_PREFIX, 1)
    # mismo nombre de archivo, bajo processed/
    return f"{OUTPUT_PREFIX}{key}"

def lambda_handler(event, context):
    try:
        logger.info("Inicio del pipeline en Lambda")

        # 1) Info del archivo recibido por el evento de S3
        record = event["Records"][0]
        bucket = record["s3"]["bucket"]["name"]
        key = unquote_plus(record["s3"]["object"]["key"])
        logger.info(f"Archivo recibido: s3://{bucket}/{key}")

        # 2) Descargar desde S3
        obj = s3.get_object(Bucket=bucket, Key=key)
        df = pd.read_csv(obj["Body"])  # asume CSV con separador por defecto (,)

        # 3) Transformaciones
        df = clean_column_names(df)
        df = drop_nulls(df)
        df = filter_positive_values(df, "precio_unitario")  # ajustá si tu columna se llama distinto

        # 4) CSV en memoria
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)

        # 5) Subir al bucket de salida
        output_key = _build_output_key(key)
        s3.put_object(
            Bucket=OUTPUT_BUCKET,
            Key=output_key,
            Body=csv_buffer.getvalue(),
            ContentType="text/csv"
        )

        logger.info(f"Archivo procesado: s3://{OUTPUT_BUCKET}/{output_key}")
        return {"statusCode": 200, "body": f"OK -> s3://{OUTPUT_BUCKET}/{output_key}"}

    except Exception as e:
        logger.exception(f"Fallo el pipeline: {e}")
        return {"statusCode": 500, "body": f"Error: {e}"}
