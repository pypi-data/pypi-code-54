import pandas as pd


def find_most_relevant_prices_factory(prices_propositions_by_category_df: pd.DataFrame, final_checks_df: pd.DataFrame, prices_final_check_by_category_df: pd.DataFrame, billings_df: pd.DataFrame, prices_billings_by_category_df: pd.DataFrame):
    def find_most_relevant_prices(shipment_id: str, proposition_id: str, initial_proposition=False):
        if initial_proposition == True:
            final_checks_filtered = final_checks_df[final_checks_df['shipment_id'] == shipment_id].reset_index(drop=True)
            if len(final_checks_filtered) > 0:
                initial_proposition_id = final_checks_filtered.loc[0, 'initial_proposition_id']
                prices_propositions_by_category_df_filtered = prices_propositions_by_category_df[prices_propositions_by_category_df['proposition_id'] == initial_proposition_id]
                if len(prices_propositions_by_category_df_filtered) > 0:
                    return prices_propositions_by_category_df_filtered

        billings_filtered = billings_df[billings_df['shipment_id'] == shipment_id].reset_index(drop=True)
        if len(billings_filtered) > 0:
            billing_id = billings_filtered.loc[0, 'id']
            prices_billings_filtered = prices_billings_by_category_df[prices_billings_by_category_df['billing_id'] == billing_id]
            if len(prices_billings_filtered) > 0:
                return prices_billings_filtered

        final_checks_filtered = final_checks_df[final_checks_df['shipment_id'] == shipment_id].reset_index(drop=True)
        if len(final_checks_filtered) > 0:
            final_check_id = final_checks_filtered.loc[0, 'id']
            prices_final_check_filtered = prices_final_check_by_category_df[prices_final_check_by_category_df['final_check_id'] == final_check_id]
            if len(prices_final_check_filtered) > 0:
                return prices_final_check_filtered

        if not pd.isna(proposition_id):
            return prices_propositions_by_category_df[prices_propositions_by_category_df['proposition_id'] == proposition_id]
        return None
    return find_most_relevant_prices


def sum_category_price(df_prices: pd.DataFrame, category: str, key='price_in_eur'):
    if df_prices is None:
        return 0
    mask_category = df_prices['category'] == category
    return df_prices[mask_category][key].sum()


def sum_vat_price(df_prices: pd.DataFrame):
    if df_prices is None:
        return 0
    return df_prices['vat_price_in_eur'].sum()


def sum_category_margin_price(df_prices: pd.DataFrame, category=None):
    if df_prices is None:
        return 0
    if category is not None:
        df_prices = df_prices[df_prices['category'] == category]
    return df_prices['margin_price_in_eur'].sum()
