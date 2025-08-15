# README – AWS Lambda para Procesar CSV desde S3

Este README describe cómo crear una función Lambda en AWS que procese automáticamente archivos CSV subidos a un bucket S3, limpie y valide datos, y guarde el resultado procesado en otro bucket.

## Requisitos Previos
- Cuenta de AWS con permisos para Lambda y S3.
- AWS CLI configurada.
- Buckets de entrada y salida creados.
- Rol de ejecución con permisos `s3:GetObject` y `s3:PutObject`.

## Variables de Entorno en Lambda
- `INPUT_BUCKET`: nombre del bucket de entrada.
- `OUTPUT_BUCKET`: nombre del bucket de salida.
- `OUTPUT_PREFIX`: prefijo o carpeta de salida (por ejemplo: `processed/`).

## Pasos para Implementar
1. Crear una función Lambda en AWS (Python 3.9 o superior).
2. Comprimir el script `lambda_function.py` en un archivo ZIP.
3. Subir el ZIP en la consola de Lambda.
4. Configurar las variables de entorno mencionadas.
5. Asignar un rol IAM con permisos para S3.
6. Crear un trigger en Lambda conectado al bucket de entrada para eventos `PUT` (cuando se suba un archivo nuevo) filtrado por prefijo `raw/`.
7. Guardar y probar.

## Ejemplo de Evento S3
```json
{
  "Records": [
    {
      "s3": {
        "bucket": { "name": "mi-bucket-entrada" },
        "object": { "key": "raw/ventas.csv" }
      }
    }
  ]
}
´´´






