from attr import attrs, attrib

from pyquire.models.common import Name, Color, OID
from pyquire.models.stamped_entity import StampedEntity

__all__ = ["TaggingEntity"]


@attrs(kw_only=True)
class TaggingEntity(StampedEntity):
    name: Name = attrib()
    """The name. 
    
    Examples:
        Later
    """

    color: Color = attrib()
    """The color. It is an index of our predefined color palette. 
    The first digit is between 0 and 5, and the second between 0 and 7.
    The color palette can be found in our Quire's color picker.
    
    Examples:
        35
    """

    project: OID = attrib()
    """OID of the project this object belongs to. 
    
    Examples:
        Dyh2YkFcu9uLgLFIeN1kB4Ld
    """
