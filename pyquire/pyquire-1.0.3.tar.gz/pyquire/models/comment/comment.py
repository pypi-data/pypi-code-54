from typing import List

from attr import attrs, attrib

from pyquire.models.attachment import Attachments
from pyquire.models.common import Description, DescriptionText, DescriptionHtml, Url, OID, OwnerType, \
    Date
from pyquire.models.stamped_entity import StampedEntity

__all__ = ["Comment", "Comments"]


@attrs(kw_only=True)
class Comment(StampedEntity):
    description: Description = attrib()
    """The content.
    
    Examples:
        It is *cool*!
    """

    descriptionText: DescriptionText = attrib()
    """The content but excluding markdown characters.
    
    Examples:
        It is cool!
    """

    descriptionHtml: DescriptionHtml = attrib()
    """The content in a form of a HTML fragment converted from markdown.
    
    Examples:
        It is <i>cool</i>!
    """

    attachments: Attachments = attrib()
    """The attachments of this task.
    """

    pinAt: Date = attrib(default=None)
    """When this comment was pinned, or null if not pinned.
    
    Examples:
        2018-12-22T02:06:58.158Z
    """

    pinBy: OID = attrib(factory=str)
    """OID of the user who pinned this comment, or null if not pinned.
    
    Examples:
        rcBHBYXZSiyDRrHrWPutatfF
    """

    editedAt: Date = attrib(default=None)
    """When this comment was edited, or null if not edited.
    
    Examples:
        2018-12-22T02:06:58.158Z
    """

    editedBy: OID = attrib(factory=str)
    """OID of the user who edited this comment, or null if not edited.
    
    Examples:
        rcBHBYXZSiyDRrHrWPutatfF
    """

    url: Url = attrib()
    """Url of this comment on Quire website.
    
    Examples:
        https://quire.io/w/my_project70/Cello_and_voilin#comment-iDsPd.QP_qM.hN.Trymukn8b
    """

    owner: OID = attrib()
    """OID of the object this comment was added to.
    
    Examples:
        Dyh2YkFcu9uLgLFIeN1kB4Ld
    """

    # TODO: Rename ownerOtype to ownerType, this is REST API bug, I've send feedback!
    ownerOtype: OwnerType = attrib()
    """The type of the object this comment was added to. It can be "Task" or "Project".
    
    Examples:
        Task
    """


Comments = List[Comment]
