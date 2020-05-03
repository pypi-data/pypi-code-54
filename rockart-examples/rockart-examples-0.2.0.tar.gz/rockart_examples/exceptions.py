class RockartExamplesException(Exception):
    pass

class RockartExamplesIndexError(RockartExamplesException, IndexError):
    pass

class RockartExamplesValueError(RockartExamplesException, ValueError):
    pass
