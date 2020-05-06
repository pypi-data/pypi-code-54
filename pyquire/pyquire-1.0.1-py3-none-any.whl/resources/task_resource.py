from typing import NoReturn

from pyquire.api import api
from pyquire.models.common import ID, OID
from pyquire.models.task.create_task_body import CreateTaskBody
from pyquire.models.task.search_task_body import SearchTaskBody
from pyquire.models.task.simple_task import SimpleTasks
from pyquire.models.task.task import Task, Tasks
from pyquire.models.task.update_task_body import UpdateTaskBody


@api.path("/task")
class TaskResource:
    """Task.

    The task is a piece of work to be done or undertaken.
    It is the basic object that you and your team can collaborate on.
    """

    @api.post
    @api.path("/{oid}")
    def create_task(self, *, oid: OID, data: CreateTaskBody) -> Task:
        """Add a new task.

        Add a new task into a project or a task.

        Args:
            oid (:obj:`str`): OID of project or task that this new task to be added to.
                If the given OID is a project, the new task will be added as a root task.
                If the given OID is a task, the new task will become its subtask.
            data (:obj:`models.task.create_task_body.CreateTaskBody`): Task to create.
        Returns:
            :obj:`models.task.Task`: Task.
        """
        pass

    @api.post
    @api.path("/id/{project_id}")
    def create_task_by_project(self, *, project_id: ID, data: CreateTaskBody) -> Task:
        """Add a new task.

        Add a new task into a project.

        Args:
            project_id (:obj:`str`): ID of project that this new task to be added to.
                The new task will be added as a root task.
            data (:obj:`models.task.create_task_body.CreateTaskBody`): Task to create.
        Returns:
            :obj:`models.task.Task`: Task.
        """
        pass

    @api.post
    @api.path("/before/{oid}")
    def create_task_before(self, *, oid: OID, data: CreateTaskBody) -> Task:
        """Add a new task before the given task.

        Add a new task before the given task.

        Args:
            oid (:obj:`str`): OID of the task that this new task to be added before.
            data (:obj:`models.task.create_task_body.CreateTaskBody`): Task to create.
        Returns:
            :obj:`models.task.Task`: Task.
        """
        pass

    @api.post
    @api.path("/after/{oid}")
    def create_task_after(self, *, oid: OID, data: CreateTaskBody) -> Task:
        """Add a new task after the given task.

        Add a new task after the given task.

        Args:
            oid (:obj:`str`): OID of the task that this new task to be added after.
            data (:obj:`models.task.create_task_body.CreateTaskBody`): Task to create.
        Returns:
            :obj:`models.task.Task`: Task.
        """
        pass

    @api.get
    @api.path("/list/{oid}")
    def get_tasks_by_oid(self, *, oid: OID) -> Tasks:
        """Get all root tasks of the given project or all subtasks of the given task.

        Returns all root task records of the given project or all subtasks of the given task by OID.
        If the given OID is a project, the root tasks are returned.
        If the given OID is a task, its subtasks are returned.

        Note:
            Tasks in the same level are return.
            That is, it won't returns subtasks of subtasks.
            You have to retrieve them recursively.

        Args:
            oid (:obj:`str`): OID of project or parent task to look for

        Returns:
            :obj:`list` of :obj:`models.task.Task`: List of Tasks.
        """
        pass

    @api.get
    @api.path("/list/id/{project_id}")
    def get_root_tasks(self, *, project_id: ID) -> Tasks:
        """Get all root tasks of the given project.

        Returns all root task records of the given project.

        Args:
            project_id (:obj:`str`): ID of project.

        Returns:
            :obj:`list` of :obj:`models.task.Task`: List of Tasks.
        """
        pass

    @api.get
    @api.path("/list/id/{project_id}/{task_id}")
    def get_subtasks(self, *, project_id: ID, task_id: ID) -> Tasks:
        """Get all subtasks of the given task.

        Returns all subtask records of the given task.
        Note: tasks in the same level are return.
        That is, it won't returns subtasks of subtasks.
        You have to retrieve them recursively.

        Args:
            project_id (:obj:`str`): ID of the parent task.
            task_id (:obj:`str`): ID of the project.

        Returns:
            :obj:`list` of :obj:`models.task.Task`: Task.
        """
        pass

    @api.get
    @api.path("/search/{project_oid}")
    def search_tasks_by_oid(self, *, project_oid: OID, params: SearchTaskBody) -> SimpleTasks:
        """Searches tasks in the given project.

        Returns task records that match the specified criteria in the given project.
        Note: it returns at most 50 records, and recent edited first.

        Args:
            project_oid (:obj:`str`): OID of the project to search for the tasks.
            params (:obj:`SearchTaskBody`): Task to search.

        Returns:
            :obj:`list` of :obj:`models.task.simple_task.SimpleTask`: Simple Task.
        """
        pass

    @api.get
    @api.path("/search/id/{project_id}")
    def search_tasks_by_id(self, *, project_id: ID, params: SearchTaskBody) -> SimpleTasks:
        """Searches tasks in the given project.

        Returns task records that match the specified criteria in the given project.
        Note: it returns at most 50 records, and recent edited first.

        Args:
            project_id (:obj:`str`): ID of the project to search for the tasks.
            params (:obj:`SearchTaskBody`): Task to search.

        Returns:
            :obj:`list` of :obj:`models.task.simple_task.SimpleTask`: Simple Task.
        """
        pass

    @api.get
    @api.path("/{oid}")
    def get_task(self, *, oid) -> Task:
        """Get an existing task by its OID.

        Returns the full task record for a single task.

        Args:
            oid (:obj:`str`): OID of the task that needs to be fetched

        Returns:
            :obj:`models.task.Task`: Task.
        """
        pass

    @api.get
    @api.path("/id/{project_id}/{id}")
    def get_task_by_id(self, *, project_id: ID, id: ID) -> Task:
        """Get an existing task by its ID.

        Returns the full task record for a single task.

        Args:
            id (:obj:`str`): ID of the task that needs to be fetched.
            project_id (:obj:`str`): ID of the project that the task belongs to.
        Returns:
            :obj:`models.task.Task`: Task.
        """
        pass

    @api.put
    @api.path("/{oid}")
    def update_task(self, *, oid, data: UpdateTaskBody) -> Task:
        """Update an existing task.

        Updates an existing task, and returns the full updated record.

        Args:
            oid (:obj:`str`): OID of task that needs to be updated.
            data (:obj:`models.task.update_task_body.UpdateTaskBody`): The new content of the task to update to.

        Returns:
            :obj:`models.task.Task`: Task.
        """
        pass

    @api.delete
    @api.path("/{oid}")
    def delete_task(self, *, oid) -> NoReturn:
        """Delete a task and all of its subtasks.

        Delete an existing task and all of its subtasks.

        Args:
            oid (:obj:`str`): OID of task that needs to be deleted

        Returns:
            :obj:`models.task.Task`: Task.
        """
        pass
