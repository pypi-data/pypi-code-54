from attr import attrs, attrib

from pyquire.models.common import OID, Description, Name, Status, Text


@attrs
class SearchTaskBody:
    text: Text = attrib(default=None)
    """Text to do a full-text search against the name, description,
    and attachments. 
    
    Note:
        It doesn't include the content and attachment of comments.
    
    Examples:
        important major
    """

    name: Name = attrib(default=None)
    """Task name to match with. To specify a regular expression, you can
    precede it with `~`. 
    To do a full-text search, please use `text` instead.
    
    Examples:
        My first task
    """

    description: Description = attrib(default=None)
    """Task's description to match with. To specify a regular expression,
    you can precede it with `~`.
    """

    board: OID = attrib(default=None)
    """OID of task's board to match with. To search tasks without
    board, you can specify `board=` or `board=none`. 
    To search tasks with any board, you can specify `board=any`.
    
    Examples:
        9GFBEKOH5J_aZjNhR82Gd9xx
    """

    status: Status = attrib(default=None)
    """Task's status to match with. You can specify a value between
    0 and 100, or \"active\" for active tasks,  \"completed\" for completed tasks.
    
    Examples:
        100
    """
