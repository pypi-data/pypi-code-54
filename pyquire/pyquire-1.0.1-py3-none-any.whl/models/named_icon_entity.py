from attr import attrs, attrib

from pyquire.models.common import IconColor, Image
from pyquire.models.named_entity import NamedEntity

__all__ = ["NamedIconEntity"]


@attrs
class NamedIconEntity(NamedEntity):
    iconColor: IconColor = attrib(factory=str)
    """The color of the icon representing this record.
    It is an index of our predefined color palette.
    example = "37"
    """

    image: Image = attrib(factory=str)
    """The image representing this record. 
    example = "https://quire.s3.amazonaws.com/oid/image.jpg"
    """
