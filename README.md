# Semana 1 – Data Pipeline Project

Este proyecto forma parte del Bootcamp de Data Engineering.

## 📦 Estructura

- `ejemplo.py`: archivo de prueba para herramientas de calidad de código.
- `venv/`: entorno virtual local (ignorado en Git).
- `requirements.txt`: dependencias instaladas.
- `.gitignore`: exclusión de carpetas innecesarias.

## 🛠️ Herramientas utilizadas

- Python 3.10+
- `black`, `flake8`, `isort`
- Git + GitHub
- VS Code

## 🚀 Cómo empezar

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt


---

# **ETL Pipeline – Ventas (Bloques 1 a 6)**

## **📌 Descripción General**

Este proyecto implementa un **pipeline ETL** para procesar y limpiar datos de ventas desde un archivo CSV, usando Python de forma modular y profesional.
La estructura se ha diseñado siguiendo buenas prácticas de **Data Engineering**, con separación en etapas y scripts reutilizables.

---

## **1️⃣ Bloque 1 – Estructura base del proyecto**

* Se crea la **estructura de carpetas**:

```
.
├── data/
│   ├── input/
│   └── output/
├── pipeline/
│   ├── load.py
│   ├── save.py
│   ├── transform.py
├── utils/
│   └── logger.py
├── main_ventas_cli.py
├── requirements.txt
└── README.md
```

* **Objetivo**: Separar la lógica de negocio, entrada/salida y utilidades en módulos.
* **Archivos creados**:

  * `pipeline/load.py`: Función para cargar CSV (`pandas.read_csv`).
  * `pipeline/save.py`: Función para guardar CSV (`DataFrame.to_csv`).
  * `pipeline/transform.py`: Funciones de limpieza y transformación.

---

## **2️⃣ Bloque 2 – Funciones de transformación**

Funciones implementadas en `pipeline/transform.py`:

* `clean_column_names(df)`: Normaliza nombres de columnas (minúsculas, sin espacios).
* `drop_nulls(df)`: Elimina filas con valores nulos.
* `filter_positive_values(df, col)`: Filtra filas con valores > 0 en una columna.
* `drop_duplicates_by_column(df, col)`: Elimina duplicados basados en una columna.
* `normalize_column_0_100(df, col)`: Normaliza valores a escala 0–100.
* `uppercase_column(df, col)`: Convierte a mayúsculas los valores de una columna.

---

## **3️⃣ Bloque 3 – Pipeline local básico**

* Se crea un `main_ventas.py` básico para encadenar las funciones:

```python
from pipeline.load import load_csv
from pipeline.save import save_csv
from pipeline.transform import (
    clean_column_names, drop_nulls, filter_positive_values,
    drop_duplicates_by_column, normalize_column_0_100, uppercase_column
)

df = load_csv("data/input/ventas.csv")
df = clean_column_names(df)
df = drop_nulls(df)
df = filter_positive_values(df, "ventas")
df = drop_duplicates_by_column(df, "cliente")
df = normalize_column_0_100(df, "ventas")
df = uppercase_column(df, "cliente")
save_csv(df, "data/output/ventas_clean.csv")
```

* **Resultado**: pipeline funcional para un archivo fijo.

---

## **4️⃣ Bloque 4 – CLI con `argparse`**

Se reemplaza el main fijo por `main_ventas_cli.py` con **parámetros desde terminal**:

```python
import argparse
from pipeline.load import load_csv
from pipeline.save import save_csv
from pipeline.transform import (
    clean_column_names, drop_nulls, filter_positive_values,
    drop_duplicates_by_column, normalize_column_0_100, uppercase_column
)

def main(input_path, output_path, column, key_col, upper_col):
    df = load_csv(input_path)
    df = clean_column_names(df)
    df = drop_nulls(df)
    df = filter_positive_values(df, column)
    if key_col in df.columns:
        df = drop_duplicates_by_column(df, key_col)
    if column in df.columns:
        df = normalize_column_0_100(df, column)
    if upper_col in df.columns:
        df = uppercase_column(df, upper_col)
    save_csv(df, output_path)

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Pipeline ventas (CLI)")
    p.add_argument("--input", required=True, help="CSV de entrada")
    p.add_argument("--output", required=True, help="CSV de salida")
    p.add_argument("--column", default="ventas", help="Columna de valores positivos")
    p.add_argument("--key-col", default="cliente", help="Columna para quitar duplicados")
    p.add_argument("--upper-col", default="cliente", help="Columna para mayúsculas")
    args = p.parse_args()
    main(args.input, args.output, args.column, args.key_col, args.upper_col)
```

Ejemplo de ejecución:

```bash
python main_ventas_cli.py --input data/input/ventas.csv --output data/output/ventas_clean.csv
```

---

## **5️⃣ Bloque 5 – Parámetros opcionales**

* Se implementan **valores por defecto** en `argparse` para mayor flexibilidad.
* Permite ejecutar con:

```bash
python main_ventas_cli.py --input data/input/ventas.csv --output data/output/ventas_clean.csv --column ventas --key-col cliente
```

* Si no se pasan parámetros opcionales, usa valores por defecto definidos en `add_argument`.

---

## **6️⃣ Bloque 6 – Logging**

* Se agrega `utils/logger.py`:

```python
import logging
import os

def get_logger(name=__name__, log_file="logs/pipeline.log"):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(log_file)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
```

* En `main_ventas_cli.py` se reemplazan los `print()` por:

```python
from utils.logger import get_logger
logger = get_logger()

logger.info("Inicio del pipeline")
...
logger.info(f"Archivo guardado en: {output_path}")
```

* **Ventaja**: los eventos quedan registrados en `logs/pipeline.log` para auditoría.

---

## **📂 Estructura final (hasta Bloque 6)**

```
.
├── data/
│   ├── input/ventas.csv
│   └── output/ventas_clean.csv
├── logs/
│   └── pipeline.log
├── pipeline/
│   ├── load.py
│   ├── save.py
│   ├── transform.py
├── utils/
│   └── logger.py
├── main_ventas_cli.py
├── requirements.txt
└── README.md
```

---

## **📦 Instalación y uso**

1. Crear y activar entorno virtual:

```bash
python -m venv venv
.\venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecutar pipeline:

```bash
python main_ventas_cli.py --input data/input/ventas.csv --output data/output/ventas_clean.csv
```

---

## **✅ Resultado esperado**

En consola:

```
✅ Archivo guardado exitosamente en: data/output/ventas_clean.csv
```

En `logs/pipeline.log`:

```
2025-08-10 15:30:01 | INFO | Inicio del pipeline
2025-08-10 15:30:01 | INFO | Cargando datos
2025-08-10 15:30:02 | INFO | Transformando datos
2025-08-10 15:30:02 | INFO | Guardando datos transformados
2025-08-10 15:30:02 | INFO | Pipeline finalizado con éxito
```

---

