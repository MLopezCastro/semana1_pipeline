## 4. Transformaciones y Limpieza de Datos

Una parte esencial en cualquier pipeline de datos es la etapa de **transformación**. Aquí es donde convertimos datos crudos en una versión más **limpia, coherente y útil para el análisis**. A continuación, se describen todas las funciones creadas en el módulo `transform.py`, explicando su propósito, lógica interna y casos de uso.

---

### 4.1 ¿Por qué modularizar?

Dividir la lógica en funciones pequeñas permite que cada paso:

- Se entienda mejor.
- Pueda reutilizarse en otros scripts o pipelines.
- Se pueda testear por separado.
- Sea más fácil de mantener o modificar si cambian los requerimientos.

En lugar de escribir una sola función que haga todo junto, definimos una transformación por función. Esto es una buena práctica profesional.

---

### 4.2 Funciones desarrolladas

A continuación se explican todas las funciones incluidas en el archivo `pipeline/transform.py`:

---

#### `clean_column_names(df)`

**Objetivo**: estandarizar los nombres de columnas, convirtiéndolos a minúsculas y reemplazando espacios por guiones bajos.

**Ejemplo**: `"Nombre Cliente"` → `"nombre_cliente"`

**¿Por qué?** Porque los nombres con mayúsculas, acentos o espacios pueden dar problemas más adelante al escribir código o al integrarse con otras herramientas.

---

#### `drop_nulls(df)`

**Objetivo**: eliminar filas con valores nulos (NaN).

**¿Cuándo usarlo?** Cuando sabemos que no podemos trabajar con datos incompletos y queremos garantizar calidad mínima.

**Ejemplo**:
Si un cliente o una venta está incompleta, esa fila se elimina.

---

#### `filter_positive_values(df, column_name)`

**Objetivo**: quedarnos solo con filas donde el valor de una columna numérica sea mayor que 0.

**¿Cuándo usarlo?** Si estamos analizando ventas, precios, unidades, y no queremos incluir datos negativos o iguales a cero.

---

#### `drop_duplicates_by_column(df, column_name)`

**Objetivo**: eliminar filas duplicadas en base a una columna clave.

**¿Ejemplo?** Si una tabla tiene varias veces el mismo producto con los mismos datos, esta función lo limpia.

---

#### `normalize_column_0_100(df, column_name)`

**Objetivo**: transformar los valores de una columna para que estén en un rango entre 0 y 100.

**¿Para qué sirve?** Para comparar datos en escalas distintas o preparar datos para visualizaciones más claras o modelos de ML.

**Ejemplo práctico**: Si tenemos ventas que van de $50 a $5.000, los normalizamos así:
- $50 → 0
- $5.000 → 100
- $2.525 → 50

**Nota**: no sobreescribe la columna original. Crea una nueva con sufijo `_norm`.

---

#### `uppercase_column(df, column_name)`

**Objetivo**: convierte los valores string de una columna a mayúsculas.

**¿Ejemplo?** `"ana"` → `"ANA"`

**¿Para qué sirve?** Para estandarizar nombres de clientes, productos, países, etc., y evitar problemas de análisis por diferencias de mayúsculas/minúsculas.

---

### 4.3 Código completo del módulo `transform.py`

```python
def clean_column_names(df):
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    return df

def drop_nulls(df):
    return df.dropna()

def filter_positive_values(df, column_name):
    return df[df[column_name] > 0]

def drop_duplicates_by_column(df, column_name):
    return df.drop_duplicates(subset=column_name)

def normalize_column_0_100(df, column_name):
    min_val = df[column_name].min()
    max_val = df[column_name].max()
    df[column_name + "_norm"] = ((df[column_name] - min_val) / (max_val - min_val)) * 100
    return df

def uppercase_column(df, column_name):
    df[column_name + "_upper"] = df[column_name].str.upper()
    return df

4.4 Testeo Manual: ¿Cómo sé que funcionan?
Antes de usar estas funciones en un pipeline real, es útil probarlas en un script o notebook separado. Esto se llama “testing manual”. Nos permite verificar que cada función hace lo que esperamos.

import pandas as pd
from pipeline.transform import (
    clean_column_names,
    drop_nulls,
    filter_positive_values,
    drop_duplicates_by_column,
    normalize_column_0_100,
    uppercase_column
)

# Creamos un DataFrame de ejemplo
df = pd.DataFrame({
    "Cliente ": ["Juan", "Ana", "Luis", "Anabella", "Oscar", None],
    "Producto": ["Notebook", "Tablet", "Smartphone", "Celular", "Mouse", "Tablet"],
    "Ventas": [1500, 800, 1200, 600, 40, 800]
})

# Aplicamos las transformaciones
df = clean_column_names(df)
df = drop_nulls(df)
df = filter_positive_values(df, "ventas")
df = drop_duplicates_by_column(df, "producto")
df = normalize_column_0_100(df, "ventas")
df = uppercase_column(df, "cliente")

print(df)


¿Qué resultado espero?

Columnas con nombres como cliente, producto, ventas.

Sin valores nulos.

Sin ventas negativas.

Una columna nueva ventas_norm con valores entre 0 y 100.

Una columna cliente_upper con los nombres en mayúscula.

💡 Consejo: Si una función te tira error, probala de forma aislada con un DataFrame mínimo. Así podés identificar qué parte está fallando y no tenés que revisar todo tu pipeline a la vez.

