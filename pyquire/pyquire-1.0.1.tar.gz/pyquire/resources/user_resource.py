from pyquire.api import api
from pyquire.models.common import ID, OID
from pyquire.models.user.user import Users, User

__all__ = ["UserResource"]


@api.path("/user")
class UserResource:
    """User.

    A user object represents an account in Quire that can
    be given access to various organizations, projects, and tasks.
    """

    @api.get
    @api.path("/list")
    def get_users(self) -> Users:
        """Get all user records.

        Returns all colleagues of the current user if he granted the app to access his contacts.
        Otherwise, it returns only colleagues who also authorized the same app.
        If the current user didn't grant the access of his contacts and none of his
        collegues authorized this app, only the current user's record will be returned.
        The first record must be the current user.

        Returns:
            :obj:`list` of :obj:`models.user.user.User`: List of Users.
        """
        pass

    @api.get
    @api.path("/list/project/id/{project_id}")
    def get_users_of_project_by_id(self, *, project_id: ID) -> Users:
        """Get all users records of the given project.

        Returns all members of the given project of the specified ID.
        If the current user doesn't grant the app to access his contacts,
        only basic information are returned.
        The first record must be the current user.

        Args:
            project_id (:obj:`str`): ID of the Project.

        Returns:
            :obj:`list` of :obj:`models.user.user.User`: List of Users.
        """
        pass

    @api.get
    @api.path("/list/project/{oid}")
    def get_users_of_project_by_oid(self, *, oid: OID) -> Users:
        """Get all users records of the given project.

        Returns all members of the given project of the specified OID.
        If the current user doesn't grant the app to access his contacts,
        only basic information are returned.
        The first record must be the current user.

        Args:
            oid (:obj:`str`): OID of the Project.

        Returns:
            :obj:`list` of :obj:`models.user.user.User`: List of Users.
        """
        pass

    @api.get
    @api.path("/id/{id}")
    def get_user_by_id(self, *, id: ID) -> User:
        """Get a user by its ID or email address.

        Returns the full user record of the given ID or email address.

        Args:
            id (:obj:`str`): ID, email address or "me" of user that needs to be fetched.
                Example: "john@gmail.com", "me"

        Returns:
            :obj:`models.user.user.User`: User.
        """
        pass

    @api.get
    @api.path("/{oid}")
    def get_user_by_oid(self, *, oid: OID) -> User:
        """Get a user by its OID.

        Returns the full user record of the given OID.

        Args:
            oid (:obj:`str`): OID of user that needs to be fetched.

        Returns:
            :obj:`models.user.user.User`: User.
        """
        pass
