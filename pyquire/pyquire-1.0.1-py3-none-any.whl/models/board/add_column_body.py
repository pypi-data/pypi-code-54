from attr import attrs

from pyquire.models.board.create_column_body import CreateColumnBody
from pyquire.models.common import Before

__all__ = ["AddColumnBody"]


@attrs
class AddColumnBody(CreateColumnBody):
    before: Before
    """(Optional) The value of the column that 
    this new column needs to be added before. 
    If specified, the new column will be put before the specified column.
    
    Examples:
        75
    """
