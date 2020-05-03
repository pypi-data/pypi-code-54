# ANSI cursor movement codes
UP = "\033[{}A"  # Move up N rows
DOWN = "\033[{}B"  # Move down N rows
LEFT = "\r"  # Move to left most column


class ProgressPrinter:
    """
    This is a multiline progress printer. It enables rendering progress bars, status updates, etc.
    across multiple lines. The printer handles tracking and moving the cursor to render line
    updates. Movement is performed using ANSI movement codes.

    An arbitrary number of lines may be added and then rendered to. Adding a line will advance
    terminal (CR) to create the new line.

    The cursor is moved to the beginning of the line after printing.

    This version of the printer does not format based on terminal size.

    Usage:
        ```
        printer = ProgressPrinter()
        printer.add_line("any_hashable_identifier")
        printer.print("any_hashable_identifier", "[    ]")
        printer.print("any_hashable_identifier", "[=   ]")
        printer.print("any_hashable_identifier", "[==  ]")
        printer.print("any_hashable_identifier", "[=== ]")
        printer.print("any_hashable_identifier", "[====]")
        printer.complete()
        ```
    """

    def __init__(self):
        self.current_line = 0
        self.line_numbers = {}
        self.is_complete = False

    def add_line(self, line_id):
        """
        Add a line for a line_id. Line_id may be any type of hashable identifier.
        The identifier is mapped to the next line_number. Subsequent prints for
        that line_id will print on it's registered line.
        :param line_id: any hashable identifier
        :return: current line number
        """
        if line_id in self.line_numbers:
            return

        # add new line number mapping
        line_count = len(self.line_numbers)
        self.line_numbers[line_id] = line_count

        # Goto the current last line, print a new line, and update the cursor position
        if line_count:
            self.goto(line_count - 1)
            print()
        self.current_line = line_count
        return self.current_line

    def goto(self, line):
        """
        Move cursor to the line number
        :param line: line to move to
        :return: None
        """
        if line == self.current_line:
            return
        if line < self.current_line:
            print(UP.format(self.current_line - line), end=LEFT)
        elif line > self.current_line:
            print(DOWN.format(line - self.current_line), end=LEFT)
        self.current_line = line

    def print(self, line_id, text):
        """
        Print text for the line_id.

        After printing the text the remainder of the line will be cleared and the cursor will
        move back to the beginning of the line.
        :param line_id: identifier for line
        :param text: text to print
        :return: None
        """
        # Move to line and then print the text
        line_number = self.line_numbers[line_id]
        self.goto(line_number)
        print("{}\033[K".format(text,), end=LEFT),

    def complete(self):
        self.is_complete = True
        self.goto(len(self.line_numbers))
