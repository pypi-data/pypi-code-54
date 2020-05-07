from attr import attrs, attrib

from pyquire.models.common import OID


@attrs(kw_only=True)
class Entity:
    oid: OID = attrib(factory=str)
    """OID, aka. UUID. 
    example = "Dyh2YkFcu9uLgLFIeN1kB4Ld"
    """
