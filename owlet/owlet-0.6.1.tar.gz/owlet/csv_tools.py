"""
Basic CSV manipulations tools

"""

import csv

__all__ = ["read_csv", "write_csv", "col_indexer", "required_fields", "column_reducer", "attribute_filter", "unique_col_values"]


def read_csv(file_path, delimiter=",", encoding="utf-8"):
    """
    Reads a CSV file

    Parameters
    ----------
    file_path : str
    delimiter : str
    encoding : str

    Returns
    -------
    collection

    """

    with open(file_path, encoding=encoding) as file:
        data_in = list(csv.reader(file, delimiter=delimiter))

    return data_in


def write_csv(file_path, csv_data, delimiter=","):
    """
    Writes CSV file from 2D list

    Parameters
    ----------
    file_path : str
    csv_data : collection
    delimiter : str

    Returns
    -------
    None

    """

    with open(file_path, "w") as csv_out:
        write = csv.writer(csv_out, delimiter=delimiter, lineterminator='\n')
        for i in csv_data:
            write.writerow(i)


def col_indexer(reference_row, cols_to_index):
    """
    Determines the column index number of specified columns.

    Parameters
    ----------
    reference_row : collection
    cols_to_index : collection

    Returns
    -------
    list

    """

    indexes = [reference_row.index(x) for x in cols_to_index]

    return indexes


def required_fields(csv_list, cols_to_check):
    """
    Reduces a CSV to only the records that contain a value in each of the columns specified by cols_to_check

    Parameters
    ----------
    csv_list : collection
    cols_to_check : list

    Returns
    -------
    collection

    """

    cols_to_check_index = col_indexer(csv_list[0], cols_to_check)
    rows_to_remove = []
    new_csv_list = []
    for row in csv_list[1:]:
        for col in cols_to_check_index:
            if row[col] == "" and row not in rows_to_remove:
                rows_to_remove.append(row)
    for row in csv_list:
        if row not in rows_to_remove:
            new_csv_list.append(row)
    return new_csv_list


def column_reducer(csv_list, cols, remove=True):
    """
    Reduces CSV to specified columns

    Parameters
    ----------
    csv_list : collection
    cols : collection
    remove : bool
        True - remove specified columns
        False - retain only specified columns

    Returns
    -------
    collection

    """

    headers = csv_list[0]
    cols = col_indexer(headers, cols)

    if remove is False:
        remove_cols = []
        keep_cols = cols
        for x in range(0, len(csv_list[0])):
            if x not in keep_cols:
                remove_cols.append(x)
        cols = remove_cols

    reduced_csv = [list(x) for x in csv_list]
    cols = sorted(cols, reverse=True)
    for row in reduced_csv:
        for col in cols:
            del row[col]

    return reduced_csv


def attribute_filter(csv_list, target_values, target_col_name, equal_to=True):
    """
    Filters a CSV to the records that have the specified values found within the specified column.

    Parameters
    ----------
    csv_list :
    target_values : collection
    target_col_name : str
    equal_to : bool
        True - keep records matching specified values
        False - remove records matching specified values


    Returns
    -------
    collection

    """

    filtered = [csv_list[0]]

    target_col_index = col_indexer(csv_list[0], [target_col_name])[0]

    if equal_to is True:
        for row in csv_list:
            if row[target_col_index] in target_values:
                filtered.append(row)
    elif equal_to is False:
        for row in csv_list:
            if row[target_col_index] not in target_values:
                filtered.append(row)
    else:
        pass

    return filtered


def unique_col_values(csv_list, target_col_name):
    """
    Finds the unique values from a specified column.

    Parameters
    ----------
    csv_list : collection
    target_col_name : str

    Returns
    -------
    collection

    """

    target_col_index = col_indexer(csv_list[0], [target_col_name])[0]
    target_col_values = [row[target_col_index] for row in csv_list[1:]]
    unique_values = sorted(set(target_col_values))

    return unique_values
