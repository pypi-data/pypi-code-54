from typing import List

from attr import attrs, attrib

from pyquire.models.column import Columns
from pyquire.models.common import OID, Date
from pyquire.models.identity import Identity

__all__ = ["Board"]


@attrs
class Board(Identity):
    """A board is a group of columns that an user can visualize the progress of tasks.
    """

    columns: Columns = attrib(default=None)
    """The column definitions of this board.
    """

    partner: OID = attrib(factory=str)
    """OID of the external team that this board belongs to.
    It is null if this board can't be accessed by a member of external teams.
    example = "rcBHBYXZSiyDRrHrWPutatfF"
    """

    archivedAt: Date = attrib(default=None)
    """When this board was archived.
    It is null if not archived.
    example = "2020-02-22T02:06:58.158Z"
    """

    due: Date = attrib(default=None)
    """When this board was aimed to complete, or null if not specified.
    example = "2020-01-22T02:06:58.158Z"
    """

    project: OID = attrib(factory=str)
    """OID of the project this board belongs to. 
    example = "Dyh2YkFcu9uLgLFIeN1kB4Ld" 
    """

    createdAt: Date = attrib(default=None)
    """When this record was created. 
    example = "2018-12-22T02:06:58.158Z"
    """

    createdBy: OID = attrib(factory=str)
    """OID of the user who created this record. 
    example = "Dyh2YkFcu9uLgLFIeN1kB4Ld"
    """


Boards = List[Board]
