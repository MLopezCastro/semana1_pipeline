Perfecto, Marcelo.
Te preparo un README enfocado solo en **cómo configurar y usar un trigger de S3 para Lambda**, con el ejemplo que vos ya tenés funcionando.

---

# **README – Trigger de S3 para ejecutar Lambda automáticamente**

## **🎯 Objetivo**

Configurar un evento en Amazon S3 para que una función AWS Lambda se ejecute **automáticamente** cada vez que se suba un archivo CSV a una carpeta específica de un bucket.

---

## **📌 Flujo de trabajo**

```
[Usuario sube archivo a S3: marcelo-ventas-pipeline-input/raw/ventas_2025-07-18.csv]
    ↓
[S3 detecta evento y dispara Lambda automáticamente]
    ↓
[Lambda procesa el archivo y guarda el resultado en:
 marcelo-ventas-pipeline-output/processed/ventas_2025-07-18.csv]
```

---

## **⚙️ Configuración del Trigger en la consola AWS**

1. **Ir a la consola de AWS Lambda**

   * Seleccionar la función: `ventasPipelineLambda`.

2. **Agregar trigger**

   * Pestaña **Triggers** → **Add trigger**.
   * Fuente: **S3**.
   * Bucket: `marcelo-ventas-pipeline-input`.
   * **Event type:** `PUT` (cuando se sube un nuevo archivo).
   * **Prefix:** `raw/` → solo activa si el archivo está en esa carpeta.
   * **Suffix:** `.csv` → solo activa si termina en `.csv`.

3. **Aceptar advertencia de Recursive Invocation**

   * Confirmar que entendés el riesgo de usar el mismo bucket para entrada/salida.
   * En este caso, no hay problema porque la salida va a otro bucket (`marcelo-ventas-pipeline-output`).

4. **Guardar cambios**

   * La consola añade automáticamente la política necesaria para que S3 pueda invocar Lambda.

---

## **💻 Código base de la Lambda**

Archivo: `lambda_function.py`
Este script:

* Recibe el evento de S3.
* Descarga el CSV de entrada.
* Limpia nombres de columnas.
* Filtra filas con valores positivos en `precio_unitario`.
* Guarda el resultado en el bucket de salida.

```python
import os, json, logging, boto3
from io import StringIO
from urllib.parse import unquote_plus
import sys
sys.path.insert(0, "/var/task/pkg")  # libs del ZIP
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
        raise
```

---

## **🧪 Prueba del Trigger**

1. Subir un archivo CSV de prueba a la carpeta `raw/` del bucket de entrada:

```bash
aws s3 cp data/ventas_raw.csv s3://marcelo-ventas-pipeline-input/raw/ventas_2025-07-18.csv
```

2. Revisar **CloudWatch Logs**:

   * Log group: `/aws/lambda/ventasPipelineLambda`.
   * Buscar el mensaje `OK -> s3://marcelo-ventas-pipeline-output/processed/...`.

3. Verificar el archivo procesado en el bucket de salida:

```bash
aws s3 ls s3://marcelo-ventas-pipeline-output/processed/
```

---

## **✅ Checklist**

* [ ] Trigger activo en Lambda.
* [ ] Lambda escribe en bucket de salida distinto al de entrada.
* [ ] Logs visibles en CloudWatch.
* [ ] Archivo procesado aparece en el bucket de salida.
* [ ] Flujo funcionando de forma automática al subir archivo a `raw/`.

---

