import pandas as pd


def sum_category_price(df_prices: pd.DataFrame, key, category=None):
    if df_prices is None:
        return 0
    if category is not None:
        mask_category = df_prices["category"] == category
        df_prices = df_prices[mask_category]
        return df_prices[mask_category][key].sum()
    return df_prices[key].sum()
