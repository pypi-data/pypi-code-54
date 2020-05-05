"""
    This module contains all the Schema objects for the Umbrella Management
    API to interact with the response object as Python native constructs. 
"""

from marshmallow import Schema, fields, post_load

from umbrella_cli.models import Site


class SiteSerializer(Schema):
    """ Umbrella internal site serializer """
    origin_id = fields.Integer(load_only=True, data_key="originId")
    name = fields.String(required=True)
    site_id = fields.Integer(load_only=True, data_key="siteId")
    is_default = fields.Boolean(load_only=True, data_key="isDefault")
    type = fields.String(load_only=True)
    internal_network_count = fields.Integer(
        load_only=True, data_key="internalNetworkCount"
        )
    va_count = fields.Integer(load_only=True, data_key="vaCount")

    #! Python datetime not supporting Zulu timezone
    #modified_at = fields.DateTime(
    #    format="YYYY-MM-DDTHH:MM:SS.fffZ", load_only=True, data_key="modifiedAt"
    #    )
    #created_at = fields.DateTime(
    #    format="YYYY-MM-DDTHH:MM:SS.fffZ", load_only=True, data_key="createdAt"
    #    )
    modified_at = fields.String(load_only=True, data_key="modifiedAt")
    created_at = fields.String(load_only=True, data_key="createdAt")

    @post_load
    def post_load(self, data, **kwargs):
        return Site(**data)