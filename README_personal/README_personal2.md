## 2.5 Estructura inicial del proyecto

```
semana_1_pipeline/
├── data/
│   ├── input.csv
│   └── output/
├── pipeline/
│   ├── __init__.py
│   ├── load.py
│   ├── transform.py
│   └── save.py
├── utils/
│   └── logger.py
├── main.py
├── requirements.txt
└── README.md
```

---

### 📁 ¿Qué representa cada carpeta y archivo?

* **data/**: Contiene los archivos de entrada (`input.csv`) y el directorio donde se guardan los resultados procesados (`output/`).

* **pipeline/**: Módulo principal de procesamiento con funciones divididas por responsabilidad:

  * `load.py`: Carga de datos.
  * `transform.py`: Transformaciones aplicadas.
  * `save.py`: Guardado de resultados.

* **utils/**: Módulos de apoyo como logs personalizados, helpers, etc.

  * `logger.py`: Manejador de logs.

* **main.py**: Script principal que ejecuta el flujo completo del pipeline.

* **requirements.txt**: Lista de dependencias necesarias para correr el proyecto.

* **README.md**: Documentación del proyecto.

---

### ⚙️ Consejos para mantener la estructura limpia

* Evitá nombres ambiguos. Usá verbos para scripts (`load`, `save`) y sustantivos para datos (`input.csv`).
* Separá lógica de negocio de entrada/salida.
* Usá `__init__.py` para convertir carpetas en módulos importables.
* Mantené el `main.py` limpio: solo debería orquestar funciones del pipeline, no tener lógica compleja.

---


