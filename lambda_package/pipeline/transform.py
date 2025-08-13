def clean_column_names(df):
    """
    Limpia los nombres de columnas: minúsculas, sin espacios, con guiones bajos.
    """
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    return df

def drop_nulls(df):
    """
    Elimina filas con valores nulos.
    """
    return df.dropna()

def filter_positive_values(df, column_name):
    """
    Filtra solo las filas donde una columna tiene valores positivos.
    """
    return df[df[column_name] > 0]

def drop_duplicates_by_column(df, column_name):
    """
    Elimina filas duplicadas basándose en una columna clave.
    """
    return df.drop_duplicates(subset=column_name)


def normalize_column_0_100(df, column_name):
    """
    Normaliza una columna numérica para que sus valores estén entre 0 y 100.
    """
    min_val = df[column_name].min()
    max_val = df[column_name].max()
    df[column_name + "_norm"] = ((df[column_name] - min_val) / (max_val - min_val)) * 100
    return df

def uppercase_column(df, column_name):
    """
    Convierte todos los valores de una columna string a mayúsculas.
    """
    df[column_name + "_upper"] = df[column_name].str.upper()
    return df
