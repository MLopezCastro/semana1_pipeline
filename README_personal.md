# 📒 Apuntes Personales – Semana 1: Setup del Proyecto

Este archivo resume todo lo que hice hasta ahora, para repasar fácilmente los comandos y conceptos básicos del entorno virtual y herramientas de calidad de código.

---

## 🧱 1. Crear carpeta del proyecto

```bash
mkdir semana1_pipeline
cd semana1_pipeline
```

---

## 🐍 2. Crear y activar entorno virtual

### Crear entorno virtual

```bash
python -m venv venv
```

Esto crea una carpeta `venv/` que contiene un entorno Python aislado.

### Activar (en Windows)

```bash
venv\Scripts\activate
```

Si aparece `(venv)` en la terminal, está activo.

### Verificar que estás usando el Python correcto

```bash
where python
```

Debe mostrar una ruta dentro de `venv\Scripts\python.exe`.

---

## 📦 3. Instalar herramientas de calidad de código

Con el entorno activado, ejecutar:

```bash
pip install black flake8 isort
```

### ¿Qué hace cada herramienta?

| Herramienta | Función |
|------------|---------|
| `black`    | Formatea automáticamente el código (espacios, sangrías, saltos de línea) |
| `flake8`   | Marca errores de estilo y posibles bugs |
| `isort`    | Ordena los `import` de forma correcta |

### Ejecutar sobre un archivo

```bash
black ejemplo.py
flake8 ejemplo.py
isort ejemplo.py
```

---

## 📁 4. Generar `requirements.txt`

```bash
pip freeze > requirements.txt
```

Esto guarda todas las dependencias instaladas para que otro pueda replicar tu entorno con:

```bash
pip install -r requirements.txt
```

---

## 🚫 5. Crear `.gitignore`

Para no subir `venv` ni archivos temporales:

```gitignore
venv/
__pycache__/
*.pyc
```

---

## 🟦 6. Subir proyecto a GitHub

### Crear repo desde GitHub (vacío)

Ejemplo: https://github.com/MLopezCastro/semana1_pipeline

### Conectar repo local con Git

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/MLopezCastro/semana1_pipeline.git
git push -u origin main
```

---

## 💡 Notas adicionales

- No se debe subir `venv` a GitHub. Siempre usar `.gitignore`.
- El entorno virtual se activa cada vez que abrís VS Code en esta carpeta.
- Si `flake8` marca errores, corregir antes de commitear (opcional pero recomendado).

---

---

## 🧠 Cómo mantener `requirements.txt` actualizado

Para no olvidar nunca qué paquetes necesita tu proyecto, seguí estas buenas prácticas:

### 1. Trabajá siempre en un entorno virtual

De esa forma, `pip freeze` solo listará las dependencias de este proyecto, sin mezclar con otros.

### 2. Cada vez que instales algo nuevo, actualizá `requirements.txt`

```bash
pip install nombre_paquete
pip freeze > requirements.txt

Ejemplo:

pip install pandas
pip freeze > requirements.txt

Verificá qué hay instalado:

pip list

(Te muestra todos los paquetes instalados y sus versiones)

---


```markdown
## 2.5 Estructura inicial del proyecto

```

semana\_1\_pipeline/
├── data/
│   ├── input.csv             # Archivo de entrada
│   └── output/               # Carpeta de salida
├── pipeline/                 # Lógica modularizada
│   ├── **init**.py
│   ├── load.py
│   ├── transform.py
│   ├── save.py
├── utils/
│   └── logger.py             # Logging centralizado
├── main.py                   # Punto de entrada del pipeline
├── requirements.txt
└── README.md

```

---

### 📁 ¿Por qué esta estructura?

- `pipeline/`: Contiene todas las funciones que componen el flujo ETL. Cada módulo hace una sola cosa.
- `utils/`: Para utilidades comunes, como logging, que serán usadas desde varios módulos.
- `data/`: Carpeta con insumos (`input.csv`) y outputs (`output/`).
- `main.py`: Punto de ejecución principal, donde se conectan todos los pasos.
- `requirements.txt`: Permite replicar el entorno fácilmente en cualquier máquina o deploy.
- `README.md`: Documentación del proyecto y cómo usarlo.

---

### 🧪 Tips adicionales

- Agregá un `.gitignore` con:

```

venv/
**pycache**/
data/output/
\*.pyc

````

- Iniciá Git:

```bash
git init
git add .
git commit -m "Initial project structure and setup"
````

---

## 2.6 Buenas prácticas desde el arranque

| Práctica                       | Qué evita                                             |
| ------------------------------ | ----------------------------------------------------- |
| Usar entorno virtual           | Conflictos de versiones y problemas en producción     |
| Dividir código en carpetas     | Mezcla de responsabilidades y código desordenado      |
| Versionar con Git              | Pérdida de historial y debugging difícil              |
| README claro                   | Proyecto difícil de entender si alguien más lo retoma |
| `requirements.txt` actualizado | Imposible de replicar el entorno exacto del proyecto  |

---

## 🎯 Resultado esperado de esta sección

Al final de esta sección, debés tener:

* [ ] &#x20;Entorno virtual funcional
* [ ] &#x20;Carpeta `pipeline/` lista para recibir funciones
* [ ] &#x20;Archivos de entrada y salida ubicados
* [ ] &#x20;Estructura ordenada para crecer a lo largo de las semanas
* [ ] &#x20;Primer commit hecho con Git

---

### 🧪 ¿Cómo verificar?

```bash
python -c "import pandas as pd; print(pd.__version__)"
ls pipeline/
```

---

## ✅ Checklist

* [ ] &#x20;Entorno virtual creado y activado
* [ ] &#x20;`pandas` instalado
* [ ] &#x20;Carpeta `pipeline/` con módulos vacíos
* [ ] &#x20;`requirements.txt` generado
* [ ] &#x20;Proyecto inicial commiteado en Git

```

---



