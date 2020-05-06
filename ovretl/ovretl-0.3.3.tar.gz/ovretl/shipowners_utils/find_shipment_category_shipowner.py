import pandas as pd


def find_shipment_category_shipowner(role: str, shipowners_associated_df: pd.DataFrame):
    mask_role = shipowners_associated_df["role"] == role
    shipowners_associated_df_filtered = shipowners_associated_df[mask_role].reset_index(
        drop=True
    )
    if len(shipowners_associated_df_filtered) > 0:
        return shipowners_associated_df_filtered.loc[0, "name"]
    return None
