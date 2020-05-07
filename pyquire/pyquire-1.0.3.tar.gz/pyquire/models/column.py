from typing import List

from attr import attrs, attrib

from pyquire.models.common import Name, Value, Color

Columns = List["Column"]


@attrs(kw_only=True)
class Column:
    name: Name = attrib()
    """name. 
    example = "TO DO"
    """

    value: Value = attrib(default=100)
    """The status that this column represents.
    
    Its value must be between 0 and 100. If 100, it means completed.
    There is exactly one column with completed status.
    example = "0"
    """

    color: Color = attrib(default=None)
    """The color. It is an index of our predefined color palette.
    The first digit is between 0 and 5, and the second between 0 and 7.
    The color palette can be found in our Quire's color picker.
    """
