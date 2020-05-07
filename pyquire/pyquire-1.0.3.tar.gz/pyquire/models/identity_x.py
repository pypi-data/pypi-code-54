from attr import attrs, attrib

from pyquire.models.common import Email, Website
from pyquire.models.identity import Identity

__all__ = ["IdentityX"]


@attrs
class IdentityX(Identity):
    email: Email = attrib(factory=str)
    """Email address. 
    example = "john@gmail.cc"
    """

    website: Website = attrib(factory=str)
    """Website. 
    example = "https://coolwebsites.com"
    """
