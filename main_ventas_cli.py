# main_ventas_cli.py
import argparse
from utils.logger import get_logger
from pipeline.load import load_csv
from pipeline.save import save_csv
from pipeline.transform import (
    clean_column_names,
    drop_nulls,
    filter_positive_values,
    drop_duplicates_by_column,
    normalize_column_0_100,
    uppercase_column,
)

# Creamos logger
logger = get_logger("ventas_cli")

def main(input_path: str, output_path: str, column: str, key_col: str, upper_col: str):
    logger.info("Inicio del pipeline (ventas CLI)")
    logger.info(f"Cargando datos desde: {input_path}")

    try:
        df = load_csv(input_path)
    except FileNotFoundError:
        logger.error(f"No se encontró el archivo: {input_path}")
        raise

    logger.info("Aplicando transformaciones")
    df = clean_column_names(df)
    df = drop_nulls(df)
    logger.info(f"Filtrando valores positivos en columna: {column}")
    df = filter_positive_values(df, column)

    if key_col in df.columns:
        logger.info(f"Eliminando duplicados por columna: {key_col}")
        df = drop_duplicates_by_column(df, key_col)
    else:
        logger.info(f"Omito drop_duplicates: no existe columna '{key_col}'")

    if column in df.columns:
        logger.info(f"Normalizando columna (0–100): {column}")
        df = normalize_column_0_100(df, column)
    else:
        logger.info(f"Omito normalización: no existe columna '{column}'")

    if upper_col in df.columns:
        logger.info(f"Creando columna en mayúsculas desde: {upper_col}")
        df = uppercase_column(df, upper_col)
    else:
        logger.info(f"Omito uppercase: no existe columna '{upper_col}'")

    logger.info(f"Guardando resultados en: {output_path}")
    save_csv(df, output_path)
    logger.info("Pipeline finalizado con éxito")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Pipeline ventas (CLI)")
    p.add_argument("--input", required=True, help="CSV de entrada, ej: data/input/ventas.csv")
    p.add_argument("--output", required=True, help="CSV de salida, ej: data/output/ventas_clean.csv")
    p.add_argument("--column", default="ventas", help="Columna a filtrar > 0 (default: ventas)")
    p.add_argument("--key-col", default="cliente", help="Columna para quitar duplicados (default: cliente)")
    p.add_argument("--upper-col", default="cliente", help="Columna para crear *_upper (default: cliente)")
    args = p.parse_args()
    main(args.input, args.output, args.column, args.key_col, args.upper_col)

