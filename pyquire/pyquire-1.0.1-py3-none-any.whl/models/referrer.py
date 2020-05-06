from typing import List

from attr import attrs, attrib

from pyquire.models.common import OID, Date


@attrs
class Referrer:
    task: OID = attrib()
    """OID of the task that refers another task. 
    
    Examples:
        wrSpgghWFCzPHBqiShSurDeD
    """

    user: OID = attrib()
    """OID of the user who made this reference. 
    Examples:
        wrSpgghWFCzPHBqiShSurDeD
    """

    when: Date = attrib()
    """When this reference is made. 
    Examples:
        2018-12-22T02:06:58.158Z
    """


Referrers = List[Referrer]
