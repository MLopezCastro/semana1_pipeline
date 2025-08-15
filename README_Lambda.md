# 🚀 Guía Completa para Crear y Ejecutar una AWS Lambda desde Cero

Esta guía documenta **todos los pasos** que seguimos para crear, configurar, probar y ver los logs de una función Lambda en AWS, asegurando que funcione correctamente y esté integrada con CloudWatch.

---

## 1️⃣ Crear la función Lambda

1. Inicia sesión en [AWS Management Console](https://aws.amazon.com/console/).
2. En el buscador, escribe **Lambda** y entra al servicio.
3. Clic en **Create function**.
4. Completa:
   - **Author from scratch**.
   - **Function name** → Ej: `ventasPipelineLambda`.
   - **Runtime** → Python 3.x (el que uses en tu código).
   - **Architecture** → x86_64 (default).
   - **Permissions**:
     - Marca **Create a new role with basic Lambda permissions**.
5. Clic en **Create function**.

---

## 2️⃣ Configurar permisos adicionales (S3, Athena, etc.)

Si la Lambda necesita acceder a otros servicios como S3 o Athena:

1. Abre la Lambda creada.
2. En la pestaña **Configuration** → **Permissions** → clic en el rol de ejecución (execution role).
3. Esto te lleva a **IAM**.
4. En **Add permissions** → **Attach policies**:
   - Busca y agrega:
     - `AmazonS3FullAccess` (o el nivel necesario).
     - `AmazonAthenaFullAccess` si usas Athena.
     - Otros permisos específicos si tu Lambda accede a más servicios.
5. Guarda cambios.

---

## 3️⃣ Subir el código de la Lambda

**Opción A – Subir un archivo ZIP** (lo que hicimos):
1. Prepara tu carpeta de proyecto con:
   - `lambda_function.py` (o el archivo principal).
   - Librerías necesarias (si no usas Layers, deben estar incluidas en la carpeta).
2. Comprime todo el contenido (no la carpeta entera, solo los archivos y subcarpetas internas) en un `.zip`.
3. En la consola de Lambda:
   - Pestaña **Code** → **Upload from** → **.zip file**.
   - Sube el archivo ZIP.
4. Asegúrate que el handler esté bien configurado:
   - Si el archivo principal se llama `lambda_function.py` y la función principal es `lambda_handler`, el handler debe ser:
     ```
     lambda_function.lambda_handler
     ```
   - Ajusta esto en **Runtime settings**.

**Opción B – Editar en el editor integrado** (no recomendado para proyectos grandes).

---

## 4️⃣ Configurar variables de entorno (opcional pero frecuente)

Si tu código usa rutas, credenciales, etc.:

1. Pestaña **Configuration** → **Environment variables**.
2. Añade cada variable `KEY = value`.
3. Guarda cambios.

---

## 5️⃣ Probar la Lambda en AWS Console

1. Dentro de la Lambda, clic en **Test**.
2. Crea un evento de prueba:
   - **Event name**: `test1` (o lo que quieras).
   - **Event JSON**: los datos de entrada que espera tu Lambda.
3. Guarda y ejecuta.
4. Revisa la salida (return) y el log rápido que aparece abajo.

---

## 6️⃣ Ver logs detallados en CloudWatch

1. Desde la consola de AWS, abre **CloudWatch**.
2. En el menú izquierdo, ve a **Logs → Log groups**.
3. Busca `/aws/lambda/<nombre_de_tu_lambda>`.
4. Clic en el **Log Group**.
5. Abre el **Log Stream** más reciente.
6. Aquí verás:
   - Mensajes `print()` o `logger.info()`.
   - Errores y trazas (`Traceback`).
   - Duración y memoria usada.

💡 **Tip:** Usa la opción **Live Tail** en CloudWatch para ver la ejecución en tiempo real.

---

## 7️⃣ Re-ejecutar y depurar

- Si hay errores:
  - Lee el log de CloudWatch para identificar el problema.
  - Corrige el código localmente.
  - Vuelve a comprimir y subir el ZIP actualizado.
- Repite la prueba hasta obtener el resultado esperado.

---

## 8️⃣ Resumen de puntos clave para no olvidar

- **Handler** correcto → `<nombre_archivo>.<nombre_función>`.
- **Permisos IAM** → agrega todas las políticas necesarias según los servicios que use la Lambda.
- **Código en ZIP** → comprimir solo el contenido, no la carpeta raíz.
- **Logs en CloudWatch** → siempre revisar para depuración.

---

✅ Con estos pasos podrás recrear cualquier Lambda que necesites en el futuro.

---

- **Runtime**: Python 3.12  
- **Arquitectura**: x86_64  
- **Dependencias**: numpy + pandas (wheels manylinux2014 para cp312) **incluidas dentro del ZIP**  
- **Sin layers** (para simplificar y evitar incompatibilidades)

---

## 1) Crear la función Lambda

1. AWS Console → **Lambda** → **Create function**
2. **Author from scratch**
   - **Function name**: `ventasPipelineLambda`
   - **Runtime**: `Python 3.12`
   - **Architecture**: `x86_64`
   - **Permissions**: *Create a new role with basic Lambda permissions*
3. **Create function**

<img width="866" height="859" alt="image" src="https://github.com/user-attachments/assets/5dba3f90-05b1-4b94-ba75-2f121bb3e18c" />

---

## 2) Agregar permisos al **Execution role**

Abrí la Lambda → **Configuration** → **Permissions** → clic en el **Role name** (te lleva a IAM).

Adjuntá estas políticas (mínimo):

- `AWSLambdaBasicExecutionRole` (ya suele venir; si no, adjuntala)
- `CloudWatchLogsFullAccess` (o equivalente administrado por AWS)
- `AmazonS3FullAccess` *(para pruebas rápidas)*. En prod usá una política mínima con `s3:GetObject` (input) + `s3:PutObject` (output).

<img width="756" height="693" alt="image" src="https://github.com/user-attachments/assets/8d5662c8-5ac0-40ca-825b-1a0f0e3a870b" />

---

## 3) Variables de entorno

En la Lambda → **Configuration** → **Environment variables**:

| Key            | Value                                     |
|----------------|-------------------------------------------|
| `INPUT_BUCKET` | `marcelo-ventas-pipeline-input`           |
| `OUTPUT_BUCKET`| `marcelo-ventas-pipeline-output`          |
| `OUTPUT_PREFIX`| `processed/` *(debe terminar en `/`)*     |

<img width="795" height="408" alt="image" src="https://github.com/user-attachments/assets/fb2f7c38-d763-4d7c-813a-7a20a1a7e06f" />

---

## 4) Código de la Lambda (`lambda_function.py`)

> **Nota**: Agregamos `/var/task/pkg` al `sys.path` porque ahí van las wheels de pandas/numpy dentro del ZIP.

```python
import os, json, logging, boto3
from io import StringIO
from urllib.parse import unquote_plus
import sys
sys.path.insert(0, "/var/task/pkg")  # donde están pandas/numpy en el ZIP

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
        df = _filter_positive(df, "precio_unitario")  # ajustar si aplica

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

---

Empaquetado correcto (💯 1 solo ZIP)

Lo hicimos en AWS CloudShell (us‑east‑1) para obtener wheels manylinux2014 compatibles con Lambda cp312 sin Docker ni layers.

# 1) carpeta limpia
rm -rf build312 && mkdir -p build312/pkg && cd build312

# 2) instalar dependencias correctas en pkg/ (manylinux2014 + cp312)
python3 -m pip install \
  --platform manylinux2014_x86_64 \
  --implementation cp \
  --python-version 312 \
  --only-binary=:all: \
  --no-deps \
  -t pkg \
  numpy==2.0.1 pandas==2.2.2 python-dateutil pytz tzdata

# 3) crear el código (o subilo con un editor; acá lo generamos inline si querés)
cat > lambda_function.py <<'PY'
# (pegar aquí el contenido del lambda_function.py que está más arriba)
PY

# 4) armar el ZIP final (pkg + código)
zip -r9 ../lambda_package_py312.zip . >/dev/null
cd ..
ls -lh lambda_package_py312.zip
# salida esperada ~40 MB

---

6) Subir el ZIP a la función

Abrí la Lambda → pestaña Code

Botón Upload from → .zip file

Seleccioná lambda_package_py312.zip → Save

Verificá que el explorador de archivos muestre:

lambda_function.py

carpeta pkg/ con pandas, numpy, etc.

Runtime settings

Handler: lambda_function.lambda_handler

Runtime: Python 3.12

---

7) Prueba manual (sin trigger)

Test → Configure test event → plantilla S3 Put

Cambiá los campos:

{
  "Records": [
    {
      "s3": {
        "bucket": { "name": "marcelo-ventas-pipeline-input" },
        "object": { "key": "raw/ventas.csv" }
      }
    }
  ]
}


<img width="478" height="231" alt="111" src="https://github.com/user-attachments/assets/f849fb38-9662-4f39-978c-d6f6e317ed00" />

---

Asegurate de tener ventas.csv en s3://marcelo-ventas-pipeline-input/raw/ventas.csv

Ejecutá Test.

Deberías ver OK -> s3://marcelo-ventas-pipeline-output/processed/ventas.csv

---








