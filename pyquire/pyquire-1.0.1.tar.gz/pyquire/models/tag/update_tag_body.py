from attr import attrs, attrib

from pyquire.models.common import Global, Color, Name, OID

__all__ = ["UpdateTagBody"]


@attrs
class UpdateTagBody:
    name: Name = attrib(factory=str)
    """(Optional) The new name of the tag.
    
    Examples:
        Later
    """

    color: Color = attrib(default=None)
    """(Optional) The color of the tag.
    
    Examples:
        35
    """

    global_: Global = attrib(default=True)
    """(Optional) Whether this tag is global. 
    If you specify false here, you have to specify "project" 
    for what project you'd like to put the tag to.
    
    Examples:
        true
    """

    project: OID = attrib(default=None)
    """(Optional) OID of the project this tag shall be limited to. 
    It is used only if "global" is also specified and false. 
    Otherwise, it is simply ignored.
    
    Examples:
        Dyh2YkFcu9uLgLFIeN1kB4Ld
    """
