from enum import Enum


class ErrorType(int, Enum):
    ERROR_OTHER = 100
    ERROR_INVALID_VALUE = 101
    ERROR_MISSING_PROPERTY = 102
    ERROR_VALIDATION_STRING_TYPE = 103
    ERROR_VALIDATION = 104
    ERROR_INVALID_PROPERTY = 105
    WARNING_MISSING_RECOMMENDED_PROPERTY = 106


class BaseError(Exception):
    """ Base class for errors """


class BaseWarning(Exception):
    """ Base class for warnings """


class InvalidValueException(BaseError):
    """
    Not valid value
    """
    def __init__(self, value):
        self.value = value
        self.code = ErrorType.ERROR_INVALID_VALUE.value


class InvalidTypeException(BaseError):
    """
    Not valid type
    """

    def __init__(self, value, expected_type):
        self.code = ErrorType.ERROR_VALIDATION.value
        self.value = value
        self.expected_type = expected_type


class ErrorInvalidPropertyException(BaseError):
    """
    Not valid dcat property
    """
    def __init__(self, values):
        self.code = ErrorType.ERROR_INVALID_PROPERTY.value
        self.values = values


class ErrorMissingPropertyException(BaseError):
    """
    Missing fields
    """
    def __init__(self, values):
        self.code = ErrorType.ERROR_MISSING_PROPERTY.value
        self.values = values


class WarningMissingRecommendedPropertyException(BaseWarning):
    """
    Missing fields
    """
    def __init__(self, values):
        self.code = ErrorType.WARNING_MISSING_RECOMMENDED_PROPERTY.value
        self.values = values
