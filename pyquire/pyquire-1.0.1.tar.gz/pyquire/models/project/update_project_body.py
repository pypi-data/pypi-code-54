from attr import attrs, attrib

from pyquire.models.common import Followers

__all__ = ["UpdateProjectBody"]


@attrs
class UpdateProjectBody:
    followers: Followers = attrib(default=None)
    """(Optional) OID of the users to replace the followers of this project. 
    Please refer to `addFollowers()` for more details.
    """

    addFollowers: Followers = attrib(default=None)
    """(Optional) OID of the followers to be added to this project. 
    If "me" is specified, it means the current user will follow this task. 
    If the application would like to follow (i.e., receive notifications),  
    it can pass "app" as one of OIDs. In additions, 
    it can pass additional information in one of the following syntax's.
    """

    removeFollowers: Followers = attrib(default=None)
    """(Optional) OID of the followers to be removed from this project. 
    Please refer to `addFollowers` for more details.
    """
