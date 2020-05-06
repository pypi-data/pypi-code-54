from typing import NoReturn

from pyquire.api import api

__all__ = ["CommentResource"]

from pyquire.models.comment.comment import Comment, Comments
from pyquire.models.comment.create_comment_body import CreateCommentBody
from pyquire.models.comment.update_comment_body import UpdateCommentBody
from pyquire.models.common import OID, ID, TaskId


@api.path("/comment")
class CommentResource:
    """Comment.

    A comment that an user can put to a task or project.
    """

    @api.post
    @api.path("/{oid}")
    def create_comment(self, *, oid, data: CreateCommentBody) -> Comment:
        """Add a new comment to a task or a project.

        Add a new comment to a task or a project.
        If the given OID is a project, the comment will be added to a project.
        If a task, the comment will be added to a task.

        Args:
            oid (:obj:`str`): OID of a project or a task that new comment will be added to
            data (:obj:`models.comment.create_comment_body.CreateCommentBody`: Comment to create.

        Returns:
            :obj:`models.comment.Comment`: Comment.
        """
        pass

    @api.post
    @api.path("/id/{project_id}")
    def create_comment_to_project(self, *, project_id, data: CreateCommentBody) -> Comment:
        """Add a new comment to a project.

        Add a new comment to a project.t.

        Args:
            project_id (:obj:`str`): ID of a project that new comment will be added to
            data (:obj:`models.comment.create_comment_body.CreateCommentBody`: Comment to create.

        Returns:
            :obj:`models.comment.Comment`: Comment.
        """
        pass

    @api.get
    @api.path("/{oid}")
    def get_comment(self, *, oid: OID) -> Comment:
        """"Get a comment.

        Returns the full comment record of the given OID.t

        Args:
            oid (:obj:`str`): OID of comment that needs to be fetched.

        Returns:
            :obj:`models.comment.Comment`: Comment.
        """
        pass

    @api.get
    @api.path("/list/{oid}")
    def get_comments(self, *, oid: OID) -> Comments:
        """Get comments added to the given object.

        Returns all comment records of the given object that can be a project or a task.

        Args:
            oid (:obj:`str`): OID of project or task that comments will be be fetched from.

        Returns:
            :obj:`list` of :obj:`models.comment.Comment`: List of Comments.
        """
        pass

    @api.get
    @api.path("/list/id/{project_id}")
    def get_project_comments(self, *, project_id: ID) -> Comments:
        """Get all comments of the given project.

        Returns all comment records of the given project by its ID.

        Args:
            project_id (:obj:`str`): ID of project.

        Returns:
            :obj:`list` of :obj:`models.comment.Comment`: List of Comments.
        """
        pass

    @api.get
    @api.path("/list/id/{oid}/{task_id}")
    def get_task_comments(self, *, oid: OID, task_id: TaskId) -> Comments:
        """Get all comments of the given task.

        Returns all comment records of the given task by its ID.

        Args:
            oid (:obj:`str`): OID of the project.
            task_id (:obj:`int`): ID of the task.

        Returns:
            :obj:`list` of :obj:`models.comment.Comment`: List of Comments.
        """
        pass

    @api.put
    @api.path("/{oid}")
    def update_comment(self, *, oid, data: UpdateCommentBody) -> Comment:
        """Update an existing comment.

        Updates an existing comment, and returns the complete updated comment record.

        Args:
            oid (:obj:`str`): OID of comment that needs to be updated.
            data (:obj:`models.comment.update_comment_body.UpdateCommentBody`): Comment to update.

        Returns:
            :obj:`models.comment.Comment`: Comment.
        """
        pass

    @api.delete
    @api.path("/{oid}")
    def delete_comment(self, *, oid: OID) -> NoReturn:
        """Delete an existing comment.

        Delete an existing comment.

        Args:
            oid (:obj:`str`): OID of comment that needs to be deleted

        Returns:
            :obj:`models.comment.Comment`: Comment.
        """
        pass
