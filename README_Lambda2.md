![alt text](image-1.png)


![alt text](image-2.png)






![alt text](image-3.png)

# 1) Crear carpeta limpia
rm -rf build312 && mkdir -p build312/pkg && cd build312

# 2) Instalar dependencias correctas en pkg/ (sin Docker ni layers)
python3 -m pip install \
  --platform manylinux2014_x86_64 \
  --implementation cp \
  --python-version 312 \
  --only-binary=:all: \
  --no-deps \
  -t pkg \
  numpy==2.0.1 pandas==2.2.2 python-dateutil pytz tzdata

# 3) Crear el código Lambda (puedes subirlo o pegarlo aquí mismo)
cat > lambda_function.py <<'PY'
# (pegar aquí el código completo mostrado arriba)
PY

# 4) Armar el ZIP final
zip -r9 ../lambda_package_py312.zip . >/dev/null
cd ..
ls -lh lambda_package_py312.zip
# Debería pesar ~40 MB


![alt text](image-4.png)

![alt text](image-5.png)

{
  "Records": [
    {
      "s3": {
        "bucket": { "name": "marcelo-ventas-pipeline-input" },
        "object": { "key": "raw/ventas.csv" }
      }
    }
  ]
}


![alt text](image-6.png)
