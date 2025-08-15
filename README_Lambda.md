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
