### 📂 SECCIÓN 3 – Carga y guardado de datos

```markdown
## 3.1 Objetivo de esta sección

El objetivo es crear funciones reutilizables y profesionales para **cargar datos desde archivos CSV** y luego **guardar los datos transformados**. Esto nos permite separar la lógica de negocio del input/output, facilitando el mantenimiento del código, las pruebas unitarias, y la futura escalabilidad del pipeline.

---

## 3.2 Estructura esperada del proyecto

Tu proyecto debe tener esta forma:

```

semana1\_pipeline/
├── data/
│   ├── input/
│   │   └── input.csv
│   └── output/
│       └── clean.csv  ← (se generará automáticamente)
├── pipeline/
│   ├── load.py       ← función load\_csv()
│   └── save.py       ← función save\_csv()
├── test\_load.py      ← script de prueba para cargar y guardar
└── README.md

````

---

## 3.3 Función `load_csv()` – Cargar un archivo CSV

**Archivo**: `pipeline/load.py`

```python
import pandas as pd

def load_csv(path):
    """
    Carga un archivo CSV desde la ruta especificada y devuelve un DataFrame.
    
    Parámetros:
        path (str): Ruta al archivo CSV.
        
    Retorna:
        pd.DataFrame: DataFrame con los datos cargados.
    """
    df = pd.read_csv(path)
    return df
````

---

## 3.4 Función `save_csv()` – Guardar un DataFrame a CSV

**Archivo**: `pipeline/save.py`

```python
def save_csv(df, path):
    """
    Guarda un DataFrame en un archivo CSV en la ruta especificada.
    
    Parámetros:
        df (pd.DataFrame): DataFrame a guardar.
        path (str): Ruta destino del archivo CSV.
    """
    df.to_csv(path, index=False)
    print(f"✅ Archivo guardado exitosamente en: {path}")
```

---

## 3.5 ¿Qué significa código modular y desacoplado?

* **Modular**: cada función cumple una única responsabilidad y vive en su propio archivo (`load.py`, `save.py`, etc.).
* **Desacoplado**: el código que transforma los datos **no depende** de si el input viene de un `.csv`, `.json`, una base de datos o un API. Se espera que todo sea manejado como un `DataFrame`.

Esto es clave para escalar, testear y automatizar tu pipeline en el futuro (con Airflow, Lambda, etc.).

---

## 3.6 Bonus – Soporte para otros formatos (parquet, json, excel)

Una vez que tengas dominado el flujo básico con CSV, podés extender la lógica para que también cargue o guarde `.parquet`, `.json`, `.xlsx` según la extensión:

```python
def load_data(path: str) -> pd.DataFrame:
    if path.endswith(".csv"):
        return pd.read_csv(path)
    elif path.endswith(".parquet"):
        return pd.read_parquet(path)
    elif path.endswith(".json"):
        return pd.read_json(path)
    elif path.endswith(".xlsx"):
        return pd.read_excel(path)
    else:
        raise ValueError("Formato no soportado")
```

Y para guardar:

```python
def save_data(df: pd.DataFrame, path: str):
    if path.endswith(".csv"):
        df.to_csv(path, index=False)
    elif path.endswith(".parquet"):
        df.to_parquet(path, index=False)
    elif path.endswith(".json"):
        df.to_json(path, orient="records", lines=True)
    elif path.endswith(".xlsx"):
        df.to_excel(path, index=False)
    else:
        raise ValueError("Formato no soportado")
```

---

## 3.7 ¿Cómo probar tus funciones `load_csv()` y `save_csv()`?

**Archivo de prueba:** `test_load.py`

```python
from pipeline.load import load_csv
from pipeline.save import save_csv

df = load_csv("data/input/input.csv")
print(df.head())

save_csv(df, "data/output/clean.csv")
```

Este script hace lo siguiente:

1. Carga el archivo `input.csv` desde `data/input/`.
2. Imprime las primeras filas para ver si se cargó bien.
3. Guarda una copia limpia en `data/output/clean.csv`.

---

## 3.8 Solución si aparece el error `FileNotFoundError`

### ❌ Problema común:

```
FileNotFoundError: [Errno 2] No such file or directory: 'data/input/input.csv'
```

### 🔍 Causa:

Este error aparece si ejecutás el script desde un directorio incorrecto. Las rutas relativas en Python **se interpretan desde donde ejecutás el script**, no desde donde está escrito.

### ✅ Solución correcta:

Siempre ejecutá desde la raíz del proyecto:

```bash
python test_load.py
```

Así, rutas como `"data/input/input.csv"` funcionarán bien.

---

## 3.9 Checklist final para que todo funcione

* [x] Estás en la raíz del proyecto (`semana1_pipeline/`).
* [x] `input.csv` está dentro de `data/input/`.
* [x] Tenés el archivo `test_load.py`.
* [x] Corrés el script con `python test_load.py`.
* [x] Se genera correctamente `clean.csv` en `data/output/`.

```

---


