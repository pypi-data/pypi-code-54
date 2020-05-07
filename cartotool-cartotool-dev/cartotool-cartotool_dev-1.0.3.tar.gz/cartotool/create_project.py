import openapi_client
from openapi_client import Configuration, Pageable, ProjectForm


class CreateProject:

    def __init__(self):
        pass

    @classmethod
    def execute(self, token, host="http://localhost:8080"):
        print("creating project")

        configuration = Configuration(
            host=host,
            api_key={'Authorization': token},
            api_key_prefix={'Authorization': "TOKEN"},
        )

        Configuration.set_default(configuration)

        api_client = openapi_client.ApiClient()

        me = openapi_client.UserControllerApi().find_me()
        print(me.name)

        workspaces = openapi_client.WorkspaceControllerApi().get_all(pageable=Pageable(page=0))
        print(workspaces[0]['code'])

        project = openapi_client.ProjectControllerApi().get_projects(pageable=Pageable(page=0))
        print(project[0].code)

        new_project = openapi_client.ProjectControllerApi().post_projects(project_form=ProjectForm(
            workspace_code="3b68befa-38e2-4396-89fd-12d2b5f1d5f3",
            name="test Project",
        ))

        print(new_project.code)



