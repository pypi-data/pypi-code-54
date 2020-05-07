from typing import List

import attr

from pyquire.models.common import ActiveCount, TaskCount, RootCount, OID, Followers, Date
from pyquire.models.identity import Identity

__all__ = ["Project", "Projects"]


@attr.s
class Project(Identity):
    """A project represents a prioritized list of tasks in Quire.
    It exists in a single organization and is accessible to a subset of
    users in that organization, depending on its permissions.
    """

    organization: OID = attr.ib(factory=str)
    """OID of the organization this project belongs to. 
    example = "Dyh2YkFcu9uLgLFIeN1kB4Ld"
    """

    taskCount: TaskCount = attr.ib(factory=int)
    """Total number of tasks in this project. 
    example = "30"
    """

    activeCount: ActiveCount = attr.ib(factory=int)
    """Number of active tasks in this project. 
    example = "20"
    """

    rootCount: RootCount = attr.ib(factory=int)
    """Number of root tasks in this project. 
    example = "5"
    """

    editedAt: Date = attr.ib(default=None)
    """When this record was edited last time. 
    example = "2018-12-22T02:06:58.158Z"
    """

    followers: Followers = attr.ib(default=None)
    """OID of users who follow this task."""

    createdAt: Date = attr.ib(default=None)
    """When this record was created. 
    example = "2018-12-22T02:06:58.158Z"
    """

    createdBy: OID = attr.ib(factory=str)
    """OID of the user who created this record. 
    example = "Dyh2YkFcu9uLgLFIeN1kB4Ld"
    """

    archivedAt: Date = attr.ib(default=None)
    """When this project was archived (aka., peekaboo).
    It is null if not archived.
    example = "2018-12-22T02:06:58.158Z"
    """


Projects = List[Project]
