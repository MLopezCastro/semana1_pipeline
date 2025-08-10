# main_ventas_cli.py
import argparse
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

def main(input_path: str, output_path: str, column: str, key_col: str, upper_col: str):
    df = load_csv(input_path)
    df = clean_column_names(df)
    df = drop_nulls(df)
    df = filter_positive_values(df, column)
    if key_col in df.columns:
        df = drop_duplicates_by_column(df, key_col)
    if column in df.columns:
        df = normalize_column_0_100(df, column)
    if upper_col in df.columns:
        df = uppercase_column(df, upper_col)
    save_csv(df, output_path)

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Pipeline ventas (CLI)")
    p.add_argument("--input", required=True, help="CSV de entrada, ej: data/input/ventas.csv")
    p.add_argument("--output", required=True, help="CSV de salida, ej: data/output/ventas_clean.csv")
    p.add_argument("--column", default="ventas", help="Columna a filtrar > 0 (default: ventas)")
    p.add_argument("--key-col", default="cliente", help="Columna para quitar duplicados (default: cliente)")
    p.add_argument("--upper-col", default="cliente", help="Columna para crear *_upper (default: cliente)")
    args = p.parse_args()
    main(args.input, args.output, args.column, args.key_col, args.upper_col)
