from .feature import Feature

class Symbols(Feature):

    def score(self, value) -> float:
        s = str(value)
        numbers = sum(c.isdigit() for c in s)
        words = sum(c.isalpha() for c in s)
        spaces = sum(c.isspace() for c in s)
        return len(s) - numbers - words - spaces
