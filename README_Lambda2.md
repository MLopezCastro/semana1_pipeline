# README – AWS Lambda para Procesar CSV desde S3

Este README describe cómo crear una función Lambda en AWS que procese automáticamente archivos CSV subidos a un bucket S3, limpie y valide datos, y guarde el resultado procesado en otro bucket.

## Requisitos Previos
- Cuenta de AWS con permisos para Lambda y S3.
- AWS CLI configurada.
- Buckets de entrada y salida creados.
- Rol de ejecución con permisos `s3:GetObject` y `s3:PutObject`.

## Variables de Entorno en Lambda
- `INPUT_BUCKET`: nombre del bucket de entrada.
- `OUTPUT_BUCKET`: nombre del bucket de salida.
- `OUTPUT_PREFIX`: prefijo o carpeta de salida (por ejemplo: `processed/`).

## Pasos para Implementar
1. Crear una función Lambda en AWS (Python 3.9 o superior).
2. Comprimir el script `lambda_function.py` en un archivo ZIP.
3. Subir el ZIP en la consola de Lambda.
4. Configurar las variables de entorno mencionadas.
5. Asignar un rol IAM con permisos para S3.
6. Crear un trigger en Lambda conectado al bucket de entrada para eventos `PUT` (cuando se suba un archivo nuevo) filtrado por prefijo `raw/`.
7. Guardar y probar.

## Ejemplo de Evento S3
```json
{
  "Records": [
    {
      "s3": {
        "bucket": { "name": "mi-bucket-entrada" },
        "object": { "key": "raw/ventas.csv" }
      }
    }
  ]
}
```

## Script Completo (lambda_function.py):

```
import os
import json
import logging
from urllib.parse import unquote_plus
from io import StringIO
import boto3
import pandas as pd

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")

INPUT_BUCKET  = os.environ.get("INPUT_BUCKET",  "marcelo-ventas-pipeline-input")
OUTPUT_BUCKET = os.environ.get("OUTPUT_BUCKET", "marcelo-ventas-pipeline-output")
OUTPUT_PREFIX = os.environ.get("OUTPUT_PREFIX", "processed/")
if not OUTPUT_PREFIX.endswith("/"):
    OUTPUT_PREFIX += "/"

def _build_output_key(input_key: str) -> str:
    k = input_key.lstrip("/")
    if k.startswith("raw/"):
        return OUTPUT_PREFIX + k[len("raw/"):]
    return OUTPUT_PREFIX + k

def _clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(r"[^a-z0-9_]", "", regex=True)
    )
    return df

def _filter_positive(df: pd.DataFrame, col: str) -> pd.DataFrame:
    if col in df.columns:
        return df[pd.to_numeric(df[col], errors="coerce") > 0]
    logger.warning(f"Columna '{col}' no encontrada; no se filtra.")
    return df

def lambda_handler(event, context):
    try:
        logger.info("Evento: %s", json.dumps(event))
        rec = event["Records"][0]
        bucket = rec["s3"]["bucket"]["name"]
        key    = unquote_plus(rec["s3"]["object"]["key"])

        obj = s3.get_object(Bucket=bucket, Key=key)
        df = pd.read_csv(obj["Body"])

        df = _clean_column_names(df)
        df = df.dropna(how="all")
        df = _filter_positive(df, "precio_unitario")

        out_key = _build_output_key(key)
        buf = StringIO()
        df.to_csv(buf, index=False)
        s3.put_object(Bucket=OUTPUT_BUCKET, Key=out_key, Body=buf.getvalue())

        msg = f"OK -> s3://{OUTPUT_BUCKET}/{out_key}"
        logger.info(msg)
        return {"statusCode": 200, "body": msg}
    except Exception as e:
        logger.exception("Error en Lambda")
        return {"statusCode": 500, "body": str(e)}

´´´









