from attr import attrs, attrib

from pyquire.models.common import Description, Pinned, AsUser

__all__ = ["CreateCommentBody"]


@attrs
class CreateCommentBody:
    description: Description = attrib()
    """The content of the new comment.
    
    Examples:
        Adjust style
    """

    pinned: Pinned = attrib(default=None)
    """(Optional) Whether to pin this comment. Default: false
    
    Examples:
        false
    """

    asUser: AsUser = attrib(default=None)
    """(Optional) Specify true if you'd like to make this new comment as created by the app.
    Default: false -- the comment is marked as created by the user authorizing 
    
    Examples:
        true
    """
