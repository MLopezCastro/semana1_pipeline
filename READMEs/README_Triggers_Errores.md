Perfecto, te armo un README en **Markdown** bien explicado, que incluya lo que hiciste y lo que hay que saber para estos dos puntos (manejo de errores + trigger en S3 con alertas por SNS).

---

````markdown
# 📦 AWS Lambda – Manejo de Errores y Triggers en S3 con Alertas por SNS

Este módulo cubre dos aspectos fundamentales para un flujo de procesamiento de datos en la nube:

1. **Manejo robusto de errores en AWS Lambda** (detección, logging, branching lógico y notificaciones por email).
2. **Automatización con triggers de S3** (ejecución de Lambda al subir un archivo).

---

## 4. Manejo de Errores y Alertas

### 🎯 Objetivo
Diseñar un flujo donde **Lambda detecte errores durante la carga o transformación de datos**, los registre en los logs y envíe un **correo de alerta** vía Amazon SNS.

---

### 🔹 4.1 Simulación de errores
Para probar el sistema, se subieron archivos con problemas comunes:
- Columnas faltantes.
- Tipos de datos inválidos.
- Valores nulos en campos obligatorios.

Esto fuerza a que la función **lance una excepción**, activando la notificación.

---

### 🔹 4.2 Manejo de errores con `try/except`
El código principal está envuelto en un bloque `try/except`:

```python
try:
    # Lógica principal: leer CSV, validar, transformar
    ...
except Exception as e:
    logger.error(f"Error al procesar el archivo: {e}")
    _notify_sns(str(e), bucket, key)  # Enviar alerta por SNS
    raise
````

---

### 🔹 4.3 Registro de errores en logs

Se usa el **logger de Python** para dejar evidencia de:

* El error ocurrido.
* El archivo que lo provocó.
* La traza (stack trace) si es necesario.

Estos logs son visibles en **CloudWatch**.

---

### 🔹 4.4 Branching lógico

Se implementaron **comportamientos distintos según condiciones** del archivo:

* **Archivo válido** → procesa, sube a carpeta `processed/`, no envía correo.
* **Archivo inválido** → detiene el proceso, registra error y envía alerta por SNS.

---

### 🔹 4.5 Retries automáticos de Lambda

Por defecto, AWS Lambda **reintenta la ejecución** en caso de error cuando la invocación viene de S3:

* Hasta **2 intentos adicionales**.
* Retraso exponencial entre intentos.
* Si el error persiste, el evento se envía a **Dead Letter Queue (DLQ)** si está configurada.

---

## 4. Triggers de S3 para Lambda

### 🎯 Objetivo

Configurar S3 para que ejecute la función Lambda **automáticamente** cada vez que se suba un archivo.

---

### 🔹 4.1 ¿Qué es un trigger en S3?

Un trigger es una **regla de evento** en S3 que le dice a AWS:

> “Cuando alguien suba un archivo a este bucket, ejecutá esta función Lambda”.

---

### 🔹 4.2 Configuración

1. Ir al bucket de S3.
2. Pestaña **Eventos** → **Crear evento**.
3. Seleccionar:

   * **Tipo de evento:** `PUT` (subida de objeto).
   * **Prefijo opcional:** carpeta de origen (ej. `raw/`).
4. Seleccionar la función Lambda.
5. Guardar.

---

### 🔹 4.3 Flujo completo validado

1. **Subida de archivo válido**:

   * Trigger de S3 → Lambda procesa → resultado limpio en `processed/`.
   * No se envía alerta.

2. **Subida de archivo inválido**:

   * Trigger de S3 → Lambda detecta error → registra log → envía mail por SNS.

---

## 📧 Notificaciones por Amazon SNS

* Se creó un **tópico SNS**.
* Se suscribió una dirección de correo electrónico.
* Lambda publica en el tópico cuando detecta un error.
* El correo llega en segundos al inbox del suscriptor.

---

## 🛠 Tecnologías utilizadas

* **AWS Lambda** – Ejecución serverless del código.
* **Amazon S3** – Almacenamiento y eventos de subida.
* **Amazon SNS** – Envío de alertas por email.
* **CloudWatch Logs** – Registro y monitoreo de ejecuciones.
* **Python** – Lógica de validación y procesamiento.

---

## 📌 Resumen de lo implementado

* [x] Simulación de errores en archivos.
* [x] Manejo de excepciones con `try/except`.
* [x] Logging detallado en CloudWatch.
* [x] Lógica condicional según validez del archivo.
* [x] Trigger de S3 para ejecución automática.
* [x] Notificación automática de errores por SNS.

---

```

---


