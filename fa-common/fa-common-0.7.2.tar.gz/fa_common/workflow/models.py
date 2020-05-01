from enum import Enum
from typing import Optional, List, Union

from fa_common import CamelModel

# from fa_common.db import DocumentDBModel


class ModuleType(str, Enum):
    SYNC = "sync"  # Is run via a service call
    ASYNC = "async"  # Is executed via gitlab ci


class JobStatus(str, Enum):
    NOT_SET = ""
    RECEIVED = "RECEIVED"
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"


class FileFieldDescription(CamelModel):
    name: str
    description: str
    valid_extensions: List[str]
    max_size: Optional[int]
    mandatory: bool = False


class ScidraModule(CamelModel):
    version: str = "1.0.0"
    name: str
    module_type: ModuleType = ModuleType.ASYNC
    docker_image: str
    input_schema: str = ""
    output_schema: str = ""
    input_files: List[FileFieldDescription] = []


class JobRun(CamelModel):
    id: int
    status: str = ""
    started_at: Optional[str]
    finished_at: Optional[str]
    duration: Optional[int]
    name: Optional[str]
    stage: Optional[str]
    output: Optional[Union[List, dict]]
    log: Optional[bytes]


class WorkflowRun(CamelModel):
    """Equivilant to  gitlab pipeline"""

    id: int
    gitlab_project_id: int
    gitlab_project_branch: str
    commit_id: str
    status: str = ""
    jobs: List[JobRun] = []
    started_at: Optional[str]
    finished_at: Optional[str]
    duration: Optional[int]


# class ScidraJob(CamelModel):
#     id: int
#     module_id: str
#     status: Optional[JobStatus]
#     inputs: dict = {}
#     outputs: dict = {}
#     console: List[str] = []


# class ScidraWorkflow(CamelModel):
#     id: int
#     user_id: str
#     project_id: str
#     workflow_description: str = ""
#     jobs: List[ScidraJob] = []
#     last_run: Optional[WorkflowRun] = None


class WorkflowProject(CamelModel):
    name: str
    user_id: str
    gitlab_project_id: int
    created: Optional[str]
