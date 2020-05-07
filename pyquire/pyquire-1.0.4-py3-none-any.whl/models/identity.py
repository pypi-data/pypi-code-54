from attr import attrs, attrib

from pyquire.models.common import ID, NameText, NameHtml, Description, DescriptionText, DescriptionHtml, Url
from pyquire.models.named_icon_entity import NamedIconEntity

__all__ = ["Identity"]


@attrs
class Identity(NamedIconEntity):
    nameText: NameText = attrib(factory=str)
    """Name but excluding markdown characters. 
    example = "My Name"
    """

    nameHtml: NameHtml = attrib(factory=str)
    """Name in a form of a HTML fragment converted from markdown. 
    example = "My Name"
    """

    description: Description = attrib(factory=str)
    """Description. 
    example = "This is *cool*!"
    """

    descriptionText: DescriptionText = attrib(factory=str)
    """Description but excluding markdown characters. 
    example = "This is cool!"
    """

    descriptionHtml: DescriptionHtml = attrib(factory=str)
    """Description in a form of a HTML fragment converted from markdown. 
    example = "This is <i>cool</i>!" 
    """

    url: Url = attrib(factory=str)
    """Url of this record on Quire website. 
    example = "https://quire.io/w/my_project"
    """

    id: ID = attrib(factory=str)
    """ID. 
    example = "My_ID"
    """
