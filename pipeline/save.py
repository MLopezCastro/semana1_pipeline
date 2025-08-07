import pandas as pd

def save_csv(df: pd.DataFrame, path: str):
    """
    Guarda un DataFrame como archivo CSV.

    Args:
        df (pd.DataFrame): Datos a guardar.
        path (str): Ruta de salida.
    """
    try:
        df.to_csv(path, index=False)
        print(f"✅ Archivo guardado exitosamente en: {path}")
    except Exception as e:
        print(f"❌ Error al guardar el archivo en: {path}")
        print(f"Detalles: {e}")
        raise
