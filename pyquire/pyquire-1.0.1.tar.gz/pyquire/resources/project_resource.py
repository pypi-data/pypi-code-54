from pyquire.api import api
from pyquire.models.common import OID, ID
from pyquire.models.project.project import Project, Projects
from pyquire.models.project.update_project_body import UpdateProjectBody

__all__ = ["ProjectResource"]


@api.path("/project")
class ProjectResource:
    """Project.

    A project represents a prioritized list of tasks in Quire.
    It exists in a single organization and is accessible to a
    subset of users in that organization, depending on its permissions.
    """

    @api.get
    @api.path("/list/{organization_oid}")
    def projects_by_organization_oid(self, *, organization_oid: OID) -> Projects:
        """Get all granted projects.

        Returns all granted project records. The `organizationOid` is optinal. If specified, only granted projects of the given organization are returned. If omitted, all granted project records will be returned.

        Args:
            organization_oid (:obj:`str`): OID of the organization..

        Returns:
            :obj:`list` of :obj:`models.project.Project`: List of Projects.
        """

    @api.get
    @api.path("/list/id/{organization_id}")
    def projects_by_organization_id(self, *, organization_id: ID) -> Projects:
        """Get all granted projects of the organization by its ID.

        Returns all project records of the given organization. Only granted projects will be returned.

        Args:
            organization_id (:obj:`str`): ID of the organization.

        Returns:
            :obj:`list` of :obj:`models.project.Project`: List of Projects.
        """

    @api.get
    @api.path("/id/{id}")
    def project_by_id(self, *, id: ID) -> Project:
        """Get a project by its ID.

        Returns the complete project record of the given ID.

        Args:
            id (:obj:`str`): ID of project that needs to be fetched.

        Returns:
            :obj:`models.project.Project`: Project.
        """

    @api.get
    @api.path("/{oid}")
    def project(self, *, oid: OID) -> Project:
        """Get a project by its OID.

        Returns the complete project record of the given OID.

        Args:
            oid (:obj:`str`): OID of project that needs to be fetched.

        Returns:
            :obj:`models.project.Project`: Project.
        """

    @api.put
    @api.path("/{oid}")
    def update_project(self, *, oid: OID, data: UpdateProjectBody) -> Project:
        """Update a project.

        Updates an existing project, and returns the complete updated project record.

        Args:
            oid (:obj:`str`): OID of project that needs to be updated.
            data (:obj:``)

        Returns:
            :obj:`models.project.Project`: Project.
        """
