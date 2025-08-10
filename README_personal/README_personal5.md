

---

# 🖥️ Sección 5 – Ejecución del pipeline por terminal con `argparse`

## 🎯 Objetivo

Implementar un sistema de **parámetros por línea de comando** para que el pipeline pueda ejecutarse desde la terminal sin modificar el código fuente. Esto hace que el script sea más **flexible**, **reutilizable** y fácil de integrar con otros procesos.

---

## 📌 Archivos clave en este paso

### `main_ventas_cli.py`

Script principal que:

1. Usa **`argparse`** para recibir parámetros.
2. Llama a las funciones del pipeline (`load_csv`, `clean_column_names`, `drop_nulls`, etc.).
3. Guarda el archivo limpio en la ubicación indicada.

Ejemplo de fragmento:

```python
import argparse
from utils.io import load_csv, save_csv
from utils.transform import clean_column_names, drop_nulls

def main(input_path, output_path):
    df = load_csv(input_path)
    df = clean_column_names(df)
    df = drop_nulls(df)
    save_csv(df, output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline de limpieza de ventas")
    parser.add_argument("--input", required=True, help="Ruta del archivo de entrada")
    parser.add_argument("--output", required=True, help="Ruta de salida para el archivo limpio")
    args = parser.parse_args()
    main(args.input, args.output)
```

---

## 🚀 Ejemplo de ejecución

Desde la carpeta raíz del proyecto y con el entorno virtual activado:

```bash
python main_ventas_cli.py --input data/input/ventas.csv --output data/output/ventas_clean.csv
```

💡 Esto permite procesar **cualquier archivo CSV** cambiando solo los parámetros, sin tocar el código.

---

## 📂 Estructura del proyecto en este punto

```
semana1_pipeline/
│
├── data/
│   ├── input/
│   │   └── ventas.csv
│   └── output/
│       └── ventas_clean.csv
│
├── utils/
│   ├── io.py
│   └── transform.py
│
├── main_ventas_cli.py
└── venv/
```

---

## ✅ Resultado esperado

Al ejecutar, se genera un archivo limpio en la carpeta de salida y se muestra un mensaje de confirmación en consola:

```
✅ Archivo guardado exitosamente en: data/output/ventas_clean.csv
```

---

## 🔍 Ventajas de usar `argparse`

* Flexibilidad: se puede usar el mismo script para distintos datasets.
* Escalabilidad: fácil integración con jobs automatizados (cron, Airflow, etc.).
* Mantenibilidad: no es necesario modificar el código para cambiar entradas/salidas.

---


