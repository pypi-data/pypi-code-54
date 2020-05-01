from typing import List


class ValidationError:
    """ValidationError base class."""

    ERROR_OTHER = 100
    ERROR_INVALID_VALUE = 101
    ERROR_MISSING_PROPERTY = 102
    ERROR_VALIDATION_STRING_TYPE = 103
    ERROR_VALIDATION = 104
    ERROR_INVALID_PROPERTY = 105
    WARNING_MISSING_RECOMMENDED_PROPERTY = 106

    def to_string(self, code: str, fields: List) -> str:
        """Errors to string."""

        items = []
        for field in fields:
            if field.get("validator"):
                items.append(f"{field['validator'].hint}:{field['field']}")
            else:
                items.append(f"{field['field']}")
        if code == ValidationError.ERROR_MISSING_PROPERTY:
            return f"Missing mandatory props(s): {items}"
        if code == ValidationError.WARNING_MISSING_RECOMMENDED_PROPERTY:
            return f"Missing recommended props(s): {items}"
        elif code == ValidationError.ERROR_INVALID_VALUE:
            return f"Not valid: {field}"
        elif code == ValidationError.ERROR_OTHER:
            return f"Could not be validated: {items}"
        elif code == ValidationError.ERROR_VALIDATION:
            return f"Invalid type: {items}"
        elif code == ValidationError.ERROR_INVALID_PROPERTY:
            return f"Property not in DCAT schema: {items}"
