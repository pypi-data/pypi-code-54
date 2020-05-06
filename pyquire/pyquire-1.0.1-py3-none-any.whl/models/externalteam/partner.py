from typing import List

from attr import attrs, attrib

from pyquire.models.common import Image
from pyquire.models.tagging_entity import TaggingEntity

__all__ = ["Partner", "Partners"]


@attrs(kw_only=True)
class Partner(TaggingEntity):
    image: Image = attrib()  # example = "https://quire.s3.amazonaws.com/oid/image.jpg"


Partners = List[Partner]
