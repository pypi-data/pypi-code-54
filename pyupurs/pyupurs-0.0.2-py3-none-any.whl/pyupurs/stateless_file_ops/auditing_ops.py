import csv

import pandas as pd

from pyupurs.stateless_file_ops import count_rows, count_cols_per_row


def audit_extra_separators(file_path: str, delimiter: str = "|", number_of_columns: int = None) -> pd.DataFrame:
    """
    Report rows where there is

    :param file_path:
    :param delimiter:
    :param number_of_columns:
    :return:
    """
    n_rows = count_rows(file_path, delimiter=delimiter)
    rows_n_cols = count_cols_per_row(file_path, delimiter=delimiter)
    if not number_of_columns:
        # Estimate of the number of cols. Assuming the most frequent col count is a valid criterion.
        number_of_columns = pd.Series(rows_n_cols).value_counts().idxmax()

    list_rows_n_cols = rows_n_cols.values()

    n_col_occurrences = len(set(list_rows_n_cols))

    abnormal_rows = []
    # Engage in defective row extraction only if the column count is suspicious
    if n_col_occurrences > 1:
        with open(file_path, "r") as file:
            f_object = csv.reader(file, delimiter=delimiter)
            for row in f_object:
                n_cols_for_this_row = len(row)
                #
                if n_cols_for_this_row != number_of_columns:
                    abnormal_rows.append(row)

    defective_df = pd.DataFrame(data=abnormal_rows)
    return defective_df
