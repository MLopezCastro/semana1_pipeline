from pipeline.load import load_csv
from pipeline.save import save_csv
from pipeline.transform import (
    clean_column_names,
    drop_nulls,
    filter_positive_values,
    drop_duplicates_by_column,
    normalize_column_0_100,
    uppercase_column
)

# 1. Cargar el archivo original
df = load_csv("data/input/ventas.csv")

# 2. Aplicar transformaciones encadenadas
df = clean_column_names(df)
df = drop_nulls(df)
df = filter_positive_values(df, "ventas")  # Asegurate que la columna se llama así después del clean
df = drop_duplicates_by_column(df, "cliente")  # O la columna que quieras usar como clave
df = normalize_column_0_100(df, "ventas")
df = uppercase_column(df, "cliente")  # O el nombre correcto

# 3. Guardar el archivo transformado
save_csv(df, "data/output/ventas_clean.csv")
