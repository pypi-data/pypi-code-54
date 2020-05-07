from typing import List

from attr import attrs, attrib

from pyquire.models.common import Date, OID
from pyquire.models.identity_x import IdentityX

__all__ = ["Organizations", "Organization"]


@attrs
class Organization(IdentityX):
    """An organization is a group of projects where members collaborate at once.
    """
    createdAt: Date = attrib(default=None)
    """When this record was created. 
    example = "2018-12-22T02:06:58.158Z"
    """

    createdBy: OID = attrib(factory=str)
    """OID of the user who created this record. 
    example = "Dyh2YkFcu9uLgLFIeN1kB4Ld"
    """


Organizations = List[Organization]
