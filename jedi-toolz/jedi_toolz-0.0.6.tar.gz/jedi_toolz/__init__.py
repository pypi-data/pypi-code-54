"""jedi_toolz is a python package containing many utilities to simplify working
with data.

jedi_toolz is divided into the following sub-modules:

1.  config: Provides helper functions to extract the contents of a .ini
            configuration file.

            as_dict -> returns values as a nested dict object.

            as_records -> returns values as a list of dict objects.

            select -> returns either a dict (section ONLY provided) or a
            value (section AND option provided).

2.  data:   Provides many helper functions for checking the type of data
            passed and converting dict objects to tables and record objects.

3.  domo:   Connects to a DOMO instance using credentials defined in a .ini
            config file and provides several helper functions.

            connect -> returns a connection object to a DOMO instance.

            tables -> returns a list of dict objects representing the datasets
            of a DOMO instance.

            get_id -> returns the dataset id when provided the dataset name.

            query -> returns the dataset data as a list of dict objects.

4.  show:   Provides several functions for printing tabular data. Utilized
            the tabulate package.

            wrap_row -> returns a string version of a dict with long values
            split into lines.

            wrap_table -> returns a string version of a list of dicts with
            long values split into lines.

            transpose -> tranposes the columns and rows of a list of dicts.

            show -> prints an ascii table using the tabulate package. Column
            and table width can be contrained by using the col_width and
            table_width parameters. The data will automatically be transposed if
            the table width is exceeded so that the output will fit the table_width.

5.  xlsx:   Provides functions for exporting and formatting data in a .xlsx file.
            Uses openpyxl to export and read data.

            to_xlsx -> Allows data to be appended to an existing file as new Sheets
            within the file.

            column_format -> a function which returns a basic format allowing for
            text alignment, number_format, and column width to be set.

            default_formats -> analyzes and existing sheet and provides default
            text alignment, column width, and number_format options based upon
            how the .xlsx file has stored the data.

            column_formats -> returns a column format for each column in the sheet
            using either provided formats or default formats.

            format_sheet -> formats a sheet and optionally adds the sheet as a
            Worksheet table with a default table format.
"""

__version__ = "0.0.6"

from jedi_toolz import config
from jedi_toolz.show import show
from jedi_toolz import xlsx
from jedi_toolz import domo
from jedi_toolz import data