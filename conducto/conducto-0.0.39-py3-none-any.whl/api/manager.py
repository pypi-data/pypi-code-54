import json
from .. import api
from ..shared import constants, request_utils, types as t
from . import api_utils


class Manager:
    def __init__(self):
        self.config = api.Config()
        self.url = self.config.get_url()

    ############################################################
    # public methods
    ############################################################
    def launch(
        self, token: t.Token, pipeline_id: t.PipelineId, env=None, is_migration=False
    ):
        if env is None:
            env = {}

        # Make sure this user has access to launch this pipeline
        perms = api.Pipeline().perms(token, pipeline_id)
        if constants.Perms.LAUNCH not in perms:
            raise PermissionError(
                f"User is not authorized to launch pipeline {pipeline_id}"
            )

        # send request for manager service to launch this
        headers = api_utils.get_auth_headers(token)
        data = json.dumps(
            {"pipeline_id": pipeline_id, "env": env, "is_migration": is_migration}
        )
        response = request_utils.post(
            self.url + f"/manager/run", headers=headers, data=data
        )
        api_utils.get_data(response)


AsyncManager = api_utils.async_helper(Manager)
