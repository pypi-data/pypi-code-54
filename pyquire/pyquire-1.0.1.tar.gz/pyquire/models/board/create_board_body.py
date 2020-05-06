from attr import attrs, attrib

from pyquire.models.column import Columns
from pyquire.models.common import ID, Name, Description, OID, Date

__all__ = ["CreateBoardBody"]


@attrs
class CreateBoardBody:
    name: Name = attrib()
    """The name. 
    example = "My Name"
    """

    id: ID = attrib(factory=str)
    """ID. 
    example = "My_ID"
    """

    description: Description = attrib(factory=str)
    """Description. 
    example = "This is *cool*!"
    """

    columns: Columns = attrib(default=None)
    """The column definitions of this board.
    """

    partner: OID = attrib(factory=str)
    """OID of the external team that this board belongs to.
    It is null if this board can't be accessed by a member of external teams.
    example = "rcBHBYXZSiyDRrHrWPutatfF"
    """

    due: Date = attrib(default=None)
    """When this board was aimed to complete, or null if not specified.
    example = "2020-01-22T02:06:58.158Z"
    """
