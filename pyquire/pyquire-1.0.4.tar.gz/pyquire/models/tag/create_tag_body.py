from attr import attrs, attrib

from pyquire.models.common import Color, Name, Global


@attrs
class CreateTagBody:
    name: Name = attrib()
    """The name of the tag
    
    Examples:
        Later
    """

    color: Color = attrib(default=None)
    """(Optional) The color of the tag. If not omitted, a color will be generated automatially.
    
    Examples:
        35
    """

    global_: Global = attrib(default=None)
    """(Optional) Whether this tag is global. If omitted, it is not global.
    
    Examples:
        true
    """
