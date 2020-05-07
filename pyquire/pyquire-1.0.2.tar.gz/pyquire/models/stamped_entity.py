from attr import attrs, attrib

from pyquire.models.common import OID, Date
from pyquire.models.entity import Entity

__all__ = ["StampedEntity"]


@attrs
class StampedEntity(Entity):
    createdAt: Date = attrib(default=None)
    """When this record was created. 
    Examples:
        2018-12-22T02:06:58.158Z
    """

    createdBy: OID = attrib(factory=str)
    """OID of the user who created this record. 
    
    Examples:
        Dyh2YkFcu9uLgLFIeN1kB4Ld
    """
