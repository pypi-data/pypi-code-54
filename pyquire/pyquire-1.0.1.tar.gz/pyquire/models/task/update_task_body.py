from attr import attrs, attrib

from pyquire.models.common import Name, Description, Priority, Status, OID, Assignees, Date, Peekaboo, Followers
from pyquire.models.recurring import Recurring
from pyquire.models.tag.tag import Tags


@attrs
class UpdateTaskBody:
    name: Name = attrib()
    """The name of the task.

    Examples:
        Design new **logo**
    """

    description: Description = attrib(default=None)
    """(Optional) An optional description about this task.

    Examples:
        This is a *cool* task.
    """

    priority: Priority = attrib(default=None)
    """(Optional) An optional priority.
    Its value must be between -1 (lowest) and 2 (highest).
    Default: 0.

    Examples:
        0
    """

    status: Status = attrib(default=None)
    """(Optional) An optional status.
    Its value must be between 0 and 100.
    Default: 0.

    Examples:
        0
    """

    board: OID = attrib(default=None)
    """(Optional) OID of the board to replace existing board of to this task. 
    If specified, it will replace existing board. 
    
    Examples:
        rcBHBYXZSiyDRrHrWPutatfF
    """

    tags: Tags = attrib(default=None)
    """(Optional) OID or names of the tags to be added to the new created task.
    Note: if tag's name is specified, it is case-insensitive.

    Examples:
        2018-12-20T00:00:00.000Z
    """

    addTags: Tags = attrib(default=None)
    """(Optional) OID or names of the tags to be added to this task.
    Note: if tag's name is specified, it is case-insensitive."""

    removeTags: Tags = attrib(default=None)
    """(Optional) OID or names of the tags to be removed to this task.
    Note: if tag's name is specified, it is case-insensitive."""

    assignees: Assignees = attrib(default=None)
    """(Optional) OID or ID of the users that this task is assigned to. 
    If specified, it will replace any existing assignee(s). 
    Instead of replacment, you can use "addAssignees" or "removeAssignees".
    """

    addAssignees: Assignees = attrib(default=None)
    """(Optional) OID or ID of the assignees to be added to this task."""

    removeAssignees: Assignees = attrib(default=None)
    """(Optional) OID or ID of the assignees to be removed to this task."""

    start: Date = attrib(default=None)
    """(Optional) An optional start time.
    Note: if time is specified, the millisecond must be `001`.
    Otherwise, it is `000` (so are the hour, minute and second fields).
    """

    due: Date = attrib(default=None)
    """(Optional) An optional start time.
    Note: if time is specified, the millisecond must be `001`.
    Otherwise, it is `000` (so are the hour, minute and second fields).
    """

    recurring: Recurring = attrib(default=None)
    """(Optional) The recurring information of this task.
    It is null if it is not a recurring task.
    """

    peekaboo: Peekaboo = attrib(default=False)
    """(Optional) Specify true or a positive integer to peekaboo this task and its subtasks, if any.
    Or, specify false to undo the previous peekaboo if any.
    If a positive integer is specified, it is the number of days to peekaboo a task.
    If true, the default number of days will be used (depending on the project's setting).
    Default: false.
    """

    followers: Followers = attrib(default=None)
    """(Optional) OID or ID of the users to replace the followers of this task. 
    Please refer to `addFollowers()` for more details.
    """

    addFollowers: Followers = attrib(default=None)
    """(Optional) OID or ID of the followers to be added to this task.
    If "me" is specified, it means the current user will follow this task.
    If the application would like to follow (i.e., receive notifications), it can pass "app" as one of OIDs.
    In additions, it can pass additional information in one of the following syntaxes.
    Syntax 1:"app|team" or "app|team|channel" where team and channel can be any value.
    Syntax 2:"app|/path"where "/path" can be any URL path. 
    It will be appended to the hook's URL when calling the registered hook. 
    For example, if the hook URL is "https://super.app/hooks/standard" and the 
    follower is "app|/soc1/33456/a7", then the notification will be 
    sent to "https://super.app/hooks/standard/soc1/33456/a7".
    """

    removeFollowers: Followers = attrib(default=None)
    """(Optional) OID or ID of the followers to be removed from this task.
    Please refer to `addFollowers()` for more details.
    """
