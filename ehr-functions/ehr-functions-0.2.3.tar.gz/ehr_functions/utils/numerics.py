import numpy as np


def make_numeric(df, cols=None, ignore_cols=None, return_new_cols=False):
    """
    :param df:
    :param cols:
    :param ignore_cols:
    :param return_new_cols:
    :return:
    """
    # Keep track of new column names that were added
    new_cols = []

    cols_search = cols
    if cols_search is None:
        cols_search = df.columns.tolist()
        cols_search.remove('PatientID')

    # If are a category column then converting it to multiple columns (column for each cat)
    for col in cols_search:
        if df[col].dtype == object:
            unique_values = df[col].unique().tolist()

            # If less than two then just convert to be boolean
            if len(unique_values) <= 2:
                df[col] = df[col].apply(lambda x: True if x == unique_values[0] else False).astype(np.int64)
            else:
                # Otherwise make separate columns for each unique value
                for value in unique_values:
                    if value != '':
                        new_col_name = col + '_' + value
                        df[new_col_name] = df[col].apply(lambda x: True if x == value else False).astype(np.int64)
                        new_cols.append(new_col_name)

                df = df.drop(columns=[col])

    if return_new_cols:
        return df, new_cols

    return df
