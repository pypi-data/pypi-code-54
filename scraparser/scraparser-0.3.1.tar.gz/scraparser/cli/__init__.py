from .entry_point import entry_point
from .fix import fix
from .googlesheet import googlesheet
from .parse_pdf import parse_pdf_to_csv
from .scrap import scrap
from .sort import sort

commands = [
    fix,
    googlesheet,
    parse_pdf_to_csv,
    scrap,
    sort,
]

for command in commands:
    entry_point.add_command(command)
