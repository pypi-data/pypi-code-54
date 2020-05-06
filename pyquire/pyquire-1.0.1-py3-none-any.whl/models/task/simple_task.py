from typing import List

from attr import attrs, attrib

from pyquire.models.common import OID, ID, Name, Status, Priority, Date, Url

__all__ = ["SimpleTask", "SimpleTasks"]


@attrs
class SimpleTask:
    oid: OID = attrib()
    """OID, aka. UUID.
    
    Examples:
        Dyh2YkFcu9uLgLFIeN1kB4Ld
    """

    id: ID = attrib()
    """
    Examples:
        12
    """

    name: Name = attrib()
    """This task's name.
    
    Examples:
        Design new <b>logo</b>
    """

    status: Status = attrib()
    """The status of this task. Its value must be between 0 and 100. If 100, it means completed.
    
    Examples:
        0
    """

    priority: Priority = attrib()
    """The priority of this task. Its value must be between -1 (lowest) and 2 (highest). Default: 0.
    
    Examples:
        0
    """

    start: Date = attrib()
    """When to start this task.Note: if time is specified, the millisecond will be `001`. Otherwise, it is `000` (so are the hour, minute and second fields).
    
    Examples:
        2018-12-20T00:00:00.000Z
    """

    due: Date = attrib()
    """When to complete this task. Note: if time is specified, the millisecond will be 001. Otherwise, it is 000 (so are the hour, minute and second fields).
    
    Examples:
        2018-12-22T00:00:00.000Z
    """

    url: Url = attrib()
    """Url of this task on Quire website.
    
    Examples:
        https://quire.io/w/my_project/123
    """


SimpleTasks = List[SimpleTask]
