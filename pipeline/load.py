import pandas as pd

def load_csv(path: str) -> pd.DataFrame:
    """
    Lee un archivo CSV y devuelve un DataFrame.

    Args:
        path (str): Ruta al archivo CSV.

    Returns:
        pd.DataFrame: Datos cargados.
    """
    return pd.read_csv(path)
