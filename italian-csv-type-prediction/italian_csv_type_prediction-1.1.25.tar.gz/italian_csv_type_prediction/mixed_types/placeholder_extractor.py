import pandas as pd
from typing import Dict


class PlaceholderExtractor:

    def _to_placeholder(self, value, value_type) -> Dict:
        return {
            "placeholder": "{{{value_type}}}".format(value_type=value_type),
            "values": {
                value_type: value
            }
        }

    def extract(self, df: pd.DataFrame, types: pd.DataFrame) -> pd.DataFrame:
        return pd.DataFrame({
            column: [
                self._to_placeholder(value, value_type)
                for value, value_type in zip(df[column], types[column])
            ]
            for column in df.columns
        })
