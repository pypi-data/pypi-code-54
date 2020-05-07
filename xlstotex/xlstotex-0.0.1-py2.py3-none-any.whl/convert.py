from xlstotex.utils import construct_header, construct_table, determine_col_widths,\
    parse_line, read_csv, write_txt


def convert(inp_file: str, out_file: str):

    csv_rows = read_csv(inp_file)
    col_widths = determine_col_widths(csv_rows)
    header = construct_header(csv_rows[0])
    lines = [parse_line(row) for row in csv_rows]
    table = construct_table(header, lines, col_widths)
    write_txt(table, out_file)
