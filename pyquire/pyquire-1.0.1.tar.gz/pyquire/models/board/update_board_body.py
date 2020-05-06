from attr import attrs, attrib

from pyquire.models.board.add_column_body import AddColumnBody
from pyquire.models.board.update_column_body import UpdateColumnBody
from pyquire.models.common import Archived, RemoveColumn, Description, Name, ID, Date

__all__ = ["UpdateBoardBody"]


@attrs
class UpdateBoardBody:
    id: ID = attrib(factory=str)
    """(Optional) ID of the board.
    
    Examples:
        Board101
    """

    name: Name = attrib(factory=str)
    """(Optional) The name of the board.
    
    Examples:
        Board 101
    """

    description: Description = attrib(factory=str)
    """(Optional) An optional description about this task.
    
    Examples:
        **Great** board to start with.
    """

    due: Date = attrib(default=None)
    """(Optional) When this board was aimed to complete. 
    
    Examples:
        2020-01-22T02:06:58.158Z
    """

    column: UpdateColumnBody = attrib(default=None)
    """(Optional) Updates an existing column with a new content.
    """

    addColumn: AddColumnBody = attrib(default=None)
    """(Optional) The new column defintion to be added to this board.
    """

    removeColumn: RemoveColumn = attrib(default=None)
    """(Optional) The status of the column that needs to be deleted.
    
    Examples:
        75
    """

    archived: Archived = attrib(default=None)
    """(Optional) Specify true to archive this board. 
    
    Examples:
        true
    """
