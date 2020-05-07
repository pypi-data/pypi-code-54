from attr import attrs, attrib

from pyquire.models.common import Type, Rate, Date, Data

__all__ = ["Recurring"]


@attrs
class Recurring:
    type: Type = attrib()
    """The type of this recurring.
    It is 0 if it is weekly. 
    It is 1 if it is monthly.
    It is 2 if it is yearly.
    It is 3 if it is custom.
    
    Examples:
        2048
    """

    rate: Rate = attrib()
    """How often this recurring shall occur. 
    If the rate is 2 and the type is weekly, it means it shall occur every two week. 
    If the type is custom, it means number of days to repeat.
    
    Examples:
        2048
    """

    end: Date = attrib()
    """When this recurring shall end. 
    If not specified, it means it is never end.
    Examples:
        2020-12-22T00:00:00.000Z
    """

    data: Data = attrib()
    """It depends on the type of this recurring. 
    If weekly, bit 0 is Sunday, bit 1 is Monday and so on. 
    For example, if the data is 6, it means every Monday and Tuesday.
    
    Examples:
        6
    """
