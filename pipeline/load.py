import pandas as pd

def load_csv(path: str) -> pd.DataFrame:
    """
    Lee un archivo CSV y devuelve un DataFrame.
    """
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {path}")
        raise
