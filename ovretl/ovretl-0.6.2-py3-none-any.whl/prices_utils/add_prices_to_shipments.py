import pandas as pd

from ovretl.prices_utils.sum_category_price import sum_category_price


def calculate_shipment_prices(shipment: pd.Series, df_prices: pd.DataFrame) -> pd.Series:
    shipment["departure_truck_freight_price"] = sum_category_price(df_prices, category="departure_truck_freight")
    shipment["departure_fees_price"] = sum_category_price(df_prices, category="departure_fees")
    shipment["freight_price"] = sum_category_price(df_prices, category="freight")
    shipment["arrival_fees_price"] = sum_category_price(df_prices, category="arrival_fees")
    shipment["arrival_truck_freight_price"] = sum_category_price(df_prices, category="arrival_truck_freight")
    shipment["insurance_price"] = sum_category_price(df_prices, category="insurance")
    shipment["turnover"] = (
        shipment["departure_truck_freight_price"]
        + shipment["departure_fees_price"]
        + shipment["freight_price"]
        + shipment["arrival_fees_price"]
        + shipment["arrival_truck_freight_price"]
        + shipment["insurance_price"]
    )
    shipment["customs_price"] = sum_category_price(df_prices, category="customs")
    shipment["other_price"] = sum_category_price(df_prices, category="other")
    shipment["vat_price"] = sum_category_price(df_prices, category="vat_price_in_eur")
    return shipment


def calculate_margins(shipment: pd.Series, df_prices: pd.DataFrame, df_prices_initial: pd.DataFrame) -> pd.Series:
    shipment["initial_margin_without_insurance"] = sum_category_price(
        df_prices_initial, category=None, key="margin_price_in_eur"
    ) - sum_category_price(df_prices_initial, key="margin_price_in_eur", category="insurance")
    shipment["initial_margin_insurance"] = sum_category_price(
        df_prices_initial, key="margin_price_in_eur", category="insurance"
    )
    shipment["margin_without_insurance"] = sum_category_price(
        df_prices, key="margin_price_in_eur"
    ) - sum_category_price(df_prices, key="margin_price_in_eur", category="insurance")
    shipment["margin_insurance"] = sum_category_price(df_prices, key="margin_price_in_eur", category="insurance")
    return shipment


def calculate_shipment_purchase_prices(shipment: pd.Series, df_prices: pd.DataFrame) -> pd.Series:
    shipment["departure_truck_freight_purchase_price"] = sum_category_price(
        df_prices, category="departure_truck_freight", key="purchase_price_in_eur"
    )
    shipment["departure_fees_purchase_price"] = sum_category_price(
        df_prices, category="departure_fees", key="purchase_price_in_eur"
    )
    shipment["freight_purchase_price"] = sum_category_price(df_prices, category="freight", key="purchase_price_in_eur")
    shipment["arrival_fees_purchase_price"] = sum_category_price(
        df_prices, category="arrival_fees", key="purchase_price_in_eur"
    )
    shipment["arrival_truck_freight_purchase_price"] = sum_category_price(
        df_prices, category="arrival_truck_freight", key="purchase_price_in_eur"
    )
    shipment["insurance_purchase_price"] = sum_category_price(
        df_prices, category="insurance", key="purchase_price_in_eur"
    )
    return shipment


def add_prices_to_shipments(shipment: pd.Series, find_most_relevant_prices) -> pd.Series:
    df_prices = find_most_relevant_prices(shipment["shipment_id"], shipment["proposition_id"])
    df_prices_initial = find_most_relevant_prices(shipment["shipment_id"], None, initial_proposition=True)
    shipment = calculate_shipment_prices(shipment=shipment, df_prices=df_prices)
    shipment = calculate_margins(shipment=shipment, df_prices=df_prices, df_prices_initial=df_prices_initial)
    shipment = calculate_shipment_purchase_prices(shipment=shipment, df_prices=df_prices)
    return shipment
