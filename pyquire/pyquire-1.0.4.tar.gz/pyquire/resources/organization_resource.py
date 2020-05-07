from pyquire.api import api
from pyquire.models.common import OID, ID
from pyquire.models.organization.organization import Organization, Organizations

__all__ = ["OrganizationResource"]


@api.path("/organization")
class OrganizationResource:
    """An organization is a group of projects where members collaborate at once."""

    @api.get
    @api.path("/list")
    def organizations(self) -> Organizations:
        """Get all organizations.

        Returns the organization records for all organizations that the current user can grant to this application.

        Returns:
            :obj:`list` of :obj:`models.organization.Organization`: List of Organizations.
        """

    @api.get
    @api.path("/id/{id}")
    def organization_by_id(self, *, id: ID) -> Organization:
        """Get an organization by its ID.

        Returns the complete organization record of the given OID.

        Args:
            id (:obj:`str`): ID of organization that needs to be fetched.

        Returns:
            :obj:`models.organization.Organization`: Organization.
        """

    @api.get
    @api.path("/{oid}")
    def organization(self, *, oid: OID) -> Organization:
        """Get an organization by its OID.

        Returns the complete organization record.

        Args:
            oid (:obj:`str`): OID of organization that needs to be fetched.

        Returns:
            :obj:`models.organization.Organization`: Organization.
        """
