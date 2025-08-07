## 3. Carga y guardado de datos CSV

---

### 3.1 🎯 Objetivo de esta sección

El objetivo es crear funciones reutilizables y profesionales para cargar y guardar datos desde y hacia archivos `.csv`, separando claramente la lógica de entrada/salida del resto del pipeline.

---

### 3.2 🗂️ Estructura del proyecto esperada

```
semana1_pipeline/
├── data/
│   ├── input/
│   │   └── input.csv
│   └── output/
│       └── clean.csv            ← generado automáticamente
├── pipeline/
│   ├── load.py                  ← función load_csv()
│   └── save.py                  ← función save_csv()
├── test_load.py                 ← script de prueba para cargar y guardar
└── README.md
```

---

### 3.3 🧩 Función `load_csv()` – Cargar un archivo CSV

**Archivo:** `pipeline/load.py`

```python
import pandas as pd

def load_csv(path):
    """
    Carga un archivo CSV desde la ruta indicada y lo devuelve como DataFrame.
    """
    return pd.read_csv(path)
```

---

### 3.4 💾 Función `save_csv()` – Guardar un archivo CSV

**Archivo:** `pipeline/save.py`

```python
def save_csv(df, path):
    """
    Guarda un DataFrame como CSV en la ruta especificada.
    """
    df.to_csv(path, index=False)
```

---

### 3.5 🔗 Código modularizado y reutilizable

Las funciones `load_csv` y `save_csv` están desacopladas y separadas en módulos distintos. Esto permite:

- 📦 Reutilizarlas desde cualquier script del proyecto.
- 🧪 Testearlas fácilmente de forma aislada.
- 🚀 Escalarlas a otras fuentes de datos (JSON, Parquet, etc.).
- 🧠 Mantener el código limpio y legible.

Podés importarlas así:

```python
from pipeline.load import load_csv
from pipeline.save import save_csv
```

---

### 3.6 🧪 Prueba de carga y guardado

Creamos un script que use ambas funciones para comprobar que funcionan correctamente.

**Archivo:** `test_load.py`

```python
from pipeline.load import load_csv
from pipeline.save import save_csv

df = load_csv("data/input/input.csv")
print(df.head())

save_csv(df, "data/output/clean.csv")
```

Si todo está bien, el archivo `clean.csv` aparecerá dentro de `data/output/`.

---

### 3.7 ⚠️ Posibles errores al ejecutar

Si ves este error:

```
FileNotFoundError: [Errno 2] No such file or directory: 'data/input/input.csv'
```

Significa que ejecutaste el script desde una carpeta incorrecta. Python interpreta las rutas relativas desde donde se lanza el script, no desde donde está guardado.

---

### 3.8 ✅ Solución: ejecutar desde la raíz

Parate en la raíz del proyecto y corré el script así:

```bash
python test_load.py
```

Con eso, las rutas relativas a `data/` van a funcionar correctamente.

---

✅ ¡Listo! Ya tenés un sistema profesional para manejar archivos CSV, con funciones desacopladas, bien probadas y estructuradas para escalar.
