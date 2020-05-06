from attr import attrs, attrib

from pyquire.models.common import Name
from pyquire.models.entity import Entity

__all__ = ["NamedEntity"]


@attrs
class NamedEntity(Entity):
    name: Name = attrib()
    """The name. 
    example = "My Name"
    """
