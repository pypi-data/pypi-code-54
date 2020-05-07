import json
import pandas as pd

def to_json(res):
    return json.loads(res)

def to_dataframe(res):
    return pd.DataFrame(res)