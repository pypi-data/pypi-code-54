from attr import attrs, attrib

from pyquire.models.common import Description, Pinned

__all__ = ["UpdateCommentBody"]


@attrs
class UpdateCommentBody:
    description: Description = attrib(factory=str)
    """(Optional) The new content of the comment.
    
    Examples:
        Adjust style
    """
    pinned: Pinned = attrib(default=None)
    """(Optional) Whether to pin this comment.
    
    Examples:
        false
    """
