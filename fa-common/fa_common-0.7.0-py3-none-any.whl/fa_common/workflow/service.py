import os
import json
from datetime import datetime
from typing import List
from .models import ScidraModule, JobRun, WorkflowProject
from .utils import get_workflow_client
from fa_common import logger as LOG
from fa_common.storage import File
import oyaml as yaml

dirname = os.path.dirname(__file__)


async def create_workflow_project(user_id: str, project_name: str) -> WorkflowProject:
    client = get_workflow_client()
    try:
        project = await client._get_project_by_name(user_id)
    except ValueError:
        LOG.info(f"Workflow User {user_id} does not exist, creating.")
        project = await client.create_project(user_id)

    branch = await client.create_branch(project.id, project_name)

    return WorkflowProject(
        name=branch.name,
        user_id=user_id,
        gitlab_project_id=project.id,
        created=str(datetime.now()),
    )


async def run_job(
    project: WorkflowProject,
    description: str,
    module: ScidraModule,
    job_data: dict,
    files: List[File] = [],
    sync: bool = False,
) -> JobRun:

    file_refs = []
    for _file in files:
        file_refs.append(_file.dict())

    with open(os.path.join(dirname, "job.yml")) as yaml_file:
        job_yaml = yaml.safe_load(yaml_file)

    job_yaml["run-job"]["image"] = module.docker_image
    job_yaml["run-job"]["variables"]["JOB_PARAMETERS"] = json.dumps(job_data)
    job_yaml["run-job"]["variables"]["FILE_REFS"] = json.dumps(file_refs)

    client = get_workflow_client()

    await client.update_ci(
        project.gitlab_project_id, project.name, job_yaml, description
    )
    job_run = await client.run_pipeline(
        project.gitlab_project_id, project.name, wait=sync
    )
    return job_run.jobs[0]


async def get_job_run(user_id: str, job_id: int, include_log: bool = False) -> JobRun:
    client = get_workflow_client()
    return await client.get_job(user_id, job_id, include_log)


async def get_job_log(user_id: str, job_id: int):
    client = get_workflow_client()
    logs = await client.get_job_log(user_id, job_id)
    return logs
