from pyquire.api import api
from pyquire.models.common import OID, ID
from pyquire.models.tag.create_tag_body import CreateTagBody
from pyquire.models.tag.tag import Tag, Tags
from pyquire.models.tag.update_tag_body import UpdateTagBody


@api.path("/tag")
class TagResource:
    """Tag.

    A tag is a label that can be attached to any task in Quire.
    """

    @api.post
    @api.path("/{project_oid}")
    def create_tag(self, *, project_oid: OID, data: CreateTagBody) -> Tag:
        """Add a new tag.

        Add a new tag into a project.

        Args:
            project_oid (:obj:`str`): OID of project that this new tag to be added to..
            data (:obj:`models.tag.create_tag_body.CreateTagBody`): Tag to create.

        Returns:
            :obj:`models.tag.Tag`: Tag.
        """
        pass

    @api.post
    @api.path("/id/{project_id}")
    def create_tag_to_project(self, *, project_id: ID, data: CreateTagBody) -> Tag:
        """Add a new tag.

        Add a new tag into a project.

        Args:
            project_id (:obj:`str`): ID of project that this new tag to be added to..
            data (:obj:`models.tag.create_tag_body.CreateTagBody`): Tag to create.

        Returns:
            :obj:`models.tag.Tag`: Tag.
        """
        pass

    @api.get
    @api.path("/{oid}")
    def get_tag(self, *, oid: OID) -> Tag:
        """Get a tag.

        Returns the full tag record of the given OID.

        Args:
            oid (:obj:`str`): OID of tag that needs to be fetched..

        Returns:
            :obj:`models.tag.Tag`: Tag.
        """
        pass

    @api.get
    @api.path("/list/{project_oid}")
    def get_tags_by_project_oid(self, *, project_oid: OID) -> Tags:
        """Get all tags of the given project by its OID.

        Returns all tag records of the given project by its OID.

        Args:
            project_oid (:obj:`str`): OID of the project..

        Returns:
            :obj:`list` of :obj:`models.tag.Tag`: List of Tags.
        """
        pass

    @api.get
    @api.path("/list/id/{project_id}")
    def get_tags_by_project_id(self, *, project_id: ID) -> Tags:
        """Get all tags of the given project by its ID.

        Returns all tag records of the given project by its ID.

        Args:
            project_id (:obj:`str`): ID of project..

        Returns:
            :obj:`list` of :obj:`models.tag.Tag`: List of Tags.
        """
        pass

    @api.put
    @api.path("/{oid}")
    def update_tag(self, *, oid: OID, data: UpdateTagBody) -> Tag:
        """Update a tag.

        Updates an existing tag, and returns the complete updated record.

        Args:
            oid (:obj:`str`): OID of tag that needs to be updated.
            data (:obj:`models.tag.update_tag_body.UpdateTagBody`): Tag to update.

        Returns:
            :obj:`models.tag.Tag`: Tag.
        """
        pass

    @api.delete
    @api.path("/{oid}")
    def delete_tag(self, *, oid: OID):
        """Delete a tag

        Delete an existing tag of the given OID.

        Args:
            oid (:obj:`str`): OID of tag that needs to be deleted.

        Returns:
            :obj:`models.tag.Tag`: Tag.
        """
        pass
