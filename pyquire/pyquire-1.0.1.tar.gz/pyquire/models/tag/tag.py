from typing import List

from attr import attrs, attrib

from pyquire.models.common import Global
from pyquire.models.tagging_entity import TaggingEntity

__all__ = ["Tag", "Tags"]


@attrs(kw_only=True)
class Tag(TaggingEntity):
    global_: Global = attrib(default=None)
    """Whether this is a global tag.
    Note: it won't be returned if this is not a global tag.

    Examples:
        true
    """


Tags = List[Tag]
