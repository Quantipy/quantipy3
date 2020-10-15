import json
import pandas as pd
from quantipy.core.helpers.functions import load_json
from quantipy.core.tools.dp.prep import start_meta

def quantipy_from_confirmit(confirmit_meta, confirmit_data, text_key='en-GB'):
    """Convert confirmit meta data and data to Quantipy

    Parameters
    ----------
    confirmit_meta : str
        File location of meta data.
    confirmit_data : type
        File location of data.
    text_key : type
        Language key. Defaults to en-GB

    Returns
    -------
    list

        Array with meta data and data, both quantipy compatible.

    """
    confirmit_meta = load_json(confirmit_meta)
    data = pd.read_json(confirmit_data, orient='records')

    # do we want the default text key to be settable? may
    meta = start_meta(text_key=text_key)

    # TODO: function that maps these
    quantipy_meta = confirmit_meta

    # TODO: function that maps these
    quantipy_data = data

    return [quantipy_meta, quantipy_data]
