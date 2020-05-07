from csv import DictReader


def construct_header(line: list) -> list:

    keys = list(line.keys())
    header = r'\hline \\[-3.6 ex] '
    for idx, key in enumerate(keys):
        header += key
        if idx != len(keys) - 1:
            header += ' & '
    return header + r' \\' + r' [0.2 ex] \hline \\ [-3 ex]'


def construct_table(header: str, lines: list, col_widths: tuple) -> str:

    table = r'\begin{tabular}{'
    for idx, width in enumerate(col_widths):
        table += r'p{' + str(width) + 'px}'
        if idx != len(col_widths) - 1:
            table += r' '
    table += r'}' + '\n'
    table += '    ' + header + '\n'
    for line in lines:
        table += r'    ' + line + '\n'
    table += r'\end{tabular}'
    return table


def determine_col_widths(rows: list) -> tuple:

    keys = list(rows[0].keys())
    widths = [8 * len(key) for key in keys]
    for idx, key in enumerate(keys):
        for row in rows:
            n_chars = len(row[key])
            if 8 * n_chars > widths[idx]:
                widths[idx] = 8 * n_chars
    return tuple([w + 1 for w in widths])


def parse_line(line: list) -> str:

    keys = list(line.keys())
    string = ''
    for idx, key in enumerate(keys):
        string += line[key]
        if idx != len(keys) - 1:
            string += r' & '
    return string + r' \\'


def read_csv(filename: str, encoding: str = 'utf8') -> list:

    with open(filename, 'r', encoding=encoding) as csv_file:
        reader = DictReader(csv_file)
        rows = [r for r in reader]
    csv_file.close()
    return rows


def write_txt(content: str, filename: str):

    with open(filename, 'w') as txt_file:
        txt_file.write(content)
    txt_file.close()
