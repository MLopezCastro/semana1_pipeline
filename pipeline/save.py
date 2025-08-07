import pandas as pd

def save_csv(df: pd.DataFrame, path: str):
    """
    Guarda un DataFrame como archivo CSV.

    Args:
        df (pd.DataFrame): Datos a guardar.
        path (str): Ruta de salida.
    """
    df.to_csv(path, index=False)
