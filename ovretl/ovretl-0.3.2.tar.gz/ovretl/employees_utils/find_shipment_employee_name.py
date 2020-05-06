import pandas as pd


def find_shipment_employee_name(
    employees_associated_df: pd.DataFrame, role: str, shipment_id: float
):
    mask_employees = employees_associated_df["role"] == role
    mask_shipment = employees_associated_df["shipment_id"] == shipment_id
    employees_associated_df_filtered = employees_associated_df[
        mask_employees & mask_shipment
    ].reset_index(drop=True)
    if len(employees_associated_df_filtered) > 0:
        return employees_associated_df_filtered.loc[0, "name"]
    return None
