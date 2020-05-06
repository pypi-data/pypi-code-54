from typing import List

from attr import attrs, attrib

from pyquire.models.attachment import Attachments
from pyquire.models.common import ID, Name, Description, NameText, \
    NameHtml, DescriptionHtml, DescriptionText, Url, Followers, \
    Status, Priority, Assignees, Assignors, \
    Order, Cover, ChildCount, Date, OID, Favorites, \
    Peekaboo
from pyquire.models.recurring import Recurring
from pyquire.models.referrer import Referrers
from pyquire.models.stamped_entity import StampedEntity

__all__ = ["Task", "Tasks"]

from pyquire.models.tag.tag import Tags


@attrs(kw_only=True)
class Task(StampedEntity):
    id: ID = attrib()
    """ID. 

    Examples:
        12
    """

    name: Name = attrib()
    """This task's name. 
    
    Examples:
        Design new **logo**
    """

    nameText: NameText = attrib(default=None)
    """This task's name but excluding markdown characters. 
    
    Examples:
        Design new **logo**
    """

    nameHtml: NameHtml = attrib(default=None)
    """This task's name in a form of a HTML fragment converted from markdown. 
    
    Examples:
        Design new <b>logo</b>
    """

    description: Description = attrib(factory=str)
    """Description about this task. 
    
    Examples:
        This is a *cool* task.
    """

    descriptionText: DescriptionText = attrib(factory=str)
    """Description but excluding markdown characters. 

    Examples:
        This is a cool task.
    """

    descriptionHtml: DescriptionHtml = attrib(factory=str)
    """Description in a form of a HTML fragment converted from markdown. 
    
    Examples:
        This is a <i>cool</i> task.
    """

    status: Status = attrib()
    """The status of this task. Its value must be between 0 and 100. 
    If 100, it means completed. 

    Examples:
        0
    """

    priority: Priority = attrib()
    """The priority of this task. 
    Its value must be between -1 (lowest) and 2 (highest). 
    Default: 0. 
    
    Examples:
        0
    """

    tags: Tags = attrib(default=None)
    """OID of tags that are tagged to this task."""

    start: Date = attrib(default=None)
    """When to start this task. 
    Note: if time is specified, the millisecond will be `001`.  
    Otherwise, it is `000` (so are the hour, minute and second fields). 
    
    Examples:
        2018-12-20T00:00:00.000Z
    """

    due: Date = attrib(default=None)
    """When to complete this task. 
    Note: if time is specified, the millisecond will be 001. 
    Otherwise, it is 000 (so are the hour, minute and second fields). 
    
    Examples:
        2018-12-22T00:00:00.000Z
    """

    recurring: Recurring = attrib(default=None)
    """The recurring information of this task. 
    It is null if it is not a recurring task."""

    assignees: Assignees = attrib(default=None)
    """OID of users who are assigned to this task."""

    assignors: Assignors = attrib(default=None)
    """OID of users who have assigned this tasks to a user. 
    For Examples:, the first item of assignees is assigned by the first item of assignors.
    """

    partner: OID = attrib(default=None)
    """OID of the external team that this task belongs to. 
    It is null if this task doesn't belong to any external team. 

    Examples:
        rcBHBYXZSiyDRrHrWPutatfF
    """

    partnerBy: OID = attrib(default=None)
    """OID of the user who assigned this task to an external team. 
    It is null if this task doesn't belong to any external team. 
    
    Examples:
        rcBHBYXZSiyDRrHrWPutatfF
    """

    board: OID = attrib(default=None)
    """OID of the board that this task was added to. 
    It is null if this task doesn't belong to any board. 

    Examples:
        rcBHBYXZSiyDRrHrWPutatfF
    """

    order: Order = attrib(default=None)
    """The order of this task shown on the board. 
    The smaller the number is, the ealier the task is shown. 
    It is meaningless if it doesn't belong to any board. 

    Examples:
        99
    """

    attachments: Attachments = attrib(default=None)
    """The attachments of this task."""

    cover: Cover = attrib(default=None)
    """The id of the attachment that is used as a cover of this task. 
    Examples:
        qfqVmUtC
    """

    childCount: ChildCount = attrib(default=None)
    """Number of subtasks of this task. 
    To retrieve these subtasks, make the GET request to "/task/list/{oid}". 
    
    Examples:
        5
    """

    referrers: Referrers = attrib(default=None)
    """A list of referrers that refer this task. 
    Note: some of them might no longer exist.
    """

    toggledAt: Date = attrib(default=None)
    """When this task's state was changed last time. 
    Examples:
        2018-12-22T02:06:58.158Z
    """

    toggledBy: OID = attrib(default=None)
    """OID of the user who changed this task's state.  
    
    Examples:
        rcBHBYXZSiyDRrHrWPutatfF
    """

    followers: Followers = attrib(default=None)
    """OID of users who follow this task."""

    favorites: Favorites = attrib(default=None)
    """OID of users who favorite this task."""

    editedAt: Date = attrib(default=None)
    """When this record was edited last time. 
    
    Examples:
        2018-12-22T02:06:58.158Z
    """

    peekaboo: Peekaboo = attrib(default=None)
    """Whether this task was peekabooed. 
    It is null if not peekabooed. 
    
    Examples:
        true
    """

    url: Url = attrib()
    """Url of this task on Quire website. 
   
    Examples:
        https://quire.io/w/my_project/123
    """

    project: OID = attrib(default=None)
    """OID of the project this task belongs to. 
   
    Examples:
        Dyh2YkFcu9uLgLFIeN1kB4Ld
    """


Tasks = List[Task]
