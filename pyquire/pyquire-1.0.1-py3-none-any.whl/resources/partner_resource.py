from pyquire.api import api
from pyquire.models.common import ID, OID
from pyquire.models.externalteam.partner import Partner, Partners

__all__ = ["PartnerResource"]


@api.path("/partner")
class PartnerResource:
    """Partner.

    An external team (aka., a partner) is a group of users
    that can access only tasks that are assigned to this team.
    """

    @api.get
    @api.path("/{oid}")
    def partner(self, *, oid: OID) -> Partner:
        """Get an external team (aka., a partner).

        Returns the full external team record of the given OID.

        Args:
            oid (:obj:`str`): OID of external team that needs to be fetched.

        Returns:
            :obj:`models.partner.Partner`: Partner
        """

    @api.get
    @api.path("/list/{project_oid}")
    def partners_by_project_oid(self, *, project_oid: OID) -> Partners:
        """Get all external teams of the given project by its OID.

        Returns all external team records of the given project by its OID.

        Args:
            project_oid (:obj:`str`): OID of the project to look for

        Returns:
            :obj:`list` of :obj:`models.partner.Partner`: Partner
        """

    @api.get
    @api.path("/list/id/{project_id}")
    def partners_by_project_id(self, *, project_id: ID) -> Partners:
        """Get all external teams of the given project by its ID.

        Returns all external team records of the given project by its ID.

        Args:
            project_id (:obj:`str`): ID of project to look for

        Returns:
            :obj:`list` of :obj:`models.partner.Partner`: Partner
        """
