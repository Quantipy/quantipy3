from pandas.core.dtypes.common import is_string_dtype
import numpy as np

def dataframe_fix_string_types(df):
    for col in df.columns:
        if is_string_dtype(df[col]):
            df[col] = df[col].astype("str").replace({'nan': np.nan})

    #df = df.replace({'nan': np.nan})
    return df

