from crdatamgt.helpers import data_extraction, workbook_load_path, rename_dictionary
import pandas as pd
import os
from toolz import interleave



def _load_formulas(path, write=False):
    wb = workbook_load_path(path, write)
    return wb


def formulation_read(wb, header=False):
    p_header, p_formulation = data_extraction(wb, 'Formulations', header)
    p_formulation.columns = map(str.lower, p_formulation.columns)
    p_formulation.set_index('formulation id', inplace=True)
    p_formulation.rename(columns=rename_dictionary(), inplace=True)
    p_formulation = p_formulation.apply(pd.to_numeric, errors='coerce')

    return [p_formulation, [p_header, p_formulation]][header]


def tests_read(wb, header=False):
    p_header, p_tests_data = data_extraction(wb, 'Tests', header)
    p_tests_data.columns = map(str.lower, p_tests_data.columns)
    p_tests_data.set_index('formulation id', inplace=True)
    return [p_tests_data, [p_header, p_tests_data]][header]


def formulation_load(path):
    wb = _load_formulas(path)
    formulas = formulation_read(wb)
    return formulas


def formulation_write(formulas, formulation_path):
    return _write_formulations_tests(formulas, formulation_path)


def _write_formulations_tests(new_data, formulation_path):
    """
    This entire bit of code will become difficult to maintain. The entire concept of formulation flexibility should be
    revisited

    :param new_data:
    :param hold_blank_data:
    :return:
    """
    if new_data.dropna(how='all').empty:
        return pd.DataFrame()
    new_data.columns = map(str.lower, new_data.columns)
    new_data.rename(columns=rename_dictionary(), inplace=True)

    data_path = os.path.join(formulation_path, 'Formulation table.xlsx')
    writer = pd.ExcelWriter(data_path, engine='openpyxl')
    writer.book = workbook_load_path(formulation_path, True)
    formulation_wb = writer.book

    sheet_formulation = 'Formulations'
    sheet_tests = 'Tests'

    formulation_header, old_formula_data = formulation_read(formulation_wb, True)
    test_header, test_data = tests_read(formulation_wb, True)

    new_formula_data = new_data.drop_duplicates().drop(columns=['formulation'], errors='ignore').dropna(how='all')
    formulation_only_test_data = new_data.loc[:, ['test', 'formulation']].dropna()

    test_set = old_formula_data.merge(new_formula_data, indicator=True, how='outer')
    test_set.index += 1
    test_set.drop(columns=['formulation', 'units'], errors='ignore', inplace=True)
    check = test_set.drop(columns=['test'], errors='ignore').sum(axis=1).between(100, 100)

    gf = test_set[check]
    bf = test_set[~check]

    # if not bf.empty:
    #     try:
    #         f_log.info(f"Bad Formulas present in {topic_path}")
    #     except PermissionError as e:
    #         f_log2 = log.get_logger(f'formulation {e}')
    #         f_log2.info(f"Bad Formulas present in {topic_path}")

    new_formulas = gf[gf['_merge'] == 'right_only'].drop(columns=['_merge'], errors='ignore').drop_duplicates()
    updated_data = old_formula_data.append([new_formulas])
    updated_data.reset_index(inplace=True)
    updated_data.rename(columns={"index": "Formulation ID"}, inplace=True)
    updated_data.index += 1

    new_tests = gf['test'].dropna()
    for formula in gf['test'].index:
        if not (test_data.index == formula).any():
            test_data.loc[formula] = ""
    for test in new_tests.index:
        m = gf['test'][test].lower()
        test_data.loc[test, m] = "x"
    for test in formulation_only_test_data.index:
        _formula = formulation_only_test_data.iloc[test].get('formulation')
        _test = formulation_only_test_data.iloc[test].get('test').lower()
        test_data.loc[_formula, _test] = 'x'

    test_data.reset_index(inplace=True)

    replace_sheet(formulation_wb, sheet_formulation, writer, formulation_header, updated_data)
    replace_sheet(formulation_wb, sheet_tests, writer, test_header, test_data)

    writer.save()
    writer.close()

    formulation_return = pd.DataFrame()
    id_only = new_data['formulation'].dropna()

    formula_only = updated_data.set_index(['Formulation ID']).drop(columns=['test'], errors='ignore')
    new_formula_only = new_formula_data.drop(columns=['test', 'units'], errors='ignore')
    with_formulation = formula_only.merge(new_formula_only, indicator=True, how='outer')
    with_formulation.index += 1
    with_formulation.reset_index(inplace=True)
    with_formulation.rename(columns={"index": "Formulation ID"}, inplace=True)
    with_formulation = with_formulation.loc[with_formulation['_merge'] == 'both', 'Formulation ID']

    if not (id_only.empty and with_formulation.empty):
        # Flattening out the array
        idx = [fx for f in [with_formulation.values, id_only.values] for fx in f]
        formulation_id = pd.DataFrame(columns=['Formulation ID'], data=idx).drop_duplicates()
        used_formulations = updated_data.loc[formulation_id['Formulation ID']].drop(columns=['test']).set_index(
            'Formulation ID')
        max = pd.DataFrame(columns=[f'{q} Max' for q in used_formulations.columns],
                           data=[used_formulations.max().values])
        min = pd.DataFrame(columns=[f'{q} Min' for q in used_formulations.columns],
                           data=[used_formulations.min().values])
        formulation_min_max = pd.concat([max, min], axis=1)[list(interleave([max, min]))]
        formulation_id = pd.DataFrame(columns=['Formulation ID'],
                                      data=[', '.join([str(int(x[0])) for x in formulation_id.values])])
        formulation_return = formulation_id.join(formulation_min_max)

    return formulation_return


def replace_sheet(wb, sheet, writer, header, data):
    idx = wb.sheetnames.index(sheet)
    wb.remove(wb.worksheets[idx])
    header.to_excel(writer, sheet, index=False, header=False)
    data.drop(columns=['test'], errors='ignore').to_excel(writer, sheet, startrow=header.shape[0], startcol=0,
                                                          index=False)
