from attr import attrs, attrib

from pyquire.models.common import Target, Name, Value, Color

__all__ = ["UpdateColumnBody"]


@attrs(kw_only=True)
class UpdateColumnBody:
    name: Name = attrib(factory=str)
    """(Optional) name. 
    example = "TO DO"
    """

    value: Value = attrib(default=None)
    """(Optional) The status that this column represents.

    Its value must be between 0 and 100. If 100, it means completed.
    There is exactly one column with completed status.
    example = "0"
    """

    color: Color = attrib(default=None)
    """(Optional) The color. It is an index of our predefined color palette.
    The first digit is between 0 and 5, and the second between 0 and 7.
    The color palette can be found in our Quire's color picker.
    """

    target: Target
    """The status of the existing column to update with the new content
    Note: it must be specified.
    
    Examples:
        0
    """
