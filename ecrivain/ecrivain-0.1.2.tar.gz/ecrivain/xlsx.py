import pandas as pd
import xlsxwriter
from xlsxwriter import Workbook


def approx_width(col: pd.Series, factor: float, threshold: int) -> int:
    """guess a good value for a cell width"""
    size_header = len(col.name) if col.name else 1
    col_str = col.astype(str).str
    size_data = max(col_str.len())    
    return min(max(size_data, size_header), threshold)*factor


def autofit(df: pd.DataFrame,
            path: str,
            sheetname: str,
            factor: float,
            threshold) -> pd.ExcelWriter:
    

    """ Apply sensible default on formating (wrap,size of cell)

    Parameters
    ----------
    path:
        specify where writer should save when `save()`is called
    sheetname:
        usual
    factor:
        scale (>1) or down width size of the cell
    threshold:
        max width size for a cell (data execeding this limit will be wrapped)

    """
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    # Convert the dfframe to an XlsxWriter Excel object.
    df.to_excel(writer, index=False, sheet_name=sheetname)
    workbook = writer.book
    worksheet = writer.sheets[sheetname]
    # format for each cell
    cell_format = workbook.add_format()
    cell_format.set_text_wrap()
    for pos, col in enumerate(df.columns):
        width = approx_width(df[col], factor, threshold)
        worksheet.set_column(pos, pos,width, cell_format=cell_format)
    return writer


def write_excel(data: pd.DataFrame, path: str):
    """Write data to a 'data' sheet and save result on disk"""
    writer = autofit(data,path,'data',1.1,150)
    writer.save()
