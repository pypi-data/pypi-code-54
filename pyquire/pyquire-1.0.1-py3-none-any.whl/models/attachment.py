from typing import List

from attr import attrs, attrib

from pyquire.models.common import Name, Url, Length, Type, Date

Attachments = List["Attachment"]


@attrs
class Attachment:
    type: Type = attrib()
    """The type of this attachment. 
    It is 1 if it is from Google Drive. 
    It is 2 if it is stored in Quire. 
    
    Examples:
        2048
    """

    name: Name = attrib()
    """Attachment's name. 
    Examples:
        file.zip
    """

    url: Url = attrib()
    """URL of this attachment. 
    Examples:
        https://quire.io/att/Ta/sdcQOGgeUtyaFFzb9p0IwAgi/qfqVmUtC/image.png
    """

    length: Length = attrib()
    """The size of this attachment. Unit: bytes. 
    Examples:
        2048
    """

    createdAt: Date = attrib()
    """When this record was created. 
    Examples:
        2018-12-22T02:06:58.158Z
    """

    createdBy: Date = attrib()
    """OID of the user who created this record. 
    Examples:
        Dyh2YkFcu9uLgLFIeN1kB4Ld
    """
