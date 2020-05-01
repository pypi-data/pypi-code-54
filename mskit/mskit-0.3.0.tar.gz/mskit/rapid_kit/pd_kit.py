import re


def select_row_with_target_col(df, ident, colname, return_col_list=None):
    _df = df[df[colname].str.contains(ident)]
    if return_col_list:
        return _df[return_col_list]
    else:
        return _df


def extract_df_with_col_ident(original_df, identifiers, focus_col, return_col_list=None):
    if isinstance(identifiers, str):
        target_df = select_row_with_target_col(original_df, identifiers, focus_col, return_col_list)
        return target_df
    elif isinstance(identifiers, list):
        target_df_list = [select_row_with_target_col(original_df, _, focus_col, return_col_list) for _ in identifiers]
        return target_df_list
    else:
        return None


def df_keep_block_first_line(df_with_blocks, filtered_col_name):
    """
    To get the first line when the file is consist of many blocks which means some same values are in the same column in neighboring lines
    This may keep same values in the selected columns because the blocks have same values in the selected column may not be neighboring
    :param df_with_blocks:
    :param filtered_col_name:
    :return:
    """
    non_block_df = df_with_blocks[df_with_blocks[filtered_col_name] != df_with_blocks[filtered_col_name].shift(1)]
    return non_block_df


def protein_groups_match(x, protein_list, col='PG.ProteinGroups', delimiter=';'):
    if isinstance(x[col], float):
        return False
    if set(x[col].split(delimiter)) & set(protein_list):
        return True
    return False


def filter_prob(
        x,
        find_col,
        prob_col,
        ident='ph',
        recept_prob=0.75,
        refute_prob=0.75):
    """
    :param x: one row of the target dataframe
    :param find_col: colname of col contains sequence with determined label. Example: col 'Modified sequence' _(ac)AAAAAAAAAAAAGDS(ph)DS(ph)WDADTFSM(ox)EDPVRK_
    :param prob_col: colname of col contains sequence with probability. Example: col 'Phospho (STY) Probabilities' AAAAAAAAAAAAGDS(0.876)DS(0.887)WDADT(0.161)FS(0.077)MEDPVRK
    """
    find_col_content = x[find_col]
    # To avoid error if there is no mod in the seq. 'Modified sequence' will
    # have no Parentheses
    if '(' not in find_col_content:
        return True
    prob_col_content = x[prob_col]
    # To avoid error if there is no target var mod in the seq. Prob col will
    # be NaN
    if '(' not in prob_col_content:
        return True
    replace_pattern = re.compile(rf'\([^{ident}]+\)')
    ident_find_seq = re.sub(
        replace_pattern,
        '',
        find_col_content).replace(
        '_',
        '')
    split_find_col = re.split(r'[\(\)]', ident_find_seq)[::2]
    split_prob_col = re.split(r'[\(\)]', prob_col_content)
    find_seq_sum = [''.join(split_find_col[:i + 1])
                    for i in range(len(split_find_col))]
    prob_seq_sum = ''
    for i in range(0, len(split_prob_col) - 1, 2):
        prob_seq_sum += split_prob_col[i]
        if prob_seq_sum in find_seq_sum:
            if float(split_prob_col[i + 1]) <= recept_prob:
                return False
        else:
            if float(split_prob_col[i + 1]) > refute_prob:
                return False
    return True
